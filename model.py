# https://github.com/josephguillaume/MaxMembershipParEst/blob/master/Catchcrop.R


"""
"Maules Creek sits between Leard State Forest and Mount Kaputar National Park. It has soft fertile soil suitable for most crops such as wheat, barley, sorghum, oats, lucerne, canola and even cotton."
https://www.wilderness.org.au/articles/our-history-and-struggle-our-land-maules-creek-nsw-laird-family


"""

"""
from powell2011representative
http://www.dpi.nsw.gov.au/research/economics-research/reports/err46
"""
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

"""
RESOURCES
we could sanity check crop water productivity from zwart2004review
http://www.sciencedirect.com/science/article/pii/S0378377404001416

using APSIM
http://www.yieldprophet.com.au/YP/wfLogin.aspx

WOFOST
http://www.wageningenur.nl/en/Expertise-Services/Research-Institutes/alterra/Facilities-Products/Software-and-models/WOFOST.htm
DSSAT

"""


"""
'All irrigated summer crops, northern NSW' and 'All dryland north-east NSW summer crop budgets' from http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops

"COTTON (Roundup Ready Flex(R) Bollgard II(R) - Single Skip)"


'All Northern NSW (East) dryland winter crop budgets' and 'All Northern irrigated winter crop budgets' from http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/winter-crops

'Managing irrigated cotton agronomy' from http://www.cottoncrc.org.au/industry/Publications/Water/WATERpak/WATERpak_S3_Irrigation_management_of_cotton
	
	https://www.cottassist.com.au/Default.aspx
	Rainman and Whopper Cropper

We need a simple relationship between yield and water available during different times.

http://www.dpi.nsw.gov.au/agriculture/resources/water

WATER

	[water_plans]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/plans_commenced/default.aspx

	[namoi_unreg]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Namoi-Unregulated-and-Alluvial

    [namoi_gw]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Upper-and-Lower-Namoi-Groundwater-Sources/default.aspx



"""


from scipy.optimize import minimize, differential_evolution


# objective function
def fun(x):
	return - sum([x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])

# contstraints

# total area farmed each season must be less than farm area
farm_area = 1300

# water use must be less than licence
water_licence = 1000

constraints = [
		{'type': 'ineq', 'fun': lambda x:  farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer"]) },
		{'type': 'ineq', 'fun': lambda x:  farm_area - sum([x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter"]) },
		{'type': 'ineq', 'fun': lambda x:  water_licence - sum([x[i] * crop["applied water"] for i,crop in enumerate(crops)]) },
		]

res = minimize(fun, 
	[0 for i in crops], 
	method='SLSQP', # 1.67825325832
	bounds=[(0, farm_area) for i in crops], 
	constraints=constraints)


# print results

for i, x_i in enumerate(res.x):
	if x_i > 1e-5:
		print crops[i]["name"], x_i
print "----------------------------------------"

print "summer", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Summer" ])
print "winter", sum([res.x[i] for i,crop in enumerate(crops) if crop["season"] == "Winter" ])
print "water", sum([res.x[i] * crop["applied water"] for i,crop in enumerate(crops)])
print "farm revenue", sum([res.x[i] * crop["yield"] * crop["price"] for i, crop in enumerate(crops)])/1e6

print "========================================"

print res


"""
BIBLIOGRAPHY

@book{powell2011representative,
  title={A representative irrigated farming system in the Lower Namoi Valley of NSW: An economic analysis},
  author={Powell, Janine and Scott, Fiona and Wales, New South},
  year={2011},
  publisher={Industry \& Investment NSW}
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
