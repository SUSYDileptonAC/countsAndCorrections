MAKERmueDependencies = python rRatioAll.py 

AN_PATH = /home/jan/Doktorarbeit/Dilepton/projects/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots


dependenciesInclusive:
		$(MAKERmueDependencies) Dependencies
dependenciesCentral:
		$(MAKERmueDependencies) Dependencies Central
dependenciesForward:
		$(MAKERmueDependencies) Dependencies Forward
centralValueInclusive:
		$(MAKERmueDependencies) CentralValue
centralValueCentral:
		$(MAKERmueDependencies) CentralValue Central
centralValueForward:
		$(MAKERmueDependencies) CentralValue Forward
		
		
copyAN:
	cp fig/8TeVrRatioDataVsMC_eta1_Central.pdf fig/8TeVrRatioDataVsMC_pt1_Central.pdf fig/8TeVrRatioDataVsMC_met_Central.pdf fig/8TeVrRatioDataVsMC_mll_Central.pdf fig/8TeVrRatioDataVsMC_nJets_Central.pdf fig/8TeVrRatioDataVsMC_nVertices_Central.pdf fig/8TeVrRatioDataVsMC_eta1_Forward.pdf fig/8TeVrRatioDataVsMC_pt1_Forward.pdf fig/8TeVrRatioDataVsMC_met_Forward.pdf fig/8TeVrRatioDataVsMC_mll_Forward.pdf fig/8TeVrRatioDataVsMC_nJets_Forward.pdf fig/8TeVrRatioDataVsMC_nVertices_Forward.pdf  $(AN_PLOTS)
	cp Tables/new_r-Values_*.txt $(AN_TABLES)

