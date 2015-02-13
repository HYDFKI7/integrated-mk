
MultipleConstrainedRegression <- function(observed, model) {
# Estimate linear model regression parameters, the slope is constrained to
# be positive.
# If the model values are constant, or the observed values are all NA,
# then scale 0 and intercept 0 are returned.
#
# INPUT:
# observed ~ s*n array, columns are the observations of the variable
# model ~ 1*s vector, the modelled variable
# OUTPUT:
# Array containing linear regression parameters
#
	
	# Number observation variables
	m = ncol(observed)
		
	# Perform linear regression for each observation bore
	coeff = array(0, dim = c(2, m))
	colnames(coeff) = colnames(observed)
	rownames(coeff) = c("scale", "intercept")
	for (i in 1:m) {
		if (!all(is.na(observed[, i])) & ! all(model == 0)) {
		
			nonNa = !is.na(observed[, i])
			dat = as.data.frame(cbind(observed[nonNa, i], model[nonNa]))
			names(dat) = c("obs", "mod")
			# Linear regression with the first coefficient constrained
			# to be positive
			fit = nls(obs ~ mod*x1 + x2, data = dat,
				start = list(x1 = 1, x2 = 1),
				algorithm = "port",
				lower = c(x1 = 0, x2 = -Inf),
				upper = c(x1 = Inf, x2 = Inf))
			fitsum = summary(fit)
			
			coeff["scale", i] = fitsum$coefficients[[1]]
			coeff["intercept", i] = fitsum$coefficients[[2]]
		}
	}

	return(coeff)
}
