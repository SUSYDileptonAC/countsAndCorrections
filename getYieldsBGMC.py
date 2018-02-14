#! /usr/bin/env python

import sys
sys.path.append("../frameWorkBase")

from helpers import readTrees, totalNumberOfGeneratedEvents,createHistoFromTree, Process, TheStack
from locations import locations

from math import sqrt
from array import array

import ROOT
import argparse	

from sys import argv
import pickle	
from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1, TH2F, TH2D, TFile, TMath
import ratios
from defs import sbottom_masses,Backgrounds,Signals,Region,Regions,Plot,getRunRange,getRegion, getPlot
from corrections import triggerEffs, rSFOF, rSFOFDirect,rMuELeptonPt, rSFOFTrig
from centralConfig import systematics, runRanges

from math import sqrt
from setTDRStyle import setTDRStyle

from ConfigParser import ConfigParser
config = ConfigParser()
config.read("../SubmitScripts/Input/Master80X_MC.ini")


ROOT.gStyle.SetOptStat(0)

massCuts = {
			"mass20To50":"mll < 50 && mll > 20",
			"mass20To60":"mll < 60 && mll > 20",
			"mass20To70":"mll < 70 && mll > 20",
			"mass20To81":"mll < 81 && mll > 20",
			"mass20To86":"mll < 86 && mll > 20",
			"mass50To81":"mll < 81 && mll > 50",
			"mass50To86":"mll < 86 && mll > 50",
			"mass60To81":"mll < 81 && mll > 60",
			"mass60To86":"mll < 86 && mll > 60",
			"mass70To81":"mll < 81 && mll > 70",
			"mass70To86":"mll < 86 && mll > 70",
			"mass81To101":"mll < 101 && mll > 81",
			"mass86To96":"mll < 96 && mll > 86",
			"mass96To150":"mll < 150 && mll > 96",
			"mass96To200":"mll < 200 && mll > 96",
			"mass101To150":"mll < 150 && mll > 101",
			"mass101To200":"mll < 200 && mll > 101",
			"mass150To200":"mll < 200 && mll > 150",
			"mass200To300":"mll > 200 && mll < 300",
			"mass200To400":"mll > 200 && mll < 400",
			"mass300To400":"mll > 300 && mll < 400",
			"massAbove300":"mll > 300 ",
			"mass400":"mll > 400 ",
			"edgeMass":"mll < 70  && mll > 20 ",
			"lowMass":"mll > 20 && mll < 86 ",
			"highMass":"mll > 96 ",
			"highMassOld":"mll > 101 ",
			}			
			
nLLCuts = {
			"default":"nLL > 0",
			"lowNLL":"nLL < 21",
			"highNLL":"nLL > 21",
			}
			
HTCuts = {
			"lowHT":"ht < 400",
			"mediumHT":"ht > 400 && ht < 800",
			"highHT":"ht > 800",
			}
			
MT2Cuts = {
			"lowMT2":"MT2 < 80",
			"highMT2":"MT2 > 80",
			}
			
			   
