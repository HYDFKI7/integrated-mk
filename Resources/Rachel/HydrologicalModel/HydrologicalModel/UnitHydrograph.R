
UnitHydrograph <- function(U, taux)
{
# Rachel Blakers 29/04/2014 v1.0
# 
# Calculate the instantaneous unit hydrograph given a time series of impulses
# (i.e. effective rainfall) and the time constant.
#
# INPUT:
# U ~ s*1 vector, the effective rainfall volume
# taux ~ scalar, the time constant 
#
# OUTPUT:
# s*1 vector, the response
#

	## Check inputs
	stopifnot(taux >= 0)
	
	## Calculate parameters
	alpha = -exp(-1/taux)
	
	## Get number of time steps
	s = length(U)

	## Allocate arrays to hold results
	Q = rep(NA, s) 

	## Calculate flow per time step
	Q_prev = 0
	alpha_U = (1 + alpha)*U
	for (k in 1:s) {
		Q[k] = (-alpha)*Q_prev + alpha_U[k]		
		Q_prev = Q[k]
	}

	ans = Q
	return(ans)
}