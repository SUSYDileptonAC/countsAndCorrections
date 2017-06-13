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


from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, cutNCountXChecks
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

def getCounts(trees, cut, isMC, backgrounds,plot,runRange,path):

	if isMC:
		source = ""
		modifier = ""
		eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		n= {}
		for region in ["central","forward"]:
			plot.cuts = cut
			if region = "central":
				plot.cuts = cut.replace("weight*(","weight*((abs(eta1)<1.4 && abs(eta2)<1.4) &&")
			elif region =="forward":
				plot.cuts = cut.replace("weight*(","weight*((1.4 <= TMath::Max(abs(eta1),abs(eta2)))")
		
			histEE = TheStack(processes,runRange.lumi,plot,trees["EE"],"None",1.0,1.0,1.0).theHistogram		
			histMM = TheStack(processes,runRange.lumi,plot,trees["MM"],"None",1.0,1.0,1.0).theHistogram
			histEM = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram
							
			histEE.Scale(getattr(triggerEffs,region).effEE.val)
			histMM.Scale(getattr(triggerEffs,region).effMM.val)	
			histEM.Scale(getattr(triggerEffs,region).effEM.val)	
		
			offsetError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).offsetErrMC/getattr(rMuELeptonPt,region).offsetMC)**2)**0.5
			fallingError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).fallingErrMC/getattr(rMuELeptonPt,region).fallingMC)**2)**0.5
			cutRMuEScaled = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offsetMC,getattr(rMuELeptonPt,region).fallingMC,getattr(rMuELeptonPt,region).offsetMC,getattr(rMuELeptonPt,region).fallingMC)
			cutRMuEScaledUp = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offsetMC*(1+offsetError),getattr(rMuELeptonPt,region).fallingMC*(1+fallingError),getattr(rMuELeptonPt,region).offsetMC*(1+offsetError),getattr(rMuELeptonPt,region).fallingMC*(1+fallingError))
			cutRMuEScaledDown = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offsetMC*(1-offsetError),getattr(rMuELeptonPt,region).fallingMC*(1-fallingError),getattr(rMuELeptonPt,region).offsetMC*(1-offsetError),getattr(rMuELeptonPt,region).fallingMC*(1-fallingError))
		
		
			plot.cuts = cutRMuEScaled
			histEMRMuEScaled = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
			histEMRMuEScaled.Scale(getattr(triggerEffs,region).effEM.val)	
					
			plot.cuts = cutRMuEScaledUp
			histEMRMuEScaledUp = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
			histEMRMuEScaledUp.Scale(getattr(triggerEffs,region).effEM.val)		
				
			plot.cuts = cutRMuEScaledDown
			histEMRMuEScaledDown = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram				
			histEMRMuEScaledDown.Scale(getattr(triggerEffs,region).effEM.val)				
				
		
			eeErr = ROOT.Double()
			ee = histEE.IntegralAndError(0,-1,eeErr)
			mmErr = ROOT.Double()
			mm = histMM.IntegralAndError(0,-1,mmErr)
			emErr = ROOT.Double()
			em = histEM.IntegralAndError(0,-1,emErr)
			
			emRMuEScaledErr = ROOT.Double()
			emRMuEScaled = histEMRMuEScaled.IntegralAndError(0,-1,emRMuEScaledErr)
			emRMuEScaledUpErr = ROOT.Double()
			emRMuEScaledUp = histEMRMuEScaledUp.IntegralAndError(0,-1,emRMuEScaledUpErr)
			emRMuEScaledDownErr = ROOT.Double()
			emRMuEScaledDown = histEMRMuEScaledDown.IntegralAndError(0,-1,emRMuEScaledDownErr)
			
			n["MM_"+region] = mm
			n["EE_"+region] = ee
			n["EM_"+region] = em
			
			n["EMRMuEScaled_"+region] = emRMuEScaled
			n["EMRMuEScaledUp_"+region] = emRMuEScaledUp
			n["EMRMuEScaledDown_"+region] = emRMuEScaledDown
			
			n["MMStatErr_"+region] = float(mmErr)
			n["EEStatErr_"+region] = float(eeErr)
			n["EMStatErr_"+region] = float(emErr)

		
	else:
		n= {}
		for region in ["central","forward"]:
			plot.cuts = cut
			if region = "central":
				plot.cuts = cut.replace("weight*(","weight*((abs(eta1)<1.4 && abs(eta2)<1.4) &&")
			elif region =="forward":
				plot.cuts = cut.replace("weight*(","weight*((1.4 <= TMath::Max(abs(eta1),abs(eta2)))")	
				
			offsetError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).offsetErr/getattr(rMuELeptonPt,region).offset)**2)**0.5
			fallingError = (getattr(systematics.rMuE,region).val**2 + (getattr(rMuELeptonPt,region).fallingErr/getattr(rMuELeptonPt,region).falling)**2)**0.5	
			cutRMuEScaled = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offset,getattr(rMuELeptonPt,region).falling,getattr(rMuELeptonPt,region).offset,getattr(rMuELeptonPt,region).falling)
			cutRMuEScaledUp = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offset*(1+offsetError),getattr(rMuELeptonPt,region).falling*(1+fallingError),getattr(rMuELeptonPt,region).offset*(1+offsetError),getattr(rMuELeptonPt,region).falling*(1+fallingError))
			cutRMuEScaledDown = "(%s)*0.5*((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))+ pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),-1))"%(plot.cuts,getattr(rMuELeptonPt,region).offset*(1-offsetError),getattr(rMuELeptonPt,region).falling*(1-fallingError),getattr(rMuELeptonPt,region).offset*(1-offsetError),getattr(rMuELeptonPt,region).falling*(1-fallingError))
			
				
			n["MM_"+region] = trees["MM"].GetEntries(plot.cuts)
			n["EE_"+region] = trees["EE"].GetEntries(plot.cuts)
			n["EM_"+region] = trees["EM"].GetEntries(plot.cuts)
			n["EMRMuEScaled_"+region] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled,100,0,1000).Integral(0,-1)
			n["EMRMuEScaledUp_"+region] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUp,100,0,1000).Integral(0,-1)
			n["EMRMuEScaledDown_"+region] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDown,100,0,1000).Integral(0,-1)

			n["MMStatErr_"+region] = n["MM_"+region]**0.5	
			n["EEStatErr_"+region] = n["EE_"+region]**0.5	
			n["EMStatErr_"+region] = n["EM_"+region]**0.5	
		
	n["cut"] = cut
	return n
	


	
	
	
	


