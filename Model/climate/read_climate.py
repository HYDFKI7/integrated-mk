import numpy as np
import csv
import datetime
import os

def read_original_data(file_name, data_col, with_dates=False):
	dates = []
	data = []
	with open(os.path.dirname(__file__) + '/'+'../hydrological/Maules_19690101_20100302/'+file_name) as csvfile:
		reader = csv.reader(csvfile)
		headers = map(str.strip, reader.next())
		date_i = headers.index('date')
		data_i = headers.index(data_col)
		for row in reader:
			if with_dates:
				dates.append(row[date_i])
			if row[data_i] == 'NA':
				data.append(np.nan)
			else:
				data.append(float(row[data_i]))

	if with_dates:
		return np.array(dates), np.array(data)
	else:
		return np.array(data)

# >>> from datetime import datetime
# >>> datetime.strptime("2012-may-31 19:00", "%Y-%b-%d %H:%M")
#  datetime.datetime(2012, 5, 31, 19, 0)

# This is an example of how to plot data once you have an array of datetimes:

# import matplotlib.pyplot as plt
# import datetime
# import numpy as np

# x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
# y = np.random.randint(100, size=x.shape)

# plt.plot(x,y)
# plt.show()


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

	print "------------------"
	for file_name in ['rain.data.csv', 'swextraction.data.csv','temperature.data.csv']:
		print read_original_data(file_name, "sw_419051", with_dates=True)
	print read_original_data('gwextraction.data.csv', "gw_shallow")
