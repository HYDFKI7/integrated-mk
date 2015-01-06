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


@article{letcher2004model,
  title={Model development for integrated assessment of water allocation options},
  author={Letcher, RA and Jakeman, AJ and Croke, BFW},
  journal={Water Resources Research},
  volume={40},
  number={5},
  year={2004},
  publisher={Wiley Online Library}
}



"""




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



