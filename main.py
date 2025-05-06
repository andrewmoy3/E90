import os
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm 
from helper_funcs.optimize import optimize
from helper_funcs.print_dorm_outputs import print_dorm_outputs
from helper_funcs.mostBuildings import mostBuildings
from helper_funcs.get_data import get_data
from helper_funcs.add_columns import add_columns
from matplotlib import pyplot as plt 
from helper_funcs.hybrid import hybrid   
from helper_funcs.plot import plot, plot_bar_chart, plot_line_chart
import matplotlib.patches as patches

def get_dorm_outputs(df, column_name, costs, budgets, maximize=False):
    col_to_be_optimized = df[column_name].to_numpy() 
    outputs = []
    total_savings = []
    for i in budgets:
        choices, savings = optimize(costs, col_to_be_optimized, i, maximize=maximize)
        outputs.append(choices)
        total_savings.append(savings)
    
    if maximize:
        filepath = "./outputs/maximize/" + column_name.lower().replace(" ", "_") + "_maximize"
    else:
        filepath = "./outputs/minimize/" + column_name.lower().replace(" ", "_") + "_minimize"
    plot(np.array(outputs), total_savings, np.array(budgets), title=column_name, filepath=filepath, ylabel=[f"{a} {b}" for a, b in df.iloc[:, 0:2].to_numpy()])
    # print_dorm_outputs(outputs, budgets, df, column_name)
    return outputs, total_savings

def main():
    df = get_data() # Get data from csv files
    add_columns(df) # Add savings columns to the dataframe
    df.to_csv('./data.csv', index=False) # write full df to csv
    df_lthw = df.loc[df['Bucket'] != 'Current'] # filter out current bucket
    costs = df_lthw['Cost'].to_numpy() # costs of building upgrades 
    maximum_budget = sum([max(costs[i], costs[i+1]) for i in range(0, len(costs), 2)]) # total cost of most expensive bucket for every pair of buckets
    num_budgets = 50 # number of budgets per item to optimize
    budgets = np.linspace(0, maximum_budget, num=num_budgets).tolist() # budgets list
    dorm_names = [f"{a} {b}" for a, b in df_lthw.iloc[:, 0:2].to_numpy()] # get dorm names from first two cols of dataframe

    # items = ['Energy Use by sqft', 'Energy Cost by sqft', 'Carbon Emissions by sqft']
    items = ['Energy Use', 'Energy Cost', 'Carbon Emissions']
    # items = ['Energy Use', 'Energy Cost', 'Carbon Emissions', 'Energy Use by sqft', 'Energy Cost by sqft', 'Carbon Emissions by sqft']
    item_values = []
    total_bar_chart = np.zeros(len(dorm_names)) 
    corr_df = df.iloc[:, [3, 4, 11, 5, 6, 12]]
    # corr_df = df.iloc[:, [14, 15, 18, 16, 17, 19]]
    correlation_matrix = corr_df.corr(method='pearson')
    print(correlation_matrix)
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(left=0.3, right=0.95, top=0.9, bottom=0.1)  # adjust margins
    fig.patches.append(
        patches.Rectangle(
            (0,0), 1, 1,
            transform=fig.transFigure,
            facecolor='none',
            edgecolor='white',
            linewidth=2,
            zorder=1000
        )
    )
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix of Energy Use, Cost, and Carbon Emissions")
    plt.subplots_adjust(bottom=0.4, left=0.4)
    fig.patch.set_facecolor('#37474f')
    plt.show()


    ###########################
    # DON'T DO MINIMIZING
    # Constraint: Required to spend 'budget' or more
    # Minimizes items in 'items'
    # for item in tqdm(items, desc="Optimizing minimization functions", unit="item"):
    #     outputs = get_dorm_outputs(df_lthw, item, costs, budgets, maximize=False)
    #     for output in outputs:
    #         bar_chart += output
    
    ###########################
    # Constraint: Maximum Budget
    # Maximizes the savings of items in 'items' when compared to 'current'
    for item in tqdm(items, desc="Optimizing maximization functions", unit="item"):
        bar_chart = np.zeros(len(dorm_names)) # create empty bar chart array to track all occurances
        item += ' Savings'
        outputs, savings = get_dorm_outputs(df_lthw, item, costs, budgets, maximize=True)
        item_values.append(savings)
        for output in outputs:
            bar_chart += output
            total_bar_chart += output
        plot_bar_chart(bar_chart, dorm_names, item, './outputs/maximize/' + item.lower().replace(" ", "_") + '_bar_chart.png')

    ###########################
    # Constraint: Maximum Budget
    # Maximize number of buildings upgraded
    outputs = []
    bar_chart = np.zeros(len(dorm_names)) 
    for i in budgets:
        choices, num_buildings = mostBuildings(costs, i)
        outputs.append(choices)
        bar_chart += choices
    plot(np.array(outputs), [], np.array(budgets), title="Number of Buildings", filepath='./outputs/maximize/num_buildings', ylabel=dorm_names)
    plot_bar_chart(bar_chart, dorm_names, "Number of Buildings", './outputs/maximize/num_buildings_bar_chart.png')

    plot_line_chart(item_values, items, budgets)
    # plot_bar_chart(total_bar_chart, dorm_names, "Total Number of Occurrences (sqft)", './outputs/total_bar_chart.png')
    plot_bar_chart(total_bar_chart, dorm_names, "Total Number of Occurrences", './outputs/total_bar_chart.png')

    
    
    ###########################
    # Combine max buildings and savings with weights
    # alpha = max buildings, beta = savings
    # for item in tqdm(items, desc="Optimizing hybrid functions", unit="item"):
    #     item += ' Savings'
    #     outputs = []
    #     for budget in budgets:
    #         outputs.append(hybrid(costs, df_lthw[item].to_numpy(), budget, alpha=1, beta=0))
    #         bar_chart += outputs[-1]
    #     plot(np.array(outputs), 0, np.array(budgets), title=item, filepath=f'./outputs/hybrid/{item.lower().replace(" ", "_")}', ylabel=dorm_names)
    

    
    # st.text("test")
    # st.bar_chart(bar_chart)



if __name__ == "__main__":
    main()
