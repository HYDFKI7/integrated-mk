
"""
title: Crop choice optimizition 
author: michael.james.asher@gmail.com
date: January 2015

To maximise revenue subject to water and land area constraints, we use scipy.optimize, scipy.linprog and linear programming optimizition library PULP, eg. https://pythonhosted.org/PuLP/index.html	

"""

from scipy.optimize import minimize
from scipy.optimize import linprog
import numpy as np
import os
from ConfigLoader import *




# maximise revenue subject to water and land area constraints
def scipy_linprog_find_optimal_crops(crops, farm_area, water_licence):
	water_cost = {
		'surface': .8,  # $/ML
		'ground' : 1.6,  # $/ML
		'dryland': 0,
	}

	# ----objective function option 1-----: 
	#C is cost ($/ha) for each crop (as opposed to profit as the optimisation runs on minimising)
	C = [crop['cost ($/ha)'] + crop["water use (ML/ha)"] * water_cost[crop['input water type']] - (crop["yield (units/ha)"] * crop["price ($/unit)"]) for crop in crops]

	# ----objective function option 2----: 
	#C is gross margin ($/ha) plus water cost
	# C = [crop["water use (ML/ha)"] * water_cost[crop['input water type']] - (crop["Gross margin ($/ha)"]) for crop in crops]
	# constraints, A is water use (ML/ha) for each crop
	A = []
	b = []
		# water use must be less than licence
	for input_water in ['surface', 'ground']:
		A.append([int(crop["input water type"]==input_water) * crop["water use (ML/ha)"] for crop in crops])
		b.append(water_licence[input_water])

	# total area farmed each season must be less than farm area for each type of irrigation
	for season in ["Summer", "Winter"]:
		for area_type in ["flood", "spray", "drip"]:
			A.append(map(int,[crop["season"] == season and crop["area type"] == area_type for crop in crops])) #T/F=1/0, summer flood crop etc.
			b.append(farm_area[area_type])
		# dryland crops may grow on any type
		A.append(map(int,[crop["season"]==season for crop in crops])) #any crop in summer/winter
		b.append(farm_area["flood"]+farm_area["drip"]+farm_area["spray"]+farm_area["dryland"]) 


	bounds = ((0,None),)*len(crops) #repeat (0,None) len(crops) (= 20) times, ie. each crop has (0,None)

	res = linprog(C, A_ub=A, b_ub=b, bounds=bounds, options={"disp": False})
	return res


def read_crops_csv(file_name):
	import csv
	import json
	crops = []
	with open(file_name) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	if row['valid'] == 'TRUE':
	    		try: 
	    			row['yield (units/ha)'] = np.array(json.loads(row['yield (units/ha)']))
	    			row['price ($/unit)'] = np.array(json.loads(row['price ($/unit)']))
	    			row['price med ($/unit)'] = np.array(json.loads(row['price med ($/unit)']))
	    			row['cost ($/ha)'] = float(row['cost ($/ha)'])
	    			row["water use (ML/ha)"] = float(row["water use (ML/ha)"])
	    			row["Gross margin ($/ha)"] = float(row["Gross margin ($/ha)"])
	    			crops.append(row)
	    		except: 
	    			print "invalid crop", row

	    		# row['water use (ML/ha)'] = json.loads(row['water use (ML/ha)'])
	    		# row['cost ($/ha)'] = json.loads(row['cost ($/ha)'])
	return crops

# print results
def print_results(res, crops):
	print "Crops grown"
	print "----------------------------------------"
	for i, x_i in enumerate(res.x):
		if x_i > 1e-3:
			print crops[i]["name"], crops[i]["area type"], "-", x_i, "ha" #print crops and area that has >1e-3 value.
	print "----------------------------------------"

	for season in ["Summer", "Winter"]:
		for area_type in ["flood", "spray", "drip", "dryland"]:
			print season, area_type, 'area', sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == season and crop["area type"] == area_type  ]), "ha"
	print "total summer area", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer" ]), "ha"
	print "total winter area", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter" ]), "ha"
	print "water", sum([res.x[i] * crop["water use (ML/ha)"] for i,crop in enumerate(crops)]), "ML"
	print "farm revenue", "$", sum([res.x[i] * (np.sum(crop["yield (units/ha)"] * crop["price ($/unit)"]) - crop['cost ($/ha)']) for i, crop in enumerate(crops)])/1e6, "M"

	print "========================================"

	# print res

