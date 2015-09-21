
ReadParamData <- function(filename, network, nodeParamNames, 
	routeParamNames){
# Rachel Blakers 22/2/2012 v0.1
#
# Read a generic parameter data file
#
# INPUT:
# filename ~ string, the path of the parameter file
# network ~ data frame, the flow network specification. 
# nodeParamNames ~ list of aquifer or catchment parameter names
# routeParamNames ~ list of aquifer or catchment flow routing parameter names
#
# OUTPUT:
# nodeParam ~ data frame, the node (aquifer or catchment) parameters. 
# routeParam ~ named list, the routing parameters].

	# Read parameter data file
	paramData = read.csv(filename, header = TRUE, colClasses = "character", 
		check.names = FALSE, strip.white = TRUE)
		
	# Number of nodes
	n = nrow(network)
	# Number of node parameters
	nNode = length(nodeParamNames)
	# Get number of routing parameters
	nRoute = length(routeParamNames) 
	
	# Get names of downstream nodes
	position = seq(nNode + 1, nrow(paramData), nRoute + 1)
	dsNodeNames = data.frame(
		paramData[position, 1:n],
		stringsAsFactors = FALSE
		)
	names(dsNodeNames) = names(paramData)[1:n]
	# Drop these rows from the parameter data 
	paramData = paramData[-position, ]

	# Convert parameter values to numeric
	if (n == 1) {
		paramData[, 1] = as.numeric(paramData[, 1])
	} else {
		paramData[, 1:n] = apply(paramData[, 1:n], 2, as.numeric)
	}
	
	if (nNode == 0) {
		# There are no node parameters
		nodeParam = NA
	} else {
		# Extract node parameters and place in a data structure
		nodeParam = data.frame(
			t(paramData[1:nNode, 1:n]),
			row.names = names(paramData)[1:n],
			check.names = FALSE
			)
		names(nodeParam) = nodeParamNames
		# Reorder rows so that they are in the same order as in the network
		nodeParam <- nodeParam[rownames(network),,drop=FALSE]
	}
	
	routeParam = as.list(rep(NA, n))
	names(routeParam) = row.names(network)
	for (i in 1:n) {
		# Get number of downstream nodes
		nds = network[[i, "nds"]]
		if (nds > 0) {
	
			# Check that downstream node names are as expected from the 
			# network data
			# Note: the columns of paramData and the rows of routeParam may
			# not be in the same order, so the required column of paramData
			# is indexed by name.
			node = names(routeParam)[[i]]
			expectedNames = network[i, 2:(nds + 1)]
			actualNames = dsNodeNames[1:nds, node]
			if (!all(expectedNames == actualNames)) {
				print(network)
				mssg = c("The downstream node names in a parameter file ", 
					"and the corresponding network file differ.")
				stop(mssg)
			}
		
			# Create data structure
			routeParam[[i]] = data.frame(
				array(NA, dim = c(nds, nRoute)), 
				row.names = network[i, 2:(nds + 1)]
			)
			names(routeParam[[i]]) = routeParamNames
			
			# Extract routing parameters
			count = nNode
			for (j in 1:nds) {
				routeParam[[i]][j, ] = paramData[(count+1):(count+nRoute), node]
				count = count + nRoute
			}
		}
	}
	
	ans = list(
		"nodeParam" = nodeParam, 
		"routeParam" = routeParam
		)
	return(ans)
}