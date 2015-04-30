import numpy as np

from climate.read_climate import read_climate_projections, read_original_data

from hydrological.RunIhacresGw import set_climate_data, run_hydrology, get_state, get_outputs

from farm_decision.farm_optimize import maximum_profit, load_crops

from ecological.ecological_indices import calculate_water_index

'''
inputs: climate scenario, crop prices, WUE, irrigation area, AWD (function that determines fraction of limits based on levels)
outputs: farm profit, profit variability, water levels (from which we compute environmental indices)
'''

if __name__ == '__main__':

	climate_type = "temperature" 
	# climate_type = "PET"

	all_crops = load_crops()

	# Water allocations for the Namoi Valley
	AWD = {"sw unregulated": 1, "gw": 1}

	# apply AWD to get water_licence
	water_limit = {"sw unregulated": 1413, "gw": 2200}

	water_licence = {}
	for licence_type in water_limit:
		water_licence[licence_type] = water_limit[licence_type] * AWD[licence_type]

	# WUE = {"flood irrigation": 0.65, "spray irrigation": 0.8, "drip irrigation": 0.85}

	farm_area = {"flood irrigation": 782*7, "spray irrigation": 0, "drip irrigation": 0, "dryland": 180*7}

	climate_dates, rainfall = read_original_data('rain.data.csv', "sw_419051", with_dates=True)
	PET = read_original_data('temperature.data.csv', "sw_419051")
	swextractions = read_original_data('swextraction.data.csv', "sw_419051")
	gwextractions = read_original_data('gwextraction.data.csv', "gw_shallow")

	# initialize
	state = (0, 422.7155/2, [0,0], 0, 0)
	burn_in = 0

	
	# run for each year
	# -------------------------------------------
	years = 40
	assert len(climate_dates) > burn_in+365*years

	all_years_flow = np.empty((365*years))
	all_years_gwstorage = np.empty((365*years))
	all_years_profit = np.empty((365*years))
	all_years_gwlevel = np.empty((365*years))

	for y in range(years):

		# TODO 
		# here adjust water_licences based on previous years climate!

		# rainfall effect on dryland yield
		# write down how you'd do infrastructure investment

		# write rainfall and PET, extractions to csv files
		start_date = burn_in+y*365
		end_date = burn_in+(y+1)*365
		set_climate_data(dates = climate_dates[start_date:end_date],
						 rainfall = rainfall[start_date:end_date],
						 PET = PET[start_date:end_date],
						 swextraction = swextractions,
						 gwextraction = gwextractions)


		hydro_sim, hydro_tdat, hydro_mod = run_hydrology(*state, climate_type=climate_type)

		# get state so model can be stopped and started
		state = get_state(hydro_sim, hydro_tdat, hydro_mod, 365)

		# extract data from hydrological model output
		dates, flow, gwlevel, gwstorage, gwfitparams = get_outputs(hydro_sim, hydro_tdat, hydro_mod)

		# run LP farmer decision model
		# -------------------------------------------
		total_water_licence = water_licence['sw unregulated']+water_licence['gw']
		farm_profit = maximum_profit(all_crops, farm_area, total_water_licence)

		all_years_gwstorage[y*365:(y+1)*365] = gwstorage
		all_years_gwlevel[y*365:(y+1)*365] = gwlevel
		all_years_flow[y*365:(y+1)*365] = flow
		all_years_profit[y*365:(y+1)*365] = farm_profit/365.0

	# run ecological model 
	water_index = calculate_water_index(all_years_gwlevel, all_years_flow, climate_dates[burn_in:burn_in+years*365])



	import datetime
	def dateifier(date_string):
		return datetime.datetime.strptime(date_string, "%Y-%m-%d")

	import matplotlib.pyplot as plt 


	# plt.show()

	plot_dates = map(dateifier, climate_dates[burn_in: burn_in+365*years])

	plt.subplot(4,1,1)
	plt.plot(plot_dates, all_years_flow)
	plt.title('flow')	
	plt.subplot(4,1,2)
	# plt.plot(plot_dates, all_years_gwstorage)
	plt.plot(plot_dates, all_years_gwlevel)

	for obsname in ["GW036186_1"]:
	# for obsname in ["GW030130_1" "GW030131_1" "GW030132_2" "GW036186_1" "GW036187_1"]:
		obs_dates, gwobs = read_original_data('gwdepth.obs.csv', obsname, with_dates=True)
		gwobs = gwobs[burn_in: burn_in+365*years]
		dates = map(dateifier, obs_dates[burn_in: burn_in+365*years])
		plt.plot(dates, gwobs, linestyle='none', marker='o', label=obsname)

	plt.legend()


	plt.title('gwlevel')	
	plt.subplot(4,1,3)
	plt.plot(plot_dates, water_index)
	plt.title('water_index')	
	plt.subplot(4,1,4)
	plt.plot(plot_dates, all_years_profit)
	plt.title('profit')
	plt.show()

