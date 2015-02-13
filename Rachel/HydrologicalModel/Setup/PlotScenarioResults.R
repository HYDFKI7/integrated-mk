
PlotScenarioResults = function(tdat, obs, sim, outdir = NA) {
# Rachel Blakers 01/05/2014 v0.1
	
	plots = list()
	for (i in 1:ncol(sim$Q)) {
		site = colnames(sim$Q)[i]
		tmp = cbind(
			tdat$tseq,
			log10(as.data.frame(obs$Qobs[, site, drop = FALSE]) + 1),
			log10(sim$Q[, i, drop = FALSE] + 1)
			)
		names(tmp) = c("Date", "obs", "sim")
		p = PlotResults(tmp, site)
		plots$Q[[i]] = p
	}
	names(plots$Q) = colnames(sim$Q)
	
	for (i in 1:ncol(sim$Glevel[[1]])) {
		site = colnames(sim$Glevel[[1]])[i]
		tmp = cbind(
			tdat$tseq,
			sim$Glevel[[1]][, i, drop = FALSE],
			as.data.frame(obs$Gobs[[1]][, site, drop = FALSE])
			)
		names(tmp) = c("Date", "sim", "obs")
		p = PlotResults(tmp, site)
		plots$G1[[i]] = p
	}
	names(plots$G1) = paste("Shallow", colnames(sim$Glevel[[1]]))
	
	for (i in 1:ncol(sim$Glevel[[2]])) {
		site = colnames(sim$Glevel[[2]])[i]
		tmp = cbind(
			tdat$tseq,
			sim$Glevel[[2]][, i, drop = FALSE],
			as.data.frame(obs$Gobs[[2]][, site, drop = FALSE])
			)
		names(tmp) = c("Date", "sim", "obs")
		p = PlotResults(tmp, site)
		plots$G2[[i]] = p
	}
	names(plots$G2) = paste("Deep", colnames(sim$Glevel[[2]]))
	

	if (!is.na(outdir)) {
		cat("Write plots to file:\t\n", outdir, "\n")
		dir.create(outdir, showWarnings = TRUE)
		for (i in 1:length(plots)) {
			for (j in 1:length(plots[[i]])) {
				png(file = paste(outdir, "/", names(plots[[i]])[j], ".png",
					sep = ""), 
					width = 12, height = 5, units = "in", 
					res = 100) 
				print(plots[[i]][[j]])
				dev.off()
			}
		}
	} else {
		for (i in 1:length(plots)) {
			for (j in 1:length(plots[[i]])) {
				dev.new(width = 12, height = 5) # Set onscreen size
				print(plots[[i]][[j]])
			}
		}
	}
	
}

PlotResults = function(tmp, site) {
	
	tmp = tmp[!is.na(tmp[, "obs"]), ]
	dat = melt(tmp, id = "Date")
	p = ggplot(dat, aes(x = Date, y = value, colour = variable)) + 
		geom_point(size = 1) + geom_line() + 
		ggtitle(site)

	return(p)
}
	