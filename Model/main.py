import csv 
import os
import numpy as np
import pandas as pd

# os.chdir('/home/mikey/Desktop/integrated-mk/Model/')
# os.chdir('C:\\UserData\\fub\\work09\\Namoi\\integrated-mk\\Model')
os.chdir('C:\\Users\\baihua\\Documents\\Projects\\Namoi\\integrated-mk\\Model')


# from climate.read_climate import read_climate_projections, read_original_data, read_all_bom_data, find_extremes
from climate.read_climate import read_all_bom_data, find_extremes

# from hydrological.RunIhacresGw import dateifier, get_year_indices, generate_extractions, run_hydrology_by_year, f_by_year

# from farm_decision.farm_optimize import load_chosen_crops, maximum_profit, list_all_combos
from farm_decision.farm_optimize import  list_all_combos

from ecological.ecological_indices import calculate_water_index, eco_weights_parameters, eco_ctf_parameters, eco_min_separation_parameters, eco_min_duration_parameters

from integrated import run_integrated

from ConfigLoader import *

def main():
	# check()
	run_scenarios()


def check():

	WUE = { "flood": 80.,
			"spray": 90. }

	# % of irrigated area in catchment
	adoption = { "flood": 100. - 16.9,
				"spray": 16.9,
				"drip": 0. }

	AWD = {"sw unregulated": 1., "gw": 1.}

	water_limit = {"sw unregulated": 1413., "gw": 2200.}


	climate_type = "temperature" 
	climate_dates, rainfall, PET = read_all_bom_data()

	per_i = np.where(climate_dates == '1950-01-01')[0][0]
	years = 20 # two years burn in
	window = 366*years
	climate_dates, rainfall, PET = climate_dates[per_i:per_i+window], rainfall[per_i:per_i+window], PET[per_i:per_i+window]


	eco_min_separation = eco_min_separation_parameters["med"]
	eco_min_duration = eco_min_duration_parameters["med"]
	eco_ctf = eco_ctf_parameters["med"]

	eco_weights = eco_weights_parameters["Default"]

	profit, surface_index, gw_index, gwlevel_mean, gwlevel_min = run_integrated(
						years, 
					   WUE, water_limit, AWD, adoption, 1.,
					   climate_dates, rainfall, PET, climate_type, 
					   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, False,
					   timing_col = 'Roberts', duration_col = 'Namoi', dry_col = 'Namoi', gwlevel_col = 'Index', cj_options = 'constant1')

	# print profit, surface_index, gw_index, gwlevel_mean, gwlevel_min