def maximum_profit(crops, farm_area, total_water_licence):

	water_cost = {
		'surface': .8,  # $/ML
		'ground' : 1.6,  # $/ML
		'dryland': 0,
	}

	res = scipy_linprog_find_optimal_crops(crops, farm_area, total_water_licence)

	# profit = sum([res.x[i] * (np.sum(crop["yield (units/ha)"] * crop["price ($/unit)"]) - crop['cost ($/ha)'] - crop["water use (ML/ha)"]*1.6) for i, crop in enumerate(crops)])

	profit = sum([res.x[i] * (np.sum(crop["yield (units/ha)"] * crop["price ($/unit)"]) - crop['cost ($/ha)'] - crop["water use (ML/ha)"]*water_cost[crop['input water type']]) for i, crop in enumerate(crops)])

	# print "=========="
	# for i, crop in enumerate(crops):
	# 	if res.x[i] > 0:
	# 		print crop['name'], crop['input water type'], crop['area type'], crop['season']
	# 		print "   "+str(res.x[i]*crop['water use (ML/ha)'])
	# print "profit: ", profit
	# print "------------"
	# print_results(res, crops)
	# water_use = sum([res.x[i] * crop["water use (ML/ha)"] for i,crop in enumerate(crops)])
	# print "water_use", water_use

	return profit

# note farm_area = {'irrigated area': x, 'dryland area': y}, different to scipy_linprog_find_optimal_crops
def lp_for_dp(crops, farm_area, water_licence):
	# objective function
	c = [crop['cost ($/ha)'] - np.sum(crop["yield (units/ha)"] * crop["price ($/unit)"]) for crop in crops]
	# contstraints
	A = [
		# water use must be less than licence
		[crop["water use (ML/ha)"] for crop in crops]
		]
	b = [water_licence]
	# total area farmed each season must be less than farm area for each type of irrgation
	for season in ["Summer", "Winter"]:
		A.append(map(int,[crop["season"] == season and crop["area type"] == "irrigated" for crop in crops]))
		b.append(farm_area['irrigated area (ha)'])
		# dryland crops may grow on any type
		A.append(map(int,[crop["season"]== season for crop in crops]))
		b.append(farm_area["irrigated area (ha)"]+farm_area["dryland area (ha)"])

	bounds = ((0,None),)*len(crops)

	res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, options={"disp": False})

	print_results(res, crops)

	profit = sum([res.x[i] * (np.sum(crop["yield (units/ha)"] * crop["price ($/unit)"]) - crop['cost ($/ha)']) for i, crop in enumerate(crops)])
	
	# water_use = sum([res.x[i] * crop["water use (ML/ha)"] for i,crop in enumerate(crops)])
	# print "water_use", water_use

	return profit


if "farm_decision" in CONFIG.paths:
	farm_dir = CONFIG.paths['farm_decision']
else:
	farm_dir = os.path.dirname('__file__')+'/'

def load_chosen_crops(WUE, crop_price_scale, WUE_scenarios=None): #WUE is....; crop_price_scale is a value e.g. 0.5 or 1 to adjust crop price
# def load_chosen_crops(WUE):
	crops = read_crops_csv(farm_dir+'chosen_crops.csv') 

	# create a different crop for each type of irrigation
	crops_expanded_by_WUE = []
	for crop in crops:
		crop["price med ($/unit)"] = crop_price_scale * crop["price med ($/unit)"]

		if crop["water use (ML/ha)"] > 0:
			for irrigation_type in ["flood", "spray"]:
				local_copy = crop.copy()

				if WUE_scenarios is not None:
					local_copy["water use (ML/ha)"] = (WUE_scenarios[local_copy['area type']]['med']/ WUE[irrigation_type]) * local_copy["water use (ML/ha)"]
				else:#run this if WUE_scenarios is not specified in load_chosen_crops()
					local_copy["water use (ML/ha)"] = (100. / WUE[irrigation_type]) * local_copy["water use (ML/ha)"]
				#End if
				
				local_copy["area type"] = irrigation_type
				for input_water in ["surface", "ground"]:
					input_water_copy = local_copy.copy()
					input_water_copy["input water type"] = input_water

					crops_expanded_by_WUE.append(input_water_copy)
		else: 
			local_copy = crop.copy()
			local_copy["area type"] = "dryland"
			local_copy["input water type"] = "dryland"
			crops_expanded_by_WUE.append(local_copy)

	return crops_expanded_by_WUE

