from rpy2 import robjects

import numpy as np

from climate.read_climate import read_climate_projections

from hydrological.RunIhacresGw import read_csv, set_climate_data, run_hydrology, get_state

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
middle_i = 27
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
state = get_state(hydro_sim, hydro_tdat, hydro_mod, middle_i)


original_gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
original_Rdiffuse = np.array(hydro_sim.rx2('Rdiffuse')).squeeze()
original_R = np.array(hydro_sim.rx2('R')).squeeze()[:,0]
original_Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
original_Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
original_Qs = np.array(hydro_sim.rx2('Qs')).squeeze()
original_swE = np.array(hydro_sim.rx2('swE')).squeeze()
original_Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
original_Qr = hydro_sim.rx2('Qr').rx2('sw_419051')
original_dates = list(hydro_tdat.rx2('dates'))
gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

set_climate_data(dates=original_dates[middle_i:end_i],
			 rainfall=original_rain[middle_i:end_i],
			 temperature=original_temperature[middle_i:end_i],
			 swextraction=original_swextraction[middle_i:end_i],
			 gwextraction=original_gwextraction[middle_i:end_i])



# hydro_sim, hydro_tdat, hydro_mod = run_hydrology(*state)
# hydro_sim, hydro_tdat, hydro_mod = run_hydrology(state[0], state[1], state[2], state[3], state[4])
hydro_sim, hydro_tdat, hydro_mod = run_hydrology(state[0], state[1], state[2], state[3], state[4])

gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
flow = np.array(hydro_sim.rx2('Q')).squeeze()



gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
Qs = np.array(hydro_sim.rx2('Qs')).squeeze()
Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
Rdiffuse = np.array(hydro_sim.rx2('Rdiffuse')).squeeze()
R = np.array(hydro_sim.rx2('R')).squeeze()[:,0]
swE = np.array(hydro_sim.rx2('swE')).squeeze()
Qr = hydro_sim.rx2('Qr').rx2('sw_419051')
Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
dates = list(hydro_tdat.rx2('dates'))
gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

print 'flow', original_flow[middle_i], flow[0]
print 'Uq', original_Uq[middle_i], Uq[0]
print 'Qq', original_Qq[middle_i], Qq[0]
print 'Qs', original_Qs[middle_i], Qs[0]
print 'Qd', original_Qd[middle_i], Qd[0]
print 'swE', original_swE[middle_i], swE[0]
print 'R', original_R[middle_i], R[0]
print 'Rdiffuse', original_Rdiffuse[middle_i], Rdiffuse[0]
print 'Qr', original_Qr[middle_i], Qr[0]



import matplotlib.pyplot as plt 
plt.plot(gwstorage-original_gwstorage[middle_i:])
plt.title('storage error')
plt.show()

plt.plot(flow - original_flow[middle_i:] )
plt.title('flow error')
plt.show()

