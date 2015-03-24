
import numpy as np

from hydrological.RunIhacresGw import set_climate_data, run_hydrology

hydro_sim, hydro_tdat, hydro_mod = run_hydrology()

gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,3] # 3rd col varies most
flow = np.array(hydro_sim.rx2('Q')).squeeze()
gwstorage = np.array(hydro_sim.rx2('G')).squeeze()[:,0]

gw_fit_params = -np.array(hydro_mod.rx2('param').rx2('gwFitParam').rx2('gw_shallow'))[3,:]


for i in range(10):
	print gwlevel[i], gwstorage[i]*gw_fit_params[0] + gw_fit_params[1]