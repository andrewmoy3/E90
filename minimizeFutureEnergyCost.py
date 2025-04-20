import pulp as pl

# Given construction costs, future annual energy costs, and a minimum spending budget, 
# pick the upgrades that minimize future energy costs.
def minimizeFutureEnergyCost(costs, savings, budget):
    n = len(costs)

    # Define problem object
    # prob = pl.LpProblem("Problem", pl.LpMaximize)
    prob = pl.LpProblem("Problem", pl.LpMinimize)

    # Define binary decision variables
    vars = [pl.LpVariable(f"x{i}", cat=pl.LpBinary) for i in range(n)]

    # better, best are mutually exclusive
    for i in range(0, n, 2):
        prob += vars[i] + vars[i+1] <= 1

    prob += pl.lpDot(savings, vars)
    prob += pl.lpDot(costs, vars) >= budget

    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    profit = prob.objective.value()
    return output, profit
