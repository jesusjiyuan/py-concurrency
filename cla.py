from pulp import LpVariable, LpAffineExpression

class MyLpVariable(LpVariable):
    def __mul__(self, other):
        return type(self)(int(self) * int(other))
    def __floordiv__(self, other):
        return type(self)(int(self) // int(other))
    def __mod__(self, other):
        x = type(self)(int(self) % int(other))
        return x
    @property
    def numerator(self):
        return type(self)(int(self.varValue))
    @property
    def denominator(self):
        return type(self)(1)

class MyLpAffineExpression(LpAffineExpression):
    def __mod__(self, other):
        e = self.emptyCopy()
        e.constant  = (int(self.constant) % int(other))
        return e
