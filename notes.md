Overview
--------------------------
The integrated model aims to allow the analysis of the ecological and economic impacts of climate, technology, markets, and policy. A hydrological model running on a daily timestep interacts with annual farmer decision, water policy, and ecological models.

Hydrology
--------------------------

``1. a surface and groundwater model that takes rainfall, temperature and extraction data, and estimates stream
flow and groundwater storage volumes
2. a stream flow routing module that uses the variable parameter lag-route method of Croke et al. (2006) to
route flow downstream through the sub-catchment network
3. a groundwater level module that converts groundwater storage volumes to levels via a regression
analysis.''

\cite{blakers2011influence}
	
\cite{jakeman1993much}


Water Policy
--------------------------
An improved water policy would seek to maintain surface and groundwater at levels determined most appropriate by the community and stakeholders. Such policy would incorporate current levels as well as the state of dependent ecosystems and economies. 	 
[water_plans]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/plans_commenced/default.aspx

[namoi_unreg]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Namoi-Unregulated-and-Alluvial

[namoi_gw]: http://www.water.nsw.gov.au/Water-management/Water-sharing-plans/Plans-commenced/Water-source/Upper-and-Lower-Namoi-Groundwater-Sources/default.aspx


Ecology
--------------------------


Farm Decision	
--------------------------
\cite{letcher2004model}



Bibliography
--------------------------


@inproceedings{blakers2011influence,
  title={The influence of model simplicity on uncertainty in the context of surface-groundwater modelling and integrated assessment},
  author={Blakers, RS and Croke, BFW and Jakeman, AJ and others},
  booktitle={19th International Congress on Modelling and Simulation, Perth, Australia},
  pages={12--16},
  year={2011}
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


@legislation{nsw2000water,
  year       = 2000,
  title      = {Water Management Act},
  note       = {NSW},
}

@article{jakeman1993much,
  title={How much complexity is warranted in a rainfall-runoff model?},
  author={Jakeman, AJ and Hornberger, GM},
  journal={Water resources research},
  volume={29},
  number={8},
  pages={2637--2649},
  year={1993},
  publisher={Wiley Online Library}
}

@article{ivkovic2009use,
  title={Use of a simple surface--groundwater interaction model to inform water management},
  author={Ivkovic, KM and Letcher, RA and Croke, BFW},
  journal={Australian Journal of Earth Sciences},
  volume={56},
  number={1},
  pages={71--80},
  year={2009},
  publisher={Taylor \& Francis}
}

@article{croke2004catchment,
  title={A catchment moisture deficit module for the IHACRES rainfall-runoff model},
  author={Croke, Barry FW and Jakeman, Anthony J},
  journal={Environmental Modelling \& Software},
  volume={19},
  number={1},
  pages={1--5},
  year={2004},
  publisher={Elsevier}
}