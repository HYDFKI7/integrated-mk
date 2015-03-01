
ReadTimeseriesData <- function(path){
# Rachel Blakers v0.1 20/03/2011
#
# Read timeseries data.
# First column assumed to contain dates.
	
	# Read input data from file
	input = read.table(path, header = TRUE, sep = ",", check.names = FALSE,
		stringsAsFactors = FALSE)

	# Convert to a zoo timeseries object
	if (ncol(input) == 2) {
		# If the data only has one column, force it to be an n*1 array,
		# rather than a row vector.
		value = array(input[, 2], dim = c(nrow(input), 1))
		tsdata = zoo(value, as.Date(input[, 1], format = "%Y-%m-%d"))
		names(tsdata) = names(input[2])
	} else {
		tsdata = zoo(input[, 2:ncol(input)], as.Date(input[, 1], 
			format = "%Y-%m-%d"))
	}	
	
	# Check that timeseries data is regular i.e. there are no
	# missing dates
	if (!all(is.regular(tsdata, strict = TRUE))) {
		mssg = paste("Timeseries data is not regular in file:", path)
		stop(mssg)
	}
	
	return(tsdata)
}