def getYields(signalRegion,useAllMC=False):
	import ratios
	
	import pickle	

	path = locations.dataSetPathNLL
	
	runRange = getRunRange("Run2016_36fb")
	
	EETrees = readTrees(path, "EE")
	EMTrees = readTrees(path, "EMu")
	MMTrees = readTrees(path, "MuMu")
	
	### Mass bins for Morion 2017 SRs, summed low and high mass regions + legacy regions
	if signalRegion == "Moriond":
		massRegions = ["mass20To60","mass60To86","mass60To81","mass81To101","mass86To96","mass96To150","mass101To150","mass150To200","mass200To300","mass300To400","mass400","lowMass","highMass"]
	elif signalRegion == "ICHEPLegacy":
		massRegions = ["highMassOld"]
	elif signalRegion == "8TeVLegacy":
		massRegions = ["edgeMass"]
	
	### Two likelihood bins and MT2 cut
	nLLRegions = ["lowNLL","highNLL"]
	MT2Regions = ["highMT2"]
	
	
	signalBins = []
	signalCuts = {}	
	
	plot = getPlot("mllPlotROutIn")

	### Moriond main regions
	if signalRegion == "Moriond":
		for massRegion in massRegions:
			for nLLRegion in nLLRegions:
				for MT2Region in MT2Regions:
					signalBins.append("%s_%s_%s"%(massRegion,nLLRegion,MT2Region))
					signalCuts["%s_%s_%s"%(massRegion,nLLRegion,MT2Region)] = "%s && %s && %s"%(massCuts[massRegion],nLLCuts[nLLRegion],MT2Cuts[MT2Region])
					
		selection = getRegion("SignalHighMT2DeltaPhiJetMet")
		backgrounds = ["RareWZOnZ","RareZZOnZ","RareTTZOnZ","RareRestOnZ"]
	
	### Check of ICHEP deviation -> No MT2 cut
	elif signalRegion == "ICHEPLegacy":
		for massRegion in massRegions:
			for nLLRegion in nLLRegions:
				signalBins.append("%s_%s"%(massRegion,nLLRegion))
				signalCuts["%s_%s"%(massRegion,nLLRegion)] = "%s && %s"%(massCuts[massRegion],nLLCuts[nLLRegion])
		selection = getRegion("SignalInclusive")
		### There were no Z+jets estimates for ICHEP region on Moriond dataset -> take from MC
		backgrounds = ["TTZNonFS","RareNonFS","ZZNonFS","WZNonFS","DrellYan"]
			
	### For 8 TeV legacy -> no MT2 and likelihood
	elif signalRegion == "8TeVLegacy":
		for massRegion in massRegions:
			signalBins.append("%s"%massRegion)
			signalCuts["%s"%massRegion] = "%s"%massCuts[massRegion]
		selection = getRegion("SignalCentralOld")
		backgrounds = ["RareWZOnZ","RareZZOnZ","RareTTZOnZ","RareRestOnZ"]
	
	plot.addRegion(selection)
	plot.cuts = plot.cuts % runRange.runCut
	plot.cuts = plot.cuts.replace("p4.M()","mll")	
	plot.variable = plot.variable.replace("p4.M()","mll")	
		
	counts = {}
	
	### To check all MC			
	if useAllMC:
		backgrounds = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
	

	eventCounts = totalNumberOfGeneratedEvents(path)
	
	defaultCut = plot.cuts
	
	### loop over signal regions
	for signalBin in signalBins:
		
		### Add signal cut and remove those that are renamed or already applied
		### on NLL datasets
		plot.cuts = defaultCut.replace("chargeProduct < 0","chargeProduct < 0 && %s"%(signalCuts[signalBin]))	
		plot.cuts = plot.cuts.replace("metFilterSummary > 0 &&","")	
		plot.cuts = plot.cuts.replace("triggerSummary > 0 &&","")	
		plot.cuts = plot.cuts.replace("p4.Pt()","pt")
		
		print plot.cuts
				
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		
		stackEE = TheStack(processes,runRange.lumi,plot,EETrees,"None",1.0,1.0,1.0,doTopReweighting=True)
		stackMM = TheStack(processes,runRange.lumi,plot,MMTrees,"None",1.0,1.0,1.0,doTopReweighting=True)
		
		histoEE = stackEE.theHistogram		
		histoMM = stackMM.theHistogram
		
		histoEEUp = stackEE.theHistogramXsecUp		
		histoMMUp = stackMM.theHistogramXsecUp
		
		histoEEDown = stackEE.theHistogramXsecDown		
		histoMMDown = stackMM.theHistogramXsecDown
		
		eventCountSF = histoEE.GetEntries()+histoMM.GetEntries()
		
		if not signalRegion == "8TeVLegacy":
			histoEE.Scale(triggerEffs.inclusive.effEE.val)
			histoMM.Scale(triggerEffs.inclusive.effMM.val)
			
			histoEEUp.Scale(triggerEffs.inclusive.effEE.val)
			histoMMUp.Scale(triggerEffs.inclusive.effMM.val)
			
			histoEEDown.Scale(triggerEffs.inclusive.effEE.val)
			histoMMDown.Scale(triggerEffs.inclusive.effMM.val)
		
		### For 8 TeV region: Central selection only
		else:
			histoEE.Scale(triggerEffs.central.effEE.val)
			histoMM.Scale(triggerEffs.central.effMM.val)
	
			histoEEUp.Scale(triggerEffs.central.effEE.val)
			histoMMUp.Scale(triggerEffs.central.effMM.val)
	
			histoEEDown.Scale(triggerEffs.central.effEE.val)
			histoMMDown.Scale(triggerEffs.central.effMM.val)

		stackEM = TheStack(processes,runRange.lumi,plot,EMTrees,"None",1.0,1.0,1.0,doTopReweighting=True)
		histoEM = stackEM.theHistogram		
		histoEMUp = stackEM.theHistogramXsecUp		
		histoEMDown = stackEM.theHistogramXsecDown
		
		if not signalRegion == "8TeVLegacy":		
			histoEM.Scale(triggerEffs.inclusive.effEM.val)
			histoEMUp.Scale(triggerEffs.inclusive.effEM.val)
			histoEMDown.Scale(triggerEffs.inclusive.effEM.val)
		else:
			histoEM.Scale(triggerEffs.central.effEM.val)
			histoEMUp.Scale(triggerEffs.central.effEM.val)
			histoEMDown.Scale(triggerEffs.central.effEM.val)
		
		eventYieldSF = histoEE.Integral(0,-1)+histoMM.Integral(0,-1)
		eventYieldSFUp = histoEEUp.Integral(0,-1)+histoMMUp.Integral(0,-1)
		eventYieldSFDown = histoEEDown.Integral(0,-1)+histoMMDown.Integral(0,-1)
		eventYieldOF = histoEM.Integral(0,-1)
		eventYieldOFUp = histoEMUp.Integral(0,-1)
		eventYieldOFDown = histoEMDown.Integral(0,-1)
		
		#~ eventCountOF = histoEM.GetEntries()
		
		counts["%s_SF"%signalBin] = eventYieldSF
		counts["%s_SF_Up"%signalBin] = eventYieldSFUp
		counts["%s_SF_Down"%signalBin] = eventYieldSFDown
		counts["MCEvents_%s_SF"%signalBin] = eventCountSF
		
		### In principle we should use event dependent rSFOF, but the difference is
		### small and the fraction for the onZ samples tiny -> makes no difference
		if not signalRegion == "8TeVLegacy":
			counts["%s_OF"%signalBin] = eventYieldOF*rSFOFDirect.inclusive.val
			counts["%s_OF_Up"%signalBin] = eventYieldOFUp*rSFOFDirect.inclusive.val
			counts["%s_OF_Down"%signalBin] = eventYieldOFDown*rSFOFDirect.inclusive.val
		else:
			counts["%s_OF"%signalBin] = eventYieldOF*rSFOFDirect.central.val
			counts["%s_OF_Up"%signalBin] = eventYieldOFUp*rSFOFDirect.central.val
			counts["%s_OF_Down"%signalBin] = eventYieldOFDown*rSFOFDirect.central.val

	if useAllMC:
		fileName = "FullMC_%s_36fb"%signalRegion
	else:
		if signalRegion == "ICHEPLegacy":
			fileName = "OnZBG_ICHEPLegacy_36fb"
		else:
			fileName = "RareOnZBG_%s_36fb"%signalRegion

	outFilePkl = open("shelves/%s.pkl"%fileName,"w")
	pickle.dump(counts, outFilePkl)
	outFilePkl.close()			
			

				
	

