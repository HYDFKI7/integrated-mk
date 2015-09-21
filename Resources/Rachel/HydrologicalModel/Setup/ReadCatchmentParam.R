
ReadCatchmentParam <- function(filename, network){
# Rachel Blakers 22/2/2012 v0.1
#
# Read non-linear and linear (quickflow only) IHACRES model parameters and 
# routing parameters.
#
# INPUT:
# path ~ string, the path of the parameter file
# network ~ data frame, the flow network specification. 
#
# OUTPUT:
# swParam ~ data frame, the IHACRES non-linear module parameters and 
#		linear module parameters (for quickflow only). 
# swFlowParam ~ named list, the flow routing parameters for each catchment.
#
	
	# Parameter names in IHACRES model and routing module
	ihacresParamNames = c("d", "e", "f", "vd", "vq", "rho", "tauq", "taus", 
		"area", "Qq0", "Qs0")
	routeParamNames = c("gama", "lambda", "alpha", "phi", "eta", "lag", "tloss")
	
	# Read parameter values
	param = ReadParamData(filename, network, ihacresParamNames, 
		routeParamNames)
	swParam = param$nodeParam
	swFlowParam = param$routeParam
	
	# Check that the sum of gamma for each of the downstream catchments = 1.
	# ('gamma' is the proportion of flow directed down each river reach)
	n = nrow(network)
	for (i in 1:n) {
		# Get number of downstream nodes
		nds = network[[i, "nds"]]
		if (nds > 0) {
			total = sum(abs(swFlowParam[[i]]$gama))
			if (abs(total - 1) > 1e-10) {
				cat(paste("	WARNING: Catchment", row.names(network)[[i]], 
					": flow routing fraction 'gamma' does not sum to 1.\n\n"))
			}
		}
	}
	
	ans = list(
		"swParam" = swParam, 
		"swFlowParam" = swFlowParam)
	return(ans)
}