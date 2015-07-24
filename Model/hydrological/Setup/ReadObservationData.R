
ReadObservationData <- function(datadir) { 
# Rachel Blakers v0-1 1/12/2013
#
# Read the data for model calibration
#
# INPUT:
# datadir ~ string, path of directory containing the input files.
#
# OUTPUT:
# Named list containing the following elements:
# Gobs, Qobs 

	# print("Read groundwater monitoring site - model zone conversion.")
	path = file.path(datadir, "GwDepthModelZoneConversion.csv", 
		fsep = .Platform$file.sep)
	gwConversion = ReadGwConversionData(path)

	# print("Read observed groundwater head data.")
	## Inflow at the upstream boundary of the system
	path = file.path(datadir, "gwdepth.obs.csv", fsep = .Platform$file.sep)
	Gobs = ReadGwHeadData(path, gwConversion)
	
	# Observed streamflow
	# print("Read observed streamflow data.")
	path = file.path(datadir, "swflow.obs.csv", fsep = .Platform$file.sep)
	Qobs = ReadTimeseriesData(path)

		
	return(list("Gobs" = Gobs, "Qobs" = Qobs))
}