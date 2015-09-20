from scipy import optimize

def f(x):
	return x[0]*x[0]*x[1]
rranges = (slice(0, 0.5, 0.25), slice(-4, 4, 0.25))
x_min, fval, grid, jout = optimize.brute(f, rranges, full_output=True,
                              finish=None)
print x_min, fval