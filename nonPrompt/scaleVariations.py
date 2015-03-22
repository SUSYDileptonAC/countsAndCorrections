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
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import triggerEffs, rSFOF
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics
from locations import locations



def getHistograms(path,plot,runRange,backgrounds,region):


	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
			
	eventCounts = totalNumberOfGeneratedEvents(path)	
	processes = []
	for background in backgrounds:
		processes.append(Process(getattr(Backgrounds,background),eventCounts))
	
	histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
	histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
	histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
	

	return histoEE , histoMM, histoEM
def getTrees(path,plot,runRange,background,region):


	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
				
	
	for index, tree in treesEE.iteritems():
		if index == background:
			treeEE = tree	
	for index, tree in treesMM.iteritems():
		if index == background:
			treeMM = tree	
	for index, tree in treesEM.iteritems():
		if index == background:
			treeEM = tree	

	return treeEE.CopyTree(plot.cuts) , treeMM.CopyTree(plot.cuts), treeEM.CopyTree(plot.cuts)

	
	
def signalRegion(path,selection,plots,runRange,backgrounds,cmsExtra):

	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		#~ plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	
		plot.cuts = plot.cuts.replace("weight*","")
		print runRange.lumi
		#~ plot.cuts = plot.cuts+"*!((abs(motherPdgId1) == 15 || abs(motherPdgId1) == 24 || abs(motherPdgId1) == 23) && (abs(motherPdgId2) == 15 || abs(motherPdgId2) == 24 || abs(motherPdgId2) == 23))"
		#~ plot.cuts = plot.cuts+"*!(abs(motherPdgId1) == 15 || abs(motherPdgId1) == 24 || abs(motherPdgId1) == 23 || abs(motherPdgId2) == 15 || abs(motherPdgId2) == 24 || abs(motherPdgId2) == 23)"
		#~ plot.cuts = plot.cuts+"*!((abs(motherPdgId1) != 15 && abs(motherPdgId1) != 24 && abs(motherPdgId1) != 23) || (abs(motherPdgId2) != 15 && abs(motherPdgId2) != 24 && abs(motherPdgId2) != 23))"
		#~ plot.cuts = plot.cuts+"*((abs(pdgId1) != 11 && abs(pdgId1) != 13 && abs(pdgId1) != 15) || ( abs(pdgId2) != 11 && abs(pdgId2) != 13 && abs(pdgId2) != 15))"
		if not "Forward" in selection.name:
			corr = rSFOF.central.val
			corrErr = rSFOF.central.err
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			corr = rSFOF.forward.val
			corrErr = rSFOF.forward.err
			region = "forward"
		#~ 
		#~ eventCounts = totalNumberOfGeneratedEvents(path)	
#~ 
		#~ for background in backgrounds:
			#~ process = Process(getattr(Backgrounds,background),eventCounts)
			#~ for subprocess in process.samples:
				#~ 
				#~ print subprocess
				#~ treeEE, treeMM, treeEM = getTrees(path,plot,runRange, subprocess,region)
				#~ for ev in treeMM:
					#~ 
					#~ print ev.motherPdgId1, ev.motherPdgId2
	
				#~ print treeEE.GetEntries(), treeMM.GetEntries(), treeEM.GetEntries()
		histEE, histMM, histOF = getHistograms(path,plot,runRange, backgrounds,region)	
		print histEE.Integral(), histMM.Integral(), histOF.Integral()
		print histEE.GetEntries(), histMM.GetEntries(), histOF.GetEntries()
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		
		style=setTDRStyle()
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()				
		logScale = plot.log
		if plot.variable == "met" or plot.variable == "type1Met" or plot.variable == "tcMet" or plot.variable == "caloMet" or plot.variable == "mht":
			logScale = True		

		yMax = histEE.GetBinContent(histEE.GetMaximumBin()) + histMM.GetBinContent(histMM.GetMaximumBin())
		
		if logScale:
			yMax = yMax*1000
		else:
			yMax = yMax*1.5
							
		#~ else: yMax = plot.yMax		
		
		
		plotPad.DrawFrame(plot.firstBin,plot.yMin,plot.lastBin,yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))	
		
		
		
		
		histSF = histEE.Clone("histSF")
		histSF.Add(histMM.Clone())
		
		histSF.SetMarkerStyle(20)
		histOF.SetLineColor(ROOT.kBlue)
		histEE.SetLineColor(ROOT.kRed)
		histMM.SetLineColor(ROOT.kGreen+3)
		histEE.SetLineStyle(ROOT.kDashed)
		histMM.SetLineStyle(ROOT.kDashed)
		
		
		histSF.Draw("samep")
		histOF.Draw("samehist")
		histEE.Draw("samehist")
		histMM.Draw("samehist")
				
		latex = ROOT.TLatex()
		latex.SetTextSize(0.04)
		latex.SetNDC(True)

		legend = TLegend(0.5, 0.6, 0.95, 0.95)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		entryHist = TH1F()
		entryHist.SetFillColor(ROOT.kWhite)
		legend.AddEntry(entryHist,selection.latex,"h")
		legend.AddEntry(histSF,"SF","p")
		legend.AddEntry(histEE,"EE","l")
		legend.AddEntry(histMM,"MM","l")
		legend.AddEntry(histOF,"OF","l")

		
		legend.Draw("same")
	



		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetNDC(True)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)

		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)				

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))		
		
		plotPad.RedrawAxis()	
		hCanvas.Print("fig/nonPromptMC_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
	
def main():



	parser = argparse.ArgumentParser(description='rMuE measurements.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=True,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")	
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	

	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.nonPrompt
	if len(args.plots) == 0:
		args.plots = plotLists.default
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.rOutIn.central.name)	
		args.selection.append(regionsToUse.rOutIn.forward.name)	
		args.selection.append(regionsToUse.rOutIn.inclusive.name)
		args.selection.append(regionsToUse.signal.central.name)	
		args.selection.append(regionsToUse.signal.forward.name)	
		args.selection.append(regionsToUse.signal.inclusive.name)
			
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)		

	path = locations.dataSetPath	

	#~ path = "/home/jan/Trees/sw538v0477"

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

			signalRegion(path,selection,args.plots,runRange,args.backgrounds,cmsExtra)

main()
