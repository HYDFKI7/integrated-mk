
ReadAquiferParam <- function(filename, gwNetwork){
# Rachel Blakers 22/2/2012 v0.1
#
# Read the aquifer parameters (used in the IHACRES linear module)
#
# INPUT:
# filename ~ string, the path of the groundwater parameter file
# gwNetwork ~ data frame, the groundwater flow network specification. 
#
# OUTPUT:
# gwParam ~ data frame, the parameters for each aquifer
# gwFlowParam ~ named list, the groundwater flow parameters for each aquifer

	gwParamNames = c("taud", "sm", "nl", "offset", "scale", "G0", "rp", 
		"taur", "nc")
	gwFlowParamNames = c("delta", "scalef", "offsetf")

	param = ReadParamData(filename, gwNetwork, gwParamNames, gwFlowParamNames)
	gwParam = param$nodeParam
	gwFlowParam = param$routeParam

	ans = list(
		"gwParam" = gwParam, 
		"gwFlowParam" = gwFlowParam)
	return(ans)
}