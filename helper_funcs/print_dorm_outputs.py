# Print out output of optimization for each budget in more readable format,
# including the dorm name and cost
def print_dorm_outputs(outputs, budgets, df, column_name):
    for i in range(len(outputs)):
        print("Budget: $", budgets[i])
        rows = [i for i, val in enumerate(outputs[i]) if val == 1.0]
        print(df.iloc[rows, 0:2])
        # total_savings = sum(df.iloc[rows][column_name])
        total_savings = df.iloc[rows][column_name]
        print(total_savings, column_name)
        print("Total savings: $", sum(total_savings))