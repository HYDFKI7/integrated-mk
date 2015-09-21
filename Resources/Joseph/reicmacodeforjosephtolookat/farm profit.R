## Linear programming model
## Maximise yield*area-pumping.cost by selecting area of each activity and volume of each water source
## Subject to constraints on area,volume and water availability

## Transpose matrices so that indexing remains the same
CropId <- t(read.csv("CropId.csv",header=FALSE))
rownames(CropId) <- c("activity.id","crop.id","rotation.proportion","irrig.level","Irrig")

## TODO: should all be by region
OFSInit
GWShare
RegShare
UnregShare
LandInit <- 54707

## 2: crop number in Yields & Prices
## 4: irrig level in Yields
## 5: irrigated/dryland/grazing
Years <- 5
EffInit <- matrix(0.65,ncol=1,nrow=3)
DamCoeff <- 0.645
Yields <- t(read.csv("Yields.csv",header=FALSE))
rownames(Yields) <- c("crop.id","irrig.level",sprintf("y%02d",1:Years))
Prices <- t(read.csv("_Prices.csv",header=FALSE))
rownames(Prices) <- c("crop.id","price","cost")
CropWaterUse <- t(read.csv("CropWaterUse.csv",header=FALSE))
rownames(CropWaterUse) <- c(sprintf("y%02d",1:Years))
Discount <- t(read.csv("_Discount.csv",header=FALSE)) ##TODO: calculate instead
UnregPrice <- 40
GWPrice <- 75
RegPrice <- 40
OneYearUnreg <- 1.25

## TODO: TEMP
crop.names <- c("Irrigated cotton lint",
                "Irrigated cotton seed",
                "Dryland cotton lint",
                "Dryland cotton seed",
                "Dryland Wheat",
                "Dryland Sorghum",
                "Continuous cotton lint",
                "Continuous cotton seed",
                "Faba bean"
                )
colnames(Yields) <- crop.names
colnames(CropWaterUse) <- crop.names
colnames(Prices) <- crop.names
CropId2 <- as.data.frame(t(CropId))
CropId2$Crop1 <- factor(CropId2[,"Crop1"],levels=1:length(crop.names),labels=crop.names)

# assuming no grazing or cultivation outside areas laid out to irrigation
TotalArea=LandInit;
CultArea=LandInit;

## Maximum activity id/ Number of activities
## bigm=0;	
## for(i in 1:ncol(CropId)){ ##TODO: 34

##   if (bigm<CropId[1,i])
##     {
##       bigm=CropId[1,i];
##     }
## }
bigm=CropId[1,i]

