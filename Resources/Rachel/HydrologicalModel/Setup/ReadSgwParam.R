
ReadSgwParam <- function(filename, network){
# Rachel Blakers 22/2/2012 v0.1
#
# Read non-linear and linear (quickflow only) IHACRES model parameters and 
# routing parameters.
#
# INPUT:
# filename ~ string, the path of the parameter file
# network ~ data frame, the surface-groundwater flow network specification. 
#
# OUTPUT:
# sgwParam ~ named list, parameters describing the surface-groundwater flow 
#	routing.
#

	sgwParamNames = c() # No parameters
	sgwFlowParamNames = c("r", "gs", "rho_na")

	param = ReadParamData(filename, network, sgwParamNames, sgwFlowParamNames)
	sgwParam = param$routeParam

	return(sgwParam)
}