import os
import re
import pandas as pd

def get_csv_files(path):
    ret = []
    dir_list = os.listdir('./data')
    for file in dir_list:
        if file.endswith('.csv'):
            ret.append(os.path.join(path, file))
    return ret

def get_data():
    dataframes = []
    csv_files = get_csv_files('./data')
    for file in csv_files:
        rgx = re.compile(r'([A-Za-z0-9_]+)\.csv')
        building_name = rgx.search(file).group(1)
        df = pd.read_csv(file)
        df.rename(columns={"Scenario": building_name}, inplace=True)
        dataframes.append(df)

    return dataframes

def main():
    dataframes = get_data()
    for df in dataframes:
        print(df)

if __name__ == "__main__":
    main()
