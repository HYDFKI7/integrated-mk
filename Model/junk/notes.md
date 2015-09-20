
models
========
'SumFlows.txt'
---------
CREATES A SINGLE INFLOW TIMES SERIES FOR USE IN HYDROLOGY MODEL ADDING UPSTREAM INFLOWS  
      
*    quick 
*    slow
    ->
*    total

'EcolResponse.txt' Baihua Fu 2011
---------
This model calculates the impact of changes in flow on various ecological assests based on the number and length of events above certain threshold flow levels.

    threshold values for low, med, high
    baseflow
    total flow
    annual flow
    cease flow days
    number of days above low, med, high threshold
    number of events above a threshold value, read across low, medium,high
    -> 
    impacts

'RepFarm.txt' Rebecca
---------
    crop types (area, return, yields)
    prices for crop inputs and outputs (optimization)
    SW 
    GW
    rainfall?
    licence rules for SW/ GW


    crops
    returns
    ???
    area
    unreg use
    unreg extraction
    GW use
    contsraints
    max extraction
    unreg max
    max total profit
    ->
    ???

'Delay_model.txt'
---------

'ExtractionLimits.txt' Rebecca Letcher 2004
---------
Taking streamflow time series to produce a yearly water extraction limit.
    
    off-allocation pumping periods and thresholds
    UnregIn
    OtherIn
    unregulated pumping thresholds and daily pumping limits
    unregulated licenced entitlement
    annual limit to off-allocation pumping
    annual declared entitlement. Created by dam model.

    daily calculated limit of unregulated pumping given pumping thresholds
    the annual sum of the daily pumping limits
    annual unregulated extraction limit
    unregulated annual extraction limit, to be passed to production model.
    Off-allocation streamflow

    -> 
    ???


'CropYield.txt'
---------
BASIC CROP MODEL DEVELOPED BY PATRICK HUTCHINGS APRIL 2012

    SoilMoistParam
    MinTemp
    MaxTemp
    Irrig
    C02
    matrix of regression coefficients for all crops, Evapotranspiration, S1, S2, AvTemp

    -> 
    Yield



'SumExtractions.txt'
---------
Code to sum and allocate to days gw and surface water extractions for the post-extraction hydrology

    number of farms
    GW extraction
    unreg extraction
    off A extraction
    Aquifers
    
    ->
    (summed extractions)

'GWSWModel.txt'
---------
Hydrological model of stream and quiafer system considering SW-GW interactions. Rachel Blakers 2012

    surface water f,e,d,vs,tauq,im, area (ihacres)
    rainfall
    temperature
    connectivity r, Gs, rho
    GW taus
    Aquifer
    Links

    -> 



Data 
========

Integration
========

outcomes
============
1. which parameters are important
2. climate projections (Barry)
3. Adoption of technology (dam deepening, irrigation method all translated to water use efficiency term) 
4. Water allocation rules

Questions for Rebecca
================
* what do all the parameters mean in RepFarm
* 
