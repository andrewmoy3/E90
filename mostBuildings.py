import pulp as pl

# Given construction costs, future annual energy costs, and a minimum spending budget, 
# pick the upgrades that minimize future energy costs.
def mostBuildings(costs, budget):
    n = len(costs)

    # Define problem object
    prob = pl.LpProblem("Problem", pl.LpMaximize)
    # prob = pl.LpProblem("Problem", pl.LpMinimize)

    # Define binary decision variables
    vars = [pl.LpVariable(f"x{i}", cat=pl.LpBinary) for i in range(n)]

    total_buildings = []
    best_preference_bonus = []

    for i in range(0, n, 2):
        x_better = vars[i]
        x_best = vars[i + 1]

        # better, best are mutually exclusive
        prob += x_better + x_best <= 1

        # Each building can contribute at most 1 to the count
        total_buildings.append(x_better + x_best)

        # Add a small bonus for choosing 'Best'
        best_preference_bonus.append(0.001 * x_best)

    prob += pl.lpDot(costs, vars) <= budget

    # problem to maximize - number of buildings + incentive for best
    # prob += pl.lpSum(vars)  
    prob += pl.lpSum(total_buildings) + pl.lpSum(best_preference_bonus)

    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    num = prob.objective.value()
    return output, num
