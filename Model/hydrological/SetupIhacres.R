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
	# cat("Set working directory:\n\t", workingdir, "\n")
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
