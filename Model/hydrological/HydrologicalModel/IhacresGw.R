
# 
# NOTES ON THE CODE:
#
# NATURAL LOSS RATE
# - The natural loss rate (in the aquifer parameter file) is implemented as an 
# absolute volume per aquifer, but it should probably be changed to a rate 
# proportional to the storage volume.
#
# NETWORK SPECIFICATION
# - It is essential that all upstream catchments are listed before downstream 
# catchments in the network.dat file. E.g. All catchments that flow into a 
# given catchment 'A' must be listed before catchment 'A' in the network.dat 
# file.
#
# FLOW ROUTING
# - if flow routing is used (i.e. there is more than one catchment in the 
# network) the code expects the first catchment to have no area
# and the discharge from this catchment will be equal to the inflow (from the
# inflow.csv file). 
# - Parameters:
#		- 'lambda' is not currently used
#		- 0 < eta < 1
#
# RAINFALL
# - Areal rainfall data is per unit area for each catchment
#
# SGW NETWORK
# - Note that results are sensitive to the order of the catchments in the 
# sgw network file. This determines the order in which discharge to the 
# stream occurs in the Discharge function.

IhacresGw <- function(param, tdat, init_gwstorage, init_C, init_Nash, init_Qq, init_Qs, period = NA, printStatus = TRUE) { 
# IN:
# period ~ NA or 1*2 vector, the start and end date of the simulation
#
# OUT:
# U ~ effective rainfall
# Ud ~ diffuse gw recharge
# Qd ~ net discharge from connected aquifers to the catchment

	CheckArgumentNames(param, tdat)
	# Select time period
	tdat = SelectTimePeriod(tdat, period)
	
	# Assign variable names in workspace
	for (i in 1:length(param)) {
		assign(names(param)[i], param[[i]])
	}
	for (i in 1:length(tdat)) {
		assign(names(tdat)[i], tdat[[i]])
	}
	
	# Number of catchments
	n = nrow(swNetwork)
	# Catchment names
	nodes = row.names(swNetwork)  
	# Number of aquifers
	m = nrow(gwNetwork)
	# Aquifer names
	aquifers = row.names(gwNetwork)
	# Number of time steps
	s = nrow(P)
	
	if (printStatus) {
		cat("\nNumber catchments:", n, "\nNumber aquifers:", m, 
			"\nNumber time steps:", s, "\n\n")
	}

	# Create a reverse mapping of the surface water network
	# (Given a downstream catchment, the reverse map finds the upstream 
	# catchments)
	swNetworkRevMap = ReverseMap(swNetwork)
	# Initialise time series with zero values
	init = InitialiseData(s, swNetwork, swInflowNetwork, gwNetwork, 
		swNetworkRevMap) 
	for (i in 1:length(init)) {
		assign(names(init)[i], init[[i]])
	}
	Qqs = Q
	Qrech = Q
	pump = R
	S = G
	Pump = R

	for (i in 1:n) {
		catchmentID = i
		if (printStatus) {
			cat("Catchment:", nodes[i], "\n")
		}
		# Proportion of rainfall infiltrating to gw
		# (Converted from depth to volume: 1mm*1km^2 = 1ML)
		Ud[, catchmentID] = (swParam[catchmentID, VD]*P[, catchmentID]*
			swParam[[catchmentID, AREA]])
		if (printStatus) {
			cat("\tCalculate catchment moisture deficit\n")
		}
		# Proportion of rainfall contributing to runoff
		Presid = (1 - swParam[catchmentID, VD])*P[, catchmentID]
		out = CatchmentMoistureDeficit(Presid, T[, catchmentID], 
			swParam[catchmentID, ], init_C)
		# Rain depth and surface area to volume conversion: 1mm*1km^2 = 1ML
		raw_C[, catchmentID] = out$C 
		C[, catchmentID] = out$C*swParam[[catchmentID, AREA]]
		U[, catchmentID] = out$U*swParam[[catchmentID, AREA]]
		E[, catchmentID] = out$E*swParam[[catchmentID, AREA]]
	
		if (printStatus) {
			cat("\tFlow partitioning\n")
		}
		out = FlowPartitioning(swParam[catchmentID, ], U[, catchmentID])
		Uq[, catchmentID] = out$Uq 
		Us[, catchmentID] = out$Us 
			
		if (printStatus) {
			cat("\tCalculate quickflow and shallow subsurface flow\n")
		}
		Qq[, catchmentID] = UnitHydrograph(Uq[, catchmentID], 
			swParam[catchmentID, TAUQ], init_Qq)
		Qs[, catchmentID] = UnitHydrograph(Us[, catchmentID], 
			swParam[catchmentID, TAUS], init_Qs)
		Qqs[, catchmentID] = Qq[, catchmentID] + Qs[, catchmentID]
			
		if (printStatus) {
			cat("\tCalculate losses to gw recharge from streamflow\n")
		}	
		Qrech[, catchmentID] = swParam[[catchmentID, RHO]]*Qqs[, catchmentID]
		Qqs[, catchmentID] = Qqs[, catchmentID] - Qrech[, catchmentID]
	}
	
	if (printStatus) {
		cat("Net recharge from rainfall, groundwater extractions and",
			"natural losses.\n")
	}

	# Apply groundwater extractions and natural losses to recharge
	for (j in 1:m) {
		aquiferID = aquifers[j]
		R[, j] = (R[, j] - gwExtraction[, aquiferID] - gwParam[aquiferID, NL])
		if (!is.na(gwParam[aquiferID, TAUD])) {
			# Pump = NashCascade(gwParam[aquiferID, SM]*gwExtraction[, aquiferID],
				# gwParam[2, SM], 1)
			# Pump = (Pump - gwParam[aquiferID, SM]*
				# gwExtraction[, aquiferID])
			pump[, j] = gwExtraction[, aquiferID]*gwParam[aquiferID, SM]
		}
	}

	# Add diffuse and streamflow recharge to gw recharge
	for (i in 1:n) {
		catchmentID = i
		for (j in 1:m) {
			aquiferID = aquifers[j]
			if (any(rownames(sgwParam[[i]]) == aquiferID)) {
				# Proportion of recharge going to this aquifer
				rechargeFrac = sgwParam[[i]][[aquiferID, RF]]
				
				# Proportion of total streamflow recharging gw
				##### NOTE: This should include upstream inflow Qr #########
				Rstream = rechargeFrac*Qrech[, catchmentID]
				# Alternative form capped at a max recharge rate
				#Rstream = unlist(lapply(rechargeFrac*Qrech[, catchmentID], min, 10))
				
				# Diffuse recharge
				if (is.na(gwParam[[aquiferID, NC]])) {
					Rdiffuse = rechargeFrac*Ud[, catchmentID]
					next_Nash = 0
				} else {
					# Apply Nash Cascade
					# Rdiffuse = NashCascade(rechargeFrac*Ud[, catchmentID], gwParam[aquiferID, TAUR], gwParam[aquiferID, NC], init_Nash)
					Nash_response = NashCascade(rechargeFrac*Ud[, catchmentID], gwParam[aquiferID, TAUR], gwParam[aquiferID, NC], init_Nash)
					Rdiffuse = Nash_response$Q
					next_Nash = Nash_response$Q_prev
				}
					
				# Total recharge
				R[, j] = R[, j] + Rstream + Rdiffuse
			}
		}
	}

	if (printStatus) {
		cat("Groundwater flow and discharge\n")
	}
	## Aquifer slow-flow time constant
	taud = gwParam[, TAUD]
	# Calculate the groundwater discharge fraction, 'a', for each aquifer
	alpha_s = -exp(-1/taud)
	a = array(-(1 + alpha_s)/alpha_s, dim = c(1, m))
	colnames(a) = rownames(gwParam)		
	# Initialise groundwater storage with net recharge
	G = G + R
	S = S + R - pump
	for (k in 1:s) {
		# Add groundwater storage volume from previous time step to each
		# aquifer
		if (k == 1) {
			G[k, ] = G[k, ] + init_gwstorage
			# G[k, ] = G[k, ] + gwParam[, GT0]
			# S[k, ] = S[k, ] + gwParam[, GT0]
		} else {
			G[k, ] = G[k, ] + G[k - 1, ]
			S[k, ] = S[k, ] + S[k - 1, ]
		}
			
		# Iterate through catchments
		for (i in 1:n) {
			# catchment name
			catchment = names(sgwParam)[i]	
			catchmentID = i
			# Route flow from upstream inflows (i.e. inflows from outside of
			# the modelled domain that are provided as input timeseries)
			ninflow = length(swInflowParam)
			if (ninflow > 0) {
				for (p in 1:ninflow) {
					if (any(rownames(swInflowParam[[p]]) == catchment)) {
						# This catchment is at the head of a flow network.
						# Route inflow data
						usname = names(swInflowParam)[p]
						routedFlow = Route(swInflowParam[[p]], 
							Qr[[catchmentID]][, usname], swInflow[, usname], k)
						# Apply transmission losses
						tloss = swInflowParam[[p]][["tloss"]]
						Qr[[catchmentID]][k, usname] = routedFlow$Qr[k]*(1 - 
							tloss)
					}
				}
			}
		
			# Route flow from upstream catchments (if present)
			nus = swNetworkRevMap[catchmentID, NUS]
			if (nus > 0) {
				for (p in 1:nus) {
					# Upstream catchment name
					usname = swNetworkRevMap[catchmentID, p + 1]
					routedFlow = Route(swFlowParam[[usname]][catchment, ], 
						Qr[[catchmentID]][, usname], Q[, usname], k)
					Qr[[catchmentID]][k, usname] = routedFlow$Qr[k]
				}
			}
		
			# Groundwater recharge discharge
			if (!all(is.na(sgwParam[[catchmentID]]))) {
				for (j in 1:nrow(sgwParam[[catchmentID]])) {
					# Get discharge start level for current catchment 
					# & aquifer
					aquifer = rownames(sgwParam[[catchmentID]][j, ])
					
					ans = GwVariableFlow(sgwParam, gwNetwork, gwFlowParam,
						G, Gf, Qd, a, catchment, aquifer, k)
					G = ans$G
					Qd = ans$Qd
					Gf = ans$Gf
					S[k, ] = S[k, ] - Qd[k, ]
				}
			}
			
			# Total flow - the sum of rainfall runoff from within the 
			# catchment, groundwater discharge, and upstream inflow
			Q[k, catchmentID] = (Qqs[k, catchmentID] + 
				Qd[k, catchmentID] + sum(Qr[[catchmentID]][k, ]))

			# Calculate total flow after extractions
			qe = Q[k, catchmentID] - swExtraction[k, catchmentID]
			Q[k, catchmentID] = max(0, qe)
			
			# Calculate extraction excess - extractions greater than the 
			# available surface water supply
			swE[k, catchmentID] = min(0, qe)
		}
	}
	# plot(S[, 1], col = "white")
	# lines(G[, 1], col = "red")
	# lines(S[, 1])
	# x11()
	# plot(cumsum(Pump))
	
	Glevel = CalculateGwHeads(G, gwFitParam)

	if (printStatus) {
		cat("Done IhacresGW\n")
	}
	out = list("U" = U, "C" = C, "E" = E, "Q" = Q, "Qq" = Qq, "Qs" = Qs, "Qr" = Qr, "raw_C" = raw_C, "next_Nash" = next_Nash,
		"Qd" = Qd, "G" = G, "Uq" = Uq, "Us" = Us, "Ud" = Ud, "R" = R, "Gf" = Gf, "swE" = swE, "Rdiffuse"=Rdiffuse,
		"S" = S, "Glevel" = Glevel)
	return(out)
}

