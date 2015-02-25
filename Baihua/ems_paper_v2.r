### For EMS paper, code extracted and modified from indexCurveUncert demo
### https://github.com/josephguillaume/indexCurveUncert
### Created: 24/4/2013
### Version 2: change gw constrains

library(indexCurveUncert)
library(reshape)
library(ggplot2)
##library(hydromad) ##eventseq

loadIndexes("C:\\UserData\\fub\\work09\\Namoi\\EMS paper\\index_all\\")
loadHydro("C:\\UserData\\fub\\work09\\Namoi\\EMS paper\\",c("Pre90","Post90"))
loadAssets("C:\\UserData\\fub\\work09\\Namoi\\EMS paper\\ctf_v5.csv")

specieslist <- c("RRGMS", "RRGRR","WCMS", "WCRR","LGMS", "LGRR")
attribs.usesduration = c(timing = "duration", duration = "duration", dry = "duration",gwlevel=NA)					 
attribs.usesduration.nogw = c(timing = "duration", duration = "duration", dry = "duration") # no gw input
attribs.usesduration.gwonly = c(gwlevel=NA)	
attribs.usesduration.duronly = c(duration = "duration")

################################################################################
### 
max.dry <- 25000
for(s in c("RRGMS","RRGWMS","BBMS","LGMS","WCMS")){
    cpt <- index.all[[sprintf("%s_%s.csv", s,"dry")]]
    index.all[[sprintf("%s_%s.csv", s,"dry")]] <-
        rbind(cpt,
              c(Days=max.dry,rep(0,ncol(cpt)-1)))
}

##Duration
for(s in specieslist) #c("RRGMS", "RRGRR", "BBMS", "BBRR", "LGMS", "LGRR"))
    index.all[[sprintf("%s_%s.csv", s,"duration")]] <-
        rbind(index.all[[sprintf("%s_%s.csv", s,"duration")]],
              c(Days=1000,rep(NA,5)))

## Gwlevel
## index.all[grep("gwlevel",names(index.all),value=T)]
for(s in specieslist)
    index.all[[sprintf("%s_%s.csv", s,"gwlevel")]] <-
        rbind(index.all[[sprintf("%s_%s.csv", s,"gwlevel")]],
              c(Level_m=30,0))

checkAttributeRanges("Pre90",specieslist,attribs=names(attribs.usesduration))
checkAttributeRanges("Post90",specieslist,attribs=names(attribs.usesduration))



#################################################################################

## Cache preference curve bounds
getPrefConstraints <- getPrefConstraintsMultIndex
cachePreferences(names(index.all))

## Use cached modified by lists
getPrefConstraints <- function(...)
  getPrefConstraintsMergeWithCache(...,extra=getPrefConstraintsLists)

#################################################################################

### Change CTF sequence
 getSeqCtfsNew<-
 function (assetid) 
 {
 asset.name=asset.table$Name[assetid]
 if(asset.name=="Gunnedah") return (seq(3000,16000,by=1000))
 if(asset.name=="Barbers Lagoon") return (seq(3000,6000, by=200))
 if(asset.name=="Maules Creek") return (sort(unique(c(110,seq(100, 1100, by=50))))) ## Maules ck
 if(asset.name=="Upstream Mollee") return(sort(unique(c(seq(1000,3000,by=500),seq(4000,9000,by=1000),8500,1600))))
 if(asset.name=="Mollee to Gunidgera") return(seq(3000,12000,by=500))
 if(asset.name=="Duncans Warrambool") return(sort(unique(c(seq(3000,6000, by=200), 4000,4500,5500))))
 if(asset.name=="Wee Waa to Bugilbone") return(seq(1000,5000, by=250))
 if(asset.name=="Bugilbone to Walgett") return(sort(unique(c(1900,6300,seq(1500,15000, by=1000)))))
 if(asset.name=="Pian Creek") return(seq(1000,3000, by=200))
 stop("Unexpected assetid")
}

### Model 0. Duration only (~ hydrological only model)
## Add breakpoints
# for(dur.cpt in grep("duration",names(index.all),value=T)) {
# index.all[[dur.cpt]] <- data.frame(X1=c(seq(0,1000,by=50)))
# cached.pref[[dur.cpt]]<-NULL
# }

# weight.comp <- pref.monoton <- list()
# pref.monoton$RRGMS_duration.csv <- data.frame(min.x=0,max.x=Inf,dir=1,min.step=0) ##must go up/steady untill 2m 
# all.diffs <- vary_all(scen="Pre90",baseline="Post90",ecospecies=specieslist,
                      # use.durs=c(T,F),do.par=T,calc.mean = TRUE,
                      # attribs.usesduration=attribs.usesduration.duronly,
                      # assets=1:nrow(asset.table),getSeqCtfs=getSeqCtfsNew#getSeqCtfs10
                      # )

# devAskNewPage(T)
# par(mfrow=c(4,4))
# plot.unique.prefs(all.diffs,attrib="duration",NA)						  

