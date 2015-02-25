
import numpy as np

"""
* get farmer to use constraints from hydrology
* update hydrology with results from farmer 
"""


"""
run hydrological model 
"""
from hydrological.RunIhacresGw import run_hydrology
hydro_sim, hydro_tdat = run_hydrology(None) # RunIhacresGw.R takes about 17 seconds

gwlevel = -np.array(hydro_sim.rx2('Glevel').rx2('gw_shallow'))[:,3] # 3rd col varies most
flow = np.array(hydro_sim.rx2('Q')).squeeze()
dates = hydro_tdat.rx2('dates')


"""
run farmer decision 
"""
from farm_decision.farm_optimize import crops, scipy_linprog_find_optimal_crops
farm_area = 1300
water_licence = 800
res_linprog = scipy_linprog_find_optimal_crops(crops, farm_area, water_licence)


"""
run ecological model 
"""
from ecological.ecological_indices import calculate_water_index
water_index = calculate_water_index(gwlevel, flow, dates)



"""

@article{fu2014assessing,
  title={Assessing certainty and uncertainty in riparian habitat suitability models by identifying parameters with extreme outputs},
  author={Fu, Baihua and Guillaume, Joseph HA},
  journal={Environmental Modelling \& Software},
  volume={60},
  pages={277--289},
  year={2014},
  publisher={Elsevier}
}

@article{fu2013water,
  title={A water suitability model for riparian vegetation in the Namoi catchment: Final Report},
  author={Fu, Baihua },
  year={2013},
  publisher={National Centre for Groundwater Research and Training}
}


"""
