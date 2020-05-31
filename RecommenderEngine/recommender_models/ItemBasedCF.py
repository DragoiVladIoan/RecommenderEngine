import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import pairwise_distances
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import CountVectorizer
import math
from scipy import spatial
location_path = '/Users/vladdragoi/Documents/ecommerce-data/'
cleaned_data_path = location_path + 'clean_data.csv'
pivot_table_cleaned_data_path = location_path + 'pivot_table_clean_data.csv'


model_df = pd.read_csv(cleaned_data_path)

print(model_df)

pivot_df = pd.pivot_table(model_df, values='Quantity_Scaled', index='CustomerID', columns='StockCode').fillna(0)

print(pivot_df)

#unsupervised k nearest neighbours



k = 3


cos_knn = NearestNeighbors(n_neighbors=k, algorithm="brute", metric="cosine")
cos_knn_fit = cos_knn.fit(pivot_df.T.values)
item_distances, item_indexes = cos_knn_fit.kneighbors()


recommendations_df = pd.DataFrame(columns=["Target_StockCode", "TOP1_StockCode", "TOP2_StockCode", "TOP3_StockCode"])


pivot_df = pivot_df.reset_index()

model_df = model_df.sort_values("StockCode")
pivot_df = pivot_df.drop(columns=["CustomerID"])

print("----")
print(pivot_df.T)
print("----")

for i in range(0, len(item_indexes)):
    recommendations_df.at[i, "Target_StockCode"] = pivot_df.T.index.values.tolist()[i]
    for rec in range(0, k):
        index = pivot_df.T.index.values.tolist()[item_indexes[i][rec]]
        print("Index=", index)
        recommendations_df.at[i, "TOP" + str(rec+1) + "_StockCode"] = index

    print(recommendations_df)

print(item_indexes)
