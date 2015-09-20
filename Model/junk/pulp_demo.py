
from pulp import *
# https://pythonhosted.org/PuLP/index.html	


crops = [
	{"season": "Summer", "applied water": 8, "name": "Cotton (BT, irrigated)", "yield": 9.5, "price": 538},
	{"season": "Summer", "applied water": 8, "name": "Cotton (conventional, irrigated)", "yield": 9.5, "price": 538},
	# {"season": "Summer", "applied water": 0, "name": "Cotton (FICTIONAL NON IRRIGATED)", "yield": 4.5, "price": 438},
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

crop_names = [crop["name"] for crop in crops]

# crop_areas = {}

crop_vars = LpVariable.dicts("Crop", crop_names, 0)

prob = LpProblem("Farmer Decision", LpMaximize)

# objective function
prob += lpSum([crop_vars[crop["name"]] * crop["yield"] * crop["price"] for crop in crops]), "total revenue"

# contstraints

# total area farmed each season must be less than farm area
farm_area = 1300
prob += lpSum([crop_vars[crop["name"]] for crop in crops if crop["season"] == "Summer"]) <= farm_area, "summer area"
prob += lpSum([crop_vars[crop["name"]] for crop in crops if crop["season"] == "Winter"]) <= farm_area, "winter area"

# water use must be less than licence
water_licence = 1000
prob += lpSum([crop_vars[crop["name"]] * crop["applied water"] for crop in crops]) <= water_licence, "water licence"

# solve
prob.solve()

print "Status:", LpStatus[prob.status]
for v in prob.variables():
    if not v.varValue == 0:
    	print v.name, "=", v.varValue
print "----------------------------------------"
print "Total Farm Revenue = ", value(prob.objective)




from pulp import *
# https://pythonhosted.org/PuLP/index.html	


"""
simple PuLP demo
see https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html
Note: simple list comprehension syntax exists

"""

prob = LpProblem("The Whiskas Problem", LpMinimize)

# variables
x1=LpVariable("ChickenPercent",0,None,LpInteger)  # LpContinuous
x2=LpVariable("BeefPercent",0)

# objective function
prob += 0.013*x1 + 0.008*x2, "Total Cost of Ingredients per can"

# constraints
prob += x1 + x2 == 100, "PercentagesSum"
prob += 0.100*x1 + 0.200*x2 >= 8.0, "ProteinRequirement"
prob += 0.080*x1 + 0.100*x2 >= 6.0, "FatRequirement"
prob += 0.001*x1 + 0.005*x2 <= 2.0, "FibreRequirement"
prob += 0.002*x1 + 0.005*x2 <= 0.4, "SaltRequirement"

# save problem
prob.writeLP("WhiskasModel.lp")

# solve
prob.solve()

print "Status:", LpStatus[prob.status]
for v in prob.variables():
    print v.name, "=", v.varValue
print "Total Cost of Ingredients per can = ", value(prob.objective)