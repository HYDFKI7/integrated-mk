crops = [
	{"season": "Summer", "applied water": 8, "name": "Cotton (BT, irrigated)", "yield": 9.5, "price": 538},
	# {"season": "Summer", "applied water": 8, "name": "Cotton (conventional, irrigated)", "yield": 9.5, "price": 538},
	# {"season": "Summer", "applied water": 7.15, "name": "Maize (irrigated)", "yield": 9, "price": 287},
	# {"season": "Summer", "applied water": 4.5, "name": "Sorghum (irrigated)", "yield": 8, "price": 242},
	# {"season": "Summer", "applied water": 1.5, "name": "Sorghum (semi irrigated)", "yield": 5.5, "price": 242},
	# {"season": "Summer", "applied water": 5.8, "name": "Soybean (irrigated)", "yield": 3, "price": 350},
	# {"season": "Winter", "applied water": 0, "name": "Chickpea (dryland)", "yield": 1.3, "price": 468},
	{"season": "Winter", "applied water": 2.7, "name": "Faba bean (irrigated)", "yield": 5, "price": 348},
	# {"season": "Winter", "applied water": 0, "name": "Faba bean (dryland)", "yield": 1.4, "price": 348},
	# {"season": "Winter", "applied water": 0, "name": "Wheat (bread, dryland)", "yield": 1.8, "price": 244},
	# {"season": "Winter", "applied water": 1.5, "name": "Wheat (bread, semi irrigated)", "yield": 4, "price": 244},
	# {"season": "Winter", "applied water": 3.6, "name": "Wheat (bread, irrigated)", "yield": 7, "price": 244},
	# {"season": "Winter", "applied water": 3.6, "name": "Wheat (durum, irrigated)", "yield": 7, "price": 275},
	# {"season": "Winter", "applied water": 1.4, "name": "Vetch (irrigated)", "yield":0, "price":0}
]


from pyswarm import pso

# objective function

def objective(x):
	return - sum([x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])

# contstraints

# total area farmed each season must be less than farm area
farm_area = 1300

# water use must be less than licence
water_licence = 1000

def constraints(x):
    return [farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer"]),
    		farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter"]),
    		water_licence - sum([x[i] * crop["applied water"] for i,crop in enumerate(crops)])]

lb = [0 for i in crops]
ub = [farm_area for i in crops]

xopt, fopt = pso(objective, lb, ub, f_ieqcons=constraints, maxiter=1000, minstep=1e-4, minfunc=1e-4)

# pso(func, lb, ub, ieqcons=[], f_ieqcons=None, args=(), kwargs={},
    # swarmsize=100, omega=0.5, phip=0.5, phig=0.5, maxiter=100, minstep=1e-8,
    # minfunc=1e-8, debug=False)

print xopt 
print fopt

print "----------------------------------------"
for i, x_i in enumerate(xopt):
	if x_i > 1e-5:
		print crops[i]["name"], x_i
	elif x_i < 0:
		print "negative", i, x_i
print "----------------------------------------"

print "summer", sum([xopt[i] for i,crop in enumerate(crops) if crop["season"] == "Summer" ])
print "winter", sum([xopt[i] for i,crop in enumerate(crops) if crop["season"] == "Winter"])
print "water", sum([xopt[i] * crop["applied water"] for i,crop in enumerate(crops)])
print "money", sum([xopt[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])/1e6
