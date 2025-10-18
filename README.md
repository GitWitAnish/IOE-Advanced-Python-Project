# Car Price Prediction

A machine learning project that predicts car prices based on various features using Linear Regression. This project includes data cleaning, exploratory data analysis, model training, and evaluation.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset](#dataset)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Performance](#model-performance)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Results](#results)
- [Contact](#contact)

## 🎯 Overview

This project aims to predict the selling price of used cars based on features such as:

- Car name and company
- Year of manufacture
- Kilometers driven
- Fuel type

The model uses Linear Regression with One-Hot Encoding for categorical variables to make accurate price predictions.

## 📊 Dataset

- **Original Dataset**: `data.csv` - Contains 893 car records
- **Cleaned Dataset**: `cleaned_data.csv` - Contains 817 records after cleaning
- **Features**:
  - `name`: Car model name
  - `company`: Car manufacturer
  - `year`: Year of manufacture
  - `kms_driven`: Distance driven in kilometers
  - `fuel_type`: Type of fuel (Petrol/Diesel/CNG/LPG)
  - `Price`: Selling price (target variable)

## ✨ Features

### Data Cleaning

- Removed non-numeric year values
- Handled "Ask For Price" entries
- Cleaned and converted price and kilometers driven to numeric format
- Removed missing fuel type entries
- Standardized car names to first 3 words
- Filtered out outlier prices (>6 million)

### Model Features

- **Algorithm**: Linear Regression
- **Preprocessing**: One-Hot Encoding for categorical variables
- **Pipeline**: Scikit-learn pipeline for streamlined processing
- **Model Selection**: Cross-validation with 1000 iterations to find optimal random state

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/car-price-prediction.git
cd car-price-prediction
```

2. Install required dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

## 💻 Usage

### Running the Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

## 📈 Model Performance

The model achieves optimal performance through:

- **Cross-validation**: 1000 iterations with different random states
- **Best R² Score**: Available in the trained model (check notebook output)
- **Feature Engineering**: Categorical encoding and numerical standardization

## 📁 Project Structure

```
Car-Price-Prediction/
├── notebook.ipynb              # Main Jupyter notebook
├── data.csv                    # Original dataset
├── cleaned_data.csv           # Processed dataset
├── LinearRegressionModel.pkl  # Trained model
├── README.md                  # Project documentation
└── .gitignore                # Git ignore file
```

## 🛠️ Technologies Used

- **Python 3.x**
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning library
  - Linear Regression
  - One-Hot Encoder
  - Train-test split
  - Pipeline
  - R² Score
- **Jupyter Notebook** - Interactive development environment

## 📊 Results

The model successfully predicts car prices with the following characteristics:

### Data Insights

- Dataset reduced from 893 to 817 records after cleaning
- Handled various data quality issues including missing values and inconsistent formats
- Price range filtered to exclude unrealistic outliers (>₹6,000,000)

### Model Features

- **Input Features**: Car name, company, year, kilometers driven, fuel type
- **Output**: Predicted price in INR
- **Preprocessing**: Automatic handling of categorical and numerical features
- **Optimization**: Model selection through extensive cross-validation

### Example Prediction

The trained model can predict prices for cars like:

- **Input**: Maruti Suzuki Swift, 2019, 100 km, Petrol
- **Output**: Predicted market price

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---
