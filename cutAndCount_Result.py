#!/usr/bin/env python

### routine to get the final results for the counting experiment

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

### Get the event counts from the trees
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
	
	

### fetch trees and loop over the different signal regions to get the results
def cutAndCountForRegion(path,selection,plots,runRange,isMC,backgrounds,preselection):
	
	### get trees
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
		
		

	### loop over plots (usually only mll)
	for plotName in plots:
		plot = getPlot(plotName)
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut	

		counts = {}
		massRanges = ["default","edgeMass","zMass","highMass","belowZ","aboveZ"]
		counts["default"] = {}
		### get the yields in each mass region without any additional cut on b-tagging (or anything else defined in centralConfig.cutNCountXChecks.cutList
		for mllCut in massRanges:
			counts["default"][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, plot.cuts+"*(%s)"%getattr(theCuts.massCuts,mllCut).cut,isMC,backgrounds,plot,runRange,path)	

		### get the subregions / cross checks
		for categoryName, category in cutNCountXChecks.cutList.iteritems():
				
			for subcut in category:
				counts[subcut] = {}				
				
				for mllCut in massRanges:
					cut = plot.cuts+"*(%s)"%getattr(getattr(theCuts,categoryName),subcut).cut
					cut = cut + "*(%s)"%getattr(theCuts.massCuts,mllCut).cut
					counts[subcut][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)		

		
		return counts


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

	### Basic preselection to make looping over the trees faster
	preselection = "nJets >= 2 && deltaR > 0.3"
	
			
	

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)
			
			### get the results
			counts = cutAndCountForRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds,preselection)
			outFile = open("shelves/cutAndCount_%s_%s.pkl"%(selection.name,runRange.label),"w")
			print "shelves/cutAndCount_%s_%s.pkl created"%(selection.name,runRange.label)
			pickle.dump(counts, outFile)
			outFile.close()

			### copy them to the central repository frameWorkBase/shelves
				
			import subprocess

			bashCommand = "cp shelves/cutAndCount_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
			print "shelves/cutAndCount_%s_%s.pkl copied to central repository"%(selection.name,runRange.label)
			process = subprocess.Popen(bashCommand.split())
			


		

main()