### Model 1a. Surface water suitability, free weights.
weight.comp <- list()
all.diffs <- vary_all(scen="Pre90",baseline="Post90",ecospecies=specieslist,
                      use.durs=c(T,F),do.par=T,calc.mean = TRUE,
                      attribs.usesduration=attribs.usesduration.nogw,
                      assets=1:nrow(asset.table),getSeqCtfs=getSeqCtfsNew#getSeqCtfs10
                      )

## Go to visualisation

### Model 1b. Surface water suitability, with weight constraints.
weight.comp <- list()
weight.bounds<-list()
# for RRGMS and LGMS, duraiton is more important than timing and dry period. timing and dry can be zero. 
weight.comp$RRGMS <- weight.comp$RRGWMS <- weight.comp$LGMS<- data.frame(a="duration",
                                 b=c("timing","dry"),
                                 status=">=",min.gap=0.05)
# weight.comp$RRGRR <- weight.comp$RRGWRR <- data.frame(a="duration",
                                 # b=c("timing"),
                                 # status=">=",min.gap=0.05)	
								 
# for RRGRR, both timing and duration are important.
weight.bounds$RRGRR <- weight.bounds$RRGWRR<-rbind(data.frame(a="timing",min=0.3,max=NA),
										data.frame(a="duration",min=0.3,max=NA))										

#for WCMS, timing is critical but duration and dry period cannot be completely neglected.										
weight.comp$WCMS <- data.frame(a="timing",
                                 b=c("duration","dry"),
                                 status=">=",min.gap=0.05)
				 
weight.bounds$WCMS <- rbind(data.frame(a="duration",min=0.1,max=NA),
										data.frame(a="dry",min=0.1,max=NA))		
								 								 
#WCRR no weight constraints found.	
	
#for LGRR, timing is more critical than duraiton, but duration cannot be completely neglected.
weight.comp$LGRR <- data.frame(a="timing", b=c("duration"),status=">=",min.gap=0.05)	
weight.bounds$LGRR <- data.frame(a="duration",min=0.1,max=NA)
			 
						  
all.diffs <- vary_all(scen="Pre90",baseline="Post90",ecospecies=specieslist,
                      use.durs=c(T,F),do.par=T, calc.mean = TRUE,
                      attribs.usesduration=attribs.usesduration.nogw,
                      assets=1:nrow(asset.table),getSeqCtfs=getSeqCtfsNew#getSeqCtfs10
                      )
## Go to visualisation

####################################

### Model 2. Groundwater suitability, no weight concern.
## Add breakpoints
for(gw.cpt in grep("gwlevel",names(index.all),value=T)) {
index.all[[gw.cpt]] <- data.frame(X1=c(seq(0,20,by=0.5),30))
## Delete existing constraints for gwlevel (as they result in single line)
cached.pref[[gw.cpt]]<-NULL
}


##min.x,max.x,min.y,max.y all inclusive
pref.bounds <- list()
pref.monoton <- list()
pref.comp<-list()
pref.smooth<-list()

## RRGMS, RRGWMS, BBMS, 0,1,1,0 at 0,2,5,12m
pref.bounds$RRGMS_gwlevel.csv <- pref.bounds$RRGWMS_gwlevel.csv <- pref.bounds$BBMS_gwlevel.csv <-rbind(
									data.frame(min.x=15,max.x=Inf,min.y=0,max.y=0), ## must be 0 beyond 25m
									  data.frame(min.x=0,max.x=0,min.y=0,max.y=0), ## must be 0 at 0m
									  ## ideal is between 2 and 15m inclusive
									  data.frame(min.x=10,max.x=Inf,min.y=NA,max.y=0.7), ## must be less than "ideal" for >=15m
									  data.frame(min.x=0,max.x=2,min.y=NA,max.y=0.7), ## must be less than "ideal" for <=2m
									  ## totally unsuitable can only be in <1m and >15m (exclusive)
									  data.frame(min.x=2,max.x=10,min.y=0.1,max.y=NA), ##must be better than "totally unsuitable" between 2m and 15m inclusive
									  data.frame(min.x=2,max.x=5,min.y=0.5,max.y=NA)
									  )
pref.monoton$RRGMS_gwlevel.csv <- pref.monoton$RRGWMS_gwlevel.csv <- pref.monoton$BBMS_gwlevel.csv<- rbind(
									data.frame(min.x=0,max.x=2,dir=1,min.step=0), ##must go up/steady untill 3m
									data.frame(min.x=5,max.x=Inf,dir=-1,min.step=0) ## must go down/steady after 5m
									) 
pref.smooth$RRGMS_gwlevel.csv<-pref.smooth$RRGWMS_gwlevel.csv<-data.frame(min.x=0,max.x=Inf,min.step=-0.9/2,max.step=0.9/2) ##to be realistic, jumping from mostly unsuitable to ideal needs to be over at least 2m
#pref.single.extreme.notp$RRGMS_gwlevel.csv<-data.frame(min.x=5,max.x=10,type="max")

# pref.comp$RRGMS_gwlevel.csv<-rbind(
# data.frame(min.x1=5,max.x1=14,min.x2=15,max.x2=Inf,dir=">",min.gap=0.01),
# data.frame(min.x1=5,max.x1=14,min.x2=0,max.x2=4,dir=">",min.gap=0.1))

