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
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
		histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		histoEE.Scale(getattr(triggerEffs,region).effMM.val)	
		histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
	

	






	
	
def main():
	




	selections = []
	selections.append(regionsToUse.rOutIn.central.name)	
	selections.append(regionsToUse.rOutIn.forward.name)	
	
			

	path = locations.dataSetPath	






	runRange = getRunRange("Full2012")
	result = {}
	for selectionName in selections:
			
		selection = getRegion(selectionName)

		plot = getPlot("mllPlot")
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	
		cuts = plot.cuts	
		plot.cuts = plot.cuts + "*(nVertices < 13)"
		histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[],"")
		
		print histEE.GetEntries(), histMM.GetEntries(), histEM.GetEntries()
		plot.cuts = cuts	
		plot.cuts = plot.cuts + "*(nVertices >= 13 && nVertices < 17)"
		histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[],"")
		
		print histEE.GetEntries(), histMM.GetEntries(), histEM.GetEntries()
		plot.cuts = cuts	
		plot.cuts = plot.cuts + "*(nVertices >= 17)"
		histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[],"")
		
		print histEE.GetEntries(), histMM.GetEntries(), histEM.GetEntries()
			 
main()
