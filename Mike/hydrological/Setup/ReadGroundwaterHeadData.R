
ReadObservationData <- function(datadir) { 
# Rachel Blakers v0-2 20/03/2012
#
# Read the data for model calibration
#
# INPUT:
# datadir ~ string, path of directory containing the input files.
#
# OUTPUT:
# Named list containing the following elements:
# swNetwork ~ 

	print("Read observed groundwater head data.")
	## Inflow at the upstream boundary of the system
	path = file.path(datadir, "gwdepth.obs.csv", fsep = .Platform$file.sep)
	Gobs = ReadTimeseriesData(path)
	
		conversionPath = file.path(datadir, "GwDepthModelZoneConversion.csv", 
		fsep = .Platform$file.sep)
	gwConversion = read.csv(conversionPath, header = TRUE, row.names = 1,
		strip.white = TRUE, stringsAsFactors = FALSE)
	gwObs = as.list(rep(NA, nrow(gwConversion)))
	names(gwObs) = row.names(gwConversion)
	for (i in 1:nrow(gwConversion)) {
		selection = unlist(gwConversion[i, ])
		selection = selection[!is.na(selection)]
		gwObs[[i]] = gwData[, selection]	
	}
	
	# Observed streamflow
	print("Read observed streamflow data.")
	path = file.path(datadir, "swflow.obs.csv", fsep = .Platform$file.sep)
	Qobs = ReadTimeseriesData(path)

	outData = list("Qobs" = swNetwork, "Gobs" = gwNetwork)
		
	# Check that timeseries data is regular i.e. there are no
	# missing dates
	regBool = sapply(outData[c("swInflow", "swExtraction", 
		"gwExtraction", "P", "T")], is.regular, strict = TRUE)
	if (!all(regBool)) {
		mssg = c("Input timeseries data is not regular.")
		stop(mssg)
	}
		
	return(outData)

}