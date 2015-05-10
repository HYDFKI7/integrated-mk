There are 3 scenarios to explore, the climate, irrigation technique, and the water allocation rules.

Climate
------------------------
If the dynamic modelling component has been included (which is the plan), then pick a period of 20 years from historic records which was the driest, wettest and 'most median' to be our three climatic periods. 

start = '1899-01-01'
end = '2011-12-27'

[NSW DPI Office of Water](http://realtimedata.water.nsw.gov.au/water.stm)
River 419051 Maules Ck@Avoca East

[BOM](http://www.bom.gov.au/climate/data/)
Maules Creek
Rainfall for 055076 Boggabri (Kanownda) NSW (7.9km away)    
Min and Max temperature for 055023 Gunnedah Pool NSW (54.8km away)    

Irrigation technique
--------------------------
--------------------------
There are two components of this, being the level of adoption of each irrigation technique, and then the water efficiency of each technique (although I have moved this component to parameter values).
 
From survey (CITE !!!), 
* Min adoption of flood = current 78% did some flood irrigation of cotton
* Max adoption of flood = 100% of respondents
* In the past, those that did flood irrigate their cotton did it for 35 – 100% of their crop.
```
adoption = [
  {
    "Irrigation regime":"Flood",
    "Min adoption":"27.30%",
    "Max adoption":"100.00%",
    "Hypothetical scenario":""
  },
  {
    "Irrigation regime":"Spray",
    "Min adoption":"0.50%",
    "Max adoption":"16.90%",
    "Hypothetical scenario":""
  }
]

water_efficiency = 
[
  {
    "Irrigation regime":"Drip ",
    "Min":"76% (calc from Harris, 2005 (17-60% saved)\n78% (calc from Henggeler, 2012 (20-20% saved)\n",
    "Most likely":"85 (Smith)\n",
    "Max":"85 (Smith)\n84.5% (1/3 less water used for drip, calc Norton & Silvertooth)\n84.5% (calc Mazur & Harris, 2006,  30% water saved)"
  },
  {
    "Irrigation regime":"Flood",
    "Min":"50 (Smith)",
    "Most likely":"65 (centre point)\n76% (Tennakoon)",
    "Max":"80 (Smith)"
  },
  {
    "Irrigation regime":"Spray",
    "Min":"",
    "Most likely":"80 (Smith)",
    "Max":"91.65 (calc, DPI budgets for wheat)"
  }
]
```


Ecology
--------------------------

```
weights = {
  "Default": {
    "Duration":0.5,
    "Timing":0.2,
    "Dry":0.3
  },
  "Favour duration": {
    "Duration":0.9,
    "Timing":0.01,
    "Dry":0.01
  },
  "Favour dry": {
    "Duration":0.4,
    "Timing":0.1,
    "Dry":0.5
  },
  "Favour timing": {
    "Duration":0.3,
    "Timing":0.5,
    "Dry":0.2
  },
  "Minimum": {
    "Duration":null,
    "Timing":null,
    "Dry":null
  }
}

ctf = { "min": 110, "med": 500, "max": 1000 }
min_separation = { "min": 1, "med": 2, "max": 5 }
min_duration = { "min": 1, "med": 3, "max": 5 }
```

TODO
==================================
* scenarios: climate, adoption, policy, crop prices
* Is the difference between 2 scenarios overwhelmed by uncertainty from other parameters.
* output: min GW depth, average GW, profit, SW eco index, GW eco index
* add
  - water trading
  - water allocation as a output
  - cease to pump threshold
  - cost of pumping varying with GW level (see dynamic programming literature)
  - fuel price


Dependencies
==================================
R libraries including hydromad
install.packages(c("zoo", "latticeExtra", "polynom", "car", "Hmisc","reshape", "nnls"))
install.packages("hydromad", repos="http://hydromad.catchment.org")

sudo pip install rpy2 (http://rpy.sourceforge.net/)

python with scipy 0.15

Integrated model for Maules Creek
===================================

[Model](/Model) contains Python code for 
* hydrological model (IHACRES with GW), written in R by Rachel Blakers, wrapped in Python
* ecological index calculations
* a simple farmer descision model



From Namoi_Unregulated_and_Alluvial
-----------------------------------
Users must cease to pump when the flow at the reference point (Maules Creek at Avoca East, Gauge 419051) is equal to or less than 1 ML/day. Note: This rule applies to all extraction from rivers and creeks including natural in-river pools within the channels of rivers and creeks. Approximate catchment area (km2) 1,095

Maules Creek Entitlement (ML/year) 1,413, Number of licenses 7

This water source has a relatively small licensed entitlement of around 1,400 ML, mostly located on Maules Creek itself. Current access conditions for these licences vary. The creek is connected with the underlying alluvial groundwater system which is the main source of water for irrigation in the area. In the past pumping restrictions have been imposed on groundwater users during dry seasons to reduce impacts on creek flows. The IRP agreed that surface water access rules should be consistent with past practice in the area, and adopted the same CTP level (1 ML/d at Avoca East gauge), to protect low flows. The more stringent access conditions applying to several licences will be carried over. Trade into the Maules and Horsearm Creeks Management Zone is restricted by an entitlement limit based on the level at the commencement of the plan, to prevent further pressure on the resource. Trade into the Tributaries Management Zone is not permitted, to protect upstream areas which are in good environmental condition, many originating in forested areas or national park. Trade rules also protect several lagoons on the Namoi floodplain from the potential impacts of water extraction.


From Upper_and_Lower_Namoi_Groundwater_Sources 
-----------------------------------
Upper Namoi Zone 11 (hereafter Zone 11), Maules Creek Groundwater Source

The AWD (Available water determination) for supplementary water access licences in Zones 5, 11 and 12 for the 2006/07 to the 2009/10 water years is 1 ML per share unit of supplementary access licence share component. The AWD for these licences in 20010/11 will be 0.84 ML per share unit reducing by 0.16 ML per year each year thereafter. It will be 0 ML per share unit in the 2015/16 water
year.

Extraction limit 2,200 ML/yr plus the total water made available to supplementary water access licences plus
basic rights in Zone 11. Based on estimation of 2,200 ML/yr recharge, 1-2% of rainfall.

The extraction limit for Zone 11 cannot be increased to more than 2,750 ML/yr, plus total water made available to supplementary water access licences, plus the total requirements for basic landholder rights at the commencement of this plan nor be decreased to less than 1,650 ML/yr, plus total water made available to supplementary water access licences plus the total requirements for basic landholder rights at the commencement of this plan


From powell2011representative
-----------------------------------
```
crops = [
  {"season": "Summer", "applied water": 8, "name": "Cotton (BT, irrigated)", "yield": 9.5, "price": 538},
  {"season": "Summer", "applied water": 8, "name": "Cotton (conventional, irrigated)", "yield": 9.5, "price": 538},
  {"season": "Summer", "applied water": 7.15, "name": "Maize (irrigated)", "yield": 9, "price": 287},
  {"season": "Summer", "applied water": 4.5, "name": "Sorghum (irrigated)", "yield": 8, "price": 242},
  {"season": "Summer", "applied water": 1.5, "name": "Sorghum (semi irrigated)", "yield": 5.5, "price": 242},
  {"season": "Summer", "applied water": 5.8, "name": "Soybean (irrigated)", "yield": 3, "price": 350},
  {"season": "Winter", "applied water": 0, "name": "Chickpea (dryland)", "yield": 1.3, "price": 468},
  {"season": "Winter", "applied water": 2.7, "name": "Faba bean (irrigated)", "yield": 5, "price": 348},
  {"season": "Winter", "applied water": 0, "name": "Faba bean (dryland)", "yield": 1.4, "price": 348},
  {"season": "Winter", "applied water": 0, "name": "Wheat (bread, dryland)", "yield": 1.8, "price": 244},
  {"season": "Winter", "applied water": 1.5, "name": "Wheat (bread, semi irrigated)", "yield": 4, "price": 244},
  {"season": "Winter", "applied water": 3.6, "name": "Wheat (bread, irrigated)", "yield": 7, "price": 244},
  {"season": "Winter", "applied water": 3.6, "name": "Wheat (durum, irrigated)", "yield": 7, "price": 275},
  {"season": "Winter", "applied water": 1.4, "name": "Vetch (irrigated)", "yield":0, "price":0}
]
```



Agricultural models (eg. APSIM)
http://www.colyirr.com.au/swagmanfarm/allUser/Simulation.asp
http://www.yieldprophet.com.au/yp/wfLogin.aspx

NSW DPI
http://www.dpi.nsw.gov.au/research/economics-research/reports/err46
http://www.dpi.nsw.gov.au/agriculture/farm-business/budgets/summer-crops
http://www.dpi.nsw.gov.au/agriculture/resources/water

"Maules Creek sits between Leard State Forest and Mount Kaputar National Park. It has soft fertile soil suitable for most crops such as wheat, barley, sorghum, oats, lucerne, canola and even cotton."
https://www.wilderness.org.au/articles/our-history-and-struggle-our-land-maules-creek-nsw-laird-family


References
---------------
```
@article{fu2014assessing,
  title={Assessing certainty and uncertainty in riparian habitat suitability models by identifying parameters with extreme outputs},
  author={Fu, Baihua and Guillaume, Joseph HA},
  journal={Environmental Modelling \& Software},
  volume={60},
  pages={277--289},
  year={2014},
  publisher={Elsevier}
}

@article{fu2013water,
  title={A water suitability model for riparian vegetation in the Namoi catchment: Final Report},
  author={Fu, Baihua },
  year={2013},
  publisher={National Centre for Groundwater Research and Training}
}


@book{powell2011representative,
  title={A representative irrigated farming system in the Lower Namoi Valley of NSW: An economic analysis},
  author={Powell, Janine and Scott, Fiona and Wales, New South},
  year={2011},
  publisher={Industry \& Investment NSW}
}

@misc{Water_sharing_plans_commenced,
  title = {Water sharing plans commenced},
  howpublished = {\url{http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/plans_commenced/default.aspx}},
  note = {Accessed: 2015-02-20}
}

@misc{Namoi_Unregulated_and_Alluvial,
  title = {Namoi Unregulated and Alluvial},
  howpublished = {\url{http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Namoi-Unregulated-and-Alluvial}},
  note = {Accessed: 2015-02-20}
}

@misc{Upper_and_Lower_Namoi_Groundwater_Sources,
  title = {Upper and Lower Namoi Groundwater Sources},
  howpublished = {\url{http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Upper-and-Lower-Namoi-Groundwater-Sources/default.aspx}},
  note = {Accessed: 2015-02-20}
}


@article{letcher2003application,
  title={Application of an adaptive method for integrated assessment of water allocation issues in the Namoi River Catchment, Australia},
  author={Letcher, RA and Jakeman, AJ},
  journal={Integrated Assessment},
  volume={4},
  number={2},
  pages={73--89},
  year={2003},
  publisher={Taylor \& Francis}
}

@article{letcher2004model,
  title={Model development for integrated assessment of water allocation options},
  author={Letcher, RA and Jakeman, AJ and Croke, BFW},
  journal={Water Resources Research},
  volume={40},
  number={5},
  year={2004},
  publisher={Wiley Online Library}
}
```
