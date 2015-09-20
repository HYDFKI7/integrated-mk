import numpy as np

from scipy import optimize

from farm_optimize import lp_for_dp, load_crops

'''


In truth this isn't dynamic because prices, inflation etc. are not dynamic yet.

It's good to have data in a semi-structured format such as JSON, with text names and random attributes, eg. source.
However simple variables and arrays seem a better fit for function arguments because 
1. using objects is asking for scoping bugs
2. it's easier to stick with language specific paradigms, eg. tuples make okay hash keys, objects don't


``In order to approach this problem via dynamic programming, we need to define the stages of the system,
the state space for each stage, and the optimal-value function.''

NOTE
decision is (increase irrigated area (ha), increase irrigation efficiency (%))
state is (irrigated area (ha), irrigation efficiency (%))

'''


# TODO sources 
farm = {"irrigated area (ha)": 782.*7., "dryland area (ha)": 180.*7.}
farm["total area (ha)"] = farm["irrigated area (ha)"] + farm["dryland area (ha)"]  

water_licence = {"sw unregulated (ML)": 1413., "gw (ML)": 2200.}
water_licence["total (ML)"] = water_licence['sw unregulated (ML)'] + water_licence['gw (ML)']

crops = load_crops()

costs = {
	'increase irrigation efficiency ($/ML/%)': 500./10., # $500 for 10%, $1000 for 20% per ML
	'increase irrigation efficiency ($/ha/%)': 1000./10., # $ 1000 for 10%, $2000 for 20% per ha
	'increase irrigated area ($/ha)': 1500.
}

beta = 1.

# state max and discretisation
min_area, max_area = (farm["irrigated area (ha)"], farm["total area (ha)"])
d_area = (max_area-min_area)/10. #100.
min_efficiency, max_efficiency = (50., 80.)
d_efficiency = 10.

def dp_transition(decision, state):
	# ha, %
	area_increase, efficiency_increase = decision
	area, efficiency = state
	return (area + area_increase, efficiency + efficiency_increase)


def dp_return(decision, state):
	area_increase, efficiency_increase = decision
	area, efficiency = state

	# TODO this assumes investment reaps no reward this year, but only in following years
	farm_profit = lp_for_dp(
		crops = crops, 
		farm_area = {'irrigated area (ha)': area, "dryland area (ha)": farm["total area (ha)"] - area},
		water_licence = (efficiency / 100.) * water_licence["total (ML)"])

	decision_cost = \
		water_licence["total (ML)"] * efficiency_increase * costs['increase irrigation efficiency ($/ML/%)'] \
		+ (area + area_increase) * efficiency_increase * costs['increase irrigation efficiency ($/ha/%)'] \
		+ area_increase * costs['increase irrigated area ($/ha)'] 
	

	return farm_profit - decision_cost


def optimal_return_over_permissible_decisions(state, future_optimal_returns):
	area, efficiency = state

	optimal_return = 0
	optimal_decision = (0.,0.)

	# for all permissible decisions
	for efficiency_increase in np.arange(0, d_efficiency + max_efficiency - efficiency, d_efficiency):
		for area_increase in np.arange(0, d_area + max_area - area, d_area):
			current_decision = (area_increase, efficiency_increase)
			
			current_return = dp_return(current_decision, state) + beta * future_optimal_returns[ dp_transition(current_decision, state) ]
			
			if current_return > optimal_return:
				optimal_return = current_return
				optimal_decision = current_decision

	return optimal_return, optimal_decision


def backwards_fill_optimal(years_ahead):
	# stage, state -> optimal return
	optimal_decisions = {}
	optimal_returns = {0: {}}

	# initialise optimal returns for final stage (no future returns)
	# for all vaid states
	for efficiency in np.arange(min_efficiency, d_efficiency + max_efficiency, d_efficiency):
		for area in np.arange(min_area, d_area + max_area, d_area):
			state = (area, efficiency)
			optimal_returns[0][state] = dp_return( (0.,0.), state )
			
	for n in range(1, years_ahead):
		optimal_decisions[n] = {}
		optimal_returns[n] = {}

		# for all vaid states
		for efficiency in np.arange(min_efficiency, d_efficiency + max_efficiency, d_efficiency):
			for area in np.arange(min_area, d_area + max_area, d_area):
				state = (area, efficiency)

				optimal_returns[n][state], optimal_decisions[n][state] = optimal_return_over_permissible_decisions(state, optimal_returns[n-1])

	return optimal_returns, optimal_decisions


