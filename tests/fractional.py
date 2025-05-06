import pulp as pl
import matplotlib.pyplot as plt
import numpy as np

# https://slama.dev/youtube/linear-programming-in-python/

name = "Willets_Building_Upgrades"

# budget in dollars
budgets = list(range(10000000, 100000000, 10000000))

# Cost of electricity in dollars per BTU per year
# Would likely vary over the course of a year/day -- this is a simplification
cost_per_btu = .5

upgrade_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# cost to build per square foot
costs = np.array([150, 130, 230, 200, 250, 300, 270, 320, 350, 400])
# BTUs saved per square foot per year
energy_savings = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
savings = energy_savings * cost_per_btu

outputs = []
profits = []
sqft = 55137

for budget in budgets:
    # Given x upgrades, costs, and savings, pick the upgrades that maximize savings
    # while staying under budget
    n = len(upgrade_names)
    # Define problem object
    prob = pl.LpProblem(name, pl.LpMaximize)

    vars = [pl.LpVariable(f"x{i}", lowBound=0) for i in range(n)]

    prob += pl.lpDot(savings, vars)
    for var in vars:
        prob += var <= sqft
    prob += pl.lpDot(costs, vars) <= budget
    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    profit = prob.objective.value()
    outputs.append(output)
    profits.append(profit)

outputs = np.array(outputs)
profits = np.array(profits)

print(outputs)

figure, axis = plt.subplots(2, 2)
# plot cost savings vs budget (dollars saved (per unit time) as a function of budget)
axis[0, 0].plot(budgets, profits)
axis[0, 0].set_title("Cost Savings vs Budget")

# plot energy savings vs budget (BTUS saved (per unit time) as a function of budget)
axis[0, 1].plot(budgets, profits / cost_per_btu)
axis[0, 1].set_title("Energy Savings vs Budget")

# plot chosen upgrades vs budget (upgrades chosen as a function of budget)
# rows, cols = np.where(outputs == 1)
# x_coords = [budgets[i-1] for i in cols]
# axis[1, 0].scatter(x_coords, rows, c='black', marker='o')


plt.show()