ReverseMap = function(network) {
# Create a reverse mapping of a network data frame.
# Given a downstream node, the reverse map gives the upstream nodes

	reverseMap = data.frame(array(NA, dim = c(nrow(network), 3)))
	names(reverseMap) = c("nus", "us1", "us2")
	row.names(reverseMap) = row.names(network)
	for (i in 1:nrow(network)) {
		# Get name of current catchment
		catchment = row.names(network)[i]
		# Get indices of upstream catchments (if they exist)
		upIndex = which(network[, 2:ncol(network), drop = FALSE] == catchment, 
			arr.ind = TRUE)
		nus = nrow(upIndex)
		if (!is.null(nus) && nus != 0) {
			# Upstream catchments exist
			reverseMap[i, "nus"] = nus
			if (nus == 1) {
				reverseMap[i, 2] = row.names(upIndex)
			} else {
				reverseMap[i, 2:(nus + 1)] = names(sort(upIndex[, 1]))
			}
		} else {
			reverseMap[i, "nus"] = 0
		}
	}
	
	return(reverseMap)
}

InitialiseData = function(s, swNetwork, swInflowNetwork, gwNetwork, 
	swNetworkRevMap) {
# Initialise time series data frames with zero values

	# Number of catchments
	n = nrow(swNetwork)
	# Catchment names
	nodes = row.names(swNetwork)  
	# Number of aquifers
	m = nrow(gwNetwork)
	# Aquifer names
	aquifers = row.names(gwNetwork)

	U = array(0, dim = c(s, n)) # Total effective rainfall
	colnames(U) = nodes
	Uq = U # Effective rainfall diverted to quickflow
	Us = U # Effective rainfall diverted to shallow groundwater
	Ud = U # Diffuse infiltration from rain to gw
	C = U # CMD
	raw_C = U
	E = U # Evapotranspiration
	Qq = U # Quickflow discharge to stream
	Qs = U # Shallow gw discharge to stream
	Qd = U # Deep gw dischage to stream
	Q = U # Total streamflow
	# Effective rainfall diverted to deep groundwater 
	R = array(0, dim = c(s, m))
	colnames(R) = aquifers
	G = R # Groundwater storage volume
	# Routed flow component
	Qr = as.list(rep(NA, n))
	names(Qr) = nodes
	for (i in 1:n) {
		# Get name of current catchment
		catchment = names(Qr)[i]
		# Get number of upstream catchments
		nus = swNetworkRevMap[[i, "nus"]]
		# Get upstream upstream inflow (if present)
		inflowNames = row.names(
			which(swInflowNetwork[, 2, drop = FALSE] == catchment, 
			arr.ind = TRUE))
		nin = length(inflowNames)
		if ((nus + nin) > 0) {
			# Upstream/inflow catchments exist
			Qr[[i]] = array(0, dim = c(s, nus + nin))
			if (nus > 0) {
				colnames(Qr[[i]]) = c(swNetworkRevMap[i, 2:(nus + 1)], 
					inflowNames)
			} else {
				colnames(Qr[[i]]) = inflowNames
			}
		} else {
			Qr[[i]] = array(0, dim = c(s, 1))
			colnames(Qr[[i]]) = NA
		}
	}
	# Surface water extraction excess
	swE = U
	
	Gf = array(0, dim = c(s, 1))
	colnames(Gf) = "GwFlow"
	
	ans = list("U" = U, "C" = C, "E" = E, "Uq" = Uq, "Us" = Us, "raw_C"=raw_C,
		"Ud" = Ud, # Diffuse gw recharge
		"Q" = Q, "Qq" = Qq, "Qs" = Qs, "Qd" = Qd, 
		"Qr" = Qr, "G" = G, "R" = R, "Gf" = Gf, "swE" = swE)
	return(ans)
}

