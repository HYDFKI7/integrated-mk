import numpy as np
import csv
import datetime
import os

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def read_bom_data(file_name, data_col):
	dates = []
	data = []
	with open(os.path.dirname(__file__) + '/' +file_name) as csvfile:
		reader = csv.reader(csvfile)
		headers = map(str.strip, reader.next())

		Year_i = headers.index('Year')
		Month_i = headers.index('Month')
		Day_i = headers.index('Day')
		data_i = headers.index(data_col)

		previous = None

		for row in reader:

			if (row[data_i] == ""):
				# skip initial empty rows
				if previous == None: 
					continue
				# fill blanks with previous value
				else:
					dates.append( "%d-%02d-%02d" % (int(row[Year_i]),int(row[Month_i]),int(row[Day_i])) )
					data.append(previous)				
			else:
				dates.append( "%d-%02d-%02d" % (int(row[Year_i]),int(row[Month_i]),int(row[Day_i])) )
				previous = float(row[data_i])
				data.append(previous)

	return np.array(dates), np.array(data)

def cut(dates, data, start, end):
	start_i = np.where( dates == start)[0]
	end_i = np.where( dates == end)[0]
	return dates[start_i: end_i+1], data[start_i: end_i+1]

def read_all_bom_data():
	max_temp_dates, max_temp = read_bom_data("IDCJAC0010_055023_1800/IDCJAC0010_055023_1800_Data.csv", "Maximum temperature (Degree C)")
	min_temp_dates, min_temp = read_bom_data("IDCJAC0011_055023_1800/IDCJAC0011_055023_1800_Data.csv", "Minimum temperature (Degree C)")
	rain_dates, rain = read_bom_data("IDCJAC0009_055076_1800/IDCJAC0009_055076_1800_Data.csv", "Rainfall amount (millimetres)")

	start = '1899-01-01'
	end = '2011-12-27'

	rain_dates, rain = cut(rain_dates, rain, start, end)
	max_temp_dates, max_temp = cut(max_temp_dates, max_temp, start, end)
	min_temp_dates, min_temp = cut(min_temp_dates, min_temp, start, end)

	temp = (min_temp  + max_temp)/2

	return (rain_dates, rain, temp)


def read_NSW_csv(file_name, skip=1):
	with open(file_name) as csvfile:
		reader = csv.reader(csvfile)
		headers = [reader.next() for i in range(skip)]
		rows = [row for row in reader]
		return rows, headers

def read_NSW_data():
	dirname = os.path.dirname(__file__)+'/'
	# 4 row header
	# Discharge (ML/d) Mean in column 1
	# 08:00:00 16/07/1975
	# 08:00:00 23/04/2015
	rows, headers = read_NSW_csv(dirname+"SW419051.csv", 4)
	rows = [row for row in rows if len(row)>1 and not row[1] == '']
	sw_dates = np.array([datetime.datetime.strptime(row[0], "%H:%M:%S %d/%m/%Y") for row in rows])
	sw = np.array([np.float(row[1]) for row in rows])
	# 4 row header
	# Bore level below MP Point in column 1
	# 00:00:00 22/04/2005
	# 00:00:00 20/05/2015
	rows, headers = read_NSW_csv(dirname+"GW036186.csv", 4)
	rows = [row for row in rows if len(row)>1 and not row[1] == '']
	gw_dates = np.array([datetime.datetime.strptime(row[0], "%H:%M:%S %d/%m/%Y") for row in rows])
	gw = np.array([np.float(row[1]) for row in rows])
	return sw_dates, sw, gw_dates, gw


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


def find_extremes(data, window):
	ma = moving_average(data, window)
	min_i = np.argmin(ma) 
	med_i = np.argmin(np.abs(ma-np.median(ma))) 
	max_i = np.argmax(ma) 
	return min_i, med_i, max_i


def dateifier(date_string):
	return datetime.datetime.strptime(date_string, "%Y-%m-%d")

if __name__ == '__main__':
	climate_dates, rainfall, PET = read_climate_projections('419051.csv', scenario=15)

	print PET[:20]
	print np.mean(PET), len(PET)

	print "------------------"
	for file_name in ['rain.data.csv', 'swextraction.data.csv','temperature.data.csv']:
		print read_original_data(file_name, "sw_419051", with_dates=True)
	print read_original_data('gwextraction.data.csv', "gw_shallow")

	print "------------------"


	rain_dates, rain, temp = read_all_bom_data()


	window = 365*20+5
	ma = moving_average(rain, window)
	assert len(ma)+window-1 == len(rain)
	assert np.mean(rain[:window]) == ma[0]

	import matplotlib.pylab as plt
	# plt.plot(ma)
	plt.plot(map(dateifier, rain_dates), rain)
	plt.show()


	min_i, med_i, max_i = find_extremes(rain, window)

	print "extremes", rain_dates[min_i], rain_dates[med_i], rain_dates[max_i] 


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
