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

import ratios


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






def plotReRecoComparison(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,doLog=True):	

	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	
		hists = {}
		histsPrompt = {}
		hists["EE"], hists["MM"], hists["EM"] = getHistograms(path,plot,runRange,isMC, backgrounds)
		histsPrompt["EE"], histsPrompt["MM"], histsPrompt["EM"]= getHistograms("/home/jan/Trees/sw538v0477",plot,runRange,isMC, backgrounds)
			
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()	

		legend = TLegend(0.6, 0.65, 0.95, 0.95)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)		
		
		
		for combination in ["EE","MM","EM"]:
			hCanvas.Clear()	
			
			legend.Clear()
			plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
			ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
			style = setTDRStyle()	
			style.SetOptStat(0)	
			plotPad.UseCurrentStyle()
			ratioPad.UseCurrentStyle()
			plotPad.Draw()	
			ratioPad.Draw()	
			plotPad.cd()	


			hists[combination].SetMarkerStyle(21)
			histsPrompt[combination].SetMarkerStyle(22)
			hists[combination].SetMarkerColor(ROOT.kGreen+3)
			histsPrompt[combination].SetMarkerColor(ROOT.kBlack)
			hists[combination].SetLineColor(ROOT.kGreen+3)
			histsPrompt[combination].SetLineColor(ROOT.kBlack)
			
			if doLog: 
				yMin=0.1
				yMax = max(hists[combination].GetBinContent(hists[combination].GetMaximumBin()),histsPrompt[combination].GetBinContent(histsPrompt[combination].GetMaximumBin()))*10
				plotPad.SetLogy()
			else: 
				yMin=0
				yMax = max(hists[combination].GetBinContent(hists[combination].GetMaximumBin()),histsPrompt[combination].GetBinContent(histsPrompt[combination].GetMaximumBin()))*1.5
			plotPad.DrawFrame(plot.firstBin,yMin,plot.lastBin,yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))

			hists[combination].Draw("samep")
			histsPrompt[combination].Draw("samep")
			
			legend.AddEntry(histsPrompt[combination],"Prompt reconstruction","p")	
			legend.AddEntry(hists[combination],"Jan22 ReReco","p")
			#~ 

			#~ 
				
			legend.Draw("same")

			latex.DrawLatex(0.94, 0.96, "19.4-%s fb^{-1} (8 TeV)"%runRange.printval)
			

			latexCMS.DrawLatex(0.19,0.89,"CMS")
			if "Simulation" in cmsExtra:
				yLabelPos = 0.82	
			else:
				yLabelPos = 0.85	

			latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))


			latex.DrawLatex(0.9, 0.25, "yield ReReco: %d#pm%d  yield prompt: %d#pm%d ratio: %.3f" % (hists[combination].Integral(),hists[combination].Integral()**0.5,histsPrompt[combination].Integral(),histsPrompt[combination].Integral()**0.5,hists[combination].Integral()/histsPrompt[combination].Integral()))

			
			print hists[combination].Integral(), "+/-", hists[combination].Integral()**0.5 , histsPrompt[combination].Integral(), "+/-", histsPrompt[combination].Integral()**0.5,hists[combination].Integral()/histsPrompt[combination].Integral()
			
			ratioPad.cd()
			
			#~ ratio = ROOT.TGraphAsymmErrors(hists[combination],histsPrompt[combination],"cp")
			#~ ratio.SetMarkerStyle(20)
			#~ ratio.SetMarkerColor(ROOT.kGreen+3)
			#~ ratio.SetLineColor(ROOT.kGreen+3)
			ratioGraphs =  ratios.RatioGraph(hists[combination],histsPrompt[combination], plot.firstBin, plot.lastBin,title="ReReco/Prompt",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kGreen+3,adaptiveBinning=0.25,labelSize=0.135)
			#~ 
			ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
			
			#~ ratioPad.DrawFrame(plot.firstBin,0,plot.lastBin,2,"; %s ; %s" %("","ReReco/Prompt"))
			#~ ratio.Draw("saeme")
			logLabel = "Log"
			if not doLog:
				logLabel = "NoLog"
			hCanvas.Print("fig/reRecoCompare_%s_%s_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName,combination,logLabel))	
			
		
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
		args.plots = plotLists.default
	if len(args.selection) == 0:
		#~ args.selection.append(regionsToUse.rSFOF.central.name)	
		#~ args.selection.append(regionsToUse.rSFOF.forward.name)	
		#~ args.selection.append(regionsToUse.rSFOF.inclusive.name)	
		#~ args.selection.append(regionsToUse.rOutIn.central.name)	
		#~ args.selection.append(regionsToUse.rOutIn.forward.name)	
		#~ args.selection.append(regionsToUse.rOutIn.inclusive.name)	
		#~ args.selection.append(regionsToUse.signal.central.name)	
		#~ args.selection.append(regionsToUse.signal.forward.name)	
		#~ args.selection.append(regionsToUse.signal.inclusive.name)	
		args.selection.append(regionsToUse.rMuE.central.name)	
		args.selection.append(regionsToUse.rMuE.forward.name)	
		args.selection.append(regionsToUse.rMuE.inclusive.name)	
		args.selection.append("Region")	

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



			plotReRecoComparison(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,doLog=False)	
			plotReRecoComparison(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,doLog=True)	
	
	
	
main()
