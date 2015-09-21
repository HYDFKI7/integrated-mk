
GwFlow <- function(gwNetwork, gwFlowParam, G, Gf, k) { 

	for (j in 1:nrow(gwNetwork)) {
		nds = gwNetwork[[j, "nds"]] 
		if (nds > 0) {
			upstream = names(gwFlowParam)[[j]]
			for (i in 1:nds) {
				delta = gwFlowParam[[j]][i, DELTA]
				scalef = gwFlowParam[[j]][i, SCALEF]
				offsetf = gwFlowParam[[j]][i, OFFSETF]
				downstream = row.names(gwFlowParam[[j]])[i]
		# Upstream gw storage after losses to downstream aquifer		
		G[k, upstream] = ((1 + delta*scalef)/(1 + delta*scalef + delta)*G[k, upstream] +
			delta/(1 + delta*scalef + delta)*(scalef*G[k, downstream] + offsetf))
		# Gw flow component
		Gf[k, 1] = (delta/(1 + delta*scalef)*G[k, upstream] - 
			delta/(1 + delta*scalef)*(scalef*G[k, downstream] + offsetf))
		# Downstream gw storage after gains from upstream aquifer
		G[k, downstream] = G[k, downstream] + Gf[k, 1]
			}
		}
	}
	
	ans = list("G" = G, "Gf" = Gf)
	return(ans)
}

