
ReadNetworkData <- function(filename) { 
# Rachel Blakers 20/03/2012 v0.3
#
# Read a generic flow network data file.
# 
# Input: 
# filename ~ string, path of network data file
#
# Output:
# network ~ n*3 data frame, flow network data.  
#		Row names = node IDs
#		Column names = 
#		"nds" ~ Number of downstream nodes
# 		"ds1" ~ Name of first downstream node
#		"ds2" ~ Name of second downstream node
#		..etc
# 		'NA' denotes no downstream node.
#

	# Read the flow network data
	networkData = read.csv(filename, header = FALSE, 
		colClasses = "character", strip.white = TRUE, na.strings = "NA")
	# Convert column containing downstream node count to numeric
	networkData[, 2] = as.numeric(networkData[, 2])

	# Get upstream node names
	nodeId = networkData[, 1]
	# Check that node names are unique
	stopifnot(length(nodeId) == length(unique(nodeId)))
	
	# Create column names
	maxds = ncol(networkData)
	cols = c("nds", paste("ds", as.character(1:(maxds - 2)), sep = ""))

	# Create data structure
	network = data.frame(
		networkData[, 2:maxds],
		row.names = nodeId,
		stringsAsFactors = FALSE
		)
	names(network) = cols
	
	return(network)
}