def forward_trace_optimal(optimal_returns, optimal_decisions, years_ahead):
	optimal_trace = []
	current_state = (farm["irrigated area (ha)"], 50.)
	for n in range(years_ahead):
		n = years_ahead-n-1
		optimal_return = optimal_returns[n][current_state]
		if n == 0:
			optimal_trace.append([None, current_state, optimal_return])
		else: 	
			optimal_decision = optimal_decisions[n][current_state]
			optimal_trace.append([optimal_decision, current_state, optimal_return])
			current_state = dp_transition(optimal_decision, current_state)
	return optimal_trace


if __name__ == '__main__':
	
	years_ahead = 7
	opt_ret, opt_dec = backwards_fill_optimal(years_ahead)

	print "-----------------------"
	print "optimal path "
	print "-----------------------"
	print 'decision', 'state', 'return'
	print "-----------------------"

	optimal_trace = forward_trace_optimal(opt_ret, opt_dec, years_ahead)

	for i in optimal_trace:
		print i[0], i[1], np.round(i[2]/1000000., 3)




# print "-----------------------"
# print "farm profit base"
# farm_profit_base = lp_for_dp(
# 	crops = crops, 
# 	farm_area = {'irrigated area (ha)': farm["irrigated area (ha)"], "dryland area (ha)": farm["total area (ha)"] - farm["irrigated area (ha)"]},
# 	water_licence = (50. / 100.) * water_licence["total (ML)"])

# print np.round(farm_profit_base/1000000., 3)

# print "-----------------------"




'''	
4 years it changes, in truth this isn't dynamic because prices, inflation etc. are not dynamic

(1200.0, 0.0) (6674.0, 50.0) 13.836
(0.0, 0.0) (6674.0, 50.0) 12.193
(0.0, 0.0) (6674.0, 50.0) 8.128
None (6674.0, 50.0) 4.064


(0.0, 0.0) (5474.0, 50.0) 10.329
(0.0, 0.0) (5474.0, 50.0) 6.886
None (5474.0, 50.0) 3.443
'''			



	# def optimize_f(d):
	# 	decision = {
	# 		'increase irrigated area (ha)': d[0],
	# 		'increase irrigation efficiency (%)': d[1]
	# 	}
	# 	return -1.*dp_return(decision, state, n) + beta*future_optimal_returns[ dp_transition(decision, state, n) ]

	# x_min, fval, grid, jout = optimize.brute(optimize_f, 
	# 	ranges = (	slice(0, 10 + state['dryland'], 10), 
	# 				slice(0, 0.1 + 0.8-state['irrigation efficiency (%)']/100., 0.1) ), 
	# 	full_output=True, finish=None)
	


# def dp_transition(decision, state):
# 	state_copy = state.copy()

# 	state_copy['irrigation efficiency (%)'] = state['irrigation efficiency (%)'] + decision['increase irrigation efficiency (%)'] 
# 	state_copy['irrigated area (ha)'] = state['irrigated area (ha)'] + decision['increase irrigated area (ha)'] 
# 	state_copy['dryland area (ha)'] = state['dryland area (ha)'] - decision['increase irrigated area (ha)'] 
# 	# unused state['farm storage']
# 	return state_copy


# def dp_return(decision, state):
# 	# TODO this assumes investment reaps no reward this year, but only in following years
# 	total_water_licence_ML = water_licence['sw unregulated (ML)'] + water_licence['gw (ML)']
# 	farm_profit = lp_for_dp(
# 		crops = crops, 
# 		farm_area = state,
# 		total_water_licence = (state['irrigation efficiency (%)'] / 100.) * total_water_licence_ML)

