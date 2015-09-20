
ListOfArrayToArray = function(listn) {
# Rachel Blakers 1/05/2014 v0.1
#
# Flatten a possibly nested list of arrays to a single
# array. Assumes that the number of rows is the same
# for all arrays.
	
	dat = c()
	FlattenList = function(x) {
		if (!is.list(x)) {
			dat = cbind(dat, x)
		} else {
			for (i in 1:length(x)) {
				tmp = FlattenList(x[[i]])
				colnames(tmp) = paste(names(x)[i], colnames(tmp), sep = ".")
				dat = cbind(dat, tmp)
			}
		}
		return(dat)
	}
	
	dat = FlattenList(listn)
	return(dat)
}
