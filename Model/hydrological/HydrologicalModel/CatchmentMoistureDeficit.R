
CatchmentMoistureDeficit <- function(P, T, swParam, init_C, b = 0, climate_type = 'temperature') {
# Rachel Blakers 22/2/2012 v0.1
#
# Convert rainfall to effective rainfall via a catchment moisture 
# deficit (CMD) accounting scheme.
#
# INPUT:
# P ~ rainfall data
# T ~ temperature data
# swParam ~ data frame, the IHACRES non-linear module parameters and 
#		linear module parameters (for quickflow only) for the current catchment. 
#		For example:
#		         d	e		f  		vs 	tauq   	im 		area
# 		419039 200 	0.166 	0.65 	0.1 1.4 	0.44 	3100
# b ~ drainage equation shape parameter.
# 	   0 = Exponential drainage function (currently only exponential drainage 
#		is implemented)
# 
# OUTPUT:
# Named list containing:
# U ~ 1*s vector, effective rainfall timeseries
# C ~ 1*s vector, catchment moisture deficit timeseries
# E ~ 1*s vector, evapotranspiration timeseries
# (s = number of time steps)
#

	f = swParam[, FC]
	e = swParam[, EC]
	d = swParam[, DC]
	## Check parameter ranges
    stopifnot(f >= 0)
    stopifnot(e >= 0)
    stopifnot(d >= 0)
	stopifnot(b == 0)

	# C_prev = d/2 ## Initial catchment moisture deficit at time t0
	C_prev = init_C ## Initial catchment moisture deficit at time t0
	g = f*d
	g2 = 2/g
	# Number of time steps
	s = length(P)

	## Allocate arrays to hold results
	U = rep(NA, s)  ## Effective rainfall
	E = rep(NA, s)  ## Evapotranspiration
	C = rep(NA, s)  ## Catchment moisture deficit
	for (k in 1:s) {
		# If rainfall is greater than 0, calculate CMD in the absence of 
		# evapotranspiration. Otherwise, leave CMD unchanged.
		if (P[k] > 0) {
			if (b == 0) {
				## Exponential form of the drainage equation
				Cf = ExponentialDrainage(C_prev, d, P[k])
			}
		} else {
			Cf = C_prev
		}

		if (climate_type == 'temperature') {
			# If temperature is greater than 0, calculate evapotranspiration and 
			# adjust CMD accordingly.
			# Otherwise, set evapotranspiration to 0 and leave CMD unchanged.
			if (T[k] <= 0) {
				E[k] = 0
				C[k] = Cf
			} else {
				if (Cf > g) {
					E[k] = e*T[k]*exp((1 - Cf/g)*2)
				} else {
					E[k] = e*T[k]
				}
				C[k] = Cf + E[k]
			}
		}
		else {
			# NOTE T will actually be PET
			if (Cf>g){
				C[k] = Cf + T[k]*exp((1 - Cf/g)*2)
			}
			else{
				C[k] = Cf 
			}
		}

		# If rainfall is greater than 0, calculate effective rainfall.
		# Otherwise,set effective rainfall to 0.
		if (P[k] > 0) {
			if (C_prev > Cf) {
				U[k] = P[k] - (C_prev - Cf)
			} else {
				U[k] = P[k]
				stop("C-prev < Cf")
			}
		} else {
			U[k] = 0
		}
		
		C_prev = C[k]
		if (U[k] < 0) {
			# Correct errors due to machine precision
			U[k] = 0
		}
		
	}

	ans = list("U" = U, "C" = C, "E" = E)
	return(ans)
}

ExponentialDrainage <- function(C_prev, d, Pk) { 

	if (C_prev >= d) {
		Cf = C_prev - Pk
		if (Cf < d) {
			## d <= C[k-1] < d + P[k]
			Cf = d*exp((Cf - d)/d)
		} 
	} else {
		## d > C[k-1]
		Cf = C_prev*exp(-Pk/d)
	}

	return(Cf)
}



