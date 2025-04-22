import os
import numpy as np
import pandas as pd
from optimize import optimize
from mostBuildings import mostBuildings
from add_columns import add_columns
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
    add_columns(df)
    df.to_csv('./test.csv', index=False)
    return df

## Print out names of dorms for each budget
def print_dorm_outputs(outputs, budgets, df):
    for i in range(len(outputs)):
        print("Minimum: $", budgets[i])
        rows = [i for i, val in enumerate(outputs[i]) if val == 1.0]
        print(df.iloc[rows, 0:2])

def get_dorm_outputs(df, column_name, costs, budgets, maximize=False):
    col_to_be_optimized = df[column_name].to_numpy() 
    outputs = []
    annual_costs = []
    for i in budgets:
        choices, annual_cost = optimize(costs, col_to_be_optimized, i, maximize=maximize)
        outputs.append(choices)
        annual_costs.append(annual_cost)
    
    title = column_name.lower().replace(" ", "_")
    if maximize:
        title += "_maximize"
    else:
        title += "_minimize"
    plot(np.array(outputs), annual_costs, np.array(budgets), title=f'{title}', ylabel=[f"{a} {b}" for a, b in df.iloc[:, 0:2].to_numpy()])
    # print_dorm_outputs(outputs, budgets, df)

def main():
    df = get_data()

    df_lthw = df.loc[df['Bucket'] != 'Current'] # filter out current bucket
    
    # costs of building upgrades 
    costs = df_lthw['Cost'].to_numpy() 

    # total cost of most expensive bucket for every pair of buckets
    maximum_budget = sum([max(costs[i], costs[i+1]) for i in range(0, len(costs), 2)]) 

    # budgets list
    budgets = np.linspace(0, maximum_budget, num=200).tolist()

    items = ['Energy Use', 'Energy Cost', 'Energy Use by sqft', 'Energy Cost by sqft', 'Carbon Emissions', 'Carbon Emissions by sqft']

    ###########################
    # Constraint: Required to spend 'budget' or more
    # Minimizes items in 'items'
    for item in items:
        get_dorm_outputs(df_lthw, item, costs, budgets, maximize=False)
    
    ###########################
    # Constraint: Maximum Budget
    # Maximizes the savings of items in 'items' when compared to 'current'
    for item in items:
        item += ' Savings'
        get_dorm_outputs(df_lthw, item, costs, budgets, maximize=True)
    

    ###########################
    # Constraint: Maximum Budget
    # Maximize number of buildings upgraded
    outputs = []
    for i in budgets:
        choices, num_buildings = mostBuildings(costs, i)
        outputs.append(choices)
    plot(np.array(outputs), [], np.array(budgets), title='max_budget_num_buildings', ylabel=[f"{a} {b}" for a, b in df_lthw.iloc[:, 0:2].to_numpy()])

    # 1-6 while maximizing number of buildings


if __name__ == "__main__":
    main()
