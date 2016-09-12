#!/usr/bin/env python

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

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rSFOFFact, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations


### routine to make dependency plots
def dependencies(path,selection,plots,runRange,isMC,nonNormalized,backgrounds,cmsExtra,verbose=True):
	### loop over plots
	for name in plots:
		##fetch plot and region
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	

		if "Forward" in selection.name:
			label = "forward"
		elif "Central" in selection.name:
			label = "central"
		else:		
			label = "inclusive"


		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,nonNormalized, backgrounds,label,verbose=verbose)
		
		### Add code to make the dependency plots here

		
		if isMC:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	



### get the histograms from the ntuples
def getHistograms(path,plot,runRange,isMC,nonNormalized,backgrounds,region="",verbose=True):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	
	### make a stack for MC
	if isMC:
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			if nonNormalized:
				processes.append(Process(getattr(Backgrounds,background),eventCounts,normalized=False))
			else:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,verbose=verbose).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,verbose=verbose).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,verbose=verbose).theHistogram
			
	else:
		histoEE = getDataHist(plot,treesEE,verbose=verbose)
		histoMM = getDataHist(plot,treesMM,verbose=verbose)
		histoEM = getDataHist(plot,treesEM,verbose=verbose)
	
	return histoEE , histoMM, histoEM
	
	

	
