import argparse
import csv
import json
import time
from pathlib import Path
from urllib.parse import unquote
from typing import Dict, List, Set, Tuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://ioepas.edu.np/"
TEACHING_STAFF_URL = "https://ioepas.edu.np/teaching-staff/"
NON_TEACHING_STAFF_URL = "https://ioepas.edu.np/non-teaching-staff/"


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    return webdriver.Chrome(options=options)


def wait_for_page(driver: webdriver.Chrome, timeout: int = 20) -> None:
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


def safe_text(parent, selector: str) -> str:
    elements = parent.find_elements(By.CSS_SELECTOR, selector)
    if not elements:
        return ""
    return elements[0].text.strip()


def clean_href(href: str) -> str:
    if not href:
        return ""
    if href.endswith("#"):
        return ""
    return href.strip()


def clean_email(email_value: str) -> str:
    if not email_value:
        return ""

    value = unquote(email_value).strip()
    value = value.replace("http://", "").replace("https://", "")
    value = value.strip("/")
    return value


def infer_department_name(label: str, page_url: str) -> str:
    if label and label.lower() != "teaching department":
        return label.strip()

    url = page_url.strip("/").lower()
    if "civil-engineering" in url:
        return "Department of Civil Engineering"
    if "electrical-engineering" in url:
        return "Department of Electrical Engineering"
    if "electronics-and-computer-engineering" in url:
        return "Department of Electronics & Computer Engineering"
    if "auto-mechanical-engineering" in url:
        return "Department of Mechanical & Automobile Engineering"
    if "geomatics-engineering" in url:
        return "Department of Geomatics Engineering"
    if "applied-sciences" in url:
        return "Department of Applied Sciences"

    return "Teaching Department"


def extract_social_details(card) -> Dict[str, str]:
    phone = ""
    email = ""
    links: List[str] = []

    anchors = card.find_elements(By.CSS_SELECTOR, ".staff-social a, .staff-entry-social-links a")
    for anchor in anchors:
        href = clean_href(anchor.get_attribute("href") or "")
        classes = (anchor.get_attribute("class") or "").lower()

        if "wpex-phone-number" in classes and href.startswith("tel:"):
            phone = href.replace("tel:", "").strip()
            continue

        if "wpex-email" in classes:
            if href.startswith("mailto:"):
                email = clean_email(href.replace("mailto:", "").strip())
            elif "@" in href:
                email = clean_email(href)
            continue

        if href:
            links.append(href)

    return {
        "phone": phone,
        "email": email,
        "social_links": " | ".join(links),
    }


def parse_staff_cards(driver: webdriver.Chrome, staff_type: str, fallback_department: str) -> List[Dict[str, str]]:
    cards = driver.find_elements(By.CSS_SELECTOR, "article.staff-entry, .staff-entry.vcex-grid-item")
    rows: List[Dict[str, str]] = []

    for card in cards:
        name = safe_text(card, ".staff-entry-title")
        designation = safe_text(card, ".staff-entry-position")
        category = safe_text(card, ".staff-entry-categories")
        department = category or fallback_department

        if not name:
            continue

        profile_url = ""
        profile_link = card.find_elements(By.CSS_SELECTOR, ".staff-entry-title a")
        if profile_link:
            profile_url = clean_href(profile_link[0].get_attribute("href") or "")

        details = extract_social_details(card)
        personal_details = {
            "designation": designation,
            "phone": details["phone"],
            "email": details["email"],
            "social_links": details["social_links"],
            "profile_url": profile_url,
        }

        rows.append(
            {
                "staff_type": staff_type,
                "name": name,
                "department": department,
                "designation": designation,
                "phone": details["phone"],
                "email": details["email"],
                "social_links": details["social_links"],
                "profile_url": profile_url,
                "source_page": driver.current_url,
                "personal_details": json.dumps(personal_details, ensure_ascii=True),
            }
        )

    return rows


def get_teaching_department_pages(driver: webdriver.Chrome) -> List[Tuple[str, str]]:
    driver.get(TEACHING_STAFF_URL)
    wait_for_page(driver)
    time.sleep(2)

    department_pages: List[Tuple[str, str]] = []
    seen: Set[str] = set()

    anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='faculty-members']")
    for anchor in anchors:
        href = clean_href(anchor.get_attribute("href") or "")
        if not href or href in seen:
            continue

        label = anchor.text.strip() or "Teaching Department"
        department_pages.append((label, href))
        seen.add(href)

    return department_pages


def deduplicate(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    unique_rows: List[Dict[str, str]] = []
    seen_keys: Set[Tuple[str, str, str, str]] = set()

    for row in rows:
        key = (
            row["staff_type"].lower(),
            row["name"].lower(),
            row["department"].lower(),
            row["designation"].lower(),
        )
        if key in seen_keys:
            continue
        seen_keys.add(key)
        unique_rows.append(row)

    return unique_rows


def write_csv(rows: List[Dict[str, str]], output_file: str) -> None:
    fieldnames = [
        "staff_type",
        "name",
        "department",
        "designation",
        "phone",
        "email",
        "social_links",
        "profile_url",
        "source_page",
        "personal_details",
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def scrape_staff(output_file: str, headless: bool) -> int:
    driver = build_driver(headless=headless)
    rows: List[Dict[str, str]] = []

    try:
        department_pages = get_teaching_department_pages(driver)

        for department_name, page_url in department_pages:
            driver.get(page_url)
            wait_for_page(driver)
            time.sleep(1.5)
            resolved_department = infer_department_name(department_name, page_url)
            rows.extend(parse_staff_cards(driver, "Teaching", resolved_department))

        driver.get(NON_TEACHING_STAFF_URL)
        wait_for_page(driver)
        time.sleep(2)
        rows.extend(parse_staff_cards(driver, "Non-Teaching", "Non-Teaching Staff"))

    except TimeoutException as exc:
        raise RuntimeError(f"Timed out while loading page: {driver.current_url}") from exc
    finally:
        driver.quit()

    rows = deduplicate(rows)
    write_csv(rows, output_file)
    return len(rows)


def main() -> None:
    default_output = str(Path(__file__).with_name("staff_details.csv"))

    parser = argparse.ArgumentParser(
        description="Scrape IOE PAS staff details using Selenium and save to CSV."
    )
    parser.add_argument(
        "--output",
        default=default_output,
    )
    parser.add_argument(
        "--headed",
        action="store_true",
    )
    args = parser.parse_args()

    count = scrape_staff(output_file=args.output, headless=not args.headed)
    print(f"Saved {count} staff records to {args.output}")


if __name__ == "__main__":
    main()
