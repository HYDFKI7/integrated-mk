
ListOfZooToZoo = function(listn, tseq) {
# Rachel Blakers 1/05/2014 v0.1
#
# Flatten a possibly nested list of zoo objects to a single
# zoo object.
	
	dat = zoo(, tseq)
	FlattenList = function(x) {
		if (!is.list(x)) {
			dat = merge(dat, x)
		} else {
			for (i in 1:length(x)) {
				tmp = FlattenList(x[[i]])
				names(tmp) = paste(names(x)[i], names(tmp), sep = ".")
				dat = merge(dat, tmp)
			}
		}
		return(dat)
	}
	
	dat = FlattenList(listn)
	return(dat)
}
