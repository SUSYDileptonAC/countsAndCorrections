MAKERmueDependencies = python rRatioAll.py 

AN_PATH = /user/schomakers/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots


inclusive:
		$(MAKERmueDependencies) 
Barrel:
		$(MAKERmueDependencies) Barrel
Endcap:
		$(MAKERmueDependencies) Endcap
		
		
copyAN:
	cp fig/8TeVrRatioDataVsMC_eta1_Barrel.pdf fig/8TeVrRatioDataVsMC_pt1_Barrel.pdf fig/8TeVrRatioDataVsMC_met_Barrel.pdf fig/8TeVrRatioDataVsMC_mll_Barrel.pdf fig/8TeVrRatioDataVsMC_nJets_Barrel.pdf fig/8TeVrRatioDataVsMC_nVertices_Barrel.pdf fig/8TeVrRatioDataVsMC_eta1_Endcap.pdf fig/8TeVrRatioDataVsMC_pt1_Endcap.pdf fig/8TeVrRatioDataVsMC_met_Endcap.pdf fig/8TeVrRatioDataVsMC_mll_Endcap.pdf fig/8TeVrRatioDataVsMC_nJets_Endcap.pdf fig/8TeVrRatioDataVsMC_nVertices_Endcap.pdf  $(AN_PLOTS)
	

