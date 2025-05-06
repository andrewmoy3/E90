import pandas as pd 
import os

# Return list of csv files in the data directory
def get_csv_files(path):
    ret = []
    dir_list = os.listdir('./data')
    for file in dir_list:
        if file.endswith('.csv'):
            ret.append(os.path.join(path, file))
    return ret
# Read all csv files in the data directory and concatenate them into a single dataframe
def get_data():
    df = pd.DataFrame()
    csv_files = get_csv_files('./data')
    for file in csv_files:
        building = pd.read_csv(file)
        df = pd.concat([df, building], axis=0, ignore_index=True)
    return df
