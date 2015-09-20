
SaveScenarioResults = function(tdat, obs, sim, outdir) {
# Rachel Blakers 01/05/2014 v0.1

	cat("Write results to file:\t\n", outdir, "\n")
	dir.create(outdir, showWarnings = TRUE)
	
	# Save model outputs to file
	results = zoo(ListOfArrayToArray(sim), tdat$tseq)
	write.zoo(results, file = paste(outdir, "Results.csv", sep="/"), 
		sep = ",", na = "")
	
	# Write observations to file
	outobs = ListOfZooToZoo(obs, tdat$tseq)
	write.zoo(outobs, file = paste(outdir, "Data.csv", sep="/"), 
		sep = ",", na = "")
		
}