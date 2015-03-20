
import numpy as np

"""

TODO

* run climate scenarios through hydrology model
* do some runs of farmer decision model


* get farmer to use constraints from hydrology including implementing water policy
* update hydrology with results from farmer 

"""


# """
# run hydrological model 
# """
# from hydrological.RunIhacresGw import run_hydrology
# hydro_sim, hydro_tdat = run_hydrology(None) # RunIhacresGw.R takes about 17 seconds

# gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,3] # 3rd col varies most
# flow = np.array(hydro_sim.rx2('Q')).squeeze()
# dates = hydro_tdat.rx2('dates')

# """
# run ecological model 
# """
# from ecological.ecological_indices import calculate_water_index
# water_index = calculate_water_index(gwlevel, flow, dates)


"""
run farmer decision 
"""
from farm_decision.farm_optimize import crops, scipy_linprog_find_optimal_crops
farm_area = 1300
water_licence = 800
res_linprog = scipy_linprog_find_optimal_crops(crops, farm_area, water_licence)


def read_crops_csv(file_name):
	import csv
	import json
	crops = []
	with open(file_name) as csvfile:
	    reader = csv.DictReader(csvfile)
	    for row in reader:
	    	if row['valid'] == 'TRUE':
	    		try: 
	    			row['yield (units/ha)'] = json.loads(row['yield (units/ha)'])
	    			row['price ($/unit)'] = json.loads(row['price ($/unit)'])
	    			crops.append(row)
	    		except: 
	    			print "invalid crop", row

	    		# row['water use (ML/ha)'] = json.loads(row['water use (ML/ha)'])
	    		# row['cost ($/ha)'] = json.loads(row['cost ($/ha)'])
	return crops

# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops
# http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/winter-crops
dpi_budget_crops = read_crops_csv('farm_decision/dpi_budget_crops.csv') 
# powell2011representative
powell_crops = read_crops_csv('farm_decision/powell_crops.csv') 

other_crops	= [{
		'name': 'SEMI-IRRIGATED COTTON',
		'yield (units/ha)': 7,
		'season': 'Summer',
		'water use (ML/ha)': 4.5,
		'source': 'fabricated',
		'cost ($/ha)': 2000,
		'price ($/unit)': 380,
		}]

all_crops = dpi_budget_crops + powell_crops + other_crops

# print all_crops

# Extraction limit 2,200 ML/yr \cite{Upper_and_Lower_Namoi_Groundwater_Sources}
gw_limit = 2200

# Maules Creek Entitlement (ML/year) 1,413 \cite{Namoi_Unregulated_and_Alluvial}
sw_limit = 1413


# Available Water Determination Order for Various NSW Groundwater Sources (No. 1) 2014
# http://www.water.nsw.gov.au/Water-management/Water-availability/Water-allocations/Available-water-determinations
AWD = 0.8

'''
"With the recent volatility in general commodity prices, and the prolonged period of limited water there are no 'typical' rotations in an irrigated farming system. Farmers are choosing crops season by season depending on available water, current commodity prices, pest and disease pressure and various soil health issues."
\cite{powell2011representative}

We need a number of crops, each with a 'name', 'growing season', 'yield (unit/ha)', 'price ($/unit)', 'water use (ML/ha)', 'cost ($/ha)'.

Rather than having a physical model (eg. APSIM) to predict yield we simply include three versions of each crop: irrigated, semi-irrigated, dryland.  


Irrigation vs yield for cotton
--------------------------------

3.2 Managing irrigated cotton agronomy 
http://www.cottoncrc.org.au/industry/Publications/Water/WATERpak/WATERpak_S3_Irrigation_management_of_cotton
CottBASE = {'irrigation' : [0, 2, 4, 6, 8], 'yield' : [1.5, 2.5, 4.5, 7.5, 8.5]}

For fully irrigate cotton, 9 bales/ha not as high as 12 bales/ha from
3.4 Managing irrigation with limited water 
http://www.cottoncrc.org.au/industry/Publications/Water/WATERpak/WATERpak_S3_Irrigation_management_of_cotton
or 
SEMI-IRRIGATED COTTON: MOREE LIMITED WATER EXPERIMENT

Prices
--------------------------------

http://www.theland.com.au/news/agriculture/cropping/cotton/cotton-paying-off/2725482.aspx?storypage=0
http://www.imf.org/external/np/res/commod/index.aspx
http://databank.worldbank.org/data/views/variableselection/selectvariables.aspx?source=global-economic-monitor-%28gem%29-commodities#

http://www.imf.org/external/np/fin/ert/GUI/Pages/Report.aspx?CU=%27AUD%27&EX=REP&P=DateRange&Fr=628929792000000000&To=635621472000000000&CF=UnCompressed&CUF=Period&DS=Ascending&DT=Blank

http://www.abs.gov.au/AUSSTATS/abs@.nsf/second+level+view?ReadForm&prodno=7501.0&viewtitle=Value%20of%20Principal%20Agricultural%20Commodities%20Produced,%20Australia,%20Preliminary~1993-94~Previous~04/08/1994&&tabname=Past%20Future%20Issues&prodno=7501.0&issue=1993-94&num=&view=&
CPI
http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/6401.0Dec%202014?OpenDocument

http://www.indexmundi.com/commodities/?commodity=cotton&months=360

http://www.cottoncrc.org.au/industry/Publications/Water/WATERpak/WATERpak_S3_Irrigation_management_of_cotton

nsw media release
http://www.water.nsw.gov.au/Water-management/Water-availability/Water-allocations/Available-water-determinations
Available Water Determination Order for Various NSW Groundwater Sources (No. 1) 2014

With the exception of the Upper Namoi groundwater Zone 1, all Upper and Lower
Namoi aquifer access licence holders will receive an allocation of 1 megalitre per unit
share of entitlement.
In Zones 5, 11, and 12 of the Upper Namoi groundwater sources, supplementary
water access licence holders will receive an allocation of 0.2 megalitre per unit share
of entitlement.


{ 
'name':,
'season':,
'yield (unit/ha)':,
'price ($/unit)':,
'water use (ML/ha)':,
'cost ($/ha)':,
  }


Note dryland cotton $20/bale less for quality
Growing summer and winter crops not possible

					water cost 	irrigation cost 	TOTAL
groundwater bore 	9.2			57.45   			66.65
river-regulated  	31.75		12.77   			44.52


http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops
http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/winter-crops




'''


