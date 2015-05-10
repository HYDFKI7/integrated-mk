import numpy as np

from climate.read_climate import read_climate_projections, read_original_data, read_all_bom_data, find_extremes

from hydrological.RunIhacresGw import dateifier, get_state, get_outputs, get_year_indices, generate_extractions, run_hydrology_by_year

from farm_decision.farm_optimize import load_crops, load_chosen_crops, maximum_profit

from ecological.ecological_indices import calculate_water_index, eco_weights, eco_ctf, eco_min_separation, eco_min_duration

# s = sum_by_year(climate_dates, rainfall)
# TODO cite all data

'''
inputs: climate scenario, crop prices, WUE, irrigation area, AWD (function that determines fraction of limits based on levels)
outputs: farm profit, profit variability, water levels (from which we compute environmental indices)
'''

# WUE = {"flood irrigation": 0.65, "spray irrigation": 0.8, "drip irrigation": 0.85}
WUE_scenarios = {
	"flood": {
		"Min": 50.,
		"Med": 65.,
		"Max": 80.,
	},
	"spray":{
		"Min": 70.,
		"Med": 80.,
		"Max": 90.,
	},
	"drip": {
		"Min": 76.,
		"Med": 85.,
		"Max": 85.,
	}
}

# % of irrigated area in catchment
# we might just take flood = 100-spray-drip ()
adoption_scenarios = {
	"flood": {
		"Min": 27.3,
		"Med": 65,
		"Max": 100,
	},
	"spray":{
		"Min": 0.5,
		"Med": 8,
		"Max": 16.9,
	},
}


WUE = { "flood": WUE_scenarios["flood"]["Min"],
		"spray": WUE_scenarios["spray"]["Min"] }


adoption = { "flood": 100. - adoption_scenarios["spray"]["Med"],
			"spray": adoption_scenarios["spray"]["Med"],
			"drip": 0. }



# for area_type in ["flood irrigation", "spray irrigation", "drip irrigation"]:


def run_integrated():

	# crop prices, yields, costs all determined here
	# TODO add min, max
	all_crops = load_chosen_crops( WUE )

	# Water allocations
	AWD = {"sw unregulated": 1., "gw": 1.}

	# TODO water adoption from JEN, fix farm_optimize
	# apply AWD to get water_licence
	water_limit = {"sw unregulated": 1413., "gw": 2200.}

	water_licence = {}
	for licence_type in water_limit:
		water_licence[licence_type] = water_limit[licence_type] * AWD[licence_type]



	total_water_allocation = AWD['sw unregulated'] * water_limit['sw unregulated'] \
								+ AWD['gw'] * water_limit['gw']


	# TODO adjust total_water_allocation based on WUE and adoption
	# discuss with Jen whether crop water uses are before or after WUE.

	# farm_area = {"irrigated area (ha)": 782*7, "dryland area (ha)": 180*7}
	farm_area = {
		"flood": 782.*7.*adoption["flood"]/100., # hectares
		"spray": 782.*7.*adoption["spray"]/100., 
		"drip": 782.*7.*adoption["drip"]/100., 
		"dryland": 180.*7.
	}

	climate_type = "temperature" 
	climate_dates, rainfall, PET = read_all_bom_data()
	window = 366*20
	min_i, med_i, max_i = find_extremes(rainfall, window)
	# pick climate scenario
	per_i = min_i
	climate_dates, rainfall, PET = climate_dates[per_i:per_i+window], rainfall[per_i:per_i+window], PET[per_i:per_i+window]

	# climate_type = "PET"
	# climate_dates, rainfall, PET = read_climate_projections('climate/419051.csv', scenario=1)

	sw_extractions, gw_extractions = generate_extractions(climate_dates, water_limit['sw unregulated']/365, water_limit['gw']/365)

	year_indices, year_list = get_year_indices(climate_dates)

	years = 2
	assert years <= len(year_indices)

	all_years_flow = np.empty((year_indices[years-1]["end"]))
	all_years_gwstorage = np.empty((year_indices[years-1]["end"]))
	all_years_gwlevel = np.empty((year_indices[years-1]["end"]))
	all_years_profit = np.empty((year_indices[years-1]["end"]))

	# initial state
	state = (0, 
				422.7155/2, # d/2
				[0,0], # must be of length NC
				0, 
				0)

	# run LP farmer decision model
	# -------------------------------------------
	farm_profit = maximum_profit(all_crops, farm_area, total_water_allocation)


	for year in range(years):
		state, flow, gwlevel, gwstorage = run_hydrology_by_year(year, state, climate_dates, rainfall, PET, sw_extractions, gw_extractions, climate_type)
		
		indices = year_indices[year]
		all_years_gwstorage[indices["start"]:indices["end"]] = gwstorage
		all_years_gwlevel[indices["start"]:indices["end"]] = gwlevel
		all_years_flow[indices["start"]:indices["end"]] = flow
		all_years_profit[indices["start"]:indices["end"]] = farm_profit/365


	print "PROFIT", farm_profit

	# run ecological model 
	# eco_weights, eco_ctf, eco_min_separation, eco_min_duration
	water_index = calculate_water_index(
							gw_level = all_years_gwlevel, 
							flow = all_years_flow, 
							dates = climate_dates[:year_indices[years-1]["end"]],
							threshold = eco_ctf["med"], 
							min_separation = eco_min_separation["med"],
							min_duration = eco_min_duration["med"],
							duration_weight = eco_weights["Default"]["Duration"],
							timing_weight = eco_weights["Default"]["Timing"],
							dry_weight = eco_weights["Default"]["Dry"],
							surface_weight = 0.5,
							gwlevel_weight = 0.5
							)

	return climate_dates[:year_indices[years-1]["end"]], all_years_flow, all_years_gwlevel, water_index, all_years_profit


if __name__ == '__main__':
	climate_dates, all_years_flow, all_years_gwlevel, water_index, all_years_profit = run_integrated()


	dates = map(dateifier, climate_dates)

	import matplotlib.pyplot as plt 

	plt.subplot(3,1,1)
	plt.plot(dates, all_years_flow)
	plt.title('flow')	
	plt.subplot(3,1,2)
	# plt.plot(dates, all_years_gwstorage)
	plt.plot(dates, all_years_gwlevel)
	plt.title('gwlevel')	
	plt.subplot(3,1,3)
	plt.plot(dates, water_index)
	plt.title('water_index')	
	# plt.subplot(3,1,4)
	# plt.plot(all_years_profit)
	# plt.title('profit')
	plt.show()



'''
===========================================
Potential research questions
===========================================
'''


'''
Climate: sensitivity of profit to WUE under different climate scenarios
'''

'''
Prices: sensitivity of profit to price and WUE
'''

'''
Adaptability: sensitivity of profit variability to WUE
'''

'''
Environmental: sensitivity of environmental indices to WUE and irrigation area 
'''

'''
Rivers And Streams > Real Time Data - Rivers And Streams > 419-Namoi River Basin
Maules Ck@Avoca East

http://realtimedata.water.nsw.gov.au/water.stm
'''


'''
===========================================
research snippets
===========================================
'''


"""

TODO

* run climate scenarios through hydrology model
* do some runs of farmer decision model
* get farmer to use constraints from hydrology including implementing water policy
* update hydrology with results from farmer 

"""


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


