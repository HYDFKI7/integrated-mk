

# CropYield

# inputs: maxtemp, mintemp, rainfall
# output: yield

def get_crop_yield(
					crop_coefficients, 
					soil_moisture
					evapotranspiration,
					temperature,
					):
	return crop_coefficients*evapotranspiration...




soil_moisture = get_soil_moisture()

crop_yield = get_crop_yield(
							crop_coefficients, 
							soil_moisture
							evapotranspiration,
							temperature,
							)






# GWSWResponse

# inputs : drainage_shp, gwextractions, inflow1, inflow2, inflow3, noupstream, routeparam, swaquifer, swcatch, sw extraction, aquifers
# output: gwstorage, otherin, totalflow, totalunregflow, unregin