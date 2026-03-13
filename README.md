# Car Price Prediction

An applied machine learning project that predicts used car prices from a real-world listings dataset.

## Dataset

- Source file: dataset/data.csv
- Cleaned file: dataset/cleaned_data.csv
- Target column: Price

The raw dataset contains noisy values (for example non-numeric prices and inconsistent mileage text), which are cleaned in the notebook pipeline.

## Pipeline Overview

The notebook workflow in notebook/notebook.ipynb performs the following:

1. Load and inspect raw data
2. Clean columns:
   - Remove rows with invalid year/price/kilometer entries
   - Convert numeric fields to proper types
   - Drop missing fuel_type values
3. Feature preparation:
   - Keep categorical and numeric predictors
   - Add engineered feature: car_age = 2026 - year
4. Train/test split
5. Train and compare multiple models
6. Evaluate with regression metrics
7. Save final model to model/RegressionModel.pkl

## Model Output

The trained model is saved as:

- model/RegressionModel.pkl

This file is loaded directly by the Streamlit app for predictions.

## Tech Stack

- Python
- pandas, numpy
- scikit-learn
- Jupyter Notebook
- Streamlit
