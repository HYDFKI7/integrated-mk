import numpy as np

from climate.read_climate import read_climate_projections

from hydrological.RunIhacresGw import set_climate_data, run_hydrology, get_state

from farm_decision.farm_optimize import maximum_profit, load_crops

from ecological.ecological_indices import calculate_water_index

'''
inputs: climate scenario, crop prices, WUE, irrigation area, AWD (function that determines fraction of limits based on levels)
outputs: farm profit, profit variability, water levels (from which we compute environmental indices)
'''

def test_annual():
	all_crops = load_crops()

	# Water allocations for the Namoi Valley
	# Available Water Determination Order for Various NSW Groundwater Sources (No. 1) 2014
	# http://www.water.nsw.gov.au/Water-management/Water-availability/Water-allocations/Available-water-determinations
	# TODO 
	# this should ideally be a function of gwlevel and flow?
	AWD = {"sw_unregulated": 1, "gw": 1}

	# apply AWD to get water_licence
	# -------------------------------------------
	# Extraction limit 2,200 ML/yr \cite{Upper_and_Lower_Namoi_Groundwater_Sources}
	# Maules Creek Entitlement (ML/year) 1,413 \cite{Namoi_Unregulated_and_Alluvial}
	water_limit = {"sw_unregulated": 1413, "gw": 2200}

	# TODO
	water_licence = {}
	for licence_type in water_limit:
		water_licence[licence_type] = water_limit[licence_type] * AWD[licence_type]

	# Comparative Irrigation Costs 2012 - NSW DPI (Peter Smith)
	# TODO 
	# does nothing
	WUE = {"flood_irrigation": 0.65, "spray_irrigation": 0.8, "drip_irrigation": 0.85}

	# \cite{powell2011representative}
	farm_area = {"flood_irrigation": 782, "spray_irrigation": 0, "drip_irrigation": 0, "dryland": 180}

	climate_dates, rainfall, PET = read_climate_projections('climate/419051.csv', scenario=1)
	# TODO
	# get climate projections temp not PET
	temperature = PET * 5


	# burn in hydrological model 
	# -------------------------------------------
	burn_in = 365*2
	# write rainfall and temperature, extractions to csv files
	extractions = [0 for i in climate_dates]
	set_climate_data(dates=climate_dates[:365*5], rainfall=rainfall[:365*5], temperature=temperature[:365*5], swextraction=extractions[:365*5], gwextraction=extractions[:365*5])
	hydro_sim, hydro_tdat, hydro_mod = run_hydrology(0, 
												422.7155/2, # d/2
												[0,0], # must be of length NC
												0, 
												0) 

	state = get_state(hydro_sim, hydro_tdat, hydro_mod, burn_in)
	
	burn_flow = np.array(hydro_sim.rx2('Q')).squeeze()
	burn_gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]

	# run for each year
	# -------------------------------------------
	years = 3
	assert len(climate_dates) > burn_in+365*years

	all_years_flow = np.empty((365*years))
	all_years_gwstorage = np.empty((365*years))

	for y in range(years):
		extractions = [0 for i in climate_dates]
		# write rainfall and temperature, extractions to csv files
		start_date = burn_in+y*365
		end_date = burn_in+(y+1)*365
		set_climate_data(dates=climate_dates[start_date:end_date], rainfall=rainfall[start_date:end_date], temperature=temperature[start_date:end_date], swextraction=extractions[start_date:end_date], gwextraction=extractions[start_date:end_date])


		hydro_sim, hydro_tdat, hydro_mod = run_hydrology(state[0], state[1], state[2], state[3], state[4])
		# hydro_sim, hydro_tdat, hydro_mod = run_hydrology(*state)

		state = get_state(hydro_sim, hydro_tdat, hydro_mod, 365)

		# extract data from hydrological model output
		gw_i = 3
		gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
		flow = np.array(hydro_sim.rx2('Q')).squeeze()
		gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
		dates = list(hydro_tdat.rx2('dates'))
		gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

		interpolated_gwlevel = map(lambda x: x*gwfitparams[0] + gwfitparams[1], gwstorage)
		assert np.alltrue( interpolated_gwlevel == gwlevel)

		all_years_gwstorage[y*365:(y+1)*365] = gwstorage
		all_years_flow[y*365:(y+1)*365] = flow

		assert np.alltrue( dates == climate_dates[start_date:end_date] )

		# run LP farmer decision model
		# -------------------------------------------
		total_water_licence = water_licence['sw_unregulated']+water_licence['gw']
		farm_profit = maximum_profit(all_crops, farm_area, total_water_licence)

		# subtract water used by farmer from flows
		# -------------------------------------------
		# TODO
		# run a year at a time
		gwstorage = gwstorage - water_limit['gw']/365.0
		interpolated_gwlevel = map(lambda x: x*gwfitparams[0] + gwfitparams[1], gwstorage)
		flow = flow - water_limit['sw_unregulated']/365.0

		# run ecological model 
		# -------------------------------------------
		water_index = calculate_water_index(interpolated_gwlevel, flow, dates)


		# print "PROFIT", farm_profit
		# print "WATER", np.min(water_index), np.mean(water_index), np.max(water_index)



	assert np.allclose(burn_flow[burn_in:], all_years_flow)

	import matplotlib.pyplot as plt 
	# plt.plot(all_years_flow, label='all years flow', ls='--')
	# plt.plot(burn_flow[burn_in:], label='burn flow')
	plt.plot(burn_flow[burn_in:]-all_years_flow)
	plt.legend()
	plt.show()
	# plt.plot(all_years_gwstorage, label='all years gwstorage', ls='--')
	# plt.plot(burn_gwstorage[burn_in:], label='burn gwstorage')
	plt.plot(burn_gwstorage[burn_in:]-all_years_gwstorage)
	plt.legend()
	plt.show()


if __name__ == '__main__':
	test_annual()