##WCMS
pref.bounds$WCMS_gwlevel.csv <- rbind(data.frame(min.x=5,max.x=Inf,min.y=0,max.y=0), ## must be 0 beyond 5m
									  #data.frame(min.x=0,max.x=0,min.y=1,max.y=NA), ## must be 1 at 0m
									  ## ideal is between 0 and 2m inclusive
									  data.frame(min.x=3,max.x=Inf,min.y=NA,max.y=0.9), ## must be less than "ideal" for >=3m
									  ## totally unsuitable can only be in <1m and >15m (exclusive)
									  data.frame(min.x=0,max.x=2,min.y=0.1,max.y=NA) ##must be better than "totally unsuitable" between 0m and 2m inclusive
									  )
pref.monoton$WCMS_gwlevel.csv <- rbind(
									data.frame(min.x=0,max.x=2,dir=1,min.step=0), ##must go up/steady untill 2m
									data.frame(min.x=2,max.x=Inf,dir=-1,min.step=0) ## must go down/steady after 2m
									) 
pref.smooth$WCMS_gwlevel.csv<-data.frame(min.x=0,max.x=Inf,min.step=-0.9/1,max.step=0.9/1) ##to be realistic, jumping from mostly unsuitable to ideal needs to be over at least 2m


#LGMS
pref.bounds$LGMS_gwlevel.csv <- rbind(data.frame(min.x=10,max.x=Inf,min.y=0,max.y=0), ## must be 0 beyond 10m
									  data.frame(min.x=0,max.x=0,min.y=0,max.y=0), ## must be 0 at 0m
									  ## ideal is between 2 and 15m inclusive
									  data.frame(min.x=4,max.x=Inf,min.y=NA,max.y=0.7), ## must be less than "ideal" for >=3m
									  data.frame(min.x=0,max.x=0.5,min.y=NA,max.y=0.7), ## must be less than "ideal" for <=1m
									  ## totally unsuitable can only be in <1m and >15m (exclusive)
									  data.frame(min.x=1,max.x=3,min.y=0.1,max.y=NA) ##must be better than "totally unsuitable" between 1m and 3m inclusive
									  )
pref.monoton$LGMS_gwlevel.csv <- rbind(
									data.frame(min.x=0,max.x=1,dir=1,min.step=0), ##must go up/steady untill 1m
									data.frame(min.x=3,max.x=Inf,dir=-1,min.step=0) ## must go down/steady after 3m
									) 
pref.smooth$LGMS_gwlevel.csv<-data.frame(min.x=0,max.x=Inf,min.step=-0.9/1,max.step=0.9/1) ##


## all RR
pref.bounds$RRGRR_gwlevel.csv <- pref.bounds$RRGWRR_gwlevel.csv <- pref.bounds$WCRR_gwlevel.csv <- pref.bounds$LGRR_gwlevel.csv<- pref.bounds$BBRR_gwlevel.csv <-rbind(
									data.frame(min.x=3,max.x=Inf,min.y=0,max.y=0), ## must be 0 beyond 3m
									  ## ideal is between 0 and 2m inclusive
									  data.frame(min.x=2,max.x=Inf,min.y=NA,max.y=0.9), ## must be less than "ideal" for >=2m
									  ## totally unsuitable can only be in <1m and >15m (exclusive)
									  data.frame(min.x=0,max.x=2,min.y=0.1,max.y=NA) ##must be better than "totally unsuitable" between 0m and 2m inclusive
									  )
pref.monoton$RRGRR_gwlevel.csv <- pref.monoton$RRGWRR_gwlevel.csv <- pref.monoton$WCRR_gwlevel.csv <- pref.monoton$LGRR_gwlevel.csv<- pref.monoton$BBRR_gwlevel.csv <-rbind(
									data.frame(min.x=0,max.x=3,dir=-1,min.step=0) ##must go down/steady until 2m
									) 


all.diffs <- vary_all(scen="Pre90",baseline="Post90",ecospecies=specieslist,
                      use.durs=c(T,F),do.par=T,calc.mean = TRUE,
                      attribs.usesduration=attribs.usesduration.gwonly,
                      assets=1:nrow(asset.table),getSeqCtfs=getSeqCtfs10 #gw run ctf irrelevant
                      )

## Show unique preference curves used					  
# devAskNewPage(T)
# par(mfrow=c(4,4))
# plot.unique.prefs(all.diffs,attrib="gwlevel",NA)		  



### Model 3. sw, gw and weight
weight.comp <- list()
weight.bounds<-list()
# for RRGMS and LGMS, duraiton is more important than timing and dry period. timing and dry can be zero. 
weight.comp$RRGMS <- weight.comp$RRGWMS <- weight.comp$LGMS<- data.frame(a="duration",
                                 b=c("timing","dry"),
                                 status=">=",min.gap=0.05)
# weight.comp$RRGRR <- weight.comp$RRGWRR <- data.frame(a="duration",
                                 # b=c("timing"),
                                 # status=">=",min.gap=0.05)	
								 
# for RRGRR, both timing and duration are important.
weight.bounds$RRGRR <- weight.bounds$RRGWRR<-rbind(data.frame(a="timing",min=0.3,max=NA),
										data.frame(a="duration",min=0.3,max=NA))										

