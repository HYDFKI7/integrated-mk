
ReadSwInflowParam <- function(filename, network){
# Rachel Blakers 12/12/2012 v0.1
#
# Read routing parameters for upstream inflow
# TO DO: Add code to check that "gama" == 1
#
# INPUT:
# filename ~ string, the path of the parameter file
# network ~ data frame, the surface-groundwater flow network specification. 
#
# OUTPUT:
# swinflowParam ~ named list, parameters describing the upstream inflow routing
#
	
	catchmentParamNames = c() # No parameters
	routeParamNames = c("gama", "lambda", "alpha", "phi", "eta", "lag",
		"tloss")

	param = ReadParamData(filename, network, catchmentParamNames, 
		routeParamNames)
	swinflowParam = param$routeParam

	return(swinflowParam)
}