
NashCascade = function(U, tauf, m, init_Q) {
	## Check inputs
	stopifnot(tauf >= 0)
	
	## Calculate parameters
	alpha = -exp(-1/tauf)
	
	## Get number of time steps
	s = length(U)

	## Allocate arrays to hold results
	Q = array(0, dim = c(s, m))

	## Calculate flow per time step
	# Q_prev = rep(0, m)
	all_Q_prev = array(0, dim = c(s, m))
	Q_prev = init_Q
	for (k in 1:s) {
		U_prev = U[k]
		for (j in 1:m) {
			Q[k, j] = (-alpha)*Q_prev[j] + (1 + alpha)*U_prev
			U_prev = Q[k, j]
		}
		Q_prev = Q[k, ]
		all_Q_prev[k, ] = Q_prev
	}
	# return(Q[, m])
	out = list("Q" = Q[, m], "Q_prev" = all_Q_prev)
	return(out)
}