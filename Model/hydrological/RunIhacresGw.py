"""
Python wrapper for Rachel Blaker's IhacresGW hydrological model of Maules Creek

Michael Asher michael.james.asher@gmail.com
February 2015
"""

from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
import os
import pandas

def run_hydrology(x):

	r_path = os.path.join(os.path.dirname(__file__), 'WrappableRunIhacresGw.R')
	with open(r_path) as r_file:

		# r_file = open('WrappableRunIhacresGw.R')


		"""
		inline editing of csv input files
		"""
		
		data_path = os.path.join(os.path.dirname(__file__), 'data/swextraction.data.csv')
		swextraction = pandas.read_csv(data_path, index_col='date')
		swextraction['sw_419051'][2] = 0.2
		swextraction['sw_419051']['2010-02-23'] = 0.2

		swextraction.to_csv(data_path)


		# shutil.move(tempfile.name, filename)


		"""
		import .R file and call function
		"""
		string = r_file.read()
		IhacresGW = SignatureTranslatedAnonymousPackage(string, "IhacresGW")
		workingdir = os.path.dirname(__file__)
		# workingdir = "~/Dropbox/integrated/Mike/hydrological"
		# datadir = workingdir + "/Maules_19690101_20100302"

		datadir = workingdir + "/data"
		# sim, tdat = IhacresGW.RunIhacresGw(workingdir, datadir)
		return IhacresGW.RunIhacresGw(workingdir, datadir)

		# return sim, tdat
		# return  sim.rx2('Q')[100]



"""
inline editing of csv input files
"""
def set_climate_data(rainfall, temperature):
	print "nothing done"

# from tempfile import NamedTemporaryFile
# import shutil
# import csv

# filename = 'data/swextraction.data.csv'
# tempfile = NamedTemporaryFile(delete=False)

# with open(filename, 'rb') as csvFile, tempfile:
#     reader = csv.reader(csvFile, delimiter=',', quotechar='"')
#     writer = csv.writer(tempfile, delimiter=',', quotechar='"')

#     for row in reader:
#         row[1] = row[1]
#         writer.writerow(row)