### Routine to get the central values for R_SF/OF
def centralValues(path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra,verbose=True):


	### get plot and selection
	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()

	plot.cuts = plot.cuts % runRange.runCut		

	### Additional plot to look at the signal region in MC
	plotSignal = getPlot("mllPlot")

	
	if "Forward" in selection.name:
		plotSignal.addRegion(getRegion("SignalForward"))
		label = "forward"
	elif "Central" in selection.name:
		plotSignal.addRegion(getRegion("SignalCentral"))
		label = "central"
	else:		
		plotSignal.addRegion(getRegion("SignalInclusive"))
		label = "inclusive"

	plotSignal.cleanCuts()
	plotSignal.cuts = plotSignal.cuts % runRange.runCut	


	### get the histograms
	histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,nonNormalized,backgrounds,label,verbose=verbose)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())

	histEESignal, histMMSignal, histEMSignal = getHistograms(path,plotSignal,runRange,isMC,nonNormalized,backgrounds,label,verbose=verbose)
	histSFSignal = histEESignal.Clone("histSFSignal")
	histSFSignal.Add(histMMSignal.Clone())
	result = {}
	

	### Add other regions beside the low mass region from here on
	### Does it make sense to add all?
	
	lowMassLow = mllBins.lowMass.low
	lowMassHigh = mllBins.lowMass.high
	
	highMassRSFOFLow = mllBins.highMassRSFOF.low
		
	eeErr = ROOT.Double()
	ee = histEE.IntegralAndError(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01),eeErr)
	
	mmErr = ROOT.Double()
	mm = histMM.IntegralAndError(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01),mmErr)
	
	ofErr = ROOT.Double()
	of = histEM.IntegralAndError(histEM.FindBin(lowMassLow+0.01),histEM.FindBin(lowMassHigh-0.01),ofErr)
	
	sf = ee + mm 
	sfErr = (eeErr**2 + mmErr**2)**0.5	
	
	### calculate R_SF/OF, R_ee/OF and R_mm/OF and the uncertainties
	rsfof = float(sf)/float(of)
	rsfofErr = rsfof*(sfErr**2/sf**2+ofErr**2/of**2)**0.5		
		
	rEEOF = float(ee)/float(of)
	rEEOFErr = rEEOF * (eeErr**2/ee**2 + ofErr**2/of**2)**0.5
	
	rMMOF = float(mm)/float(of)
	rMMOFErr = rMMOF * (mmErr**2/mm**2 + ofErr**2/of**2)**0.5	
		
	
	result = {}
	result["EE"] = ee
	result["MM"] = mm
	result["SF"] = sf
	result["OF"] = of		
		
	result["rSFOF"] = rsfof
	result["rSFOFErr"] = rsfofErr
	result["rEEOF"] = rEEOF
	result["rEEOFErr"] = rEEOFErr
	result["rMMOF"] = rMMOF
	result["rMMOFErr"] = rMMOFErr

	if isMC:
		### for MC also store results in the signal region

		eeErrSignal = ROOT.Double()
		eeSignal = histEESignal.IntegralAndError(histEESignal.FindBin(lowMassLow+0.01),histEESignal.FindBin(lowMassHigh-0.01),eeErrSignal)
		
		mmErrSignal = ROOT.Double()
		mmSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(lowMassLow+0.01),histMMSignal.FindBin(lowMassHigh-0.01),mmErrSignal)
		
		ofErrSignal = ROOT.Double()
		ofSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(lowMassLow+0.01),histEMSignal.FindBin(lowMassHigh-0.01),ofErrSignal)	
		
		sfSignal = eeSignal + mmSignal
		sfErrSignal = (eeErrSignal**2 + mmErrSignal**2)**0.5
		
		rsfofSignal = float(sfSignal)/float(ofSignal)
		rsfofErrSignal = rsfofSignal*(sfErrSignal**2/sfSignal**2+ofErrSignal**2/ofSignal**2)**0.5
		
		rEEOFSignal = float(eeSignal)/float(ofSignal)
		rEEOFErrSignal = rEEOFSignal * (eeErrSignal**2/eeSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
		
		rMMOFSignal = float(mmSignal)/float(ofSignal)
		rMMOFErrSignal = rMMOFSignal * (mmErrSignal**2/mmSignal**2 + ofErrSignal**2/ofSignal**2)**0.5

		### The transfer factor is the ratio of R_SFOF in signal and control region
		### It is a test how the method works
		transferFaktor = rsfofSignal/rsfof
		transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
		transferFaktor = rsfofSignal/rsfof
		transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
		transferFaktorEE = rEEOFSignal/rEEOF
		transferFaktorEEErr = transferFaktorEE*((rEEOFErr/rEEOF)**2+(rEEOFErrSignal/rEEOFSignal)**2)**0.5
		transferFaktorMM = rMMOFSignal/rMMOF
		transferFaktorMMErr = transferFaktorMM*((rMMOFErr/rMMOF)**2+(rMMOFErrSignal/rMMOFSignal)**2)**0.5
		
		result["EESignal"] = eeSignal
		result["MMSignal"] = mmSignal
		result["SFSignal"] = sfSignal
		result["OFSignal"] = ofSignal
		
		result["rSFOFSignal"] = rsfofSignal
		result["rSFOFErrSignal"] = rsfofErrSignal
		result["rEEOFSignal"] = rEEOFSignal
		result["rEEOFErrSignal"] = rEEOFErrSignal
		result["rMMOFSignal"] = rMMOFSignal
		result["rMMOFErrSignal"] = rMMOFErrSignal
		result["transfer"] = transferFaktor
		result["transferErr"] = transferFaktorErr
		result["transferEE"] = transferFaktorEE
		result["transferEEErr"] = transferFaktorEEErr
		result["transferMM"] = transferFaktorMM
		result["transferMMErr"] = transferFaktorMMErr
	
	return result
	
	
def main():
	
	

	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
	parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False,
						  help="Switch verbose mode off. Do not show cut values and samples on the console whenever a histogram is created")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
	parser.add_argument("-n", "--nonNormalized", action="store_true", dest="nonNormalized", default=False,
						  help="do not normalize to cross section")	
					
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.rSFOF
	if len(args.plots) == 0:
		args.plots = plotLists.rSFOF
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.rSFOF.central.name)	
		args.selection.append(regionsToUse.rSFOF.forward.name)	
		args.selection.append(regionsToUse.rSFOF.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
		
	if args.quiet:
		verbose = False
	else:
		verbose = True		

	path = locations.dataSetPath
		
	cmsExtra = "Private Work"
	if args.mc:
		cmsExtra = "#splitline{Private Work}{Simulation}"


	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)

			### Calculate the central values for R_SF/OF and store the in shelves
			if args.central:
				
				centralVal = centralValues(path,selection,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra,verbose=verbose)
				if args.mc:
					outFilePkl = open("shelves/rSFOF_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rSFOF_%s_%s_MC.pkl created"%(selection.name,runRange.label)
				else:
					outFilePkl = open("shelves/rSFOF_%s_%s.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rSFOF_%s_%s.pkl created"%(selection.name,runRange.label)
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
			
			### make dependency plots	
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra,verbose=verbose)		
			
			### copy .pkl files to frameWorkBase/shelves to be used by other tools	
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rSFOF_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					print "shelves/rSFOF_%s_%s_MC.pkl copied to central repository"%(selection.name,runRange.label)		
				else:	
					bashCommand = "cp shelves/rSFOF_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					print "shelves/rSFOF_%s_%s.pkl copied to central repository"%(selection.name,runRange.label)	
				process = subprocess.Popen(bashCommand.split())					
main()
