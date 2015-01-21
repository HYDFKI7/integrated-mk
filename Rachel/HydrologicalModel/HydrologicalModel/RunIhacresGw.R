RunIhacresGw <- function(workingdir, datadir) { 
# Run the IHACRES-GW model
# Results are saved to the directory named according to the format:
# <datadir>Results_<datestamp>
#
# Input:
# workingdir ~ string, the path of the Project directory 
# 	e.g. D:/dir/Project
# datadir ~ string, the path of the directory containing the input data.
#	e.g. D:/dir/Project/Scenario/MaulesCreek
#

	workingdir = "C:/Data/Work/PhD/Projects/IhacresGw"
	datadir = paste(workingdir, "Scenarios/Maules_19690101_20100302", 
		sep = "/")
	scenStart = "1969-01-01"
	scenEnd = "2010-03-02"
	
	# Set working directory
	setwd(workingdir)
	cat("Working directory:\n\t", workingdir, "\n")
	cat("Scenario directory:\n\t", datadir, "\n")
	
	# Setup the IHACRES model script environment
	source("Code/HydrologicalModelSetup/SetupIhacres.R")
	SetupIhacres(workingdir)

	# Read the input file data
	mod = GetIhacresInputs(datadir)
	tdat = mod$tdat
	param = mod$param
	obs = mod$obs

	# Run model
	sim = IhacresGw(param, tdat) 
	mod$sim = sim
	
	# Save results to file
	today = format(Sys.Date(), "%Y%m%d")
	outdir = paste(datadir, "/Results_", today, sep = "")
	SaveScenarioResults(tdat, obs, sim, outdir)
	
	# Save plots to file
	PlotScenarioResults(tdat, obs, sim, paste(outdir, "/Plots", sep = ""))
		
}


# Run the script if it is being called from the workspace (i.e. executed
# directly by the user).
# Do nothing if it is being loaded by another function.
if(sys.parent() == 0) {

}