#for WCMS, timing is critical but duration and dry period cannot be completely neglected.										
weight.comp$WCMS <- data.frame(a="timing",
                                 b=c("duration","dry"),
                                 status=">=",min.gap=0.05)
				 
weight.bounds$WCMS <- rbind(data.frame(a="duration",min=0.1,max=NA),
										data.frame(a="dry",min=0.1,max=NA))		
								 								 
#WCRR no weight constraints found.	
	
#for LGRR, timing is more critical than duraiton, but duration cannot be completely neglected.
weight.comp$LGRR <- data.frame(a="timing", b=c("duration"),status=">=",min.gap=0.05)	
weight.bounds$LGRR <- data.frame(a="duration",min=0.1,max=NA)

weight.bounds<-list()
for(s in specieslist) weight.bounds[[s]]<-  data.frame(a="gwlevel",min=NA,max=0.5)


all.diffs <- vary_all(scen="Pre90",baseline="Post90",ecospecies=specieslist,
                      use.durs=c(T,F),do.par=T,calc.mean = TRUE,
                      attribs.usesduration=attribs.usesduration,
                      assets=1:nrow(asset.table),getSeqCtfs=getSeqCtfsNew#getSeqCtfs10
                      )
					  

 
################################################################################
## Check pref and constraints
xx=envindex.diff.qp(scen="Pre90",baseline="Post90",ecospecies="RRGMS",assetid=1,ctf=3000,calc.mean = TRUE,attribs.usesduration=attribs.usesduration.nogw, use.durs=TRUE)
plot.envindex.bound<-
function (x, y, ..., attribs = NA, subset = T, main = NULL, xlabb=capwords(attrib), ylabb="Preference") 
{
    if (!exists("getPrefConstraints")) {
        warning("function getPrefConstraints not set, using getPrefConstraintsMultIndex")
        assign("getPrefConstraints", getPrefConstraintsMultIndex, 
            env = .GlobalEnv)
    }
    e <- substitute(subset)
    x <- x[sapply(x, function(o) {
        r <- eval(e, o, parent.frame())
        r <- r & !is.na(r)
    })]
    wanted.attribs <- attribs
    wanted.main <- main
    for (o in x) {
        if (is.na(wanted.attribs)) 
            attribs <- names(o$pars.min.weights)
        for (attrib in attribs) {
            cpt <- index.all[[sprintf("%s_%s.csv", o$species, 
                attrib)]]
            if (is.null(cpt)) 
                next
            constr <- getPrefConstraints(o$species, attrib)
            plot(cpt[, 1], o[[sprintf("pars.min.%s", attrib)]], 
                type = "l", col = red(), ylab = ylabb, 
                ylim = c(0, 1), xlab = xlabb, lty = "dashed", 
                lwd = 3)
            polygon(x = c(cpt[, 1], rev(cpt[, 1])), y = c(constr$bounds$upper, 
                rev(constr$bounds$lower)), col = grey(0.9), border = NA)
            lines(cpt[, 1], o[[sprintf("pars.min.%s", attrib)]], 
                type = "l", col = red(), lty = "dashed", lwd = 3)
            lines(cpt[, 1], o[[sprintf("pars.max.%s", attrib)]], 
                type = "l", col = green(), lty = "dotted", lwd = 3)
            abline(v = cpt[, 1], lty = "dashed", col = "grey")
            if (is.null(wanted.main)) 
                main <- sprintf("%s %s\n%s", o$species, attrib, 
                  ifelse(o$use.dur, "As average of event", "As total for event"))
            title(main = main)
        }
    }
}

tiff(filename = "constr_duration.tif",width =5, height = 5, units = "in", pointsize = 10, res=500)
plot(xx, attribs="duration", xlabb="Flood duration (days)", ylabb="Suitability index", main="")
dev.off()

tiff(filename = "constr_timing.tif",width =5, height = 5, units = "in", pointsize = 10, res=500)
plot(xx, attribs="timing", xlabb="Flood timing (month)", ylabb="Suitability index", main="")
dev.off()


what.weights(xx)
 
showPrefConstraintsLists("RRGMS","duration")
getPrefConstraints("RRGMS","duration")

## get pref curve constraints graph
devAskNewPage(T)
pdf("prefcurves_noweight.pdf")
#par(mfrow=c(4,4))
plot.unique.prefs(subset(all.diffs, species=="RRGMS" & assetid==1),attrib="duration",NA)
dev.off()

what.weights(subset(all.diffs,assetid==1 & species=="LGRR"))

