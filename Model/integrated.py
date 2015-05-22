import csv 
import os
import numpy as np

from climate.read_climate import read_climate_projections, read_original_data, read_all_bom_data, find_extremes, read_NSW_data

from hydrological.RunIhacresGw import dateifier, get_year_indices, generate_extractions, run_hydrology_by_year, f_by_year

from farm_decision.farm_optimize import load_chosen_crops, maximum_profit, list_all_combos

from ecological.ecological_indices import calculate_water_index, eco_weights_parameters, eco_ctf_parameters, eco_min_separation_parameters, eco_min_duration_parameters

# TODO cite all data

def plot_results(climate_dates, all_years_flow, all_years_gwlevel, surface_index, gwlevel_index, farm_profit):

	sw_dates, sw, gw_dates, gw = read_NSW_data()

	gw = -1.*gw

	print "PROFIT", farm_profit

	dates = map(dateifier, climate_dates)

	import matplotlib.pyplot as plt 

	plt.subplot(3,1,1)
	plt.plot(dates, all_years_flow, label='mod')
	plt.plot(sw_dates, sw, label="obs")
	plt.legend()	
	plt.title('flow')	
	plt.subplot(3,1,2)
	# plt.plot(dates, all_years_gwstorage)
	plt.plot(dates, all_years_gwlevel, label="mod")
	plt.plot(gw_dates, gw, label="obs")
	plt.legend()	
	plt.title('gwlevel')	
	plt.subplot(3,1,3)
	plt.plot(dates, surface_index, label='surface')
	# plt.plot(dates, gwlevel_index, label='gw')
	plt.title('water_index')
	plt.legend()	
	plt.show()


def run_integrated(WUE, water_limit, AWD, adoption, crop_price_choice,
				   climate_dates, rainfall, PET, climate_type,
				   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, plot,
				   	timing_col, duration_col, dry_col, gwlevel_col):

	# TODO add prices as parameter once we have min, max
	# crop prices, yields, costs all determined here
	crops = load_chosen_crops( WUE, crop_price_choice )

	water_licence = {}
	for licence_type in water_limit:
		water_licence[licence_type] = water_limit[licence_type] * AWD[licence_type]


	total_water_allocation = AWD['sw unregulated'] * water_limit['sw unregulated'] \
								+ AWD['gw'] * water_limit['gw']


	farm_area = {
		"flood": 782.*7.*adoption["flood"]/100., # hectares
		"spray": 782.*7.*adoption["spray"]/100., 
		"drip": 782.*7.*adoption["drip"]/100., 
		"dryland": 180.*7.
	}

	sw_extractions, gw_extractions = generate_extractions(climate_dates, water_limit['sw unregulated']/365, water_limit['gw']/365)

	year_indices, year_list = get_year_indices(climate_dates)

	# 2 years of burn in
	years = 12
	assert years <= len(year_indices)

	all_years_flow = np.empty((year_indices[years-1]["end"]))
	all_years_gwstorage = np.empty((year_indices[years-1]["end"]))
	all_years_gwlevel = np.empty((year_indices[years-1]["end"]))
	all_years_profit = np.empty((year_indices[years-1]["end"]))

	# hydrological timeseries model initial state
	state = (0, 
				422.7155/2, # d/2
				[0,0], # must be of length NC
				0, 
				0)

	# run LP farmer decision model
	farm_profit = maximum_profit(crops, farm_area, total_water_allocation)

	for year in range(years):
		state, flow, gwlevel, gwstorage = run_hydrology_by_year(year, state, climate_dates, rainfall, PET, sw_extractions, gw_extractions, climate_type)
		
		indices = year_indices[year]
		all_years_gwstorage[indices["start"]:indices["end"]] = gwstorage
		all_years_gwlevel[indices["start"]:indices["end"]] = gwlevel
		all_years_flow[indices["start"]:indices["end"]] = flow
		all_years_profit[indices["start"]:indices["end"]] = farm_profit/365


	# dispose of burn in dates
	the_dates = climate_dates[year_indices[2]["start"]:year_indices[years-1]["end"]]
	all_years_flow = all_years_flow[year_indices[2]["start"]:]
	all_years_gwlevel = all_years_gwlevel[year_indices[2]["start"]:]


	# run ecological model 
	surface_index, gwlevel_index = calculate_water_index(
							gw_level = all_years_gwlevel, 
							flow = all_years_flow, 
							dates = the_dates,
							threshold = eco_ctf, 
							min_separation = eco_min_separation,
							min_duration = eco_min_duration,
							duration_weight = eco_weights["Duration"],
							timing_weight = eco_weights["Timing"],
							dry_weight = eco_weights["Dry"],
							surface_weight = 0.5,
							gwlevel_weight = 0.5,
							timing_col = timing_col,
							duration_col = duration_col,
							dry_col = dry_col,
							gwlevel_col = gwlevel_col
							)


	if plot:
		plot_results(the_dates, all_years_flow, all_years_gwlevel, surface_index, gwlevel_index, farm_profit)

	surface_index_sum, years = f_by_year(the_dates, surface_index, np.sum)
	gw_index_sum, years = f_by_year(the_dates, gwlevel_index, np.sum)
	gw_level_min, years = f_by_year(the_dates, all_years_gwlevel, np.min)


	return farm_profit, np.mean(surface_index_sum), np.mean(gw_index_sum), np.mean(all_years_gwlevel), np.mean(gw_level_min) 
