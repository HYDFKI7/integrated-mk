
Discharge <- function(sgwParam, Qqs, Qr, G_k, Qd_k, a, catchment, aquifer, k)
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
	rho = sgwParam[[catchment]][aquifer, RHO]
	rho_inv = 1/(1 + rho)

	Q_star = (Qqs[k, catchment] + sum(Qr[[catchment]][k, ]))
	G_k = G_k + rho*rho_inv*Q_star
	
	# Calculate groundwater discharge to the current catchment
	# If the groundwater volume is greater than a threshold,
	# then it discharges to the stream.  If not, there is no
	# discharge.
	# Recharge is a constant proportion of the flow volume
	if (G_k > Gs) {
		# Groundwater storage volume after discharge
		G_k = ((1 + rho)/(1 + rho + a[, aquifer])*(G_k + 
			(a[, aquifer]*rho_inv)*Gs))
		# Add discharge volume to slow-flow
		Qd_k = (Qd_k + rho_inv*(a[, aquifer]*(G_k - Gs)- rho*Q_star))
	} else {
		Qd_k = Qd_k - rho*rho_inv*Q_star
	}

	ans = list("Qd_k" = Qd_k, "G_k" = G_k)
	return(ans)
}