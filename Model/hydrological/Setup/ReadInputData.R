
ReadInputData <- function(datadir) { 
# Rachel Blakers v0-2 20/03/2012
#
# Read the IHACRES input files
#
# INPUT:
# datadir ~ string, path of directory containing the input files.
#
# OUTPUT:
# Named list containing the following elements:
# swNetwork ~ data frame, the surface water flow network specification. 
#		Row names: catchment names
#		Column names: nds (number of downstream catchments), 
#		ds1 (name of first downstream catchment), 
# 		ds2 (name of second downstream catchment), etc.
#		For example:
#		       	 nds    ds1    	 ds2
#		419039   2 		419065 419021
# 		419065   1 		419049   <NA>
# 		419021   0 		<NA>     <NA>
# gwNetwork ~ data frame, the groundwater flow network specification. 
#		Row names: aquifer names
#		Column names: nds (number of downstream aquifers), 
#		ds1 (name of first downstream aquifer), 
# 		ds2 (name of second downstream aquifer), etc.
#		For example:
#		    nds	ds1	ds2
#		aq1	1	aq2 <NA>
#		aq2	2	aq3 aq4
# sgwNetwork ~ data frame, surface groundwater connectivity network. 
#		Row names: catchment names
#		Column names: nds (number of downstream aquifers), 
#		ds1 (name of first downstream aquifers), 
# 		ds2 (name of second downstream aquifers), etc.
# swInflow ~ timeseries object, the inflow data for the catchment at the 
#		head of the flow network.
# swExtraction ~ timeseries object, surface water extraction data.
# 		For example:
#				   419021 419026
#		1880-01-01    5.0   10.0
#		1880-01-02    6.0   10.0
#		1880-01-03    7.0   10.0
#		etc...
# gwExtraction ~ timeseries object, groundwater water extraction data.
# P ~ timeseries object, precipitation data.
#		For example:
#				      gw1    gw2
#		1880-01-01    0.0    0.0
#		1880-01-02    0.9    0.1
#		1880-01-03    1.5    2.0
#		etc...
# T ~ timeseries object, temperature data.
# swParam ~ data frame, the IHACRES non-linear module parameters and 
#		linear module parameters (for quickflow only). 
#		Row names: the catchment names
#		Column names: the paramter names
#		For example:
#		         d	e		f  		vs 	tauq   	im 		area
# 		419039 200 	0.166 	0.65 	0.1 1.4 	0.44 	3100
# 		419065 200 	0.166 	0.65 	0.1 1.4 	0.44 	1000
# swFlowParam ~ named list, the routing parameters for each catchment.
#		Names: the catchment names
#		Values: data frame of the form:
#		       						gamma lambda alpha  phi		eta
# 		DownstreamCatchmentName     1     0  	 0.05 	0.83   	0
# gwParam ~ data frame, the parameters for each aquifer
#		Row names: the aquifer names
#		Column names: the aquifer parameter names
#		For example:
# 			taus  nl
# 		gw1 30    0.1
# 		gw2 30    0.1
# 		gw3 30    0.1
# 		..etc
# gwFlowParam ~ named list, the groundwater flow parameters for each 
#		aquifer (not currently used).
# sgwParam ~ named list, the surface - groundwater interaction parameters.
#		Names: the catchment names
#		Values: data frame of the form:
#		           f  g0
#		Aquifer1 0.8 0.0
#		Aquifer2 0.2 1.0
#		..etc

	# print("Read network data: surface water flow")
	path = file.path(datadir, "sw.network.csv", fsep = .Platform$file.sep)
	swNetwork = ReadNetworkData(path)
	if (ncol(swNetwork) > 3) {
		mssg = c("Each catchment in the surface water flow network, ",
			"specified in the sw.network file, can have a most two ", 
			"downstream catchments.")
		stop(mssg)
	}

	# print("Read network data: upstream inflow")
	path = file.path(datadir, "swinflow.network.csv", fsep = .Platform$file.sep)
	swInflowNetwork = ReadNetworkData(path)
	if (ncol(swInflowNetwork) > 2) {
		mssg = c("Each upstream catchment specified in the ",
			"swinflow.network file, can have a most one ", 
			"downstream catchment.")
		stop(mssg)
	}
	
	# print("Read network data: groundwater flow.")
	path = file.path(datadir, "gw.network.csv", fsep = .Platform$file.sep)
	gwNetwork = ReadNetworkData(path)
	
	# print("Read network data: surface-groundwater connectivity.")
	path = file.path(datadir, "sgw.network.csv", fsep = .Platform$file.sep)
	sgwNetwork = ReadNetworkData(path)
	# Error checking
	if (any(row.names(swNetwork) != row.names(sgwNetwork))) {
		mssg = c("The order of catchments in the sw.network file ", 
			"and the sgw.network file differ.")
		stop(mssg)
	}

	# print("Read upstream inflow data.")
	## Inflow at the upstream boundary of the system
	path = file.path(datadir, "swinflow.data.csv", fsep = .Platform$file.sep)   
	swInflow = ReadTimeseriesData(path)
	
	# print("Read surface water extraction data.")
	path = file.path(datadir, "swextraction.data.csv", fsep = .Platform$file.sep)
	swExtraction = ReadTimeseriesData(path)
	# Error checking
	if (any(row.names(swNetwork) != names(swExtraction))) {
		mssg = c("The order of catchments in the sw.network.csv file ", 
			"and the swextraction.data.csv file differ.")
		stop(mssg)
	}
	
	# print("Read groundwater extraction data.")
	path = file.path(datadir, "gwextraction.data.csv", 
		fsep = .Platform$file.sep)   
	gwExtraction = ReadTimeseriesData(path)
	if (any(row.names(gwNetwork) != names(gwExtraction))) {
		mssg = c("The order of catchments in the gw.network.csv file ", 
			"and the gwextraction.data.csv file differ.")
		stop(mssg)
	}
	# print("Read rainfall data.")
	path = file.path(datadir, "rain.data.csv", fsep = .Platform$file.sep)
	P = ReadTimeseriesData(path)
	# Error checking
	if (any(row.names(swNetwork) != names(P))) {
		mssg = c("The order of catchments in the sw.network.csv file ", 
			"and the rain.data.csv file differ.")
		stop(mssg)
	}
	
	# print("Read temperature data.")
	path = file.path(datadir, "temperature.data.csv", fsep = .Platform$file.sep)
	T = ReadTimeseriesData(path)
	# Error checking
	if (any(row.names(swNetwork) != names(T))) {
		mssg = c("The order of catchments in the sw.network.csv file ", 
			"and the temperature.data.csv file differ.")
		stop(mssg)
	}
	
	# cat("Read catchment parameters.\n")
	path = file.path(datadir, "sw.param.csv", fsep = .Platform$file.sep)
	param = ReadCatchmentParam(path, swNetwork)
	swParam = param$swParam
	swFlowParam = param$swFlowParam
	if (any(row.names(swNetwork) != row.names(swParam))) {
		mssg = c("The order of catchments in the sw.network.csv file ", 
			"and the sw.param.csv file differ.")
		stop(mssg)
	}
	
	# cat("Read upstream inflow parameters.\n")
	path = file.path(datadir, "swinflow.param.csv", fsep = .Platform$file.sep)
	swInflowParam = ReadSwInflowParam(path, swInflowNetwork)
	if (any(row.names(swInflowNetwork) != row.names(swInflowParam))) {
		mssg = c("The order of catchments in the swinflow.network.csv file ", 
			"and the swinflow.param.csv file differ.")
		stop(mssg)
	}

	# cat("Read aquifer parameters.\n")
	path = file.path(datadir, "gw.param.csv", fsep = .Platform$file.sep)
	param = ReadAquiferParam(path, gwNetwork)
	gwParam = param$gwParam
	gwFlowParam = param$gwFlowParam
	if (any(row.names(gwNetwork) != row.names(gwParam))) {
		mssg = c("The order of aquifers in the gw.network.csv file ", 
			"and the gw.param.csv file differ.")
		stop(mssg)
	}
	
	# cat("Read surface-groundwater connectivity parameters.\n")
	path = file.path(datadir, "sgw.param.csv", fsep = .Platform$file.sep)
	sgwParam = ReadSgwParam(path, sgwNetwork)
	if (any(row.names(sgwParam) != row.names(swNetwork))) {
		mssg = c("The order of catchments in the sgw.param.csv file ", 
			"and the sw.param.csv file differ.")
		stop(mssg)
	}
	
	# print("Read groundwater monitoring site - model zone conversion.")
	path = file.path(datadir, "GwDepthModelZoneConversion.csv", 
		fsep = .Platform$file.sep)
	gwConversion = ReadGwConversionData(path)

	# cat("Read gw fit data.\n")
	## Inflow at the upstream boundary of the system
	path = file.path(datadir, "gwfit.param.csv", fsep = .Platform$file.sep)
	gwFitParam = ReadGwFitParam(path, gwConversion)
	
	tdat = list("P" = P, "T" = T, "swInflow" = swInflow, 
		"gwExtraction" = gwExtraction, "swExtraction" = swExtraction)	
	param = list("swNetwork" = swNetwork, 
		"gwNetwork" = gwNetwork, 
		"sgwNetwork" = sgwNetwork, 
		"swInflowNetwork" = swInflowNetwork, 
		"swParam" = swParam, 
		"gwParam" = gwParam, 
		"sgwParam" = sgwParam,
		"swFlowParam" = swFlowParam,
		"swInflowParam" = swInflowParam,
		"gwFlowParam" = gwFlowParam,
		"gwFitParam" = gwFitParam)	
			
	# Check that timeseries data is regular i.e. there are no
	# missing dates
	regBool = sapply(tdat, is.regular, strict = TRUE)
	if (!all(regBool)) {
		mssg = c("Input timeseries data is not regular.")
		stop(mssg)
	}
	
	return(list("tdat" = tdat, "param" = param))

}