def cutAndCountForRegion(path,selection,plots,runRange,isMC,backgrounds):
	
	
	if not isMC:
		trees = getDataTrees(path)
		for label, tree in trees.iteritems():
			trees[label] = tree.CopyTree("nJets > 1")		
	else:
		treesEE = readTrees(path,"EE",source = "",modifier= "")
		treesEM = readTrees(path,"EMu",source = "",modifier= "")
		treesMM = readTrees(path,"MuMu",source = "",modifier= "")		
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
		
		massBins = ["mass20To60","mass60To81","mass60To86","mass81To101","mass86To96","mass96To150","mass101To150","mass150To200","mass200To300","mass300To400","mass400","highMassOld","highMass","lowMass","lowMassOld"]
		nLLRegions = ["lowNLL","highNLL"]
		MT2Regions = ["lowMT2","highMT2"]
		
		counts["default"] = {}
		eventLists["default"] = {}
		for mllCut in massBins:
			cut = plot.cuts + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
			cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
			#~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
			if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
				cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
			cut = cut.replace("p4.M()","mll")
			cut = cut.replace("p4.Pt()","pt")
			cut = cut.replace("metFilterSummary > 0 &&","")
			cut = cut.replace("triggerSummary > 0 &&","")
			cut = cut.replace("genWeight*","")
			cut = cut.replace("weight*","")
			cut = cut.replace("leptonFullSimScaleFactor1*","")
			cut = cut.replace("leptonFullSimScaleFactor2*","")
			cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
			#~ cut = "genWeight*weight*("+cut+")"
				
			
			counts["default"][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)
			#~ eventLists["default"][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees,cut,isMC)		

		for nLLRegion in nLLRegions:		
			counts[nLLRegion] = {}
			eventLists[nLLRegion] = {}					
			
			for mllCut in massBins:
				cut = plot.cuts+" && (%s)"%getattr(theCuts.nLLCuts,nLLRegion).cut
				cut = cut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
				cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
				#~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
				if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
					cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
				cut = cut.replace("p4.M()","mll")
				cut = cut.replace("p4.Pt()","pt")
				cut = cut.replace("metFilterSummary > 0 &&","")
				cut = cut.replace("triggerSummary > 0 &&","")
				cut = cut.replace("genWeight*","")
				cut = cut.replace("weight*","")
				cut = cut.replace("leptonFullSimScaleFactor1*","")
				cut = cut.replace("leptonFullSimScaleFactor2*","")
				cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
				#~ cut = "genWeight*weight*("+cut+")"
			
				counts[nLLRegion][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)
				
			for MT2Region in MT2Regions:
				for mllCut in massBins:
					cut = plot.cuts+" && (%s)"%getattr(theCuts.nLLCuts,nLLRegion).cut
					cut = cut + " && (%s)"%getattr(theCuts.mt2Cuts,MT2Region).cut
					cut = cut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
					cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
					#~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
					if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
						cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
					cut = cut.replace("p4.M()","mll")
					cut = cut.replace("p4.Pt()","pt")
					cut = cut.replace("metFilterSummary > 0 &&","")
					cut = cut.replace("triggerSummary > 0 &&","")
					cut = cut.replace("genWeight*","")
					cut = cut.replace("weight*","")
					cut = cut.replace("leptonFullSimScaleFactor1*","")
					cut = cut.replace("leptonFullSimScaleFactor2*","")
					cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
					#~ cut = "genWeight*weight*("+cut+")"
			
					counts[nLLRegion][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path)

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
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	

					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.signal
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.signal.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	


	path = locations.dataSetPathNLL
	
			
	

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)
			
			
			if args.write:

				import subprocess

				bashCommand = "cp shelves/cutAndCountNLL_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())		
			
			else:
				counts = cutAndCountForRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds)
				outFile = open("shelves/cutAndCountNLL_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(counts, outFile)
				outFile.close()
			


		

main()

