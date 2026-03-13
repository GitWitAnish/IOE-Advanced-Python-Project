from pathlib import Path
import pickle

import pandas as pd
import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "dataset" / "cleaned_data.csv"
MODEL_PATH = ROOT_DIR / "model" / "RegressionModel.pkl"
CURRENT_YEAR = 2026


@st.cache_data
def load_data() -> pd.DataFrame:
	df = pd.read_csv(DATA_PATH)
	if "Unnamed: 0" in df.columns:
		df = df.drop(columns=["Unnamed: 0"])
	return df


@st.cache_resource
def load_model():
	with open(MODEL_PATH, "rb") as f:
		return pickle.load(f)


def inr(value: float) -> str:
	return f"Rs {value:,.0f}"


def predict_price(model, name: str, company: str, year: int, kms_driven: int, fuel_type: str) -> float:
	row = pd.DataFrame(
		{
			"name": [name],
			"company": [company],
			"year": [year],
			"kms_driven": [kms_driven],
			"fuel_type": [fuel_type],
			"car_age": [CURRENT_YEAR - year],
		}
	)
	pred = model.predict(row)[0]
	return float(max(pred, 0.0))


def show_predict_tab(df: pd.DataFrame, model) -> None:
	st.subheader("Predict Car Price")
	st.caption("Enter car details to estimate resale value.")

	companies = sorted(df["company"].dropna().unique().tolist())
	fuel_types = sorted(df["fuel_type"].dropna().unique().tolist())

	col1, col2 = st.columns(2)
	with col1:
		company = st.selectbox("Company", companies)
		year = st.slider("Manufacturing Year", min_value=1995, max_value=CURRENT_YEAR, value=2018)
		fuel_type = st.selectbox("Fuel Type", fuel_types)
	with col2:
		company_car_names = sorted(
			df.loc[df["company"] == company, "name"].dropna().unique().tolist()
		)
		name = st.selectbox("Car Name", company_car_names)
		kms_driven = st.number_input("Kilometers Driven", min_value=0, max_value=1_000_000, value=30_000, step=1_000)

	if st.button("Predict Price", type="primary"):
		price = predict_price(
			model=model,
			name=name,
			company=company,
			year=int(year),
			kms_driven=int(kms_driven),
			fuel_type=fuel_type,
		)
		st.success(f"Estimated Price: {inr(price)}")


def show_data_tab(df: pd.DataFrame) -> None:
	st.subheader("Data Insights")

	c1, c2, c3 = st.columns(3)
	c1.metric("Records", f"{len(df):,}")
	c2.metric("Average Price", inr(float(df["Price"].mean())))
	c3.metric("Median Price", inr(float(df["Price"].median())))

	st.markdown("Top Companies by Listings")
	company_counts = df["company"].value_counts().head(10)
	st.bar_chart(company_counts)

	st.markdown("Price Trend by Year")
	year_price = df.groupby("year", as_index=False)["Price"].median().sort_values("year")
	st.line_chart(year_price, x="year", y="Price")

	st.markdown("Fuel Type Distribution")
	fuel_counts = df["fuel_type"].value_counts()
	st.bar_chart(fuel_counts)

	with st.expander("Show Dataset Preview"):
		st.dataframe(df.head(30), use_container_width=True)


def main() -> None:
	st.set_page_config(page_title="Car Price Prediction", page_icon="car", layout="wide")

	st.title("Car Price Prediction App")
	st.caption("Interactive UI for prediction and data exploration.")

	if not DATA_PATH.exists() or not MODEL_PATH.exists():
		st.error("Dataset or trained model not found. Please verify project files.")
		st.stop()

	df = load_data()
	model = load_model()

	tab_predict, tab_data = st.tabs(["Predict", "Data Insights"])

	with tab_predict:
		show_predict_tab(df, model)
	with tab_data:
		show_data_tab(df)


if __name__ == "__main__":
	main()
