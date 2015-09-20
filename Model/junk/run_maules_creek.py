

# inputs
# * groundwater level
# * preceding dry period, date, duration of flood events (above threashold)



def run(x):
	print "x", x

	# cease-to-flow days (annual)
	# yearly number of days above CTF levels
	# median/total flow/baseflow levels (annual)
	# number of overflow events (flow above a threshold)
	# 	By default, the minimum number of days that can separate events is 5 days,
	#	and the minimum number of days in each event window is 1 day.

################################
###  Hydrological indicators  ###
################################

## Function to calculate cease-to-flow days (annual).
## Function to calculate median/total flow/baseflow levels (annual), if total, fun=sum.
## Function to calculate yearly number of days above CTF levels. Input (x) is surfaceflow.
## Function to calculate annual averaged number of overflow (flow above a threshold) events. Input (x) is surfaceflow
## By default, the minimum number of days that can separate events is 5 days,
## and the minimum number of days in each event window is 1 day.

################################
###  Ecological indicators  ####
################################
## Function to generate index curve for flood timing.
## Function to generate index curve for flood duration.
## Function to generate index curve for interflood dry period.
## Function to calculate weighted index.
## Function to generate event summary.
## Function to generate yearly index from daily sw+gw index data.
##  Function to calculate groundwater level index, inputs and outputs are daily data
##  Function to calculate groundwater salinity index
## Function to combine surface water (event-based) and groundwater indices (daily), using weighted average.
