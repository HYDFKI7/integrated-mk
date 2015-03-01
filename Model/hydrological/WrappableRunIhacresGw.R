RunIhacresGw <- function(workingdir, datadir) {

	scenStart = "1969-01-01"
	scenEnd = "2010-03-02"

	cat("Scenario directory:\n\t", datadir, "\n")
	
	# Setup the IHACRES model script environment
	source(paste(workingdir,"/","SetupIhacres.R",sep = ""))
	SetupIhacres(workingdir)

	# Read the input file data
	mod = GetIhacresInputs(datadir)
	tdat = mod$tdat
	param = mod$param
	obs = mod$obs

	# Run model
	sim = IhacresGw(param, tdat) 
	
	tdat$dates = as.character(tdat$tseq)
	return (list("sim" = sim, "tdat" = tdat))
	# return(sim)
    # return(x^2)
}
