import csv

import numpy as np
import pandas as pd

from Misc import apply_hash, apply_abs

location_path = '/Users/vladdragoi/Documents/ecommerce-data/'

data_path = location_path + 'data.csv'

cleaned_data_path = location_path + 'clean_data.csv'
#pivot_table_cleaned_data_path = location_path + 'pivot_table_clean_data.csv'


def normalize_data(data):
    df_matrix = pd.pivot_table(data, values='Quantity', index='CustomerID', columns='StockCode')
    df_matrix_norm = (df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min())
    d = df_matrix_norm.reset_index()
    d.index.names = ['Quantity_Scaled']
    return pd.melt(d, id_vars=['CustomerID'], value_name='Quantity_Scaled').dropna()


def model_df_to_csv(df):
    df.to_csv(cleaned_data_path, index=False)


full_df = pd.read_csv(data_path, encoding="ISO-8859-1")

model_df = full_df[["StockCode", "Quantity", "CustomerID"]]

model_df.dropna(subset=["CustomerID"], inplace=True)

model_df["StockCode"] = model_df["StockCode"].apply(apply_hash)

model_df["Quantity"] = model_df["Quantity"].apply(apply_abs)

model_df["CustomerID"] = model_df["CustomerID"].apply(apply_abs)


#normalize data


model_df = normalize_data(model_df)

model_pivot_df = pd.pivot_table(model_df, values='Quantity_Scaled', index='CustomerID', columns='StockCode').fillna(0)

model_df_to_csv(model_df)