## for gw grey area example
xx=envindex.diff.qp(scen="Pre90",baseline="Post90",ecospecies="RRGMS",assetid=1,ctf=3000,calc.mean = TRUE,attribs.usesduration=attribs.usesduration.gwonly, use.durs=TRUE)
plot.envindex.bound<-
function (x, y, ..., attribs = NA, subset = T, main = NULL, xlabb=capwords(attrib), ylabb="Preference") 
{
    if (!exists("getPrefConstraints")) {
        warning("function getPrefConstraints not set, using getPrefConstraintsMultIndex")
        assign("getPrefConstraints", getPrefConstraintsMultIndex, 
            env = .GlobalEnv)
    }
    e <- substitute(subset)
    x <- x[sapply(x, function(o) {
        r <- eval(e, o, parent.frame())
        r <- r & !is.na(r)
    })]
    wanted.attribs <- attribs
    wanted.main <- main
    for (o in x) {
        if (is.na(wanted.attribs)) 
            attribs <- names(o$pars.min.weights)
        for (attrib in attribs) {
            cpt <- index.all[[sprintf("%s_%s.csv", o$species, 
                attrib)]]
            if (is.null(cpt)) 
                next
            constr <- getPrefConstraints(o$species, attrib)
            plot(cpt[, 1], o[[sprintf("pars.min.%s", attrib)]], 
                type = "l", col = grey(0.9), ylab = ylabb, 
                ylim = c(0, 1), xlab = xlabb, lty = "dashed", 
                lwd = 3, xlim=c(0,20))
            polygon(x = c(cpt[, 1], rev(cpt[, 1])), y = c(constr$bounds$upper, 
                rev(constr$bounds$lower)), col = grey(0.9), border = NA)
            # lines(cpt[, 1], o[[sprintf("pars.min.%s", attrib)]], 
                # type = "l", col = red(), lty = "dashed", lwd = 3)
            # lines(cpt[, 1], o[[sprintf("pars.max.%s", attrib)]], 
                # type = "l", col = green(), lty = "dotted", lwd = 3)
            abline(v = cpt[, 1], lty = "dashed", col = "grey")
            if (is.null(wanted.main)) 
                main <- sprintf("%s %s\n%s", o$species, attrib, 
                  ifelse(o$use.dur, "As average of event", "As total for event"))
            title(main = main)
        }
    }
}
plot(xx, xlabb="Groundwater level (m below ground)", ylabb="Suitability index", main="")


##################################################################################################
## Visualisation

tab <- do.call(rbind,lapply(subset(all.diffs,subset=!is.na(diff.min)),
                            function(r) as.data.frame(r[c("assetid","ctf","species","diff.min","diff.max","use.dur")])))
## Convert to long form
tabm <- melt(tab,id.var=c("assetid","ctf","species","use.dur"))
## Convert continuous variable to discrete - which scenario is favoured
tabm$value[abs(tabm$value)<0.01] <- NA ## treat zero as ambiguous
#tabm$value <- ifelse(tabm$value>0,"Scenario or =","Baseline or =")
tabm$value <- ifelse(tabm$value>0,"Pre90 or the same","Post90 or the same")

## Check for uncertainty
##answers <- marginalise(tabm,assetid+species+ctf~.,verbose=T)
answers<-marginalise(tabm,assetid+species+ctf~.,verbose=T,na.rm=TRUE) ## treat zero as ambiguous
#answers<-marginalise(tabm,assetid+species+ctf+use.dur~.,verbose=T, na.rm=TRUE) 

## Treat NAs as zero
answers$"(all)"<-as.character(answers$"(all)")
answers$"(all)"[is.na(answers$"(all)")]<-"No difference"

## Plot from viz_vary_all.R

## Make variables more readable, and ordered
answers$assetid <- ordered(answers$assetid,level=1:nrow(asset.table),label=asset.table$Name)
#answers$"(all)" <- ordered(answers$"(all)",level=c("Scenario or =","Uncertain","Baseline or =","Same"))
answers$"(all)" <- ordered(answers$"(all)",level=c("Pre90 or the same","Uncertain","Post90 or the same","No difference"))
lookup <- c("RRGMS"="River red gum MS",
            "RRGRR"="River red gum RR",
			"RRGWMS" = "River red gum woodland MS",
			"RRGWRR"="River red gum woodland RR",
            "BBMS"="Black box MS",
            "BBRR"="Black box RR",
            "LGMS"="Lignum MS",
            "LGRR"="Lignum RR",
            "WCMS"="Water couch MS",
            "WCRR"="Water couch RR"
            )
## lookup <- c("RRGMS"="River red gum\nMaintenance\nand survival",
##             "RRGRR"="River red gum\nRegeneration\nand reproduction",
##             "BBMS"="Black box\nMaintenance\nand survival",
##             "BBRR"="Black box\nRegeneration\nand reproduction",
##             "LGMS"="Lignum\nMaintenance\nand survival",
##             "LGRR"="Lignum\nRegeneration\nand reproduction",
##             "WCMS"="Water couch\nMaintenance\nand survival",
##             "WCRR"="Water couch\nRegeneration\nand reproduction"
##             )
answers$species <- lookup[as.character(answers$species)]

## Convert CTF levels from asset.table for comparison
all.ctf <- melt(asset.table[,3:6])
names(all.ctf) <- c("assetid","variable","value")

##answers <- subset(answers,assetid %in% c("Barbers lagoon","Gunnedah"))


##  Answer for each ctf, species & asset with ctf overlain

