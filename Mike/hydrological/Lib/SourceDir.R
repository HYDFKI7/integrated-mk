
SourceDir <- function(path, trace = TRUE, ...) {
# Rachel Blaker v0.1 20/03/2012
#
# Add all R files in a directory to source
#
# Input:
# path ~ string, the path of the directory containing the R files.
#

	## Iterate through *.R files in path
    for (nm in list.files(path, pattern = "\\.[RrSsQq]$")) {
       if(trace) cat(nm,":")    
		## Add R file to source
       source(file.path(path, nm), ...)
       if(trace) cat("\n")
    }
 }