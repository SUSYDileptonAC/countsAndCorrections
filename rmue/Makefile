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
		
dependenciesControlInclusiveBlockAReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockAReprocessed
dependenciesControlCentralBlockAReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockAReprocessed Central
dependenciesControlForwardBlockAReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockAReprocessed Forward
centralValueControlInclusiveBlockAReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockAReprocessed
centralValueControlCentralBlockAReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockAReprocessed Central
centralValueControlForwardBlockAReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockAReprocessed Forward
		
dependenciesControlInclusiveBlockAFrozen:
		$(MAKERmueDependenciesControl) Dependencies BlockAFrozen
dependenciesControlCentralBlockAFrozen:
		$(MAKERmueDependenciesControl) Dependencies BlockAFrozen Central
dependenciesControlForwardBlockAFrozen:
		$(MAKERmueDependenciesControl) Dependencies BlockAFrozen Forward
centralValueControlInclusiveBlockAFrozen:
		$(MAKERmueDependenciesControl) CentralValue BlockAFrozen
centralValueControlCentralBlockAFrozen:
		$(MAKERmueDependenciesControl) CentralValue BlockAFrozen Central
centralValueControlForwardBlockAFrozen:
		$(MAKERmueDependenciesControl) CentralValue BlockAFrozen Forward
		
dependenciesControlInclusiveBlockBReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockBReprocessed
dependenciesControlCentralBlockBReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockBReprocessed Central
dependenciesControlForwardBlockBReprocessed:
		$(MAKERmueDependenciesControl) Dependencies BlockBReprocessed Forward
centralValueControlInclusiveBlockBReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockBReprocessed
centralValueControlCentralBlockBReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockBReprocessed Central
centralValueControlForwardBlockBReprocessed:
		$(MAKERmueDependenciesControl) CentralValue BlockBReprocessed Forward
		
		
copyAN:
	cp fig/8TeVrRatioDataVsMCControl_eta1_Central.pdf fig/8TeVrRatioDataVsMCControl_pt1_Central.pdf fig/8TeVrRatioDataVsMCControl_met_Central.pdf fig/8TeVrRatioDataVsMCControl_mll_Central.pdf fig/8TeVrRatioDataVsMCControl_nJets_Central.pdf fig/8TeVrRatioDataVsMCControl_nVertices_Central.pdf fig/8TeVrRatioDataVsMCControl_eta1_Forward.pdf fig/8TeVrRatioDataVsMCControl_pt1_Forward.pdf fig/8TeVrRatioDataVsMCControl_met_Forward.pdf fig/8TeVrRatioDataVsMCControl_mll_Forward.pdf fig/8TeVrRatioDataVsMCControl_nJets_Forward.pdf fig/8TeVrRatioDataVsMCControl_nVertices_Forward.pdf  $(AN_PLOTS)
	cp Tables/new_r-ValuesControl_*.txt $(AN_TABLES)

