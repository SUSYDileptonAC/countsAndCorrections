#!/usr/bin/env python

import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import os
import pickle

from messageLogger import messageLogger as log

import math

from array import array

import argparse	


import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, getDataTrees

from corrections import triggerEffs, rSFOF
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics
from locations import locations

import ratios


def isPromptOnly(runNr,lumiSec):
	
	s = open('PromptOnly.txt', 'r').read()
	jsonDict = eval(s)	
	if str(runNr) in jsonDict.keys():
		found = False
		for x in jsonDict[str(runNr)]:
			for y in range(x[0],x[1]):
				if lumiSec == y:
					found =  True
		return found
	else:
		return False

		
def isReRecoOnly(runNr,lumiSec):
	#~ print runNr, lumiSec
	
	s = open('ReRecoOnly.txt', 'r').read()
	jsonDict = eval(s)	
	#~ print jsonDict
	if str(runNr) in jsonDict.keys():
		found = False
		for x in jsonDict[str(runNr)]:
			
			if not x[0] == x[1]:
				for y in range(x[0],x[1]):
					if lumiSec == y:
						found =  True
						print runNr, lumiSec
			else:
				print lumiSec, x[0]
				if lumiSec == x[0]:
					found =  True
					print runNr, lumiSec
		return found
	else:
		return False

def getHistograms(path,plot,runRange,isMC,backgrounds):


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

		
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	

	return histoEE , histoMM, histoEM

def getTrees(path,plot):


	trees = getDataTrees(path)
		
	treeEE = trees["EE"].CopyTree(plot.cuts)
	treeMM = trees["MM"].CopyTree(plot.cuts)
	treeEM = trees["EM"].CopyTree(plot.cuts)

	

	return treeEE , treeMM, treeEM


def getEvent(path,combination,runNr,lumiSec,eventNr,lookInPrompt=False):
	
	trees = getDataTrees(path)	
	
	event = trees[combination].CopyTree("runNr == %d && lumiSec == %d && eventNr == %d"%(runNr,lumiSec,eventNr))
	
	return event

