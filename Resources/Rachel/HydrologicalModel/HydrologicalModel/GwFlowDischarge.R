
GwFlowDischarge <- function(sgwParam, gwNetwork, gwFlowParam,
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
	
	# Get discharge start level for current catchment & aquifer
	Gs = sgwParam[[catchment]][aquifer, GS]
	# Get gw flow parameters for current aquifer
	nds = gwNetwork[[aquifer, NDS]]
	if (nds > 0) {
		# NOTE:
		# ASSUMES THERE IS ONLY 1 DOWNSTREAM AQUIFER - NEED TO ALLOW FOR MANY
		dsAquifer = gwNetwork[[aquifer, 2]]
		b = gwFlowParam[[aquifer]][[dsAquifer, DELTA]]
		S_star = (1 + b)*G[k, aquifer] + b*G[k, dsAquifer]
	} else {
		b = 0
		S_star = G[k, aquifer]
	}
		
	if (S_star >= Gs*(1 + 2*b)) {
		# Calculate gw storage and discharge to stream
		G[k, aquifer] = (1/(1 + 2*b + a[, aquifer] + a[, aquifer]*b))*S_star
	} else {
		# Calculate gw storage no discharge
		G[k, aquifer] = (1/(1 + 2*b))*S_star
	}
	if (nds > 0) {
		G[k, dsAquifer] = (1/(1 + b))*(G[k, dsAquifer] + b*G[k, aquifer])
	}
	
	Qd[k, catchment] = a[, aquifer]*G[k, aquifer]
	Gf[k, 1] = b*(G[k, aquifer] - G[k, dsAquifer])

	ans = list("Qd" = Qd, "G" = G, "Gf" = Gf)
	return(ans)
}