
Route = function(param, Qr, Q, k) {
# Rachel Blakers 29/5/2012 v0.2
#
# Route flow through the stream network.
# NOTE: I should probably change this code to just output Qr and Qrb for the
# current time step k, rather than the complete time series.
#
# INPUT:
# param ~ named list, the sw flow routing parameters for the upstream 
# 		catchment.
# Qr ~ s*1 data frame, streamflow routed to the downstream catchment. 
# Qrb ~ s*1 data frame, baseflow component of routed streamflow. 
# Q ~ s*1 data frame, streamflow in the upstream catchment. 
# Qs ~ s*1 data frame, baseflow component of streamflow in the upstream 
#		catchment.
# k ~ integer, current time step 
#
# OUTPUT:
# Qr ~ s*1 data frame, streamflow routed to the downstream catchment
# Qrb ~ s*1 data frame, baseflow component of routed streamflow
#

	# Flow lag (in days)
	lagg = param[, LAG]
	# Broadening of flow peak
	alpha = param[, ALPHA]
	# Proportion of flow directed to downstream node
	gama = param[, GAMMA]
	# Calculate time constant for upstream flow delay
	eta = param[, ETA]
	phi = param[, PHI]
	# if (k >= (lagg + 1)) {
		# if (Q[k - lagg] == 0) {
			# omega = 1
		# } else {
			# omega = phi/(Q[k - lagg]^eta)
			# if (omega > 1) {
				# omega = 1
				# warning("Route: omega > 1, setting omega = 1")
			# }
		# }
	# }
	omega = phi

	# Route total flow to downstream node
	# Upstream inflow
	if (k < (lagg + 1)) {
		upstream = 0
	} else if (k == (lagg + 1)) {
		upstream = gama*(1 - omega)*Q[k - lagg]
	} else {
		upstream = gama*((1 - omega)*Q[k - lagg] + omega*Q[k - lagg - 1])
	}
	# Routed flow
	if (k == 1) {
		Qr[k] = (1 - alpha)*upstream
	} else {
		Qr[k] = alpha*Qr[k - 1] + (1 - alpha)*upstream
	}
	
	ans = list("Qr" = Qr)
	return(ans)
}