def compareRecos(path,selection,plots,runRange):
	for name in plots:
		plot = getPlot("mllPlotLowMass")
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	
		
		plot.cuts = plot.cuts
		
		trees = {}
		treesPrompt = {}
				
		trees["EE"], trees["MM"], trees["EM"] = getTrees(path,plot)
		treesPrompt["EE"], treesPrompt["MM"], treesPrompt["EM"]= getTrees("/home/jan/Trees/sw538v0477",plot)	
		
		trees["EE"] = trees["EE"].CopyTree("!((runNr == 194480 && lumiSec >= 9 && lumiSec <=16) || (runNr == 195552 && lumiSec >= 1392 && lumiSec <=1393) || (runNr == 196218 && lumiSec >= 738 && lumiSec <=738) || (runNr == 196239 && lumiSec >= 498 && lumiSec <=502) || (runNr == 199832 && lumiSec >= 58 && lumiSec <=62) || (runNr == 199832 && lumiSec >= 65 && lumiSec <=118) || (runNr == 199832 && lumiSec >= 121 && lumiSec <=139) || (runNr == 199832 && lumiSec >= 142 && lumiSec <=286) || (runNr == 199834 && lumiSec >= 1 && lumiSec <=9) || (runNr == 199834 && lumiSec >= 11 && lumiSec <=11) || (runNr == 199834 && lumiSec >= 14 && lumiSec <=18) || (runNr == 199834 && lumiSec >= 21 && lumiSec <=54) || (runNr == 199834 && lumiSec >= 56 && lumiSec <=57) || (runNr == 199834 && lumiSec >= 62 && lumiSec <=65) || (runNr == 199834 && lumiSec >= 69 && lumiSec <=284) || (runNr == 199834 && lumiSec >= 286 && lumiSec <=503) || (runNr == 199834 && lumiSec >= 505 && lumiSec <=942) || (runNr == 199967 && lumiSec >= 60 && lumiSec <=120) || (runNr == 199967 && lumiSec >= 122 && lumiSec <=170) || (runNr == 199967 && lumiSec >= 172 && lumiSec <=198) || (runNr == 200160 && lumiSec >= 52 && lumiSec <=68) || (runNr == 200161 && lumiSec >= 1 && lumiSec <=97) || (runNr == 200161 && lumiSec >= 100 && lumiSec <=112) || (runNr == 200174 && lumiSec >= 81 && lumiSec <=84) || (runNr == 200177 && lumiSec >= 1 && lumiSec <=56) || (runNr == 200178 && lumiSec >= 1 && lumiSec <=38) || (runNr == 200186 && lumiSec >= 1 && lumiSec <=3) || (runNr == 200186 && lumiSec >= 6 && lumiSec <=24) || (runNr == 203709 && lumiSec >= 1 && lumiSec <=121) || (runNr == 203742 && lumiSec >= 1 && lumiSec <=29) || (runNr == 203777 && lumiSec >= 103 && lumiSec <=113) || (runNr == 203830 && lumiSec >= 82 && lumiSec <=182) || (runNr == 203832 && lumiSec >= 1 && lumiSec <=11) || (runNr == 203833 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203833 && lumiSec >= 73 && lumiSec <=128) || (runNr == 203834 && lumiSec >= 1 && lumiSec <=40) || (runNr == 203835 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203835 && lumiSec >= 73 && lumiSec <=358) || (runNr == 203853 && lumiSec >= 122 && lumiSec <=222) || (runNr == 208352 && lumiSec >= 1 && lumiSec <=15) || (runNr == 208352 && lumiSec >= 17 && lumiSec <=17) || (runNr == 208352 && lumiSec >= 19 && lumiSec <=19))")
		trees["MM"] = trees["MM"].CopyTree("!((runNr == 194480 && lumiSec >= 9 && lumiSec <=16) || (runNr == 195552 && lumiSec >= 1392 && lumiSec <=1393) || (runNr == 196218 && lumiSec >= 738 && lumiSec <=738) || (runNr == 196239 && lumiSec >= 498 && lumiSec <=502) || (runNr == 199832 && lumiSec >= 58 && lumiSec <=62) || (runNr == 199832 && lumiSec >= 65 && lumiSec <=118) || (runNr == 199832 && lumiSec >= 121 && lumiSec <=139) || (runNr == 199832 && lumiSec >= 142 && lumiSec <=286) || (runNr == 199834 && lumiSec >= 1 && lumiSec <=9) || (runNr == 199834 && lumiSec >= 11 && lumiSec <=11) || (runNr == 199834 && lumiSec >= 14 && lumiSec <=18) || (runNr == 199834 && lumiSec >= 21 && lumiSec <=54) || (runNr == 199834 && lumiSec >= 56 && lumiSec <=57) || (runNr == 199834 && lumiSec >= 62 && lumiSec <=65) || (runNr == 199834 && lumiSec >= 69 && lumiSec <=284) || (runNr == 199834 && lumiSec >= 286 && lumiSec <=503) || (runNr == 199834 && lumiSec >= 505 && lumiSec <=942) || (runNr == 199967 && lumiSec >= 60 && lumiSec <=120) || (runNr == 199967 && lumiSec >= 122 && lumiSec <=170) || (runNr == 199967 && lumiSec >= 172 && lumiSec <=198) || (runNr == 200160 && lumiSec >= 52 && lumiSec <=68) || (runNr == 200161 && lumiSec >= 1 && lumiSec <=97) || (runNr == 200161 && lumiSec >= 100 && lumiSec <=112) || (runNr == 200174 && lumiSec >= 81 && lumiSec <=84) || (runNr == 200177 && lumiSec >= 1 && lumiSec <=56) || (runNr == 200178 && lumiSec >= 1 && lumiSec <=38) || (runNr == 200186 && lumiSec >= 1 && lumiSec <=3) || (runNr == 200186 && lumiSec >= 6 && lumiSec <=24) || (runNr == 203709 && lumiSec >= 1 && lumiSec <=121) || (runNr == 203742 && lumiSec >= 1 && lumiSec <=29) || (runNr == 203777 && lumiSec >= 103 && lumiSec <=113) || (runNr == 203830 && lumiSec >= 82 && lumiSec <=182) || (runNr == 203832 && lumiSec >= 1 && lumiSec <=11) || (runNr == 203833 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203833 && lumiSec >= 73 && lumiSec <=128) || (runNr == 203834 && lumiSec >= 1 && lumiSec <=40) || (runNr == 203835 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203835 && lumiSec >= 73 && lumiSec <=358) || (runNr == 203853 && lumiSec >= 122 && lumiSec <=222) || (runNr == 208352 && lumiSec >= 1 && lumiSec <=15) || (runNr == 208352 && lumiSec >= 17 && lumiSec <=17) || (runNr == 208352 && lumiSec >= 19 && lumiSec <=19))")
		trees["EM"] = trees["EM"].CopyTree("!((runNr == 194480 && lumiSec >= 9 && lumiSec <=16) || (runNr == 195552 && lumiSec >= 1392 && lumiSec <=1393) || (runNr == 196218 && lumiSec >= 738 && lumiSec <=738) || (runNr == 196239 && lumiSec >= 498 && lumiSec <=502) || (runNr == 199832 && lumiSec >= 58 && lumiSec <=62) || (runNr == 199832 && lumiSec >= 65 && lumiSec <=118) || (runNr == 199832 && lumiSec >= 121 && lumiSec <=139) || (runNr == 199832 && lumiSec >= 142 && lumiSec <=286) || (runNr == 199834 && lumiSec >= 1 && lumiSec <=9) || (runNr == 199834 && lumiSec >= 11 && lumiSec <=11) || (runNr == 199834 && lumiSec >= 14 && lumiSec <=18) || (runNr == 199834 && lumiSec >= 21 && lumiSec <=54) || (runNr == 199834 && lumiSec >= 56 && lumiSec <=57) || (runNr == 199834 && lumiSec >= 62 && lumiSec <=65) || (runNr == 199834 && lumiSec >= 69 && lumiSec <=284) || (runNr == 199834 && lumiSec >= 286 && lumiSec <=503) || (runNr == 199834 && lumiSec >= 505 && lumiSec <=942) || (runNr == 199967 && lumiSec >= 60 && lumiSec <=120) || (runNr == 199967 && lumiSec >= 122 && lumiSec <=170) || (runNr == 199967 && lumiSec >= 172 && lumiSec <=198) || (runNr == 200160 && lumiSec >= 52 && lumiSec <=68) || (runNr == 200161 && lumiSec >= 1 && lumiSec <=97) || (runNr == 200161 && lumiSec >= 100 && lumiSec <=112) || (runNr == 200174 && lumiSec >= 81 && lumiSec <=84) || (runNr == 200177 && lumiSec >= 1 && lumiSec <=56) || (runNr == 200178 && lumiSec >= 1 && lumiSec <=38) || (runNr == 200186 && lumiSec >= 1 && lumiSec <=3) || (runNr == 200186 && lumiSec >= 6 && lumiSec <=24) || (runNr == 203709 && lumiSec >= 1 && lumiSec <=121) || (runNr == 203742 && lumiSec >= 1 && lumiSec <=29) || (runNr == 203777 && lumiSec >= 103 && lumiSec <=113) || (runNr == 203830 && lumiSec >= 82 && lumiSec <=182) || (runNr == 203832 && lumiSec >= 1 && lumiSec <=11) || (runNr == 203833 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203833 && lumiSec >= 73 && lumiSec <=128) || (runNr == 203834 && lumiSec >= 1 && lumiSec <=40) || (runNr == 203835 && lumiSec >= 1 && lumiSec <=70) || (runNr == 203835 && lumiSec >= 73 && lumiSec <=358) || (runNr == 203853 && lumiSec >= 122 && lumiSec <=222) || (runNr == 208352 && lumiSec >= 1 && lumiSec <=15) || (runNr == 208352 && lumiSec >= 17 && lumiSec <=17) || (runNr == 208352 && lumiSec >= 19 && lumiSec <=19))")
		
		
		#~ for name in treesPrompt:
			#~ for ev in treesPrompt[name]:
				#~ print ev.runNr, ev.lumiSec, ev.eventNr
		#~ 
		#~ 
		#~ 
		reRecoOnly = {}
		promptOnly = {}
		inPromptJSONOnly = 0	
		inReRecoJSONOnly = 0		
		for combination in ["EE","MM","EM"]:
			isNotInOtherTree = 0	
			isNotInOtherTreePrompt = 0	
			inPromptJSONOnly = 0	
			inReRecoJSONOnly = 0				
			nJets = 0	
			nJetsPrompt = 0	
			met = 0	
			metPrompt = 0	
			leptonPt = 0	
			leptonPtPrompt = 0	
			mll = 0	
			mllPrompt = 0	
			print trees[combination].GetEntries(), treesPrompt[combination].GetEntries()
			localReRecoOnly = []
			localPromptOnly = []
			for evReReco in trees[combination]:
				found = False
				for evPrompt in treesPrompt[combination]:
					if evReReco.runNr == evPrompt.runNr and evReReco.lumiSec == evPrompt.lumiSec and evReReco.eventNr == evPrompt.eventNr:
						found = True
				if not found:
					localReRecoOnly.append("%s:%s:%s"%(evReReco.runNr,evReReco.lumiSec,evReReco.eventNr))	 
					inReRecoJSONOnly += int(isReRecoOnly(evReReco.runNr,evReReco.lumiSec))
					lostEvents = getEvent("/home/jan/Trees/sw538v0477",combination,evReReco.runNr,evReReco.lumiSec,evReReco.eventNr)
					if lostEvents.GetEntries() == 0:
						isNotInOtherTree += 1
						if not isReRecoOnly(evReReco.runNr,evReReco.lumiSec):
							print "%d:%d:%d"%(evReReco.runNr,evReReco.lumiSec,evReReco.eventNr)
					else:
						for lostEvent in lostEvents:
							if (lostEvent.met > 100 and lostEvent.nJets < 3) or (lostEvent.met > 150 and lostEvent.nJets < 2):
								nJets += 1
							if (lostEvent.nJets == 2 and lostEvent.met < 150) or (lostEvent.nJets >= 3 and lostEvent.met < 100):
								met += 1
							if lostEvent.pt1 < 20 or lostEvent.pt2 < 20:
								leptonPt += 1
							if lostEvent.p4.M() < 20 or lostEvent.p4.M() > 70:
								mll += 1					   
			
			print "test"
			for evPrompt in treesPrompt[combination]:
				found = False
				for evReReco in trees[combination]:
					if evReReco.runNr == evPrompt.runNr and evReReco.lumiSec == evPrompt.lumiSec and evReReco.eventNr == evPrompt.eventNr:
						found = True
				if not found:
					localPromptOnly.append("%s:%s:%s"%(evPrompt.runNr,evPrompt.lumiSec,evPrompt.eventNr))	 
					inPromptJSONOnly += int(isPromptOnly(evPrompt.runNr,evPrompt.lumiSec))
					lostEvents = getEvent(path,combination,evPrompt.runNr,evPrompt.lumiSec,evPrompt.eventNr)
					if lostEvents.GetEntries() == 0:
						isNotInOtherTreePrompt += 1
						if not isPromptOnly(evPrompt.runNr,evPrompt.lumiSec):
							print "%d:%d:%d"%(evPrompt.runNr,evPrompt.lumiSec,evPrompt.eventNr)
					else:
						for lostEvent in lostEvents:
							if (lostEvent.met > 100 and lostEvent.nJets < 3) or (lostEvent.met > 150 and lostEvent.nJets < 2):
								nJetsPrompt += 1
							if (lostEvent.nJets == 2 and lostEvent.met < 150) or (lostEvent.nJets >= 3 and lostEvent.met < 100):
								metPrompt += 1
							if lostEvent.pt1 < 20 or lostEvent.pt2 < 20:
								leptonPtPrompt += 1
							if lostEvent.p4.M() < 20 or lostEvent.p4.M() > 70:
								mllPrompt += 1						
			reRecoOnly[combination] = localReRecoOnly
			promptOnly[combination] = localPromptOnly
			
			print "%s : %d (%d) ReReco only, %d (%d) Prompt Only"%(combination,len(localReRecoOnly),inReRecoJSONOnly,len(localPromptOnly),inPromptJSONOnly)
			print isNotInOtherTree, isNotInOtherTreePrompt
			print "ReReco: nJets %d MET %d lepton pt %d mll %d"%(nJets,met,leptonPt,mll)
			print "Prompt: nJets %d MET %d lepton pt %d mll %d"%(nJetsPrompt,metPrompt,leptonPtPrompt,mllPrompt)
			#~ 
			
def main():

	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
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
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")						  				
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.signal
	if len(args.selection) == 0:
		#~ args.selection.append(regionsToUse.rSFOF.central.name)	
		#~ args.selection.append(regionsToUse.rSFOF.forward.name)	
		#~ args.selection.append(regionsToUse.rSFOF.inclusive.name)	
		#~ args.selection.append(regionsToUse.rOutIn.central.name)	
		#~ args.selection.append(regionsToUse.rOutIn.forward.name)	
		#~ args.selection.append(regionsToUse.rOutIn.inclusive.name)	
		args.selection.append(regionsToUse.signal.central.name)	
		#~ args.selection.append(regionsToUse.signal.forward.name)	
		#~ args.selection.append(regionsToUse.signal.inclusive.name)	
		#~ args.selection.append(regionsToUse.rMuE.central.name)	
		#~ args.selection.append(regionsToUse.rMuE.forward.name)	
		#~ args.selection.append(regionsToUse.rMuE.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPath	


	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
		if args.mc:
			cmsExtra = "#splitline{Private Work}{Simulation}"
	elif args.mc:
		cmsExtra = "Simulation"	
	else:
		cmsExtra = "Preliminary"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)			



			compareRecos(path,selection,args.plots,runRange)
	
	
	
main()
