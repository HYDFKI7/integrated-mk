
GwVariableFlow <- function(sgwParam, gwNetwork, gwFlowParam,
	G, Gf, Qd, a, catchment, aquifer, k)
{
# Rachel Blakers 29/05/2012 v0.3
# 
# Calculate discharge to the stream (slowflow) from the selected aquifer.
#
# INPUT:
# sgwParam ~ named list, the surface - groundwater interaction parameters
#			for the current catchment.
# a ~ data frame, the groundwater discharge fraction for each aquifer
#
# OUTPUT:
# Named list with the following elements:
# Qd_k ~ s*n data frame, net discharge from connected aquifers to the catchment
# G_k ~ s*n vector, groundwater storage volume (relative)
#
	
	a = a[, aquifer]
	# Get discharge start level for current catchment & aquifer
	Gs = sgwParam[[catchment]][aquifer, GS]
	# Get gw flow parameters for current aquifer
	nds = gwNetwork[[aquifer, NDS]]
	if (nds > 0) {
		# NOTE:
		# ASSUMES THERE IS ONLY 1 DOWNSTREAM AQUIFER - NEED TO ALLOW FOR MANY
		dsAquifer = gwNetwork[[aquifer, 2]]
		b = gwFlowParam[[aquifer]][[dsAquifer, DELTA]]
		Gds0 = gwFlowParam[[aquifer]][[dsAquifer, OFFSETF]]
		
		Gds_star = G[k, dsAquifer]
		
		if (Gds_star >= Gds0) {
			Gup_star = G[k, aquifer] + (b/(1 + b))*Gds_star
			if (((1 + b)/(1 + 2*b))*Gup_star >= Gs) {
				# Gw storage in upstream aquifer
				G[k, aquifer] = ((1 + b)/(1 + 2*b + a + a*b))*Gup_star
				# Gw discharge to stream from upstream aquifer
				Qd[k, catchment] = Qd[k, catchment] + a*G[k, aquifer]
			} else {
				G[k, aquifer] = ((1 + b)/(1 + 2*b))*Gup_star
				Qd[k, catchment] = Qd[k, catchment] + 0
			}
			# Gw storage volume in downstream aquifer
			G[k, dsAquifer] = (1/(1 + b))*(Gds_star + b*G[k, aquifer])
			# Gw flow between aquifers
			Gf[k, 1] = b*(G[k, aquifer] - G[k, dsAquifer])
		} else {
			Gup_star = G[k, aquifer] + b*Gds0
			if ((1/(1 + b))*Gup_star >= Gs) {
				G[k, aquifer] = (1/(1 + b + a))*Gup_star
				Qd[k, catchment] = Qd[k, catchment] + a*G[k, aquifer]
			} else {
				G[k, aquifer] = (1/(1 + b))*Gup_star
				Qd[k, catchment] = Qd[k, catchment] + 0
			}
			# Gw flow between aquifers
			Gf[k, 1] = b*(G[k, aquifer] - Gds0)
			# Gw storage volume in downstream aquifer
			G[k, dsAquifer] = Gds_star + Gf[k, 1]
		}
	} else {
		# There is no flow between aquifers, calculate discharge to the
		# stream only
		if (G[k, aquifer] >= Gs) {
			# Gw storage in upstream aquifer
			G[k, aquifer] = (1/(1 + a))*G[k, aquifer] 
			# Gw discharge to stream from upstream aquifer
			Qd[k, catchment] = Qd[k, catchment] + a*G[k, aquifer]
		} 
	}
	
	ans = list("Qd" = Qd, "G" = G, "Gf" = Gf)
	return(ans)
}