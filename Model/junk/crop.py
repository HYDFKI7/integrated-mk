"""

M. Asher
January 2015

Crop model based on 

@article{letcher2003application,
  title={Application of an adaptive method for integrated assessment of water allocation issues in the Namoi River Catchment, Australia},
  author={Letcher, RA and Jakeman, AJ},
  journal={Integrated Assessment},
  volume={4},
  number={2},
  pages={73--89},
  year={2003},
  publisher={Taylor \& Francis}
}

@article{letcher2004model,
  title={Model development for integrated assessment of water allocation options},
  author={Letcher, RA and Jakeman, AJ and Croke, BFW},
  journal={Water Resources Research},
  volume={40},
  number={5},
  year={2004},
  publisher={Wiley Online Library}
}

Maules Ck has 5 Land use options
1. Irrigated cotton/wheat rotation
2. Irrigated continuous cotton
3. Irrigated cotton/faba bean rotation
4. Dryland cotton/wheat rotation
5. Dryland sorghum/wheat rotation

Profit maximising farmer
* long term investments to change the area laid out to irrigation, on-farm storage capacity and/or irrigation efficiency
* annual production decisions (i.e., the crop rotations to plant each year)
* daily flow model



"""

# CropYield.txt

def soil_water(av_temp, rain, irrig_per_day):
	""" 
	@article{sheikh2009simple,
	  title={A simple model to predict soil moisture: Bridging Event and Continuous Hydrological (BEACH) modelling},
	  author={Sheikh, Vahedberdi and Visser, Saskia and Stroosnijder, Leo},
	  journal={Environmental Modelling \& Software},
	  volume={24},
	  number={4},
	  pages={542--556},
	  year={2009},
	  publisher={Elsevier}
	}

	"""

	return 0


"""
inputs
 SoilMoistParam is matrix of parameter values for the soil moisture component of the model read across crop, read down ocf1, ocf2, oll1, oll2, os1, os2, D1, D2, Kcb, Ksat
 ?????Check with Patrick - these all vary by crop, same structure for all crops?
  MinTemp is row of minimum daily temperature
  MaxTemp is row of maximum daily temperature
  Irrig is row of irrigation per day values
  CO2 is row matrix read across year, average daily value in ppm
 MonthDays is row of days in each month. Note don't account for leap years.
  Crops is matrix of regression coefficients for all crops, read across crop type, reas down paramaters by month (in same order as MonthDays), Evapotranspiration, S1, S2, AvTemp, C02 (single coeffiencient not dependent on month) 

"""




# JUNK	



def get_crop_yield(crop_option, water):

	# price_per_ton * ton_per_hectare (water)

	if crop_option == "Irrigated cotton/wheat rotation":
		crop_yield = 10 * 100 * water

	if crop_option == "Irrigated continuous cotton":
		crop_yield = 10 * 100 * water

	if crop_option == "Irrigated cotton/faba bean rotation":
		crop_yield = 10 * 100 * water

	if crop_option == "Dryland cotton/wheat rotation":
		crop_yield = 10 * 100 

	if crop_option == "Dryland sorghum/wheat rotation":
		crop_yield = 10 * 100 

	return crop_yield



