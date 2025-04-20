import os
import numpy as np
import pandas as pd
from minimizeFutureEnergyCost import minimizeFutureEnergyCost
from mostBuildings import mostBuildings
from plot import plot

def get_csv_files(path):
    ret = []
    dir_list = os.listdir('./data')
    for file in dir_list:
        if file.endswith('.csv'):
            ret.append(os.path.join(path, file))
    return ret

def get_data():
    df = pd.DataFrame()
    csv_files = get_csv_files('./data')
    for file in csv_files:
        building = pd.read_csv(file)
        df = pd.concat([df, building], axis=0, ignore_index=True)
        # df.to_csv('./test.csv', index=False)
    return df

def main():
    df = get_data()
    df_lthw = df.loc[df['Bucket'] != 'Current'] # filter out current bucket

    # Total Annual Cost of Natural Gas for Current Buildings
    print("Current Annual Cost of Natural Gas: $", sum(df.loc[df['Bucket'] == 'Current', 'Energy Cost ($/yr)']))
    # cost to build 
    costs = df_lthw['Cost($)'].to_numpy() 
    # total cost of most expensive bucket for every pair of buckets
    max_minimum = sum([max(costs[i], costs[i+1]) for i in range(0, len(costs), 2)]) 


    ###########################
    # Minimize energy costs if you have to spend

    column_name = 'Annual Energy Use/EUI (kBTU/sqft/yr)'
    # column_name = 'Energy Cost ($/yr)'
    outputs = []
    annual_costs = []
    energy_costs = df_lthw[column_name].to_numpy() # future annual energy costs
    increment = 5000000
    budgets = range(0, max_minimum, increment)
    for i in budgets:
        choices, annual_cost = minimizeFutureEnergyCost(costs, energy_costs, i)
        outputs.append(choices)
        annual_costs.append(annual_cost)
    
    plot(np.array(outputs), annual_costs, np.array(budgets), ylabel=[f"{a} {b}" for a, b in df_lthw.iloc[:, 0:2].to_numpy()])

    ########## 
    ## Print out names of dorms for each budget
    for i in range(len(outputs)):
        print("Minimum: $", budgets[i])
        rows = [i for i, val in enumerate(outputs[i]) if val == 1.0]
        print(df_lthw.iloc[rows, 0:2])

    ##########
    ## Maximize number of upgrade buildings
    outputs = []
    for i in budgets:
        choices, num_buildings = mostBuildings(costs, i)
        print("Number of buildings:", num_buildings)
        outputs.append(choices)
    plot(np.array(outputs), [], np.array(budgets), ylabel=[f"{a} {b}" for a, b in df_lthw.iloc[:, 0:2].to_numpy()])

if __name__ == "__main__":
    main()
