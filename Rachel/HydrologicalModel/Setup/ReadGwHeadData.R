
ReadGwHeadData <- function(path, gwConversion) { 
# Rachel Blakers v0-1 1/12/2013
#
#
# INPUT:
# 
#
# OUTPUT:
# 

	Gobs = ReadTimeseriesData(path)
	
	Gobs = lapply(gwConversion, function(x) Gobs[, x])
		
	# Check that timeseries data is regular i.e. there are no
	# missing dates
	regBool = sapply(Gobs, is.regular, strict = TRUE)
	if (!all(regBool)) {
		mssg = c("Input timeseries data is not regular.")
		stop(mssg)
	}
		
	return(Gobs)
}