tiff(filename = "traffic plot.tif",width = 9.5, height = 6, units = "in", pointsize = 11, res=500)
#ggplot(data=subset(answers,use.dur==TRUE))+
ggplot(data=answers)+
  facet_wrap(~assetid,scale="free")+
  geom_point(aes(y=species,x=ctf,col=get("(all)")),size=3)+
         scale_color_manual(name="Which period\nis better",
                            values=c(
                            #Plus
                            "Pre90 or the same"=green(),
                            #Uncertain
                            "Uncertain"=grey(0.9),#rgb(241,242,241,maxColorValue=255),
                            #Minus
                            "Post90 or the same"=red(),
							# Zero
							"No difference"="lemonchiffon"
                            ))+
    ylab("Species")+
    xlab("Commence-to-flood level (ML/day)")+
	theme_bw()+
	theme(legend.position=c(.8,0.1))+
    ##TODO: ggplot can't set breaks for each panel?
    ##scale_x_continuous(breaks=seq(2000,20000,by=2000))+
    geom_vline(aes(xintercept=value),
               data=subset(all.ctf,assetid %in% unique(answers$assetid)),linetype="dashed")

dev.off()



## for Fig8:
nowt<-read.csv("answers.noweight.csv")
wwt<-read.csv("answers.withweight.csv")
answersm<-merge(nowt,wwt, by=c("assetid", "species", "ctf"))
changed=subset(answersm,X.all..x!=X.all..y)


tiff(filename = "traffic plot changed.tif",width = 9.5, height = 6, units = "in", pointsize = 11, res=500)
#ggplot(data=subset(answers,use.dur==TRUE))+
ggplot(data=answers)+
  facet_wrap(~assetid,scale="free")+
  geom_point(aes(y=species,x=ctf),col="yellow",size=5,data=changed)+
  ##geom_point(aes(y=species,x=ctf,col=X.all..x),size=5,data=changed)+ #show previous colour in bg (all grey)
  geom_point(aes(y=species,x=ctf,col=get("(all)")),size=3)+
         scale_color_manual(name="Which period\nis better",
                            values=c(
                            #Plus
                            "Pre90 or the same"=green(),
                            #Uncertain
                            "Uncertain"=grey(0.9),#rgb(241,242,241,maxColorValue=255),
                            #Minus
                            "Post90 or the same"=red(),
							# Zero
							"No difference"="lemonchiffon"
                            ))+
    ylab("Species")+
    xlab("Commence-to-flood level (ML/day)")+
	theme_bw()+
	theme(legend.position=c(.8,0.1))+
    ##TODO: ggplot can't set breaks for each panel?
    ##scale_x_continuous(breaks=seq(2000,20000,by=2000))+
    geom_vline(aes(xintercept=value),
               data=subset(all.ctf,assetid %in% unique(answers$assetid)),linetype="dashed")

dev.off()
			   
			   
############################################################################			   
### plot for Model 2, gw only
tab <- do.call(rbind,lapply(subset(all.diffs,subset=!is.na(diff.min)),
                            function(r) as.data.frame(r[c("assetid","ctf","species","diff.min","diff.max","use.dur")])))
## Convert to long form
tabm <- melt(tab,id.var=c("assetid","ctf","species","use.dur"))
## Convert continuous variable to discrete - which scenario is favoured
tabm$value[abs(tabm$value)<0.01] <- NA ## treat zero as ambiguous
#tabm$value <- ifelse(tabm$value>0,"Scenario or =","Baseline or =")
tabm$value <- ifelse(tabm$value>0,"Pre90 or the same","Post90 or the same")

## Check for uncertainty
##answers <- marginalise(tabm,assetid+species+ctf~.,verbose=T)
answers<-marginalise(tabm,assetid+species+ctf~.,verbose=T,na.rm=TRUE) ## treat zero as ambiguous
#answers<-marginalise(tabm,assetid+species+ctf+use.dur~.,verbose=T, na.rm=TRUE) 

## Treat NAs as zero
answers$"(all)"<-as.character(answers$"(all)")
answers$"(all)"[is.na(answers$"(all)")]<-"No difference"

## Plot from viz_vary_all.R

## Make variables more readable, and ordered
answers$assetid <- ordered(answers$assetid,level=1:nrow(asset.table),label=asset.table$Name)
#answers$"(all)" <- ordered(answers$"(all)",level=c("Scenario or =","Uncertain","Baseline or =","Same"))
answers$"(all)" <- ordered(answers$"(all)",level=c("Pre90 or the same","Uncertain","Post90 or the same","No difference"))
lookup <- c("RRGMS"="River red \ngum MS",
            "RRGRR"="River red \ngum RR",
			"RRGWMS" = "River red gum \nwoodland MS",
			"RRGWRR"="River red gum \nwoodland RR",
            "BBMS"="Black \nbox MS",
            "BBRR"="Black \nbox RR",
            "LGMS"="Lignum \nMS",
            "LGRR"="Lignum \nRR",
            "WCMS"="Water \ncouch MS",
            "WCRR"="Water \ncouch RR"
            )
## lookup <- c("RRGMS"="River red gum\nMaintenance\nand survival",
##             "RRGRR"="River red gum\nRegeneration\nand reproduction",
##             "BBMS"="Black box\nMaintenance\nand survival",
##             "BBRR"="Black box\nRegeneration\nand reproduction",
##             "LGMS"="Lignum\nMaintenance\nand survival",
##             "LGRR"="Lignum\nRegeneration\nand reproduction",
##             "WCMS"="Water couch\nMaintenance\nand survival",
##             "WCRR"="Water couch\nRegeneration\nand reproduction"
##             )
answers$species <- lookup[as.character(answers$species)]

