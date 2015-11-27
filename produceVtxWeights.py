import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import os
import pickle

from messageLogger import messageLogger as log

import math
from math import sqrt
from array import array

import argparse	


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rSFOFFact, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations


def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

	#~ print table


def getHistograms(path,plot,runRange,isMC,backgrounds,region=""):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		backgrounds =  ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
		processes =  []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoEE.Scale(getattr(triggerEffs,region).effMM.val)	
		#~ histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
	

	






	
	
def main():
	




	selections = []
	selections.append("Inclusive")	
	
			

	path = locations.dataSetPathTrigger	


	#~ f = ROOT.TFile("weights_Run2015_25ns.root","recreate")
	f = ROOT.TFile("data_PU_25ns.root","recreate")
	f.cd()

	histo = TH1F("pileup","pileup",60,0,60)


	runRange = getRunRange("Run2015_25ns")
	result = {}
	

	weights = []
	weightSum = 0
	for selectionName in selections:
			
		selection = getRegion(selectionName)

		plot = getPlot("nVtxPlotWeights")
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	

		histEEMC, histMMMC, histEMMC = getHistograms(path,plot,runRange,True,[],"")
		histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[],"")
		
		histEE.Add(histMM)
		histEEMC.Add(histMMMC)
		print histEE.GetEntries(), histEEMC.GetEntries()
		histEE.Scale(1./histEE.GetEntries())
		histEEMC.Scale(1./histEEMC.Integral())

		for i in range(0,histEE.GetNbinsX()+1):
			if histEEMC.GetBinContent(i) > 0:
				histo.SetBinContent(i,float(histEE.GetBinContent(i)))
				weights.append(float(histEE.GetBinContent(i))/histEEMC.GetBinContent(i))
				weightSum += (float(histEE.GetBinContent(i))/histEEMC.GetBinContent(i))
			else:
				histo.SetBinContent(i,float(histEE.GetBinContent(i)))
				weights.append(1)
				weightSum += 1
			
		print weights
		print weightSum
		
	f.Write()
	f.Close()
	
	
	#from Vince
	#~ 
	#~ f = ROOT.TFile("nvtx_ratio.root")
	#~ f.cd()
	#~ 
	#~ histo = ROOT.TH1F()
	#~ histo = f.Get("h_vet_ratio")
	#~ print type(histo)
	#~ 
	#~ vinceWeights = []
#~ 
	#~ for i in range(0,histo.GetNbinsX()+1):
		#~ vinceWeights.append(histo.GetBinContent(i))
#~ 
	#~ print vinceWeights		 
main()
