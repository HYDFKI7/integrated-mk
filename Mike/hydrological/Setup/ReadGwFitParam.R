
ReadGwFitParam <- function(path, gwConversion) { 
# Rachel Blakers v0-1 1/12/2013
#
#
# INPUT:
# 
#
# OUTPUT:
# 

	gwfitParam = read.csv(path, header = TRUE, row.names = 1,
		strip.white = TRUE, stringsAsFactors = FALSE)
	
	gwfitParam = lapply(gwConversion, function(x) gwfitParam[, x])

	return(gwfitParam)
}