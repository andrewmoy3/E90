import numpy as np
import pandas as pd

# This function adds columns to the upgrades bucket dataframe to provide the differences between
# the current bucket and the upgrades buckets. 
def add_columns(df):
    # get df with only current buckets
    df_current = df[df['Bucket'] == 'Current'].set_index('Dorm Name')
    items = ['Energy Use', 'Energy Cost', 'Energy Use by sqft', 'Energy Cost by sqft', 'Carbon Emissions', 'Carbon Emissions by sqft']

    for item in items:
        df[f'{item} Savings'] = df.apply(
            lambda row: df_current.loc[row['Dorm Name'], item] - row[item], axis=1
        )

    # print(df_current)
    # print(df)
    # return df

