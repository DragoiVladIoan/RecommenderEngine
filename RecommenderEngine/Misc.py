import pandas as pd


def generate_columns():
    columns = []
    for i in range(0, 5):
        columns.append('TOP ' + str(i + 1) + ' StockCode')
        columns.append('TOP ' + str(i + 1) + ' Rating')
    return pd.DataFrame(columns=columns)


def concat_data_from_list(my_list, df, current_index):
    i = 0
    for row in my_list:
        df.at[current_index, 'TOP ' + str(i + 1) + ' StockCode'] = row['StockCode']
        df.at[current_index, 'TOP ' + str(i + 1) + ' Rating'] = row['rating']
        i += 1
    return df


def apply_hash(x):
    try:
        int(x)
        return x
    except:
        return abs(int(hash(x)/1000000000000))


def apply_abs(x):
    return abs(int(x))