## create all local and output variables
Crops <- matrix(0,nrow=6,ncol=ncol(CropId))
Returns <- matrix(0,nrow=(bigm+4)*Years,ncol=1)
rownames(Returns) <- 1:nrow(Returns)
D <- matrix(0,nrow=bigm,ncol=Years)
CreateMatrix(Coeffs,(bigm+4)*_Years,_Years,DOUBLEPRECISION,ERASE);
C <- matrix(0,nrow=bigm,ncol=Years)
CreateMatrix(Area,_Years,bigm+1,DOUBLEPRECISION,ERASE);
CreateMatrix(Unreg_use,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(Unreg_Extract,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(Reg_use,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(GW_use,_Years,1,DOUBLEPRECISION,ERASE);
Constraints <- matrix(0,nrow=(bigm+4)*Years+2,ncol=10*Years-5)
rownames(Constraints) <- 1:nrow(Constraints)
colnames(Constraints) <- 1:ncol(Constraints)
CreateMatrix(RegInflow,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(AllReginflow,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(ExtractMax,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(UnregEff,_Years,1,DOUBLEPRECISION,ERASE);
CreateMatrix(MaxTotalProfit,_Years,1,DOUBLEPRECISION,ERASE);

##TODO: NEW
Code <- matrix(0,nrow=11,ncol=1)
  	
ubefore=0;

UnregEff=EffInit[1,1]*DamCoeff;

##construct matrix of crop information using global data on prices
##data format for crops is 
## activity no, yield, price, cost, rotation %, water use.  
## One activity number may be used for several crops in rotation.

##_Prices is global data containing: crop id, price per unit output, variable cost per unit area (not water)
## Crop codes are as follows:
##Irrigated cotton lint	1
##Irrigated cotton seed	2
##Dryland cotton lint	3
##Dryland cotton seed	4
##Dryland Wheat	5
##Dryland Sorghum	6
##Continuous cotton lint	7
##Continuous cotton seed	8
##Faba bean	9
##Cotton lint with FB	10
##Cotton seed with FB	11
##Lucerne	12	
## Calculate per hectare water use each year for each activity

for(f in 1:Years){
  
  ## Obtain returns and water use matrix for each activity for this year
  for(j in 1:ncol(CropId)){
    ## activity id
    k=CropId[1,j];
    y=0;
    w=0;
    Code[k,1]=CropId[5,j]; ## is code for irrigated (=1), dryland crop (=2) or grazing (=3) NOTE: this overwritess for all crops within a rotation so will be equal to the last of these.
    ## find yield and water use value for crop
    ## K is matched Yield column for the crop number
    for(s in 1:ncol(Yields)){
      if ((CropId[2,j]==Yields[1,s])&&(CropId[4,j]==Yields[2,s]))
        {K=s;}
    }
    ##p is matched Prices column for the crop number
    for(t in 1:ncol(Prices)){
      if (CropId[2,j]==Prices[1,t])
        {
          p=t; ## Note irrigated and dryland crops are given different crop numbers
        }
    }
    ## create returns and water use matrix
    ##D[(f-1)*bigm+k,1]=D[(f-1)*bigm+k,1]+(Yields[2+f,K]*Prices[2,p]-Prices[3,p])*CropId[3,j]*Discount[f,1];
    D[k,f]=D[k,f]+(Yields[2+f,K]*Prices[2,p]-Prices[3,p])*CropId[3,j];
    C[k,f]=C[k,f]+CropWaterUse[f,K]*CropId[3,j];	
  }

  
  for(m in 1:bigm){ ##For each activity
    ## Assign discounted return rounded to cents
    B1=D[m,f]*Discount[f,1];	
    Returns[(f-1)*bigm+m,1]=round(B1*100)/100;
    
    ##/ irrigated land constraint - excludes dryland cultivation and grazing areas
    if (Code[m,1]<=2){Constraints[(f-1)*bigm+m,f]=1 } ## sum of dryland crop and irrigated areas in each year is less than area laid out to irrigation
    Constraints[(f-1)*bigm+m,Years+f]=round(C[m,f]*100)/100; ## sum of areas times water use by crop minus water decided upon from all sources is less than zero
  }
  rownames(Returns)[(f-1)*bigm+1:bigm] <- sprintf("area.A%d",1:bigm)
  rownames(Constraints)[(f-1)*bigm+1:bigm] <- sprintf("Y%d.A%d",f,1:bigm)
  colnames(Constraints)[f]=sprintf("area.constraint.y%d",f)
  colnames(Constraints)[Years+f]=sprintf("water.constraint.y%d",f)

  ## Price of water sources
  B2=UnregPrice*Discount[f,1];
  Returns[Years*(bigm+1)+f,1]=-round(B2*100)/100;## price is attributed to extraction not use for unreg
  B3=GWPrice*Discount[f,1];
  Returns[Years*(bigm+2)+f,1]=-round(B3*100)/100;  ## cost of groundwater extraction
  B4=RegPrice*Discount[f,1];
  Returns[Years*(bigm+3)+f,1]=-round(B4*100)/100; ## cost of reg extraction
  
  ## create constraints matrix - decision variables are area for each crop option in each year, unreg use in each year
  ## unreg extraction in each year, groundwater extraction in each year, regulated extraction in each year
	
  rownames(Constraints)[(bigm+4)*Years+1:2] <- c("direction","value")
  rownames(Constraints)[Years*(bigm+1)+f] <- sprintf("water.Unreg.y%02d",f)
  rownames(Constraints)[Years*(bigm+2)+f] <- sprintf("water.GW.y02%d",f)
  rownames(Constraints)[Years*(bigm+3)+f] <- sprintf("water.Reg.y02%d",f)

  ## land constraint (Years rows)
  Constraints[(bigm+4)*Years+1,f]=-1;
  Constraints[(bigm+4)*Years+2,f]=LandInit;## land constraint
  ## water constraint	(Years rows)
  Constraints[bigm*Years+f,f+Years]=-EffInit[1,1];  ## unreg use coefficient is efficiency of irrigation method (NOT including dam losses) in appropriate year, zero otherwise
  Constraints[(bigm+2)*Years+f,f+Years]=-EffInit[3,1];  ## gw coefficient is gw efficiency in appropriate year, zero otherwise
  Constraints[(bigm+3)*Years+f,f+Years]=-EffInit[2,1]; ## reg use coefficient is reg efficiency in appropriate year, zero otherwise
  Constraints[(bigm+4)*Years+1,f+Years]=-1; ## less than or equal to
  Constraints[(bigm+4)*Years+2,f+Years]=0; ## water constraint - ie. demand minus use is less than zero (demand is less than use)

                    
############UNREG use and extraction constraints
  ## one year extraction rule for unreg (Years rows)
  Constraints[(bigm+1)*Years+f,f+2*Years]=1;  ## unreg extraction coefficient is 1 in appropriate year, zero otherwise
  Constraints[(bigm+4)*Years+1,f+2*Years]=-1;## less than or equal to
  Constraints[(bigm+4)*Years+2,f+2*Years]=min(OneYearUnreg*UnregShare, AnnUnregLimit[f,1]);## limit extraction to minimum of one year rule and feasible extraction limit calculated above
  colnames(Constraints)[f+2*Years] <- sprintf("limit.unreg.1yr.y%02d",f)
  
  ## Use limited to extraction times effective efficiency (calculated above) (Years rows)
  if (OFSInit>0){
    if (f<2){
      Constraints[bigm*Years+1,f+3*Years]=1; ## Extraction minus use must be less than or equal to OFS for all years up to current, minus evap losses. NOTE use here is water that gets sent to the crop so the amount 'used' or sent to the crop is modified by irrigation method efficiency
      Constraints[(bigm+1)*Years+1,f+3*Years]=-DamCoeff^1; ## coefficient on extraction is efficiency calculated above for all years up to current
    } else {
      Constraints[bigm*Years+f,f+3*Years]=1;
      Constraints[(bigm+1)*Years+f,f+3*Years]=-DamCoeff^1
      Constraints[bigm*Years+f-1,f+3*Years]=DamCoeff^1
      Constraints[(bigm+1)*Years+f-1,f+3*Years]=-DamCoeff^2
    }

    Constraints[(bigm+4)*Years+1,f+3*Years]=-1; ## less than or equal to
    Constraints[(bigm+4)*Years+2,f+3*Years]=OFSInit; ## constraint
  } else {
    ## use is extraction if no on-farm storage
    Constraints[bigm*Years+f,f+3*Years]=1; ## coefficient on use is 1 for all years up to current - water sent to crop
    Constraints[(bigm+1)*Years+f,f+3*Years]=-1; ## coefficient on extraction i1 as water sent to crop=water extracted (no storage)
    Constraints[(bigm+4)*Years+1,f+3*Years]=0;  ## equal to
    Constraints[(bigm+4)*Years+2,f+3*Years]=0;  ## constraint
  }
  ## less than or equal to zero (ie. sum of use less than or equal to sum of extraction by efficiency
  colnames(Constraints)[f+3*Years] <- sprintf("limit.unreg.extraction.y%02d",f)
  
  ## three year rule on unregulated use (Years-2 rows)
  if (f<=Years-2){
      Constraints[(bigm+1)*Years+f,f+4*Years]=1;
      Constraints[(bigm+1)*Years+f+1,f+4*Years]=1;
      Constraints[(bigm+1)*Years+f+2,f+4*Years]=1;
      Constraints[(bigm+4)*Years+1,f+4*Years]=-1;
      Constraints[(bigm+4)*Years+2,f+4*Years]=_ThreeYearUnreg*UnregShare;	
    }
  colnames(Constraints)[f+4*Years] <- sprintf("limit.unreg.3yr.y%02d",f)
	
############/ GW use constraints##################/
  ## one year extraction limit
  Constraints[(bigm+2)*Years+f,f+5*Years-2]=1;
  Constraints[(bigm+4)*Years+1,f+5*Years-2]=-1;
  Constraints[(bigm+4)*Years+2,f+5*Years-2]=_GWOneYearLim*GWShare;
  colnames(Constraints)[f+5*Years] <- sprintf("limit.gw.1yr.y%02d",f)
  
  ## carry forward limit - means use is less than fwd limit + share in any year
  Constraints[(bigm+2)*Years+f,f+6*Years-2]=1;
  Constraints[(bigm+4)*Years+1,f+6*Years-2]=-1;
  Constraints[(bigm+4)*Years+2,f+6*Years-2]=(_GWfwdlim+1)*GWShare;
  colnames(Constraints)[f+6*Years] <- sprintf("limit.gw.carryforward.y%02d",f)
  
  ## carry forward limit: cumulative use is always less than cumulative share (Years-1) rows
  if (f<=Years-1){
    for (i=1;i<=f;i++)
      {
        Constraints[(bigm+2)*Years+i,f+7*Years-2]=1;
      }
    Constraints[(bigm+4)*Years+1,f+7*Years-2]=-1;
    Constraints[(bigm+4)*Years+2,f+7*Years-2]=f*GWShare;
  }
  colnames(Constraints)[f+7*Years] <- sprintf("limit.gw.carryforward.y%02d",f)
  
########REG use constraints
  ## one year extraction limit
  Constraints[(bigm+3)*Years+f,f+8*Years-3]=1;
  Constraints[(bigm+4)*Years+1,f+8*Years-3]=-1;
  Constraints[(bigm+4)*Years+2,f+8*Years-3]=_RegOneYearLim*RegShare;
  colnames(Constraints)[f+8*Years] <- sprintf("limit.reg.1yr.y%02d",f)
  
  ## reg three year limit (_years -2 rows)
  if (f<=Years-2){
    Constraints[(bigm+3)*Years+f,f+9*Years-3]=1;
    Constraints[(bigm+3)*Years+f+1,f+9*Years-3]=1;
    Constraints[(bigm+3)*Years+f+2,f+9*Years-3]=1;
    Constraints[(bigm+4)*Years+1,f+9*Years-3]=-1;
    Constraints[(bigm+4)*Years+2,f+9*Years-3]=_RegThreeyearLim*RegShare;
  }
  colnames(Constraints)[f+9*Years] <- sprintf("limit.reg.3yr.y%02d",f)

##########################################################################
  ## Simplex LP algorithm##################################################/
##########################################################################
  ## assumes all constraints are of form <= other than the positivity constraints
  ## ie. no >= or = constraints in problem
  ##column of signs on constraints and of constraints values
  
  m1=0;
  m2=0;
  m3=0;
  
  ## find number of constraints of each type
  for(k in 1:ncol(Constraints)){
    if (Constraints[nrow(Constraints)-1,k]==-1)
      {m1=m1+1;}
    if(Constraints[nrow(Constraints)-1,k]==1)
      {m2=m2+1;}
    if(Constraints[nrow(Constraints)-1,k]==0)
      {m3=m3+1;}
  }
  
  n11=nrow(Constraints)-2;
	
  CreateMatrix(Table,n11+1,m1+m2+m3+2,DOUBLEPRECISION,ERASE);  ## need m across for adding slack variables - one for each <= constraint
  CreateMatrix(Coeffs,nrow(Returns),1,DOUBLEPRECISION,ERASE);

  m=MatrixHeight(Table)-2;
  n=MatrixWidth(Table)-1;

  ## get table into necessary format
  k1=0;
  k2=0;
  k3=0;
  for (i=1;i<=m1+m2+m3;i++){
    if (Constraints[MatrixWidth(Constraints)-1,i]==-1)
      {
        k1=k1+1;
        Table[1,k1+1]=Constraints[MatrixWidth(Constraints),i];
        for (k=1;k<=n11;k++)
          {	Table[k+1,k1+1]=-Constraints[k,i];}
      }
    if (Constraints[MatrixWidth(Constraints)-1,i]==1)
      {
        k2=k2+1;
        Table[1,k2+m1+1]=Constraints[MatrixWidth(Constraints),i];
        for (k=1;k<=n11;k++)
          {	Table[k+1,k2+m1+1]=-Constraints[k,i];}
      }
    if (Constraints[MatrixWidth(Constraints)-1,i]==0)
      {
        k3=k3+1;
        Table[1,k3+m1+m2+1]=Constraints[MatrixWidth(Constraints),i];
        for (k=1;k<=n11;k++)
          {	Table[k+1,k3+m1+m2+1]=-Constraints[k,i];}
      }
  }##each constraint except slack variables
  
  for (k=1;k<=n11;k++){
    Table[k+1,1]=Returns[k,1];
  }

  CreateMatrix(MValues,3,1,INTEGERPRECISION, ERASE);
  MValues[1,1]=m1;
  MValues[2,1]=m2;
  MValues[3,1]=m3;
  
  Result = SimplexLP(MValues, Table, MAXIMISE, FProfit, Coeffs);

  ################################################################################
  TotalReturn=0;
  ##/ find other dryland and grazing areas. Assume highest proftability (of dryland crop and grazing) on CultArea-LandInit, then grazing only on TotArea-CultArea
  CreateMatrix(CultCrop,Years,1,INTEGERPRECISION,ERASE);
  CreateMatrix(GMCult,MatrixWidth(D),Years,DOUBLEPRECISION,ERASE);
  CreateMatrix(AreaCult,Years,MatrixWidth(D)+1,DOUBLEPRECISION,ERASE);
  
  for (f=1;f<=Years;f++){
    MaxGMCult=0;
    for (k=1;k<=MatrixWidth(D);k++)
      {
        if (Code[k,1]==2)
          {
            GMCult[k,f]=D[k,f];
            MaxGMCult=max(MaxGMCult,GMCult[k,f]);
            if (MaxGMCult==GMCult[k,f])
              {CultCrop[f,1]=k;}
          } ## end Code
      }     ## end k
	
    ## check grazing isn't highest GM option
    MaxGMCult=max(GMGrazing,MaxGMCult);
    if (MaxGMCult==GMGrazing)
      {CultCrop[f,1]=MatrixWidth(D)+1;}
	
    ## set area on cultivated land to non laid out to irriation for maximum GM option, otherwise zero
    AreaCult[f,CultCrop[f,1]]=CultArea-LandInit;
  } ## end f

  ## Write out values
  for (f=1;f<=Years;f++){
    for (i=1;i<=bigm;i++){
      if (Coeffs[(f-1)*bigm+i,1]<0.001)
        {		Coeffs[(f-1)*bigm+i,1]=0;}
      Area[f,i]=Coeffs[(f-1)*bigm+i,1]+AreaCult[f,i]; 
      MaxTotalProfit[f,1]=MaxTotalProfit[f,1]+Area[f,i]*Returns[(f-1)*bigm+i,1];
      Area[f,bigm+1]=AreaCult[f,bigm+1]+TotalArea-CultArea; ## this is grazing area
    } ## end for i
    
    MaxTotalProfit[f,1]=MaxTotalProfit[f,1]+Area[f,bigm]*GMGrazing;

    if (Coeffs[Years*bigm+f,1]>=0.001)
      {Unreg_use[f,1]=Coeffs[Years*bigm+f,1];}
    if (Coeffs[Years*(bigm+1)+f,1]>=0.001)
      {Unreg_Extract[f,1]=Coeffs[Years*(bigm+1)+f,1];}
    if (Coeffs[Years*(bigm+2)+f,1]>=0.001)
      {GW_use[f,1]=Coeffs[Years*(bigm+2)+f,1];}
    if (Coeffs[Years*(bigm+3)+f,1]>=0.001)
      {Reg_use[f,1]=Coeffs[Years*(bigm+3)+f,1];}
	
    MaxTotalProfit[f,1]=MaxTotalProfit[f,1]+Unreg_Extract[f,1]*Returns[Years*(bigm+1)+f,1]+GW_use[f,1]*Returns[Years*(bigm+2)+f,1]+Reg_use[f,1]*Returns[Years*(bigm+3)+f,1];
    _AnnualReturn[f,RegionNumber]=MaxTotalProfit[f,1]/_Discount[f,1];

    TotalReturn=_AnnualReturn[f,RegionNumber]+TotalReturn;

    ## find maximum and minimum annual returns for each region
    if (_MaxReturn[RegionNumber,1]<_AnnualReturn[f,RegionNumber])
      {_MaxReturn[RegionNumber,1]=_AnnualReturn[f,RegionNumber];}

    if (_MinReturn[RegionNumber,1]>_AnnualReturn[f,RegionNumber])
      {_MinReturn[RegionNumber,1]=_AnnualReturn[f,RegionNumber];}

    ## Write out global variables for output
    _Unreg_Use[f,RegionNumber]=Unreg_use[f,1];
    _Unreg_Extract[f,RegionNumber]=Unreg_Extract[f,1];
    _GW_Use[f,RegionNumber]=GW_use[f,1];
    _Reg_Use[f,RegionNumber]=Reg_use[f,1];
	
    ## write out reguse for Regulated flow model
    ##_FinalRegUseDam1[f,RegNode]=Reg_use[f,1];

	
  } ## end f

k=RegionNumber;
_RegionReturn[k,1]=TotalReturn/Years;

##_StorageArea[k,1]=StorageArea;
if (_RegionReturn[k,1]!=0){_VarReturn[k,1]=(_MaxReturn[k,1]-_MinReturn[k,1])/_RegionReturn[k,1];}

  ## put your finalising routines here
##/ remove this code - only here to check LP working OK
	##CreateMatrix(Constraints,1,MatrixHeight(Table)-2,BYTEPRECISION,ERASE);
	##CreateMatrix(Evaluate,MatrixWidth(Coeffs),MatrixHeight(Table)-2,DOUBLEPRECISION,ERASE);
	##CreateMatrix(Value,1,MatrixHeight(Table)-2,DOUBLEPRECISION,ERASE);
	##CreateMatrix(ReturnCheck,MatrixWidth(Coeffs),1,DOUBLEPRECISION,ERASE);
##			n=RegionNumber;
##	for (t=1;t<=MatrixHeight(Table)-2;t++)
##	{
	##	for (k=1;k<=MatrixWidth(Coeffs);k++)
	##	{
	##		Evaluate[k,t]=Coeffs[k,1]*Table[k+1,1+t];
	##		Value[1,t]=Evaluate[k,t]+Value[1,t];
	##	}
	##	if (Table[1,t+1]+Value[1,t]>=-0.001)
	##	{Constraints[1,t]=0;}
	##	else
	##	{Constraints[1,t]=1;}
##		_Constraints[n,1]=_Constraints[n,1]+Constraints[1,t];
##}
	##ProfitCheck=0;
 ##   for (k=1;k<=MatrixWidth(Coeffs);k++)
	##	{
	##	ReturnCheck[k,1]=Coeffs[k,1]*Table[k+1,1];
	##	ProfitCheck=ProfitCheck+ReturnCheck[k,1];
	##	}
		
	##	ProfitDiff=FProfit-ProfitCheck;
		

	##	_ProfitDiff[n,1]=Round(ProfitDiff);

  return 0;
}

function Finalisation()
{

  return 0;
}