def load_crops():
	# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops
	# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/winter-crops
	dpi_budget_crops = read_crops_csv(farm_dir+'dpi_budget_crops.csv') 
	# powell2011representative
	powell_crops = read_crops_csv(farm_dir+'powell_crops.csv') 
	# see SEMI-IRRIGATED COTTON: MOREE LIMITED WATER EXPERIMENT
	other_crops	= [{
			'name': 'SEMI-IRRIGATED COTTON',
			'yield (units/ha)': 7,
			'season': 'Summer',
			'water use (ML/ha)': 4.5,
			'source': 'fabricated by mjasher',
			'cost ($/ha)': 2000,
			'price ($/unit)': 380,
			'area type': 'flood irrigation'
			}]

	# all_crops = dpi_budget_crops + powell_crops + other_crops
	all_crops = dpi_budget_crops

	return all_crops

def potential_load_crops():
	return [{
			'name': 'SEMI-IRRIGATED COTTON',
			'yield (units/ha)': 7,
			'season': 'Summer',
			'water use (ML/ha)': 4.5,
			'source': 'fabricated by mjasher',
			'cost ($/ha)': 2000,
			'price ($/unit)': 380,
			'area type': 'flood irrigation'
			},
			{
			'name': 'FULLY-IRRIGATED COTTON',
			'yield (units/ha)': 10,
			'season': 'Summer',
			'water use (ML/ha)': 7.5,
			'source': 'fabricated by mjasher',
			'cost ($/ha)': 2100,
			'price ($/unit)': 380,
			'area type': 'flood irrigation'
			},
			]	




def list_all_combos(parameters):
	# eg. 
	# all_combos([], [['a','b', 'c'], ['1', '2']])
	possible_combos = []
	def next_combos(combo, parameters):
		if parameters[1:]:
			for option in parameters[0]:
				next_combos(combo+[option], parameters[1:])
		else:
			for option in parameters[0]:
				possible_combos.append(combo+[option])

	next_combos([], parameters)

	return possible_combos

# print list_all_combos([['a','b', 'c'], ['1', '2'], ['e', 'f']])



if __name__ == '__main__':

	# demo run
	water_licence = {"sw_unregulated": 1413, "gw": 2200}
	total_water_licence = water_licence['sw_unregulated']+water_licence['gw']
	farm_area = {"flood": 782, "spray": 0, "drip": 0, "dryland": 180}

	# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops
	# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/winter-crops

	# if "farm_decision" in CONFIG.paths:
	# 	farm_dir = CONFIG.paths['farm_decision']
	# else:
	# 	farm_dir = os.path.dirname('__file__')+'/'

	dpi_budget_crops = read_crops_csv(farm_dir + 'dpi_budget_crops.csv') 
	# powell2011representative
	powell_crops = read_crops_csv(farm_dir + 'powell_crops.csv') 
	# SEMI-IRRIGATED COTTON: MOREE LIMITED WATER EXPERIMENT
	other_crops	= [{
			'name': 'SEMI-IRRIGATED COTTON',
			'yield (units/ha)': 7,
			'season': 'Summer',
			'water use (ML/ha)': 4.5,
			'source': 'fabricated',
			'cost ($/ha)': 2000,
			'price ($/unit)': 380,
			'area type': 'flood irrigation'
			}]

	# demo_crops = dpi_budget_crops + powell_crops + other_crops
	demo_crops = dpi_budget_crops 

	res_linprog = scipy_linprog_find_optimal_crops(demo_crops, farm_area, total_water_licence)
	print_results(res_linprog, demo_crops)

	print maximum_profit(demo_crops, farm_area, total_water_licence)





"""
BIBLIOGRAPHY

@book{powell2011representative,
  title={A representative irrigated farming system in the Lower Namoi Valley of NSW: An economic analysis},
  author={Powell, Janine and Scott, Fiona and Wales, New South},
  year={2011},
  publisher={Industry \& Investment NSW},
  url={http://www.dpi.nsw.gov.au/research/economics-research/reports/err46
}
}

@article{zwart2004review,
  title={Review of measured crop water productivity values for irrigated wheat, rice, cotton and maize},
  author={Zwart, Sander J and Bastiaanssen, Wim GM},
  journal={Agricultural Water Management},
  volume={69},
  number={2},
  pages={115--133},
  year={2004},
  publisher={Elsevier}
}



"""