## Convert CTF levels from asset.table for comparison
all.ctf <- melt(asset.table[,3:6])
names(all.ctf) <- c("assetid","variable","value")


answers<-unique(subset(answers,select=-ctf))
## Traffic light plot

tiff(filename = "gw only result.tif",width =7.7, height = 3.1, units = "in", pointsize = 10, res=500)
ggplot(data=answers)+
  geom_tile(aes(y=assetid,x=species,fill=get("(all)")))+
         scale_fill_manual(name="Which period\nis better",
						values=c(
                            "Pre90 or the same"=green(),
                            #Uncertain
                            "Uncertain"=grey(0.9),#rgb(241,242,241,maxColorValue=255),
                            #Minus
                            "Post90 or the same"=red(),
							# Zero
							"No difference"="lemonchiffon"
                             ))+
	theme_bw()+
	xlab("Species")+
    ylab("Assets")
dev.off()	


##Alternatively if you want separate facetted plots for use.dur
# ggplot(data=answers)+
  # geom_tile(aes(y=assetid,x=species,fill=get("(all)")))+
  # facet_wrap(~use.dur)+
         # scale_fill_manual(values=c(
                      # "Plus"=rgb(0,146,70,maxColorValue=255),
                      # "Uncertain"=rgb(241,242,241,maxColorValue=255),
                      # "Minus"=rgb(206,43,55,maxColorValue=255)
                             # ))

							 
########################################################
## Hydrology
get.hydrol.ts=function(scenario,assetid){
 bore <- asset.table$Bore[assetid]
      gauge <- asset.table[assetid, 2]
	     gwlevel <- all.hydroinputlist[[scenario]]$gwlevel.csv[, 
            as.character(bore)]
        surfaceflow <- all.hydroinputlist[[scenario]][[paste(gauge, 
            ".csv", sep = "")]][, 1]
        combined <- list(gwlevel = gwlevel, surfaceflow = surfaceflow, 
            baseflow = all.hydroinputlist[[scenario]][[paste(gauge, 
                ".csv", sep = "")]]$Baseflow, all = F)
        combined <- do.call(cbind.zoo, combined[!sapply(combined, 
            is.null)])
        coredata(combined)[!complete.cases(combined), ] <- NA
        if (!is.null(gwlevel) && !identical(index(gwlevel), index(surfaceflow))) {
            warning(sprintf("In %s with assetid %d gwlevel and surfaceflow time periods do not match, automatically trimming\nNew time range %s to %s", 
                scenario, assetid, min(index(combined)), max(index(combined))))
        }
		combined
}

annualflow<-data.frame()
for (i in 1: length(asset.table[,1])){
	annualflow[i,1] <- sum(na.omit(get.hydrol.ts("Pre90",i)$surfaceflow))/length(get.hydrol.ts("Pre90",i)$surfaceflow)*365/1000
	annualflow[i,2] <- sum(na.omit(get.hydrol.ts("Post90",i)$surfaceflow))/length(get.hydrol.ts("Post90",i)$surfaceflow)*365/1000
}
annualflow <- round(annualflow,2)
round(annualflow$V1/annualflow$V2,2)

xyplot(get.hydrol.ts("Post90",7))
xyplot(rbind(get.hydrol.ts("Pre90",1),get.hydrol.ts("Post90",1)))

pdf("seasonal flow.pdf")
for (i in 1:length(asset.table[,1])){
hydropre <- as.data.frame(get.hydrol.ts("Pre90",i))
hydropre$Date <- as.Date(row.names(hydropre))
hydropre$Month <- as.POSIXlt(hydropre$Date)$mon+1
hydropre$Period <- "Pre90"
hydropost <- as.data.frame(get.hydrol.ts("Post90",i))
hydropost$Date <- as.Date(row.names(hydropost))
hydropost$Month <- as.POSIXlt(hydropost$Date)$mon+1
hydropost$Period <- "Post90"
hydroall <- rbind(hydropre, hydropost)
hydroall$Asset <- paste("Asset",i,sep="")
p <- ggplot(subset(hydroall, surfaceflow > asset.table[i,7]), aes(factor(Month), surfaceflow)) +geom_boxplot(aes(fill = factor(Period)))
print(p)
}
dev.off()



gwlevel=do.call(rbind,c(lapply(1:nrow(asset.table),function(assetid) data.frame(assetid=assetid,Period="Pre90",gwlevel=coredata(get.hydrol.ts("Pre90",assetid)$gwlevel))),
lapply(1:nrow(asset.table),function(assetid) data.frame(assetid=assetid,Period="Post90",gwlevel=coredata(get.hydrol.ts("Post90",assetid)$gwlevel)))
))

gwlevel$assetid <- ordered(gwlevel$assetid,level=1:nrow(asset.table),label=asset.table$Name)

gwpre <- aggregate(gwlevel ~ assetid, data=subset(gwlevel, Period=="Pre90"), FUN=mean)
gwpost <- aggregate(gwlevel ~ assetid, data=subset(gwlevel, Period=="Post90"), FUN=mean)
gwpost-gwpre


