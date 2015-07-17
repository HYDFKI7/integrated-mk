import csv 
import os
import numpy as np
import matplotlib.pyplot as plt 

from climate.read_climate import read_climate_projections, read_original_data, read_all_bom_data, find_extremes, read_NSW_data

from hydrological.RunIhacresGw import dateifier, get_year_indices, generate_extractions, run_hydrology_by_year, f_by_year

from farm_decision.farm_optimize import load_chosen_crops, maximum_profit, list_all_combos

from ecological.ecological_indices import calculate_water_index, eco_weights_parameters, eco_ctf_parameters, eco_min_separation_parameters, eco_min_duration_parameters

from ConfigLoader import *

# TODO cite all data

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def intersection_scatter(x1,y1,x2,y2):
	if x1[0] in x2:
		first_i = x2.index(x1[0])
		x2 = x2[first_i:]
		y2 = y2[first_i:]
	elif x2[0] in x1:
		first_i = x1.index(x2[0])
		x1 = x1[first_i:]
		y1 = y1[first_i:]
	else:
		print "PROBLEM"
	if x1[-1] in x2:
		last_i = x2.index(x1[-1])+1
		x2 = x2[:last_i]
		y2 = y2[:last_i]
	elif x2[-1] in x1:
		last_i = x1.index(x2[-1])+1
		x1 = x1[:last_i]
		y1 = y1[:last_i]
	else:
		print "PROBLEM"
	

	print "COR"
	print np.corrcoef(moving_average(y1,3),moving_average(y2,3))
	print np.corrcoef(moving_average(y1,10),moving_average(y2,10))
	print np.corrcoef(moving_average(y1,30),moving_average(y2,30))
	print np.corrcoef(y1, y2)

	# plt.scatter(moving_average(y1,30),moving_average(y2,30))
	plt.show()

def plot_results(climate_dates, all_years_flow, all_years_gwlevel, surface_index, gwlevel_index, farm_profit):

	sw_dates, sw, gw_dates, gw = read_NSW_data()

	gw = -1.*gw

	print "PROFIT", farm_profit

	dates = map(dateifier, climate_dates)


	# intersection_scatter([d.date() for d in sw_dates], sw.tolist(), [d.date() for d in dates], all_years_flow.tolist())

	plt.subplot(3,1,1)
	plt.plot(dates, all_years_flow, label='mod')
	plt.plot(sw_dates[9556:], sw[9556:], label="obs", ls="dotted")
	plt.legend()	
	plt.title('flow')	
	plt.subplot(3,1,2)
	# plt.plot(dates, all_years_gwstorage)
	plt.plot(dates, all_years_gwlevel, label="mod")
	plt.plot(gw_dates, gw, label="obs", ls="dotted")
	plt.legend()	
	plt.title('gwlevel')	
	plt.subplot(3,1,3)
	plt.plot(dates, surface_index, label='surface')
	plt.plot(dates, gwlevel_index, label='gw')
	plt.title('water_index')
	plt.legend()	
	plt.show()


def run_integrated(years, WUE, water_limit, AWD, adoption, crop_price_choice,
				   climate_dates, rainfall, PET, climate_type,
				   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, plot,
				   	timing_col, duration_col, dry_col, gwlevel_col):

	# TODO add prices as parameter once we have min, max
	# crop prices, yields, costs all determined here
	crops = load_chosen_crops(WUE, crop_price_choice ) #load chosen crops.csv data, then manipulate water use (ML/ha) based on WUE scenarios (e.g. min flood wue is 50%)

	water_licence = {}
	for licence_type in water_limit: # water limit is the annual total sw and gw water allocation
		water_licence[licence_type] = water_limit[licence_type] * AWD[licence_type]

	#total water allocation after accounting for annual total water allocation (water_limit) and allocation rate (awd)
	total_water_allocation = AWD['sw unregulated'] * water_limit['sw unregulated'] \
								+ AWD['gw'] * water_limit['gw']

	#adoption['flood'] = % area under flood irrigation (0~100). Used in optimisation, farm_area = max farm area (km^2) under flood and spray irrigation.
	farm_area = {
		"flood": 782.*7.*adoption["flood"]/100., # hectares #/100 to convert adoption rate from 0~100 to 0~1.
		"spray": 782.*7.*adoption["spray"]/100., 
		"drip": 782.*7.*adoption["drip"]/100., 
		"dryland": 180.*7.
	}

	#calculate daily extractions, same every day, same for all climates, depends on annual limits only.
	sw_extractions, gw_extractions = generate_extractions(climate_dates, water_limit['sw unregulated']/365, water_limit['gw']/365)

	#years for the selected climate period, and the daily indices.
	year_indices, year_list = get_year_indices(climate_dates)

	#model can't run if the years parameter is longer than the # of years for selected climate period. 
	assert years <= len(year_indices)
	#create number of very small values. n = in the climate period, find the # of dates in the first 12 (=years parameter) years. eg if the first year starts 31 dec, then it's practically 11 years+1 day data 
	all_years_flow = np.empty((year_indices[years-1]["end"])) 
	all_years_gwstorage = np.empty((year_indices[years-1]["end"]))
	all_years_gwlevel = np.empty((year_indices[years-1]["end"]))
	all_years_profit = np.empty((year_indices[years-1]["end"]))

	# hydrological timeseries model initial state
	state = (0, #initial gw storage
				422.7155/2, # d/2 #initial C
				[0,0], # must be of length NC # initial Nash
				0,  #initial Qq
				0) #initial Qs

	# run LP farmer decision model
	farm_profit = maximum_profit(crops, farm_area, total_water_allocation)

	for year in range(years):
		state, flow, gwlevel, gwstorage = run_hydrology_by_year(year, state, climate_dates, rainfall, PET, sw_extractions, gw_extractions, climate_type)
		
		indices = year_indices[year]
		all_years_gwstorage[indices["start"]:indices["end"]] = gwstorage #no use
		all_years_gwlevel[indices["start"]:indices["end"]] = gwlevel
		all_years_flow[indices["start"]:indices["end"]] = flow
		all_years_profit[indices["start"]:indices["end"]] = farm_profit/365 #no use


	# dispose of burn in dates
	# start with the third year. ie burn in period different for the climate periods, which start at different date of a year.
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

	# sw_dates, sw, gw_dates, gw = read_NSW_data()
	# np.savetxt("gw_obs.csv", gw, delimiter=",") 
	# with open("gw_obs.csv", "wb") as csvfile:
	# 	writer = csv.writer(csvfile)
	# 	for i in range(len(gw_dates)):
	# 		writer.writerow([gw_dates[i], gw[i]])

	
	# with open("modelled_flow.csv", "wb") as csvfile:
	# 	writer = csv.writer(csvfile)
	# 	for i in range(len(climate_dates)):
	# 		print climate_dates[i], all_years_flow[i], all_years_gwlevel[i]
	# 		writer.writerow([climate_dates[i], all_years_flow[i], all_years_gwlevel[i]])


	if plot:
		plot_results(the_dates, all_years_flow, all_years_gwlevel, surface_index, gwlevel_index, farm_profit)

	surface_index_sum, years = f_by_year(the_dates, surface_index, np.sum)
	gw_index_sum, years = f_by_year(the_dates, gwlevel_index, np.sum)
	gw_level_min, years = f_by_year(the_dates, all_years_gwlevel, np.min)

	#return: annual farm profit, 
	return farm_profit, np.mean(surface_index_sum), np.mean(gw_index_sum), np.mean(all_years_gwlevel), np.mean(gw_level_min) 

