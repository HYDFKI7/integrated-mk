# sudo R
# install.packages("zoo")


SetupIhacres = function(workingdir) { 
## Setup IHACRES program environment.
##

	## Load library packages
	library(zoo)
	library(hydromad)
	library(ggplot2)
	library(nnls)
	library(reshape) # for 'melt'
	
	# Set working directory
	cat("Set working directory:\n\t", workingdir, "\n")
	setwd(workingdir)

	## Load the source directory function
	source("Lib/SourceDir.R")

	## Add required R files to the source
	## All code is assumed to be in subdirectories of the working directory
	SourceDir("HydrologicalModel", trace = FALSE)
	SourceDir("Setup", trace = FALSE)
	SourceDir("Lib", trace = FALSE)
	# SourceDir("Code/DataProcessing", trace = FALSE)
	# SourceDir("Code/MissingDataInference", trace = FALSE)
	# SourceDir("Code/ObjectiveFns", trace = FALSE)

	# Set global constants
	SetGlobalConstants()

}

SetGlobalConstants = function() {
	# Sw param
	assign("DC", 1, envir = .GlobalEnv)
	assign("EC", 2, envir = .GlobalEnv)
	assign("FC", 3, envir = .GlobalEnv)
	assign("VD", 4, envir = .GlobalEnv)
	assign("VQ", 5, envir = .GlobalEnv)
	assign("RHO", 6, envir = .GlobalEnv)
	assign("TAUQ", 7, envir = .GlobalEnv)
	assign("TAUS", 8, envir = .GlobalEnv)
	assign("AREA", 9, envir = .GlobalEnv)
	# Gw param
	assign("TAUD", 1, envir = .GlobalEnv)
	assign("SM", 2, envir = .GlobalEnv)
	assign("NL", 3, envir = .GlobalEnv)
	assign("OFFSET", 4, envir = .GlobalEnv)
	assign("SCALE", 5, envir = .GlobalEnv)
	assign("GT0", 6, envir = .GlobalEnv)
	assign("RP", 7, envir = .GlobalEnv)
	assign("TAUR", 8, envir = .GlobalEnv)
	assign("NC", 9, envir = .GlobalEnv)
	# Sgw param
	assign("RF", 1, envir = .GlobalEnv)
	assign("GS", 2, envir = .GlobalEnv)
	assign("RHO_NA", 3, envir = .GlobalEnv)
	# Sw flow param
	assign("GAMMA", 1, envir = .GlobalEnv)
	assign("LAMBDA", 2, envir = .GlobalEnv)
	assign("ALPHA", 3, envir = .GlobalEnv)
	assign("PHI", 4, envir = .GlobalEnv)
	assign("ETA", 5, envir = .GlobalEnv)
	assign("LAG", 6, envir = .GlobalEnv)
	# Gw flow param
	assign("DELTA", 1, envir = .GlobalEnv)
	assign("SCALEF", 2, envir = .GlobalEnv)
	assign("OFFSETF", 3, envir = .GlobalEnv)
	# Sw network 
	assign("NDS", 1, envir = .GlobalEnv)
	# Sw network reverse map
	assign("NUS", 1, envir = .GlobalEnv)
}