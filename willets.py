import pulp as pl
import matplotlib.pyplot as plt
import numpy as np

name = "Willets_Building_Upgrades"

# budget in dollars
budget = 100000
# Cost of electricity in dollars per BTU per year
# Would likely vary over the course of a year/day -- this is a simplification
cost_per_btu = .5

upgrade_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# cost to build per square foot
costs = np.array([15000, 13000, 23000, 20000, 25000, 30000, 27000, 32000, 35000, 40000])
# BTUs saved per square foot per year
energy_savings = np.array([1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])
savings = energy_savings * cost_per_btu

# print(energy_savings/costs)

outputs = []
profits = []

budgets = list(range(10000, 100000, 10000))
print(budgets)

for budget in budgets:
    # Given x upgrades, costs, and savings, pick the upgrades that maximize savings
    # while staying under budget
    n = len(upgrade_names)
    # Define problem object
    prob = pl.LpProblem(name, pl.LpMaximize)

    vars = [pl.LpVariable(f"x{i}", cat=pl.LpBinary) for i in range(n)]

    prob += pl.lpDot(savings, vars)
    prob += pl.lpDot(costs, vars) <= budget

    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    profit = prob.objective.value()
    outputs.append(output)
    profits.append(profit)
    # print("weights:", [v.value() for v in vars])
    # print("profit:", prob.objective.value())

outputs = np.array(outputs)
profits = np.array(profits)

figure, axis = plt.subplots(2, 2)
# plot cost savings vs budget (dollars saved (per unit time) as a function of budget)
axis[0, 0].plot(budgets, profits)
axis[0, 0].set_title("Cost Savings vs Budget")

# plot energy savings vs budget (BTUS saved (per unit time) as a function of budget)
axis[0, 1].plot(budgets, profits / cost_per_btu)
axis[0, 1].set_title("Energy Savings vs Budget")

# plot chosen upgrades vs budget (upgrades chosen as a function of budget)
print(outputs)
rows, cols = np.where(outputs == 1)
x_coords = [budgets[i-1] for i in cols]
axis[1, 0].scatter(x_coords, rows, c='black', marker='o')


plt.show()