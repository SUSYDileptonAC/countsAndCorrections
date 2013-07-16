MAKERinout = python RinOut_Syst.py
MAKERinoutMC = python RinOut_Syst_MC.py
MAKERinoutPlot = python RinOut.py
AN_PATH = /user/schomakers/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots


RinoutPlot: RinOut.py
		$(MAKERinoutPlot) Barrel
		$(MAKERinoutPlot) Endcap
		$(MAKERinoutPlot) Inclusive	
		$(MAKERinoutPlot) BothEndcap		
		
RinoutSyst: RinOut_Syst.py
		$(MAKERinout) Barrel
		$(MAKERinout) Endcap
		$(MAKERinout) Inclusive	
		$(MAKERinout) BothEndcap		
		
RinoutMC: RinOut.py
		$(MAKERinoutMC)
		
copyAN:
	cp Rinout_Barrel.pdf Rinout_Endcap.pdf Rinout_NoLog_Barrel.pdf Rinout_NoLog_Endcap.pdf RinoutSystMET_Barrel.pdf RinoutSystMET_Endcap.pdf RinoutSystNJets_Barrel.pdf RinoutSystNJets_Endcap.pdf $(AN_PLOTS)
	

