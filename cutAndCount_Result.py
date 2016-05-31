#!/usr/bin/env python
import gc
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

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse	

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

from setTDRStyle import setTDRStyle
from helpers import getDataTrees, TheStack, totalNumberOfGeneratedEvents, Process, readTrees


from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, cutNCountXChecks

from locations import locations


def getEventLists(trees, cut,isMC, colNames = ["eventNr","lumiSec","runNr"]):
	result = {
		"columns": colNames,
		"cut": cut
		}
	if not isMC:	
		for comb in trees:
			subtree = trees[comb].CopyTree(cut)
			result[comb] = set()
			for ev in subtree:
				
				cols = []
				for varName in colNames:
					cols.append( getattr(ev, varName) )
				result[comb].add(tuple(cols))
			subtree.IsA().Destructor(subtree) ### ROOT destructor to really get the memeory released
			gc.collect()
	return result

def getCounts(trees, cut, isMC, backgrounds,plot,runRange,path):

	if isMC:
		tmpCut = plot.cuts
		plot.cuts = cut
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histEE = TheStack(processes,runRange.lumi,plot,trees["EE"],"None",1.0,1.0,1.0).theHistogram		
		histMM = TheStack(processes,runRange.lumi,plot,trees["MM"],"None",1.0,1.0,1.0).theHistogram
		histEM = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram
							
		
		eeErr = ROOT.Double()
		ee = histEE.IntegralAndError(1,histEE.GetNbinsX(),eeErr)
		mmErr = ROOT.Double()
		mm = histMM.IntegralAndError(1,histMM.GetNbinsX(),mmErr)
		emErr = ROOT.Double()
		em = histEM.IntegralAndError(1,histEM.GetNbinsX(),emErr)
		
		
		
		n= {
			"MM": ee,
			"EE": mm,
			"EM": em,
			}
		n["MMStatErr"] = float(eeErr)	
		n["EEStatErr"] = float(mmErr)	
		n["EMStatErr"] = float(emErr)		
		
		plot.cuts = tmpCut
		
	else:		
		n= {
			"MM": trees["MM"].GetEntries(cut),
			"EE": trees["EE"].GetEntries(cut),
			"EM": trees["EM"].GetEntries(cut),
			}
		n["MMStatErr"] = n["MM"]**0.5	
		n["EEStatErr"] = n["EE"]**0.5	
		n["EMStatErr"] = n["EM"]**0.5	
	n["cut"] = cut
	return n
	


	
	
	
	


def cutAndCountForRegion(path,selection,plots,runRange,isMC,backgrounds,preselection):
	
	if not isMC:
		trees = getDataTrees(path)
		for label, tree in trees.iteritems():
			trees[label] = tree.CopyTree(preselection)		
	else:
		treesEE = readTrees(path,"EE")
		treesEM = readTrees(path,"EMu")
		treesMM = readTrees(path,"MuMu")		
		trees = {
				"EE":treesEE,
				"MM":treesMM,
				"EM":treesEM,
		}
		
		

	for plotName in plots:
		plot = getPlot(plotName)
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	

		counts = {}
		eventLists = {}
		massRanges = ["default","edgeMass","zMass","highMass","belowZ","aboveZ"]
		counts["default"] = {}
		eventLists["default"] = {}
		for mllCut in massRanges:
			counts["default"][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, plot.cuts+"*(%s)"%getattr(theCuts.massCuts,mllCut).cut,isMC,backgrounds,plot,runRange,path)
			eventLists["default"][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees, plot.cuts+"*(%s)"%getattr(theCuts.massCuts,mllCut).cut,isMC)		

		for categoryName, category in cutNCountXChecks.cutList.iteritems():
			if categoryName == "leptonPt":
				for subcut in category:
					counts[subcut] = {}
					eventLists[subcut] = {}
					
					for mllCut in massRanges:
						cut = plot.cuts.replace("pt1 > 20 && pt2 > 20 &&","")
						cut = cut+"*(%s)"%getattr(theCuts.ptCuts,subcut).cut + "*(%s)"%getattr(theCuts.massCuts,mllCut).cut
						counts[getattr(theCuts.ptCuts,subcut).name][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)
						eventLists[getattr(theCuts.ptCuts,subcut).name][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees, cut,isMC)
			elif categoryName == "mets":
				for subcut in category:
					counts[subcut] = {}
					eventLists[subcut] = {}					
					
					for mllCut in massRanges:
						cut = plot.cuts.replace("met",subcut)
						cut = cut + "*(%s)"%getattr(theCuts.massCuts,mllCut).cut
						counts[subcut][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)
						eventLists[subcut][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees, cut,isMC)			
				
			else:
				for subcut in category:
					counts[subcut] = {}
					eventLists[subcut] = {}					
					
					for mllCut in massRanges:
						cut = plot.cuts+"*(%s)"%getattr(getattr(theCuts,categoryName),subcut).cut
						cut = cut + "*(%s)"%getattr(theCuts.massCuts,mllCut).cut
						counts[subcut][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)
						eventLists[subcut][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees, cut,isMC)				

		
		return counts, eventLists


def main():
	parser = argparse.ArgumentParser(description='produce cut & count event yields.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.signal
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.signal.central.name)	
		args.selection.append(regionsToUse.signal.forward.name)	
		args.selection.append(regionsToUse.signal.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	


	path = locations.dataSetPath

	preselection = "nJets >= 2 && deltaR > 0.3"
	
			
	

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)
			
			
			
			if args.write:

				import subprocess

				bashCommand = "cp shelves/cutAndCount_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())		
			
			else:
				counts, eventLists = cutAndCountForRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds,preselection)
				outFile = open("shelves/cutAndCount_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(counts, outFile)
				outFile.close()
				if not args.mc:
					outFile = open("shelves/eventLists_%s_%s.pkl"%(selection.name,runRange.label),"w")
					pickle.dump(eventLists, outFile)
					outFile.close()
			


		

main()

