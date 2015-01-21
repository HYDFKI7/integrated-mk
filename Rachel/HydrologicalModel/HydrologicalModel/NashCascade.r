
NashCascade = function(U, tauf, m) {
	## Check inputs
	stopifnot(tauf >= 0)
	
	## Calculate parameters
	alpha = -exp(-1/tauf)
	
	## Get number of time steps
	s = length(U)

	## Allocate arrays to hold results
	Q = array(0, dim = c(s, m))

	## Calculate flow per time step
	Q_prev = rep(0, m)
	for (k in 1:s) {
		U_prev = U[k]
		for (j in 1:m) {
			Q[k, j] = (-alpha)*Q_prev[j] + (1 + alpha)*U_prev
			U_prev = Q[k, j]
		}
		Q_prev = Q[k, ]
	}

	return(Q[, m])
}