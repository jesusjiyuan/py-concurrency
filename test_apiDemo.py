import pulp as pl

def test():
    model = pl.LpProblem("Example", pl.LpMinimize)
    _var = pl.LpVariable('a')
    _var2 = pl.LpVariable('a2')
    model += _var + _var2 == 1
    solver = pl.PULP_CBC_CMD()
    result = model.solve(solver)
    print(result)

test()