
FlowPartitioning <- function(swParam, U)
{
# Rachel Blakers 19/11/2013 v2.0
#
# Calculate the volume of effective rainfall partitioned to quickflow (surface
# runoff) and slowflow (shallow sub-surface flow).
#
# Input:
# swParam ~ data frame, the IHACRES parameters for the current catchment
# U ~ s*1 vector, effective rainfall for the current catchment.
# (s = number of time steps)
# 
# Output:
# Named list containing:
# Uq ~ s*1 vector, effective rainfall partitioned to quickflow for the current 
#		catchment
# Us ~ s*1 vector, effective rainfall partitioned to slowflow for the current 
#		catchment
#

	# Surface runoff fraction
	vq = swParam[, VQ]
	# Shallow subsurface flow fraction
	vs = 1 - vq
	# Check inputs
	stopifnot(vs >= 0 && vs <= 1)
	stopifnot(vq >= 0 && vq <= 1)
	stopifnot((vq + vs) == 1)

	# Quickflow volume
	Uq = U*vq
	# Shallow groundwater volume
	Us = U*vs

	ans = list("Uq" = Uq, "Us" = Us)
	return(ans)
}

