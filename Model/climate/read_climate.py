import numpy as np
import csv
import datetime

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
			dt = datetime.datetime.strptime(row[date_i], '%d/%m/%Y') # .strftime('%Y-%m-%d'
			dates.append( "%d-%02d-%02d" % (dt.year,dt.month,dt.day) )
			rain.append(float(row[rain_i]))
			PET.append(float(row[PET_i]))

	return np.array(dates), np.array(rain), np.array(PET)


if __name__ == '__main__':
	climate_dates, rainfall, PET = read_climate_projections('419051.csv', scenario=15)

	print PET[:20]
	print np.mean(PET), len(PET)
