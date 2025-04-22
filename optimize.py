import pulp as pl

# Given construction costs, future annual energy costs, and a minimum spending budget, 
# pick the upgrades that minimize future energy costs.
def optimize(costs, objective, budget, maximize=False):
    n = len(costs)

    # Define binary decision variables
    vars = [pl.LpVariable(f"x{i}", cat=pl.LpBinary) for i in range(n)]

    # Define problem object
    if maximize:
        prob = pl.LpProblem("Problem", pl.LpMaximize)
        prob += pl.lpDot(costs, vars) <= budget
    else:
        prob = pl.LpProblem("Problem", pl.LpMinimize)
        prob += pl.lpDot(costs, vars) >= budget

    # better, best are mutually exclusive
    for i in range(0, n, 2):
        prob += vars[i] + vars[i+1] <= 1

    prob += pl.lpDot(objective, vars)

    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    profit = prob.objective.value()
    return output, profit
