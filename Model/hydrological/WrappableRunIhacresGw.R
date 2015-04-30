RunIhacresGw <- function(workingdir, datadir, init_gwstorage, init_C, init_Nash, init_Qq, init_Qs, climate_type) {

	# scenStart = "1969-01-01"
	# scenEnd = "2010-03-02"

	cat("Scenario directory:\n\t", datadir, "\n")

	# Setup the IHACRES model script environment
	source(paste(workingdir,"/","SetupIhacres.R",sep = ""))
	SetupIhacres(workingdir)

	# Read the input file data
	mod = GetIhacresInputs(datadir)
	tdat = mod$tdat
	param = mod$param
	obs = mod$obs

	# param$swParam$Qq0 = 456789098765434567
	# param$swParam$Qs0 = init_Qs

	# Run model
	sim = IhacresGw(param, tdat, init_gwstorage, init_C, init_Nash, init_Qq, init_Qs, climate_type = climate_type) 
	
	tdat$dates = as.character(tdat$tseq)
	return (list("sim" = sim, "tdat" = tdat, "mod"=mod))
	# return(sim)
    # return(x^2)
}