def run_scenarios():
	# import json
	if "working_dir" in CONFIG.paths:
		path = CONFIG.paths['working_dir']
	else:
		path = os.path.dirname('__file__')
	# end if

	output_file = os.path.join(path, "runs.csv")
	with open(output_file,'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow([
		"eco_weights_choice", 
		"WUE_flood_choice",
		"WUE_spray_choice",
		"adoption_choice", 
		"climate_choice",
		"eco_min_separation_choice",
		"eco_min_duration_choice",
		"eco_ctf_choice",
		"AWD_surface_choice",
		"AWD_gw_choice",
		"crop_price_choice",
		"timing_col",
		"duration_col",
		"dry_col",
		"gwlevel_col",
		"sw_uncertainty_choice",
		"gw_uncertainty_choice",
		"crop_trend",
		"cj_options"
		] +
		["profit_mean",
		"profit_std", 
		"surface_index", 
		"gw_index", 
		"gwlevel_mean", 
		"gwlevel_min"
		])


	# all_combos = list_all_combos([
	# 		["Default", "Favour duration", "Favour dry", "Favour timing"],  	# 	eco_weights_choice
	# 		["min", "med", "max"],   											# 	WUE_flood_choice
	# 		["min", "med", "max"],  											# 	WUE_spray_choice
	# 		["min", "med", "max"],  											# 	adoption_choice
	# 		["dry", "avg", "wet"],  											# 	climate_choice
	# 		["min", "med", "max"],  											# 	eco_min_separation_choice
	# 		["min", "med", "max"],  											# 	eco_min_duration_choice
	# 		["min", "med", "max"],  											# 	eco_ctf_choice
	# 		[0.5, 0.8, 1.], 															# 	AWD_surface_choice
	# 		[0.5, 0.8, 1.], 															# 	AWD_gw_choice
	# 		[1.], 															# 	crop_price_choice
	# 		["MFAT1", "Roberts", "Rogers"],
	# 		["MFAT1", "MFAT2", "MFAT3", "MFAT4", "Roberts", "Rogers", "Namoi"],
	# 		["MFAT1", "MFAT2", "Roberts", "Rogers", "Namoi"],
	# 		["Index", "F1", "F2"]
	# 		["80%", "100%", "120%"]
	# 		["80%", "100%", "120%"]
	# 		["down", "flat", "up"]	
	# 		])

	all_combos = list_all_combos([
			["Default", "Favour duration"],  										# 	eco_weights_choice
			["min", "max"],   									# 	WUE_flood_choice
			["min", "max"],  									# 	WUE_spray_choice
			["min", "max"],  									# 	adoption_choice
			["min", "max"],  									# 	climate_choice
			["med"],  											# 	eco_min_separation_choice
			["med"],  											# 	eco_min_duration_choice
			["min", "med"],  									# 	eco_ctf_choice
			[0.5, 1.], 											# 	AWD_surface_choice
			[0.5, 1.], 											# 	AWD_gw_choice
			[1.], 											# 	crop_price_choice
			["Roberts", "Rogers"],								# timing_col
			["Roberts", "Rogers"],								# duration_col
			["Roberts"],								# dry_col
			["Index", "F1"],									# gwlevel_col
			["min", "max"],								# sw_uncertainty_choice
			["min", "max"],								# gw_uncertainty_choice
			["down", "up"],								# crop_trend
			["byrain","constant1","forcefix","oppfix","oppandforcefix"],	#conjunctive use options
			])

	
	default_combos = [
		["Favour duration", "min", "min", "min", "dry", "med", "med", "min", 0.5, 0.5, 1., 'Roberts', 'Roberts', 'Roberts', 'Index', '50%', '120%', 'down','byrain'],	#min case
		["Default", "max", "max", "max", "wet", "med", "med", "min", 2, 2., 1., 'Roberts', 'Rogers', 'Roberts', 'F2','150%', '80%', 'up','oppandforcefix'],	#max case
		["Default", "med", "med", "med", "avg", "med", "med", "min", 1., 1., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#base case	
	]

	cj_combos = [
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 2., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','byrain'],	#min case
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 2., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#max case
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 2., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','forcefix'],
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 2., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','oppfix'],
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 2., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','oppandforcefix'],	#base case	
	]

	awd_combos = [
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 0.5, 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#min case
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 1., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#max case
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 1.5, 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],
		["Default", "med", "med", "med", "wet", "med", "med", "min", 0.5, 1., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1., 1., 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#base case	
		["Default", "med", "med", "med", "wet", "med", "med", "min", 1.5, 1, 1., 'Roberts', 'Roberts', 'Roberts', 'Index','100%', '100%', 'flat','constant1'],	#base case	
	]

	hydro_combos =  list_all_combos([
			["Default", "Favour duration"],  										# 	eco_weights_choice
			["med"],   									# 	WUE_flood_choice
			["med"],  									# 	WUE_spray_choice
			["med"],  									# 	adoption_choice
			["dry", "avg","wet"],  									# 	climate_choice
			["med"],  											# 	eco_min_separation_choice
			["med"],  											# 	eco_min_duration_choice
			["min"],  									# 	eco_ctf_choice
			[1.], 											# 	AWD_surface_choice
			[1.], 											# 	AWD_gw_choice
			[1.], 											# 	crop_price_choice
			["Roberts"],								# timing_col
			["Roberts", "Rogers"],								# duration_col
			["Roberts"],								# dry_col
			["Index", "F2"],									# gwlevel_col
			["50%", "80%", "100%", "120%","150%"],								# sw_uncertainty_choice
			["50%", "80%", "100%", "120%","150%"],								# gw_uncertainty_choice
			["flat"],								# crop_trend
			["byrain", "constant1"],	#conjunctive use options
			])


	all_combos2 = list_all_combos([
			["Default", "Favour duration"],  										# 	eco_weights_choice
			["min", "max"],   									# 	WUE_flood_choice
			["min", "max"],  									# 	WUE_spray_choice
			["min", "max"],  									# 	adoption_choice
			["dry", "wet"],  									# 	climate_choice
			["med"],  											# 	eco_min_separation_choice
			["med"],  											# 	eco_min_duration_choice
			["min"],  									# 	eco_ctf_choice
			[0.5, 2.], 											# 	AWD_surface_choice
			[0.5, 2.], 											# 	AWD_gw_choice
			[1.], 											# 	crop_price_choice
			["Roberts"],								# timing_col
			["Roberts", "Rogers"],								# duration_col
			["Roberts"],								# dry_col
			["Index", "F2"],									# gwlevel_col
			["50%", "150%"],								# sw_uncertainty_choice
			["80%", "120%"],								# gw_uncertainty_choice
			["down", "up"],								# crop_trend
			["byrain","constant1","forcefix","oppandforcefix"],	#conjunctive use options
			])

	# print "COMBOS", len(all_combos2), 
	# print "Estimated time (h)", len(all_combos2)*6/60/60

	# for combo in all_combos2:
	for combo in default_combos:
	# for combo in cj_combos:
	# for combo in awd_combos:
	# for combo in combos[:30]:
	# combo=default_combos[0]

		(eco_weights_choice, 
		WUE_flood_choice,
		WUE_spray_choice,
		adoption_choice, 
		climate_choice,
		eco_min_separation_choice,
		eco_min_duration_choice,
		eco_ctf_choice,
		AWD_surface_choice,
		AWD_gw_choice,
		crop_price_choice,
		timing_col,
	 	duration_col,
	 	dry_col,
		gwlevel_col,
		sw_uncertainty_choice,
		gw_uncertainty_choice,
		crop_trend,
		cj_options) = combo
		
		# SCENARIO/PARAMETER - climate
		# [min_i, med_i, max_i]
		climate_type = "temperature" 
		climate_dates, rainfall, PET = read_all_bom_data()
		window = 366*12
		years = 12 # 2 years burn in
		min_i, med_i, max_i = find_extremes(rainfall, window) #3 climate scenarios
		climate_scenarios = {"dry": min_i, "avg": med_i, "wet": max_i}

		WUE_scenarios = {
			"flood": {
				"min": 50.,
				"med": 65.,
				"max": 80.,
			},
			"spray":{
				"min": 70.,
				"med": 80.,
				"max": 90.,
			},
			"drip": {
				"min": 76.,
				"med": 85.,
				"max": 85.,
			}
		}

		# SCENARIO/PARAMETER - irrigation WUE
		# ["min", "med", "max"]
		WUE = { "flood": WUE_scenarios["flood"][WUE_flood_choice],
				"spray": WUE_scenarios["spray"][WUE_spray_choice] }

		# % of irrigated area in catchment
		# as specified below, only spray values are used. flood - 100-spray
		# implication: only one irrigation approach per area.
		adoption_scenarios = {
			"flood": {
				"min": 27.3,
				"med": 65.,
				"max": 100.,
			},
			"spray":{
				"min": 0.5,
				"med": 8.,#e.g. if choose 'med' in adoption_choice, then it's 8% spray irrigation area and 92% flood irrigation area
				"max": 16.9,
			},
		}

		# SCENARIO/PARAMETER - irrigation tech adoption
		# ["min", "med", "max"]
		# flood = 100-spray-drip () # drip set to 0; spray specified in scenario (ie adoption choice, in min/med/max); whatever left is flood.
		# adoption = % area under flood and spray irrigation. 
		adoption = { "flood": 100. - adoption_scenarios["spray"][adoption_choice], 
					"spray": adoption_scenarios["spray"][adoption_choice],
					"drip": 0. }

		# SCENARIO/PARAMETER - water allocations
		AWD = {"sw unregulated": AWD_surface_choice, "gw": AWD_gw_choice} #AWD_surface/gw_choice is a value betewen 0 and 1, as an index to adjust annual water entitlement (water_limit)

		# Water entitlment for Maules ck. 
		#Source: "Water Sharing Plan for the Namoi Unregulated and Alluvial Water Sources 2012"
		#http://www.legislation.nsw.gov.au/#/view/regulation/2012/493
		#Current version for 8 January 2015 to date (accessed 23 May 2016 at 14:15).
		water_limit = {"sw unregulated": 1406., "gw": 2200.} 
	

		# SCENARIO/PARAMETER - climate
		# ["min", "med", "max"]
		per_i = climate_scenarios[climate_choice]
		climate_dates, rainfall, PET = climate_dates[per_i:per_i+window], rainfall[per_i:per_i+window], PET[per_i:per_i+window]

		# climate_type = "PET"
		# climate_dates, rainfall, PET = read_climate_projections('climate/419051.csv', scenario=1)

		# SCENARIO/PARAMETER - eco
		# ["min", "med", "max"]
		eco_min_separation = eco_min_separation_parameters[eco_min_separation_choice]
		eco_min_duration = eco_min_duration_parameters[eco_min_duration_choice]
		eco_ctf = eco_ctf_parameters[eco_ctf_choice]

		# SCENARIO/PARAMETER - eco
		# ["Default", "Favour duration", "Favour dry", "Favour timing"]
		eco_weights = eco_weights_parameters[eco_weights_choice]

		sw_uncertainty = {"50%": 0.50, "80%": 0.80, "100%": 1.0, "120%": 1.20, "150%": 1.50}[sw_uncertainty_choice]
		gw_uncertainty = {"50%": 0.50, "80%": 0.80, "100%": 1.0, "120%": 1.20, "150%": 1.50}[gw_uncertainty_choice]

		profit, surface_index, gw_index, gwlevel_mean, gwlevel_min = run_integrated(
							years, 
						   WUE, water_limit, AWD, adoption, crop_price_choice,
						   climate_dates, rainfall, PET, climate_type,
						   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, False,
						   timing_col=timing_col, duration_col=duration_col, dry_col=dry_col, gwlevel_col=gwlevel_col,
						   sw_uncertainty=sw_uncertainty, gw_uncertainty=gw_uncertainty, crop_trend=crop_trend, cj_options=cj_options)


		with open(output_file,'ab') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([
				eco_weights_choice, 
				WUE_flood_choice,
				WUE_spray_choice,
				adoption_choice, 
				climate_choice,
				eco_min_separation_choice,
				eco_min_duration_choice,
				eco_ctf_choice,
				AWD_surface_choice,
				AWD_gw_choice,
				crop_price_choice,
				timing_col,
			 	duration_col,
			 	dry_col,
				gwlevel_col,
				sw_uncertainty_choice,
				gw_uncertainty_choice,
				crop_trend,
				cj_options,] +
				[np.mean(profit),
				np.percentile(profit,1), 
				surface_index, 
				gw_index, 
				gwlevel_mean, 
				gwlevel_min
				])

		# print eco_weights_choice, WUE_flood_choice, WUE_spray_choice, adoption_choice, climate_choice, eco_min_separation_choice, eco_min_duration_choice, eco_ctf_choice, profit, surface_index, gw_index, gwlevel_mean, gwlevel_min

		# print profit, surface_index, gw_index, gwlevel_mean, gwlevel_min

if __name__ == '__main__':
	main()
