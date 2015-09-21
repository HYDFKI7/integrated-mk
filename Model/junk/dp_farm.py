
'''
return/cost of decision d_n \in D_n (permissible decisions) and state with n stages to go s_n
	f_n(d_n, s_n)

transition function
	s_{n-1}=t_n(d_n, s_n)

optimize choice of d_n, ..., d_0 to solve value
	v_n (s_n) = Max [ f_n (d_n, s_n) + \beta^1 f_{n-1}(d_{n-1}, s_{n-1}) + ... + \beta^n f_0(d_0, s_0) ]
	subject to permissible decisions and s_{m-1} = t_m(d_m , s_m) and d_m \in D_m for m=0,...,n
->
	v_n(s_n) = Max [ f_n(d_n, s_n) + \beta v_{n-1}(s_{n-1}) ]
->
	v_n(s_n) = Max [ f_n(d_n, s_n) + \beta v_{n-1}(t_n(d_n, s_n)) ] 
	subject to d_n \in D_n

zero stage problem
	v_0 (s_0 ) = Max f_0 (d_0 , s_0 )


	
'''

import numpy as np
from scipy import optimize

cost_per_plant = [None, 5400.0, 5600.0, 5800.0, 5700.0, 5500.0, 5200.0]
cumulative_demand = [0., 1., 2., 4., 6., 7., 8.] # permissible states
years = [1980, 1981, 1982, 1983, 1984, 1985, 1986]

horizon = 6

def dp_return(decision, state, n):
	if decision > 0:
		return 1500.0 + cost_per_plant[horizon-n+1]*decision
	else:
		return 0.


def dp_transition(decision, state, n):
	return state + decision

beta = 0.87


def get_permissible_decisions(state, n):
	if n == 0:
		return [0.]
	min_build = max(0., cumulative_demand[horizon-n+1] - state)
	max_build = min(8.- state, 3.0)
	return np.arange(min_build, max_build+1)


# dp_value



def get_optimal_decisions(years_ahead, starting_state, debug=True):

	discrete_states = np.arange(0,9)
	optimal_decisions = {}
	optimal_returns = {}

	future_min_returns = {8. : 0} 

	for n in range(years_ahead):
		optimal_decisions[n] = {}
		optimal_returns[n] = {}

		permissible_states = np.arange(cumulative_demand[horizon-n], 9)
		
		if n == years_ahead-1:
			permissible_states = [starting_state]

		if debug:
			print permissible_states
			
		# curiously this "resets" future_min_returns = current_min_returns
		current_min_returns = {}

		for state in permissible_states:
		# for state_i in range(len(discrete_states)):
		# 	state = discrete_states[state_i]
		# 	if not state in permissible_states:
		# 		continue

			# resbrute = optimize.brute(v, (possible_decisions,), full_output=True, finish=None)

			permissible_decisions = get_permissible_decisions(state, n)

			def ret_func(decision):
				return dp_return(decision, state, n) + beta*future_min_returns[ dp_transition(decision, state, n) ]

			returns = map(ret_func, permissible_decisions)
			min_i = np.argmin(returns)
			optimal_decisions[n][state] = permissible_decisions[min_i]
			optimal_returns[n][state] = returns[min_i]

			current_min_returns[state] = np.min(returns)

			# print "optimal", permissible_decisions[np.argmin(returns)]

			# if current_state == state && n == years_ahead-1:
			# 	print "SETTING"
			# 	optimal = permissible_decisions[np.argmin(returns)]

			if debug: 
				print '   ', permissible_decisions, np.around(returns)

		future_min_returns = current_min_returns

	return optimal_decisions, optimal_returns

# compare output with Figure 11.10
optimal_decisions, optimal_returns = get_optimal_decisions(years_ahead=7, starting_state=0, debug=True)

print "-----------------------"

print "optimal path starting 6 years out with 0"
print "-----------------------"
print 'decision', 'return'
print "-----------------------"
current_state = 0
for n in range(6):
	n = 6-n
	optimal_decision = optimal_decisions[n][current_state]
	optimal_return = optimal_returns[n][current_state]
	print optimal_decision, np.round(optimal_return)
	current_state = dp_transition(optimal_decision, current_state, n)


