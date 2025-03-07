# Proyek Data Analysis

## Description
Proyek Analisis Data menggunakan dataset e-commerce

## Project Structure
```
| Dashboard
    |_ dashboard.py
    |_ function.py
    |_ logo.png
| Data
    |_ all_data.csv
    |_ customers_dataset.csv
    |_ geolocation_dataset.csv
    |_ order_items_dataset.csv
    |_ order_payments_dataset.csv
    |_ order_reviews_dataset.csv
    |_ orders_dataset.csv
    |_ product_category_name_translation.csv
    |_ products_dataset.csv
    |_ sellers_dataset.csv
| notebook.ipynb
| README.md
| requirements.txt
```

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```
## Setup Jupyter Notebook
```
pip install notebook
jupyter notebook
```

## Run steamlit app
```
cd Dashboard
streamlit run dashboard.py
```