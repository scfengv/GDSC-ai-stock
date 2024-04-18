import os
import pandas as pd

def find_csv(directory):

    df_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                df_list.append(df)
    
    if df_list:
        return pd.concat(df_list, ignore_index = True)