# 	new_area_ha = state['irrigated area (ha)'] + decision['increase irrigated area (ha)']

# 	decision_cost = \
# 		total_water_licence_ML * decision['increase irrigation efficiency (%)'] * costs['increase irrigation efficiency ($/ML/%)'] \
# 		+ new_area_ha * decision['increase irrigation efficiency (%)'] * costs['increase irrigation efficiency ($/ha/%)'] \
# 		+ decision['increase irrigated area (ha)'] * costs['increase irrigated area ($/ha)'] 
# 	# unused decision['increase farm storage']
	
# 	return farm_profit - decision_cost






# recursive approach
# def recursive():
# 	for all possible state changes:
# 		find optimal profit
# 		recursive(next stage) 

# for all states:
# 	find optimal profit




# crops = read_crops_csv('rebecca_thesis_crops.csv')

# activities = [
# 				{"Dryland winter wheat (irrig cotton rotation)": 1/3, "Irrigated cotton": 2/3},
# 				{"Dryland wheat": 1/3, "Dryland cotton": 2/3},
# 				{"Dryland wheat": 1/3, "Dryland sorghum": 2/3},
# 				{"Continuous cotton": 1},
# 				{"Faba bean": 1, "Irrigated cotton": 0.5},
# 				]

# print crops



'''

http://quant-econ.net/py/dp_intro.html

Integrating Irrigation Water Demand, Supply, and Delivery Management in a Stochastic Environment
NORMAN J. DUDLEY AND BRADLEY W. SCOTT

A linear dynamic programming approach to irrigation system management with depleting groundwater
'''

'''
Rebecca's Thesis
Maules Creek is region M. Option 3

Possible activities
1. Irrigated cotton/ wheat rotation
2. Irrigated continuous cotton
3. Irrigated cotton/ faba bean rotation
4. Dryland cotton/ wheat rotation
5. Dryland sorghum/ wheat rotation



on_farm_storage = [143, 150, 157]
increase_storage_cost = 1000 # per ML
irrigation_area = [60, 63, 66]
increase_irrigation_area_cost = 1500 # per ha

irrigation_efficiency = {
	"unregulated /off-allocation/ supplementary": [0.42, 0.52, 0.57],
	"regulated": [0.65, 0.75, 0.8],
	"groundwater": [0.7, 0.8, 0.85],
	"spray": [0.9]
}
increase_irrigation_efficiency_cost_ML = [500, 1000] # per ML
increase_irrigation_efficiency_cost_ha = [1000, 2000] # per ha

'rebecca_thesis_crops.csv'

activities = {
			1: {"Dryland wheat": 0.33, "Irrigated cotton": 0.67},
			2: {"Dryland wheat": 0.33, "Dryland cotton": 0.67},
			3: {"Dryland wheat": 0.33, "Dryland sorghum": 0.67},
			4: {"Continuous cotton": 1},
			5: {"Faba bean": 1, "Irrigated cotton": 0.5},
				}


'''





'''

Dynamic programming for long term capital investment decisions

irrigation technology options (k): current flood, 10-15% iimprovement, 15-20% improvement
area laid out to irrigation (Omega)
on farm storage capacity (d)

Maximise sum_t 1/(1+r)^(t+1) max_profit() 


maximise sum of discounted profits. Profits are max profit possible with given state - cost of state.


we want to maximise the expected profit

profit is discounted sum of revenue-costs

state transition
x_{i+1} = T(x_i, u_i, s_i)
needs bounds too
x_i is state (infrastructure)
u_i is control decision (crop choice, investment choices?)
s_i uncertain input (prices, weather)

if future states are unknown, we cannot specify control decision but control policy which depends on state

=========

We could simply choose different investment options in 1st year only. 

'''
# import numpy as np
# # http://en.wikipedia.org/wiki/Dynamic_programming

# years = 20
# consumption = np.empty((years))
# capital = np.empty((years))
# impatience_discount = 0.9 

# def utility(consumption_t):
# 	return np.log(consumption_t)

# initial_capital = 10000

# def iterate_capital(capital_t):
# 	next_capital = A*capital_t - consumption_t


