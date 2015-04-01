from farm_optimize import maximum_profit, load_crops

from scipy import optimize

farm_area = {"flood_irrigation": 782, "spray_irrigation": 0, "drip_irrigation": 0, "dryland": 180}
water_licence = {"sw_unregulated": 1413, "gw": 2200}

crops = load_crops()

increase_irrigation_area_cost = 1500 # per ha
increase_irrigation_efficiency_cost_ML = 500 # [500, 1000] # per ML
increase_irrigation_efficiency_cost_ha = 1000 # [1000, 2000] # per ha


# print maximum_profit(crops, farm_area=farm_area, total_water_licence=total_water_licence)

def dp_transition(decision, state):
	state['irrigation efficiency'] = state['irrigation efficiency'] + decision['increase irrigation efficiency'] 
	state['irrigation area'] = state['irrigation area'] + decision['increase irrigation area'] 
	# state['farm storage']

	return state

def dp_return(decision, state):
	
	# state['irrigation efficiency']
	# state['farm storage']
	# state['irrigation area']

	total_water_licence = water_licence['sw_unregulated']*state['irrigation efficiency'] + water_licence['gw']

	farm_area['flood_irrigation'] = state['irrigation area']

	farm_profit = maximum_profit(
		crops = crops, 
		farm_area = farm_area,
		total_water_licence = total_water_licence)

	# decision['increase irrigation efficiency']
	# decision['increase farm storage']
	# decision['increase irrigation area']

	decision_cost = \
		water_licence['sw_unregulated']*increase_irrigation_efficiency_cost_ML \
		+ farm_area['flood_irrigation']*increase_irrigation_efficiency_cost_ha \
		+ decision['increase irrigation area']*increase_irrigation_area_cost 
	
	return farm_profit - decision_cost

from scipy import optimize
resbrute = optimize.brute(f, rranges, args=params, full_output=True,
                              finish=optimize.fmin)
from scipy.optimize import brute
possible_decions = 
maximum()

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


