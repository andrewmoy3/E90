import pulp as pl

def hybrid(costs, savings, budget, alpha=1.0, beta=0.001):
    """
    Maximizes number of buildings upgraded (weighted by alpha)
    and minimizes energy cost (weighted by beta).
    """
    n = len(costs)
    prob = pl.LpProblem("HybridProblem", pl.LpMaximize)
    vars = [pl.LpVariable(f"x{i}", cat=pl.LpBinary) for i in range(n)]

    total_buildings = []
    energy_savings = []

    for i in range(0, n, 2):
        x_better = vars[i]
        x_best = vars[i + 1]

        # Mutually exclusive: can’t choose both better and best
        prob += x_better + x_best <= 1

        # Building upgrade counts as 1
        total_buildings.append(x_better + x_best * 1.001)

        # Penalize future energy cost
        energy_savings.append(savings[i] * x_better + savings[i + 1] * x_best)

    # Total cost must be within budget
    prob += pl.lpDot(costs, vars) <= budget

    # Objective: maximize buildings upgraded plus weighted energy savings
    prob += alpha * pl.lpSum(total_buildings)  + beta * pl.lpSum(energy_savings)

    prob.solve(pl.PULP_CBC_CMD(msg=False))
    output = [v.value() for v in vars]
    score = prob.objective.value()
    return output