# This method just waits for a button to be pressed
def waitForInput():
    raw_input("Press any key to continue!")
    return

# entry point
#-------------
if (__name__ == "__main__"):
    
    
	parser = argparse.ArgumentParser(description='MC yields in signal region')
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
	parser.add_argument("-a", "--useAllMC", action="store_true", dest="useAllMC", default=False,
						  help="Use all MC samples instead of only (rare) on Z")	
					
	args = parser.parse_args()
    
	
	if args.write:
		import subprocess
		if args.useAllMC:
			bashCommand1 = "cp shelves/RareOnZBG_Moriond_36fb.pkl ..frameWorkBase/shelves"		
			bashCommand2 = "cp shelves/OnZBG_ICHEPLegacy_36fb.pkl ..frameWorkBase/shelves"	
			bashCommand3 = "cp shelves/RareOnZBG_8TeVLegacy_36fb.pkl ..frameWorkBase/shelves"	
		else:
			bashCommand1 = "cp shelves/FullMC_Moriond_36fb.pkl ..frameWorkBase/shelves"		
			bashCommand2 = "cp shelves/FullMC_ICHEPLegacy_36fb.pkl ..frameWorkBase/shelves"	
			bashCommand3 = "cp shelves/FullMC_8TeVLegacy_36fb.pkl ..frameWorkBase/shelves"	
		process = subprocess.Popen(bashCommand1.split())
		process = subprocess.Popen(bashCommand2.split())
		process = subprocess.Popen(bashCommand3.split())
		
	else:
		getYields("Moriond",args.useAllMC)
		getYields("ICHEPLegacy",args.useAllMC)
		getYields("8TeVLegacy",args.useAllMC)
 
