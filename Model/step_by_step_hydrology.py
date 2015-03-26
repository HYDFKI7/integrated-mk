from rpy2 import robjects

import numpy as np

from climate.read_climate import read_climate_projections

from hydrological.RunIhacresGw import read_csv, set_climate_data, run_hydrology

from farm_decision.farm_optimize import maximum_profit, read_crops_csv

from ecological.ecological_indices import calculate_water_index

'''
Runs hydrological model of Maules Creek, originally by Rachel Blakers.
The model is writen in R and takes its inputs and parameters from csv files.
Some inputs are now passed as arguments.
We have customised it so it can be run for an interval, outputs read, and then run for the following interval.
This file tests this customisation
'''

# tests if model[start_i, end_i] = model[start_i,middle_i] + model[middle_i, end_i]
start_i = 0
middle_i = 500
end_i = 3000

gw_i = 3

# read original csv inputs
original_rain = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/rain.data.csv'))[1:,1])
original_temperature = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/temperature.data.csv'))[1:,1])
original_swextraction = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/swextraction.data.csv'))[1:,1])
original_gwextraction = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/gwextraction.data.csv'))[1:,1])
original_dates = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/rain.data.csv'))[1:,0])

# write original data
set_climate_data(dates=original_dates[:end_i],
 rainfall=original_rain[:end_i],
 temperature=original_temperature[:end_i],
 swextraction=original_swextraction[:end_i],
 gwextraction=original_gwextraction[:end_i])

# init_Qq = 0, init_Qs = 0 makes no difference
hydro_sim, hydro_tdat, hydro_mod = run_hydrology(0, 
												422.7155/2, # d/2
												robjects.FloatVector([0,0]), # must be of length NC
												0, 
												0) 

original_flow = np.array(hydro_sim.rx2('Q')).squeeze()
original_gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
original_raw_C = np.array(hydro_sim.rx2('raw_C')).squeeze()
original_next_Nash = np.array(hydro_sim.rx2('next_Nash')).squeeze()
original_Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
original_Qs = np.array(hydro_sim.rx2('Qs')).squeeze()

set_climate_data(dates=original_dates[middle_i:end_i],
			 rainfall=original_rain[middle_i:end_i],
			 temperature=original_temperature[middle_i:end_i],
			 swextraction=original_swextraction[middle_i:end_i],
			 gwextraction=original_gwextraction[middle_i:end_i])

hydro_sim, hydro_tdat, hydro_mod = run_hydrology(original_gwstorage[middle_i-1], original_raw_C[middle_i-1], robjects.FloatVector(original_next_Nash[middle_i-1]), original_Qq[middle_i-1], original_Qs[middle_i-1]) # RunIhacresGw.R takes about 17 seconds

gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
flow = np.array(hydro_sim.rx2('Q')).squeeze()

import matplotlib.pyplot as plt 
plt.plot(gwstorage-original_gwstorage[500:3000])
plt.title('storage error')
plt.show()

plt.plot(flow - original_flow[500:3000] )
plt.title('flow error')
plt.show()



# original_gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
# original_Rdiffuse = np.array(hydro_sim.rx2('Rdiffuse')).squeeze()
# original_R = np.array(hydro_sim.rx2('R')).squeeze()[:,0]
# original_Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
# original_swE = np.array(hydro_sim.rx2('swE')).squeeze()
# original_Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
# original_Qr = hydro_sim.rx2('Qr').rx2('sw_419051')
# original_dates = list(hydro_tdat.rx2('dates'))
# gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

# print "ORIGINAL"
# print original_flow[499]
# print original_Uq[499]
# print original_Qq[499]
# print original_Qs[499]
# print original_Qd[499]
# print original_swE[499]
# print original_R[499]
# print original_Rdiffuse[499]
# print original_next_Nash[499]
# print original_Qr






# gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
# Qs = np.array(hydro_sim.rx2('Qs')).squeeze()
# Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
# Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
# swE = np.array(hydro_sim.rx2('swE')).squeeze()
# Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
# dates = list(hydro_tdat.rx2('dates'))
# gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

# print "SLOW"
# print flow[0]
# print Uq[0]
# print Qq[0]
# print Qs[0]
# print Qd[0]
# print swE[0]


# plt.plot(np.array([0 for i in range(500)]+gwstorage.tolist)
# plt.plot(original_gwstorage[:1500], ls='--')