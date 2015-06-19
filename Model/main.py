import csv 
import os
import numpy as np

# from climate.read_climate import read_climate_projections, read_original_data, read_all_bom_data, find_extremes
from climate.read_climate import read_all_bom_data, find_extremes

# from hydrological.RunIhacresGw import dateifier, get_year_indices, generate_extractions, run_hydrology_by_year, f_by_year

# from farm_decision.farm_optimize import load_chosen_crops, maximum_profit, list_all_combos
from farm_decision.farm_optimize import  list_all_combos

from ecological.ecological_indices import calculate_water_index, eco_weights_parameters, eco_ctf_parameters, eco_min_separation_parameters, eco_min_duration_parameters

from integrated import run_integrated

def main():
	check()
	# run_scenarios()


def check():

	WUE = { "flood": 65.,
			"spray": 80. }

	# % of irrigated area in catchment
	adoption = { "flood": 100. - 8.,
				"spray": 8.,
				"drip": 0. }

	AWD = {"sw unregulated": 1., "gw": 1.}

	water_limit = {"sw unregulated": 1413., "gw": 2200.}


	climate_type = "temperature" 
	climate_dates, rainfall, PET = read_all_bom_data()

	per_i = np.where(climate_dates == '2000-01-01')[0][0]
	years = 12 # two years burn in
	window = 366*12
	climate_dates, rainfall, PET = climate_dates[per_i:per_i+window], rainfall[per_i:per_i+window], PET[per_i:per_i+window]


	eco_min_separation = eco_min_separation_parameters["med"]
	eco_min_duration = eco_min_duration_parameters["med"]
	eco_ctf = eco_ctf_parameters["med"]

	eco_weights = eco_weights_parameters["Default"]

	profit, surface_index, gw_index, gwlevel_mean, gwlevel_min = run_integrated(
						years, 
					   WUE, water_limit, AWD, adoption, 1.,
					   climate_dates, rainfall, PET, climate_type, 
					   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, True,
					   timing_col = 'Namoi', duration_col = 'Namoi', dry_col = 'Namoi', gwlevel_col = 'Index')


def run_scenarios():

	output_file = os.path.join(os.path.dirname(__file__), "runs.csv")

	with open(output_file,'w') as csvfile:
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
		"gwlevel_col"] +
		["profit", 
		"surface_index", 
		"gw_index", 
		"gwlevel_mean", 
		"gwlevel_min"
		])



	all_combos = list_all_combos([
			["Default", "Favour duration", "Favour dry", "Favour timing"],  	# 	eco_weights_choice
			["min", "med", "max"],   											# 	WUE_flood_choice
			["min", "med", "max"],  											# 	WUE_spray_choice
			["min", "med", "max"],  											# 	adoption_choice
			["min", "med", "max"],  											# 	climate_choice
			["min", "med", "max"],  											# 	eco_min_separation_choice
			["min", "med", "max"],  											# 	eco_min_duration_choice
			["min", "med", "max"],  											# 	eco_ctf_choice
			[0.5, 1.], 															# 	AWD_surface_choice
			[0.5, 1.], 															# 	AWD_gw_choice
			[0.5, 1.], 															# 	crop_price_choice
			["MFAT1", "Roberts", "Rogers", "Rogers", "Namoi"],
			["MFAT1", "MFAT2", "MFAT3", "MFAT4", "Roberts", "Rogers", "Namoi"],
			["MFAT1", "MFAT2", "Roberts", "Rogers", "Namoi"],
			["Index", "F1", "F2"]
			])


	# combos = list_all_combos([
	# 		["Default"],  	# 	eco_weights_choice
	# 		["min", "max"],   											# 	WUE_flood_choice
	# 		["min", "max"],  											# 	WUE_spray_choice
	# 		["min", "max"],  											# 	adoption_choice
	# 		["min", "max"],  											# 	climate_choice
	# 		["med"],  															# 	eco_min_separation_choice
	# 		[ "med" ],  											# 	eco_min_duration_choice
	# 		["med"],  											# 	eco_ctf_choice
	# 		[1.], 															# 	AWD_surface_choice
	# 		[0.5, 1.], 															# 	AWD_gw_choice
	# 		[0.5, 1.] 															# 	crop_price_choice
	# 		])
	


	default_combos = [["Default", "med", "med", "med", "min", "med", "med", "med", 1., 1., 1., 'Namoi', 'Namoi', 'Namoi', 'Index']]

	print "COMBOS", len(all_combos)


	for combo in all_combos[:3]:
	# for combo in combos[:30]:

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
		gwlevel_col) = combo
		



		# SCENARIO/PARAMETER - climate
		# [min_i, med_i, max_i]
		climate_type = "temperature" 
		climate_dates, rainfall, PET = read_all_bom_data()
		window = 366*3
		years = 3 # 2 years burn in
		min_i, med_i, max_i = find_extremes(rainfall, window)
		climate_scenarios = {"min": min_i, "med": med_i, "max": max_i}


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
		adoption_scenarios = {
			"flood": {
				"min": 27.3,
				"med": 65.,
				"max": 100.,
			},
			"spray":{
				"min": 0.5,
				"med": 8.,
				"max": 16.9,
			},
		}


		# SCENARIO/PARAMETER - irrigation tech adoption
		# ["min", "med", "max"]
		# flood = 100-spray-drip ()
		adoption = { "flood": 100. - adoption_scenarios["spray"][adoption_choice],
					"spray": adoption_scenarios["spray"][adoption_choice],
					"drip": 0. }

		# SCENARIO/PARAMETER - water allocations
		AWD = {"sw unregulated": AWD_surface_choice, "gw": AWD_gw_choice}

		water_limit = {"sw unregulated": 1413., "gw": 2200.}



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


		profit, surface_index, gw_index, gwlevel_mean, gwlevel_min = run_integrated(
							years, 
						   WUE, water_limit, AWD, adoption, crop_price_choice,
						   climate_dates, rainfall, PET, climate_type,
						   eco_min_separation, eco_min_duration, eco_ctf, eco_weights, False,
						   timing_col=timing_col, duration_col=duration_col, dry_col=dry_col, gwlevel_col=gwlevel_col)


		with open(output_file,'a') as csvfile:
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
				gwlevel_col] +
				[profit, 
				surface_index, 
				gw_index, 
				gwlevel_mean, 
				gwlevel_min,
				])

		# print eco_weights_choice, WUE_flood_choice, WUE_spray_choice, adoption_choice, climate_choice, eco_min_separation_choice, eco_min_duration_choice, eco_ctf_choice, profit, surface_index, gw_index, gwlevel_mean, gwlevel_min

		# print profit, surface_index, gw_index, gwlevel_mean, gwlevel_min

if __name__ == '__main__':
	main()
