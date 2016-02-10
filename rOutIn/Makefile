MAKERinout = python RinOut_Syst.py
MAKERinoutHighMass = python RinOut_Syst_highMass.py
MAKERinoutMC = python RinOut_Syst_MC.py
MAKERinoutPlot = python RinOut.py
AN_PATH = /home/jan/Doktorarbeit/Dilepton/projects/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots


RinoutPlot: RinOut.py
		$(MAKERinoutPlot) Barrel SF
		$(MAKERinoutPlot) Endcap SF
		$(MAKERinoutPlot) Barrel EE
		$(MAKERinoutPlot) Endcap EE
		$(MAKERinoutPlot) Barrel MM
		$(MAKERinoutPlot) Endcap MM
		
		
RinoutSyst: RinOut_Syst.py
		$(MAKERinout) Barrel SF
		$(MAKERinout) Endcap SF
		$(MAKERinout) Barrel EE
		$(MAKERinout) Endcap EE
		$(MAKERinout) Barrel MM
		$(MAKERinout) Endcap MM
RinoutSystHighMass: RinOut_Syst_highMass.py
		$(MAKERinoutHighMass) Barrel SF
		$(MAKERinoutHighMass) Endcap SF
		$(MAKERinoutHighMass) Barrel EE
		$(MAKERinoutHighMass) Endcap EE
		$(MAKERinoutHighMass) Barrel MM
		$(MAKERinoutHighMass) Endcap MM
	
		
RinoutMC: RinOut.py
		$(MAKERinoutMC)
		
copyAN:
	cp Rinout_Barrel_SF.pdf Rinout_Endcap_SF.pdf Rinout_NoLog_Barrel_SF.pdf Rinout_NoLog_Endcap_SF.pdf RinoutSystMET_Barrel_SF.pdf RinoutSystMET_Endcap_SF.pdf RinoutSystNJets_Barrel_SF.pdf RinoutSystNJets_Endcap_SF.pdf $(AN_PLOTS)
	

