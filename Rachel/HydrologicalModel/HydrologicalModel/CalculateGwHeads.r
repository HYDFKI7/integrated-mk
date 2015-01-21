
CalculateGwHeads = function(Gstorage, gwFitParam) {
	
	applyFit = function(fitParam, G) {
		Glevel = apply(fitParam, 2, 
			function(x) {G*x["scale"] + x["intercept"]})
		return(Glevel)
	}
	Glevel = mapply(applyFit, gwFitParam, 
		unlist(apply(Gstorage, 2, list), recursive = FALSE))

	return(Glevel)
}