CheckArgumentNames = function(param, tdat) {
# Check that the input arguments "param" and "tdat" are lists 
# containing the correct variable names. Order and extra variables do not
# matter.
# Return an error if not.
#
	paramNames = c("swNetwork", "gwNetwork", "sgwNetwork", "swInflowNetwork",
		"swParam", "gwParam", "sgwParam", "swFlowParam", "swInflowParam", 
		"gwFlowParam")
	tdatNames = c("P", "T", "swInflow", "gwExtraction", "swExtraction")
	
	if (!(all(paramNames %in% names(param)) & 
		all(tdatNames %in% names(tdat)))) {
		cat("ERROR: IhacresGw: Expected the following inputs:\n")
		print(paramNames)
		print(tdatNames)
		stop()
	} 
}

SelectTimePeriod = function(tdat, period) {
# Trim a (possibly nested) list of arrays to the the selected period.
# 
# IN:
# tdat ~ list of arrays, needs to contain an element called 'tseq' which
# 	contains a list of dates
# period ~ 1*2 list, the start and end dates of the desired period
#
	if (all(is.na(period))) {
		newdat = tdat
	} else {
		startIndex = which(tdat$tseq == period[[1]])	
		endIndex = which(tdat$tseq == period[[2]])
		
		# Recursively trim arrays to the selected time period
		SelectPeriod = function(x) {
			if (!is.list(x)) {
				# Trim the vector to the desired range
				if (is.null(dim(x))) {
					# x is a row vector
					x = x[startIndex:endIndex]
				} else {
					# x is an array
					x = x[startIndex:endIndex, , drop = FALSE]
				}
			} else {
				# x is a list, trim the list elements
				for (i in 1:length(x)) {
					x[[i]] = SelectPeriod(x[[i]])
				}
			}
			
			return(x)
		}
		newdat = SelectPeriod(tdat)
	}

	return(newdat)
}