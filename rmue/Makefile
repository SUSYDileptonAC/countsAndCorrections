MAKERmueDependencies = python rRatioAll.py 
MAKERmueDependenciesControl = python rRatioControl.py 

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
		
		
dependenciesControlInclusiveFull2012:
		$(MAKERmueDependenciesControl) Dependencies Full2012
dependenciesControlCentralFull2012:
		$(MAKERmueDependenciesControl) Dependencies Full2012 Central
dependenciesControlForwardFull2012:
		$(MAKERmueDependenciesControl) Dependencies Full2012 Forward
centralValueControlInclusiveFull2012:
		$(MAKERmueDependenciesControl) CentralValue Full2012
centralValueControlCentralFull2012:
		$(MAKERmueDependenciesControl) CentralValue Full2012 Central
centralValueControlForwardFull2012:
		$(MAKERmueDependenciesControl) CentralValue Full2012 Forward
		
		
copyAN:
	cp fig/8TeVrRatioDataVsMCControl_eta1_Central.pdf fig/8TeVrRatioDataVsMCControl_pt1_Central.pdf fig/8TeVrRatioDataVsMCControl_met_Central.pdf fig/8TeVrRatioDataVsMCControl_mll_Central.pdf fig/8TeVrRatioDataVsMCControl_nJets_Central.pdf fig/8TeVrRatioDataVsMCControl_nVertices_Central.pdf fig/8TeVrRatioDataVsMCControl_eta1_Forward.pdf fig/8TeVrRatioDataVsMCControl_pt1_Forward.pdf fig/8TeVrRatioDataVsMCControl_met_Forward.pdf fig/8TeVrRatioDataVsMCControl_mll_Forward.pdf fig/8TeVrRatioDataVsMCControl_nJets_Forward.pdf fig/8TeVrRatioDataVsMCControl_nVertices_Forward.pdf  $(AN_PLOTS)
	cp Tables/new_r-ValuesControl_*.txt $(AN_TABLES)

