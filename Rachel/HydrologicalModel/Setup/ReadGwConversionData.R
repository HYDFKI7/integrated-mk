
ReadGwConversionData <- function(path) { 
# Rachel Blakers v0-1 1/12/2013
#
#
# INPUT:
#
# OUTPUT:

	gwConversion = read.csv(path, header = TRUE, row.names = 1,
		strip.white = TRUE, stringsAsFactors = FALSE)
	# Convert to list
	gwConversion = unlist(apply(gwConversion, 1, list), recursive = FALSE)
	# Remove NA elements
	gwConversion = lapply(gwConversion, function (x) x[!is.na(x)])
		
	return(gwConversion)

}