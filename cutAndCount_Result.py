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
from helpers import getDataTrees, TheStack, totalNumberOfGeneratedEvents, Process, readTrees, createHistoFromTree


from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics
from corrections import rMuELeptonPt

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
			#~ print comb
			for ev in subtree:
				
				#~ print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
				cols = []
				for varName in colNames:
					cols.append( getattr(ev, varName) )
				result[comb].add(tuple(cols))
			subtree.IsA().Destructor(subtree) ### ROOT destructor to really get the memeory released
			gc.collect()
	return result

def getCounts(trees, cut, isMC, backgrounds,plot,runRange,path,region):
	if isMC:
		tmpCut = plot.cuts
		plot.cuts = cut
		source = ""
		modifier = ""
		eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histEE = TheStack(processes,runRange.lumi,plot,trees["EE"],"None",1.0,1.0,1.0).theHistogram		
		histMM = TheStack(processes,runRange.lumi,plot,trees["MM"],"None",1.0,1.0,1.0).theHistogram
		histEM = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram
		
		offsetError = (systematics.rMuE.inclusive.val**2 + (rMuELeptonPt.inclusive.offsetErrMC/rMuELeptonPt.inclusive.offsetMC)**2)**0.5
		fallingError = (systematics.rMuE.inclusive.val**2 + (rMuELeptonPt.inclusive.fallingErrMC/rMuELeptonPt.inclusive.fallingMC)**2)**0.5
		cutRMuEScaled = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offsetMC,getattr(rMuELeptonPt,region).fallingMC,getattr(rMuELeptonPt,region).offsetMC,getattr(rMuELeptonPt,region).fallingMC)
		cutRMuEScaledUp = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offsetMC*(1+offsetError),getattr(rMuELeptonPt,region).fallingMC*(1+fallingError),getattr(rMuELeptonPt,region).offsetMC*(1+offsetError),getattr(rMuELeptonPt,region).fallingMC*(1+fallingError))
		cutRMuEScaledDown = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offsetMC*(1-offsetError),getattr(rMuELeptonPt,region).fallingMC*(1-fallingError),getattr(rMuELeptonPt,region).offsetMC*(1-offsetError),getattr(rMuELeptonPt,region).fallingMC*(1-fallingError))
		
		plot.cuts = cutRMuEScaled
		histEMRMuEScaled = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
		plot.cuts = cutRMuEScaledUp
		histEMRMuEScaledUp = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
		plot.cuts = cutRMuEScaledDown
		histEMRMuEScaledDown = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
				
		
		eeErr = ROOT.Double()
		ee = histEE.IntegralAndError(1,histEE.GetNbinsX(),eeErr)
		mmErr = ROOT.Double()
		mm = histMM.IntegralAndError(1,histMM.GetNbinsX(),mmErr)
		emErr = ROOT.Double()
		em = histEM.IntegralAndError(1,histEM.GetNbinsX(),emErr)
		
		emRMuEScaledErr = ROOT.Double()
		emRMuEScaled = histEMRMuEScaled.IntegralAndError(1,histEMRMuEScaled.GetNbinsX(),emRMuEScaledErr)
		emRMuEScaledUpErr = ROOT.Double()
		emRMuEScaledUp = histEMRMuEScaledUp.IntegralAndError(1,histEMRMuEScaledUp.GetNbinsX(),emRMuEScaledUpErr)
		emRMuEScaledDownErr = ROOT.Double()
		emRMuEScaledDown = histEMRMuEScaledDown.IntegralAndError(1,histEMRMuEScaledDown.GetNbinsX(),emRMuEScaledDownErr)
		
		
		
		n= {
			"MM": ee,
			"EE": mm,
			"EM": em,
			"EMRMuEScaled": emRMuEScaled,
			"EMRMuEScaledUp": emRMuEScaledUp,
			"EMRMuEScaledDown": emRMuEScaledDown,
			}
		n["MMStatErr"] = float(eeErr)	
		n["EEStatErr"] = float(mmErr)	
		n["EMStatErr"] = float(emErr)				
		
		plot.cuts = tmpCut
		
	else:
		offsetError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).offsetErr/getattr(rMuELeptonPt,region).offset)**2)**0.5
		fallingError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).fallingErr/getattr(rMuELeptonPt,region).falling)**2)**0.5	
		cutRMuEScaled = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offset,getattr(rMuELeptonPt,region).falling,getattr(rMuELeptonPt,region).offset,getattr(rMuELeptonPt,region).falling)
		cutRMuEScaledUp = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offset*(1+offsetError),getattr(rMuELeptonPt,region).falling*(1+fallingError),getattr(rMuELeptonPt,region).offset*(1+offsetError),getattr(rMuELeptonPt,region).falling*(1+fallingError))
		cutRMuEScaledDown = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(cut,getattr(rMuELeptonPt,region).offset*(1-offsetError),getattr(rMuELeptonPt,region).falling*(1-fallingError),getattr(rMuELeptonPt,region).offset*(1-offsetError),getattr(rMuELeptonPt,region).falling*(1-fallingError))
		
		n= {
			"MM": trees["MM"].GetEntries(cut),
			"EE": trees["EE"].GetEntries(cut),
			"EM": trees["EM"].GetEntries(cut),
			"EMRMuEScaled": createHistoFromTree(trees["EM"],"mll",cutRMuEScaled,100,0,1000).Integral(0,-1),
			"EMRMuEScaledUp": createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUp,100,0,1000).Integral(0,-1),
			"EMRMuEScaledDown": createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDown,100,0,1000).Integral(0,-1),
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
		treesEE = readTrees(path,"EE",source = "",modifier= "")
		treesEM = readTrees(path,"EMu",source = "",modifier= "")
		treesMM = readTrees(path,"MuMu",source = "",modifier= "")		
		trees = {
				"EE":treesEE,
				"MM":treesMM,
				"EM":treesEM,
		}
	
	if "Central" in selection.name:
		region = "central"	
	elif "Forward" in selection.name:
		region = "forward"	
	else:
		region = "inclusive"		

	for plotName in plots:
		plot = getPlot(plotName)
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut
		plot.variable = plot.variable.replace("p4.M()","mll")	


		counts = {}
		eventLists = {}
		#~ massRanges = ["default","edgeMass","zMass","highMass","belowZ","aboveZ"]
		massRanges = ["edgeMass"]
		counts["default"] = {}
		eventLists["default"] = {}
		for mllCut in massRanges:
			cut = plot.cuts + "*(%s)"%getattr(theCuts.massCuts,mllCut).cut
			cut = cut.replace("p4.M()","mll")
			cut = cut.replace("p4.Pt()","pt")
			cut = cut.replace(" metFilterSummary > 0 &&","")
			cut = cut.replace(" triggerSummary > 0 &&","")
			cut = cut.replace("genWeight*","")
			cut = cut.replace("weight*","")
			cut = cut.replace("leptonFullSimScaleFactor1*","")
			cut = cut.replace("leptonFullSimScaleFactor2*","")
			cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
			cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
			#~ cut = "genWeight*weight*("+cut+")"
			counts["default"][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path,region)
			eventLists["default"][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees, cut,isMC)		
			

		
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
		args.selection.append(regionsToUse.signal.legacy.name)	
		#~ args.selection.append(regionsToUse.signalOld.forward.name)	
		#~ args.selection.append(regionsToUse.signalOld.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	


	path = locations.dataSetPathNLL

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

