
GetIhacresInputs = function(datadir, skipObs = FALSE) {
# Rachel Blakers 29/04/2014 v0.1
#
# Read model input data, parameters and calibration data. 	
# 
# Input:
# datadir ~ string, path of directory containing model inputs
# skipObs ~ boolean, if true, don't read observation data
#
# Output:
# Model data 
#

	if (!skipObs) {
		cat("Read observation data.\n")
		# Observed groundwater depth
		obs = ReadObservationData(datadir)
	} else {
		obs = list()
	}

	cat("Read IHACRES_GW input data.\n")
	# Parameters, rainfall temperature and extraction data
	input = ReadInputData(datadir)
	tdat = input$tdat
	param = input$param
	
	# Store original input time series in observation data
	obs = c(tdat, obs)
	
	cat("Strip dates from model input time series.\n")
	# Get list of dates in time series
	timeseq = time(tdat$P)
	tdat$tseq = timeseq
	tdat$swInflow = data.matrix(tdat$swInflow)
	tdat$P = data.matrix(tdat$P)
	tdat$T = data.matrix(tdat$T)
	tdat$gwExtraction = data.matrix(tdat$gwExtraction)
	tdat$swExtraction = data.matrix(tdat$swExtraction)
	
	return(list("obs" = obs, "tdat" = tdat, "param" = param))
}