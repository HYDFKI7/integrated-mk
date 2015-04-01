

# following AMP-Chapter-11.pdf

import numpy as np

from scipy import optimize


cost_per_plant = [5400.0, 5600.0, 5800.0, 5700.0, 5500.0, 5200.0]
cumulative_demand = [1., 2., 4., 6., 7., 8.] # permissible states
years = [1981, 1982, 1983, 1984, 1985, 1986]

horizon = 5

# state is number of plants
# decision is number to construct
# return/utility is 

def dp_return(decision, state, n):
	if decision > 0:
		return 1500.0 + cost_per_plant[horizon-n+1]*decision
	else:
		return 0.

def dp_transition(decision, state, n):
	return state + decision


beta = 1.


# value_0(8) = 0
def dp_value(state, n):
	if cumulative_demand[horizon-n+1] - state > 3:
		print "IMPOSSIBLE"
		return None

	if n == 0:
		print "INVALID"
		return None

	if n == 1:
		if state == 8:
			return (0,0)
		else:
			return (8-state, dp_return(8-state,state,n))

	def v(decision):
		# print "ARG", decision
		value = dp_return(decision, state, n) + beta*dp_value( dp_transition(decision, state, n), n-1)[1]
		return value

	# possible_decisions = slice(0, cumulative_demand[horizon-n]-state, 1)
	if 8-state > 0:

		# don't build more than 8-state, can only build 3, build at least cumulative_demand-state
		min_build = cumulative_demand[horizon-n+1] - state
		max_build = min(1.+8.-state, 4.0)
		possible_decisions = slice(min_build, max_build, 1.)
		resbrute = optimize.brute(v, (possible_decisions,), full_output=True, finish=None) #optimize.fmin
		return resbrute
	else:
		return (0,0)


print "dp_value(s,n) = v_n(s)"
print "====================="
n = 4
for s in range(8,0,-1):
	if s >= cumulative_demand[horizon-n]:
		print s, dp_value(s,n)


# params = (2, 3, 7, 8, 9, 10, 44, -1, 2, 26, 1, -2, 0.5)
# def f1(z, *params):
#      x, y = z
#      a, b, c, d, e, f, g, h, i, j, k, l, scale = params
#      return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f)


# def f2(z, *params):
#      x, y = z
#      a, b, c, d, e, f, g, h, i, j, k, l, scale = params
#      return (-g*np.exp(-((x-h)**2 + (y-i)**2) / scale))


# def f3(z, *params):
#      x, y = z
#      a, b, c, d, e, f, g, h, i, j, k, l, scale = params
#      return (-j*np.exp(-((x-k)**2 + (y-l)**2) / scale))


# def f(z, *params):
#      x, y = z
#      a, b, c, d, e, f, g, h, i, j, k, l, scale = params
#      return f1(z, *params) + f2(z, *params) + f3(z, *params)

# a= slice(-4,4,0.25)
# rranges = (slice(-4, 4, 0.25), slice(-4, 4, 0.25))
# from scipy import optimize
# resbrute = optimize.brute(f, rranges, args=params, full_output=True,
#                               finish=optimize.fmin)
# print resbrute[0]  # global minimum
# print resbrute[1]  # function value at global minimum
