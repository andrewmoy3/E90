import pulp as pl

solver_list = pl.listSolvers(onlyAvailable=True)
print(solver_list)

problem = pl.LpProblem("Farmers", pl.LpMaximize)    

# Define decision variables
x = pl.LpVariable("x", lowBound=0)  # x >= 0
y = pl.LpVariable("y", lowBound=0)  # y >= 0

problem += x * 1.2 + y * 1.7

problem += x       <= 3000  # potatoes
problem +=       y <= 4000  # carrots
problem += x + y <= 5000  # fertilizer

status = problem.solve(pl.PULP_CBC_CMD(msg=False))

print("potatoes:", x.value())
print("carrots:", y.value())
print("profit:", problem.objective.value())