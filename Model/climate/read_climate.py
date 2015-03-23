import numpy as np
import csv


def read_climate_projections(file, scenario=1):
	dates = []
	rain= []
	PET = []
	with open(file) as csvfile:
		reader = csv.reader(csvfile)

		headers = map(str.strip, reader.next())
		date_i = headers.index('DATE')
		rain_i = headers.index('RAI_'+str(scenario))
		PET_i = headers.index('PET_'+str(scenario))

		for row in reader:
			dates.append(row[date_i])
			rain.append(float(row[rain_i]))
			PET.append(float(row[PET_i]))

	return dates, rain, np.array(PET)


if __name__ == '__main__':
	climate_dates, rainfall, pet = read_climate_projections('419051.csv', scenario=15)

	print pet[:20]
	print np.mean(pet), pet.shape
