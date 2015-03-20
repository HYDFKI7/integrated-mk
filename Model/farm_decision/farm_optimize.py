
"""
title: Crop choice optimizition 
author: michael.james.asher@gmail.com
date: January 2015

To maximise revenue subject to water and land area constraints, we use scipy.optimize, scipy.linprog and linear programming optimizition library PULP, eg. https://pythonhosted.org/PuLP/index.html	

"""

from scipy.optimize import minimize
from scipy.optimize import linprog


# the three below functions use three different libraries to maximise revenue subject to water and land area constraints
def scipy_min_find_optimal_crops(crops, farm_area, water_licence):

	# objective function
	def objective(x):
		return - sum([x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])

	# contstraints
	constraints = [
			# total area farmed each season must be less than farm area
			{'type': 'ineq', 'fun': lambda x:  farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer"]) },
			{'type': 'ineq', 'fun': lambda x:  farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter"]) },
			# water use must be less than licence
			{'type': 'ineq', 'fun': lambda x:  water_licence - sum([x[i] * crop["applied water"] for i,crop in enumerate(crops)]) },
			]

	res = minimize(objective, 
		[0 for i in crops], 
		method='SLSQP', 
		bounds=[(0, farm_area) for i in crops], 
		constraints=constraints)

	return res


def scipy_linprog_find_optimal_crops(crops, farm_area, water_licence):

	# objective function
	c = [-crop["yield"] * crop["price"] for crop in crops]
	# contstraints
	A = [
		# total area farmed each season must be less than farm area
		map(int,[crop["season"]=="Summer" for crop in crops]), 
		map(int,[crop["season"]=="Winter" for crop in crops]),
		# water use must be less than licence
		[crop["applied water"] for crop in crops]
		]
	b = [farm_area, farm_area, water_licence]

	bounds = ((0,None),)*len(crops)

	res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, options={"disp": True})
	return res


def pulp_find_and_print_optimal_crops(crops, farm_area, water_licence):
	
	from pulp import LpVariable, LpProblem, LpMaximize, LpStatus, lpSum, value

	crop_names = [crop["name"] for crop in crops]

	crop_vars = LpVariable.dicts("Crop", crop_names, 0)

	prob = LpProblem("Farmer Decision", LpMaximize)

	# objective function
	prob += lpSum([crop_vars[crop["name"]] * crop["yield"] * crop["price"] for crop in crops]), "total revenue"

	# contstraints

	# total area farmed each season must be less than farm area
	prob += lpSum([crop_vars[crop["name"]] for crop in crops if crop["season"] == "Summer"]) <= farm_area, "summer area"
	prob += lpSum([crop_vars[crop["name"]] for crop in crops if crop["season"] == "Winter"]) <= farm_area, "winter area"

	# water use must be less than licence
	prob += lpSum([crop_vars[crop["name"]] * crop["applied water"] for crop in crops]) <= water_licence, "water licence"

	# solve
	prob.solve()

	print "Status:", LpStatus[prob.status]
	for v in prob.variables():
	    if not v.varValue == 0:
	    	print v.name, "=", v.varValue
	print "----------------------------------------"
	print "Total Farm Revenue = ", value(prob.objective)
	print "========================================"


# print results
def print_results(res):
	print "Crops grown"
	print "----------------------------------------"
	for i, x_i in enumerate(res.x):
		if x_i > 1e-3:
			print crops[i]["name"], "-", x_i, "ha"
	print "----------------------------------------"

	print "summer area", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer" ]), "ha"
	print "winter area", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter" ]), "ha"
	print "water", sum([res.x[i] * crop["applied water"] for i,crop in enumerate(crops)]), "ML"
	print "farm revenue", "$", sum([res.x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])/1e6, "M"

	print "========================================"

	# print res


#data from powell2011representative
crops = [
	{"season": "Summer", "applied water": 8, "name": "Cotton (BT, irrigated)", "yield": 9.5, "price": 538},
	{"season": "Summer", "applied water": 8, "name": "Cotton (conventional, irrigated)", "yield": 9.5, "price": 538},
	{"season": "Summer", "applied water": 7.15, "name": "Maize (irrigated)", "yield": 9, "price": 287},
	{"season": "Summer", "applied water": 4.5, "name": "Sorghum (irrigated)", "yield": 8, "price": 242},
	{"season": "Summer", "applied water": 1.5, "name": "Sorghum (semi irrigated)", "yield": 5.5, "price": 242},
	{"season": "Summer", "applied water": 5.8, "name": "Soybean (irrigated)", "yield": 3, "price": 350},
	{"season": "Winter", "applied water": 0, "name": "Chickpea (dryland)", "yield": 1.3, "price": 468},
	{"season": "Winter", "applied water": 2.7, "name": "Faba bean (irrigated)", "yield": 5, "price": 348},
	{"season": "Winter", "applied water": 0, "name": "Faba bean (dryland)", "yield": 1.4, "price": 348},
	{"season": "Winter", "applied water": 0, "name": "Wheat (bread, dryland)", "yield": 1.8, "price": 244},
	{"season": "Winter", "applied water": 1.5, "name": "Wheat (bread, semi irrigated)", "yield": 4, "price": 244},
	{"season": "Winter", "applied water": 3.6, "name": "Wheat (bread, irrigated)", "yield": 7, "price": 244},
	{"season": "Winter", "applied water": 3.6, "name": "Wheat (durum, irrigated)", "yield": 7, "price": 275},
	{"season": "Winter", "applied water": 1.4, "name": "Vetch (irrigated)", "yield":0, "price":0}
]
    	

if __name__ == '__main__':

	# demo run
	farm_area = 1300
	water_licence = 800

	res_pulp = pulp_find_and_print_optimal_crops(crops, farm_area, water_licence)
	res_min = scipy_min_find_optimal_crops(crops, farm_area, water_licence)
	res_linprog = scipy_linprog_find_optimal_crops(crops, farm_area, water_licence)
	print_results(res_min)
	print_results(res_linprog)





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
