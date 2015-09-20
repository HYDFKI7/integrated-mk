import numpy as np

from climate.read_climate import read_climate_projections

from hydrological.RunIhacresGw import read_csv, set_climate_data, run_hydrology

from farm_decision.farm_optimize import maximum_profit, read_crops_csv

from ecological.ecological_indices import calculate_water_index

'''
inputs: climate scenario, crop prices, WUE, irrigation area, AWD (function that determines fraction of limits based on levels)
outputs: farm profit, profit variability, water levels (from which we compute environmental indices)
'''


original_rain = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/rain.data.csv'))[1:,1])
original_temperature = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/temperature.data.csv'))[1:,1])
original_swextraction = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/swextraction.data.csv'))[1:,1])
original_gwextraction = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/gwextraction.data.csv'))[1:,1])
original_dates = list(np.array(read_csv('/home/mikey/Dropbox/integrated/Model/hydrological/Maules_19690101_20100302/rain.data.csv'))[1:,0])

set_climate_data(dates=original_dates[:2000],
 rainfall=original_rain[:2000],
 temperature=original_temperature[:2000],
 swextraction=original_swextraction[:2000],
 gwextraction=original_gwextraction[:2000])


hydro_sim, hydro_tdat, hydro_mod = run_hydrology(0,422.7155/2) # RunIhacresGw.R takes about 17 seconds

gw_i = 3
original_gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
original_flow = np.array(hydro_sim.rx2('Q')).squeeze()
original_raw_C = np.array(hydro_sim.rx2('raw_C')).squeeze()
original_Qs = np.array(hydro_sim.rx2('Qs')).squeeze()
original_Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
original_Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
original_swE = np.array(hydro_sim.rx2('swE')).squeeze()
original_Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
original_Qr = hydro_sim.rx2('Qr').rx2('sw_419051')
original_gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
original_dates = list(hydro_tdat.rx2('dates'))
gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]


print "ORIGINAL"
print original_flow[500]
print original_Uq[500]
print original_Qq[500]
print original_Qs[500]
print original_Qd[500]
print original_swE[500]
# print original_Qr



climate_dates, rainfall, PET = read_climate_projections('../climate/419051.csv', scenario=1)
temperature = PET * 5
set_climate_data(dates=original_dates[500:1500],
			 rainfall=original_rain[500:1500],
			 temperature=original_temperature[500:1500],
			 swextraction=original_swextraction[500:1500],
			 gwextraction=original_gwextraction[500:1500])

hydro_sim, hydro_tdat, hydro_mod = run_hydrology(original_gwstorage[500], original_raw_C[500]) # RunIhacresGw.R takes about 17 seconds
print "ORIGINGAL C", original_raw_C[500]
gw_i = 3
gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,gw_i] # 3rd col varies most
flow = np.array(hydro_sim.rx2('Q')).squeeze()
Qs = np.array(hydro_sim.rx2('Qs')).squeeze()
Qq = np.array(hydro_sim.rx2('Qq')).squeeze()
Qd = np.array(hydro_sim.rx2('Qd')).squeeze()
swE = np.array(hydro_sim.rx2('swE')).squeeze()
Uq = np.array(hydro_sim.rx2('Uq')).squeeze()
gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]
dates = list(hydro_tdat.rx2('dates'))
gwfitparams = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[gw_i,:]

print "SLOW"
print flow[0]
print Uq[0]
print Qq[0]
print Qs[0]
print Qd[0]
print swE[0]




import matplotlib.pyplot as plt 
plt.plot([0 for i in range(500)]+gwstorage.tolist())
plt.plot(original_gwstorage[:1500], ls='--')
plt.show()

plt.plot([0 for i in range(500)]+flow.tolist())
plt.plot(original_flow[:1500], ls='--')
plt.show()