tiff(filename = "groundwater.tif",width = 8.5, height = 6, units = "in", pointsize = 10, res=500)
ggplot(data=gwlevel)+
geom_density(aes(x=gwlevel,col=Period,y = ..scaled..))+
facet_wrap(~assetid)+
theme_bw() +
xlab("Groundwater level (m)") + 
ylab("Density")+
theme(legend.position=c(.9,0.1))
dev.off()

##plot(ppoints(5401),fdc.allpoints(na.omit(coredata(get.hydrol.ts("Pre90",1)$surfaceflow))),log="y")

# fdc=do.call(rbind,c(lapply(1:nrow(asset.table),function(assetid) {
# flow=na.omit(coredata(get.hydrol.ts("Pre90",assetid)$surfaceflow))
# data.frame(assetid=assetid,Period="Pre90",prob=ppoints(length(flow)),flow=fdc.allpoints(flow))
# }),
# lapply(1:nrow(asset.table),function(assetid) {
# flow=na.omit(coredata(get.hydrol.ts("Post90",assetid)$surfaceflow))
# data.frame(assetid=assetid,Period="Post90",prob=ppoints(length(flow)),flow=fdc.allpoints(flow))
# })
# ))

# fdc$assetid <- ordered(fdc$assetid,level=1:nrow(asset.table),label=asset.table$Name)

# ggplot(data=fdc)+
# geom_line(aes(x=prob,y=flow,col=Period))+
# facet_wrap(~assetid,scale="free_y")+
# scale_y_log10()


### flow duraton curves

fdc2=do.call(rbind,c(lapply(1:nrow(asset.table),function(assetid) {
flow=na.omit(coredata(get.hydrol.ts("Pre90",assetid)$surfaceflow))
df=data.frame(assetid=assetid,Period="Pre90",prob=ppoints(length(flow)),flow=fdc.allpoints(flow))
df=subset(df,flow<asset.table[assetid,"CTF_high"])
df
}),
lapply(1:nrow(asset.table),function(assetid) {
flow=na.omit(coredata(get.hydrol.ts("Post90",assetid)$surfaceflow))
df=data.frame(assetid=assetid,Period="Post90",prob=ppoints(length(flow)),flow=fdc.allpoints(flow))
df=subset(df,flow<asset.table[assetid,"CTF_high"])
df
})
))
fdc2$assetid <- ordered(fdc2$assetid,level=1:nrow(asset.table),label=asset.table$Name)


tiff(filename = "flow duration curve.tif",width = 8.5, height = 6, units = "in", pointsize = 10, res=500)
ggplot(data=fdc2)+
geom_line(aes(y=prob,x=flow,col=Period))+
facet_wrap(~assetid,scale="free_x")+
    geom_vline(aes(xintercept=value),
               data=subset(all.ctf,assetid %in% unique(answers$assetid)),linetype="dashed")+
theme_bw()+
xlab("Flow (ML/day)") +
ylab("Exceedance Probability") +
theme(legend.position=c(.9,0.1))
dev.off()

			   
			   
			   
totalflow <- aggregate(flow ~ Period + assetid, data=fdc2, FUN=sum)
totalflow$flow <- round(totalflow$flow/1000, 0)
totalflow


############################################################################

species="RRGMS"
attrib="duration"
# index.all[[sprintf("%s_%s.csv", species, 
                # attrib)]]<-index.all[[sprintf("%s_%s.csv", species, 
                # attrib)]][-nrow(index.all[[sprintf("%s_%s.csv", species, 
                # attrib)]]),]
getPrefConstraints=getPrefConstraintsMultIndex
library(RColorBrewer)
pal=brewer.pal(7,"Accent")



            cpt <- index.all[[sprintf("%s_%s.csv", species, 
                attrib)]]
            constr <- getPrefConstraints(species, attrib)
            plot(cpt[, 1], rep(NA,nrow(cpt)), 
                type = "l", col = grey(0.9),
                ylim = c(0, 1),  lty = "dashed", 
				xlab="Flood duration (days)",ylab="Suitability index",
                lwd = 3)
            polygon(x = c(cpt[, 1], rev(cpt[, 1])), y = c(constr$bounds$upper, 
                rev(constr$bounds$lower)), col = grey(0.9), border = NA)
				#for(i in 2:ncol(cpt)) lines(cpt[, 1], cpt[,i],type = "l")
				#for(i in 2:ncol(cpt)) curve(approx.fun(cpt[, 1], cpt[,i]),from=min(cpt[,1]),to=max(cpt[,1]))
for(i in 2:ncol(cpt)) lines(approx(cpt[, 1], cpt[,i]),col=pal[i],lwd=2)
            abline(v = cpt[, 1], lty = "dashed", col = "grey")
			#text(a<-locator(1),labels="e.g. monotonicity constraint:\nfrom 200 days onwards,\n all curves agree that suitability\n is decreasing or steady")

text(list(x = 548.73786407767, y = 0.832834101382488),labels="e.g. monotonicity constraint:\nfrom 200 days onwards,\n all curves agree that suitability\n is decreasing or steady")
