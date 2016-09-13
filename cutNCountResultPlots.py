#!/usr/bin/env python

### routine to make the result plot for the counting experiment

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


plotNames = {"default":"mllPlot","noBTags":"mllPlotNoBTags","geOneBTags":"mllPlotGeOneBTags","geTwoBTags":"mllPlotGeTwoBTags"}


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors, TFile, TH2F
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds, defineMyColors, myColors,sbottom_masses

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process,createMyColors,createHistoFromTree 

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rOutIn, rOutInEE, rOutInMM, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, zPredictions, OtherPredictions, OnlyZPredictions
import corrections
import ratios
from locations import locations

		
### routines to get the different histograms	
def getSignalMCHistograms(path,plot,runRange,sampleName,verbose=True):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")

	histoEE = getDataHist(plot,treesEE,dataname = sampleName,verbose=verbose)
	histoMM = getDataHist(plot,treesMM,dataname = sampleName,verbose=verbose)
	histoEM = getDataHist(plot,treesEM,dataname = sampleName,verbose=verbose)

	return histoEE , histoMM, histoEM
	
def getHistograms(path,plot,runRange,verbose=True):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	histoEE = getDataHist(plot,treesEE,verbose=verbose)
	histoMM = getDataHist(plot,treesMM,verbose=verbose)
	histoEM = getDataHist(plot,treesEM,verbose=verbose)
	
	return histoEE , histoMM, histoEM

### get an additional histogram for the uncertainties both in the main plot and the ratio
def getErrHist(plot,bSelection,region,ofHist,dyHist,rSFOFErr):
	
	### get Z prediction and rOutIn factors
	localZPred = getattr(zPredictions,bSelection).SF
	localROutIn = rOutIn
	
	### Histogram for the systematic uncertainties
	hist = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	
	### Histograms to plot the error band in the ratio
	histUp = TH1F("errHistUp","errHistUp",plot.nBins,plot.firstBin,plot.lastBin)
	histDown = TH1F("errHistDown","errHistDown",plot.nBins,plot.firstBin,plot.lastBin)
	
	### Graph that holds the uncertainties for the main plot
	graph = TGraphAsymmErrors()
	
	
	### Set bin content of error histogram to 1 and error to rSFOF uncertainty 
	### which is the systematic uncertainty of the flavor-symmetric prediction
	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinContent(i,1)
		hist.SetBinError(i,ofHist.GetBinContent(i)*rSFOFErr)
		
	### Take uncertainty on Z prediction and R_Out/In into account, if a DY histogram is given
	if dyHist is not None:
		
		### loop over mass regions. OnZ has to be treated differently since no R_Out/In factor is used
		for massRegion in ["lowMass","belowZ","aboveZ","highMass"]:
			for i in range(hist.FindBin(getattr(mllBins,massRegion).low+0.01),hist.FindBin(getattr(mllBins,massRegion).high-0.01 + 1)):				
				if region == "inclusive":
					zErrCentral = (((localZPred.central.err*getattr(localROutIn,massRegion).central.val)**2 + (localZPred.central.val*getattr(localROutIn,massRegion).central.err)**2)**0.5) / (localZPred.central.val*getattr(localROutIn,massRegion).central.val) * dyHist.GetBinContent(i)
					zErrForward = (((localZPred.forward.err*getattr(localROutIn,massRegion).forward.val)**2 + (localZPred.forward.val*getattr(localROutIn,massRegion).forward.err)**2)**0.5) / (localZPred.forward.val*getattr(localROutIn,massRegion).forward.val) * dyHist.GetBinContent(i)
					
					zErr = (zErrCentral**2 + zErrForward**2)**0.5
				else:
					zErr = (((getattr(localZPred,region).err*getattr(getattr(localROutIn,massRegion),region).val)**2 + (getattr(localZPred,region).val*getattr(getattr(localROutIn,massRegion),region).err)**2)**0.5) / ((getattr(localZPred,region).val*getattr(getattr(localROutIn,massRegion),region).val)) * dyHist.GetBinContent(i)
								
				hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 
		
		### on Z	 
		for i in range(hist.FindBin(mllBins.onZ.low+0.01),hist.FindBin(mllBins.onZ.high-0.01)):
			if region == "inclusive":
				zErrCentral = (localZPred.central.err / localZPred.central.val) * dyHist.GetBinContent(i)
				zErrForward = (localZPred.forward.err / localZPred.forward.val) * dyHist.GetBinContent(i)
				
				zErr = (zErrCentral**2 + zErrForward**2)**0.5
			else:
				zErr = (getattr(localZPred,region).err / getattr(localZPred,region).val) * dyHist.GetBinContent(i) 
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 

		### Set points for the main plot. 
		### Content is (i, center of bin(i),  background prediction in bin(i))
		### Error is (i, 0.5*BinWidthX, 0.5*BinWidthX, sqrt(systUnc**2 + statUnc**2), sqrt(systUnc**2 + statUnc**2) )
		### Systematic uncertainty comes from hist, statistics from the background histograms
		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),dyHist.GetBinContent(i) + ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5)			
		
		### Set histograms for the band in the ratio plot
		### Add/subtract uncertainty from background prediction
		for i in range(0,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) - hist.GetBinError(i))
			
	
	### Same if no DY histogram is given
	else:
		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5)	
		for i in range(0,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,ofHist.GetBinContent(i) - hist.GetBinError(i))			
		
	return graph, histUp, histDown

### lines to mark the different signal regions
def getLines(yMin,yMax, xPos = [70.,81., 101., 120.]):
	from ROOT import TLine, kGray
	result = []
	for x in xPos:
		result.append(TLine(x, yMin, x,yMax))
		result[-1].SetLineWidth(1)
		result[-1].SetLineColor(kGray+2)
		result[-1].SetLineStyle(2)
	return result

### main plot routine	
def makePlot(sfHist,ofHist,selection,plot,runRange,region,cmsExtra,bSelection,path,dyHist=None,lowMassEdge=False,differentEdgePositions=False,stackSignal=False,verbose=True):

	### get canvas, pads and style
	
	colors = createMyColors()	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	ROOT.gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()

	yMax = sfHist.GetBinContent(sfHist.GetMaximumBin())
	
	if plot.yMax == 0:
		yMax = yMax*2.25
		#~ if lowMassEdge or differentEdgePositions: 
			#~ yMax = yMax*1.75 
		#~ else:
			#~ yMax = yMax*2.
						
	else: 
		yMax = plot.yMax
					
	
	plotPad.DrawFrame(plot.firstBin,0,plot.lastBin, yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	#set overflow bin
	sfHist.SetBinContent(sfHist.GetNbinsX(),sfHist.GetBinContent(sfHist.GetNbinsX())+sfHist.GetBinContent(sfHist.GetNbinsX()+1))
	sfHist.SetBinError(sfHist.GetNbinsX(),(sfHist.GetBinContent(sfHist.GetNbinsX())+sfHist.GetBinContent(sfHist.GetNbinsX()+1))**0.5)
	ofHist.SetBinContent(ofHist.GetNbinsX(),ofHist.GetBinContent(ofHist.GetNbinsX())+ofHist.GetBinContent(ofHist.GetNbinsX()+1))
	ofHist.SetBinError(ofHist.GetNbinsX(),(ofHist.GetBinContent(ofHist.GetNbinsX())+ofHist.GetBinContent(ofHist.GetNbinsX()+1))**0.5)

	
	bkgHist = ofHist.Clone("bkgHist")
	if dyHist is not None:
		bkgHist.Add(dyHist)
		
	
	sfHist.SetMarkerStyle(20)
	sfHist.SetLineColor(ROOT.kBlack)
	bkgHist.SetLineColor(ROOT.kBlue+3)
	bkgHist.SetLineWidth(2)
	
	dyHist.SetLineColor(ROOT.kGreen+2)
	dyHist.SetFillColor(ROOT.kGreen+2)
	#~ dyHist.SetFillStyle(3002)
	
	### get the histograms for the different on-Z contributions, assume the same shape
	dyOnlyHist = dyHist.Clone("dyOnlyHist")
	dyOnlyHist.Scale(getattr(getattr(OnlyZPredictions,bSelection).SF,region).val / getattr(getattr(zPredictions,bSelection).SF,region).val)
	
	rareBGHist = dyHist.Clone("rareBGHist")
	rareBGHist.Scale(getattr(getattr(OtherPredictions,bSelection).SF,region).val / getattr(getattr(zPredictions,bSelection).SF,region).val)
	
	rareBGHist.SetLineColor(ROOT.kViolet+2)
	rareBGHist.SetFillColor(ROOT.kViolet+2)
	
	from ROOT import THStack
	
	### stack the 2 on-Z histograms
	stack = THStack()
	stack.Add(rareBGHist)	
	stack.Add(dyOnlyHist)
	
	### dummy histogram for the legend
	bkgHistForLegend = bkgHist.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)	
	
	
	### latex styles and fonts for labels	
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.055)
	latex.SetLineWidth(2)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.93, 0.942, "%s fb^{-1} (13 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.86,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.80	
	else:
		yLabelPos = 0.83	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

	rSFOFErr = getattr(rSFOF,region).err
	
	### Get the error histograms both for the main plot and the ratio
	errGraph, histUp, histDown = getErrHist(plot,bSelection,region,ofHist,dyHist,rSFOFErr)
	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3001)
	
	### Use data trigger efficiencies since there is no trigger emulation on FastSim signal
	EETriggerEff = getattr(triggerEffs,region).effEE.val
	EMuTriggerEff = getattr(triggerEffs,region).effEM.val
	MuMuTriggerEff = getattr(triggerEffs,region).effMM.val
	RSFOF = getattr(rSFOF,region).val
	

	### Add 3 predefined signal MC points with an edge at 75 GeV, similar to the edge observed at 8 TeV
	if lowMassEdge:
		
		### Get the histogram for the normalization
		denominatorFile = TFile("../SignalScan/T6bbllsleptonDenominatorHisto.root")
		denominatorHisto = TH2F(denominatorFile.Get("massScan"))
		
		### Take scale factors into account
		cutsWithoutSignalScaleFactors = plot.cuts
		plot.cuts = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*leptonFastSimScaleFactor1*leptonFastSimScaleFactor2*bTagWeight*(%s)"%plot.cuts

		### Get the first mass point
		EEHistSignal450, MMHistSignal450, EMHistSignal450 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_450_mneutralino_175",verbose=verbose)
		
		### normalize it
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(450),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_450").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal450.Scale(EETriggerEff * scalingLumi)
		MMHistSignal450.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal450.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		edgeHist450 = EEHistSignal450.Clone()
		edgeHist450.Add(MMHistSignal450.Clone())
		edgeHist450.Add(EMHistSignal450.Clone(),-1)
		
		### take into account that the OF subtraction might yield negative values	
		for i in range(0,edgeHist450.GetNbinsX()):
			if edgeHist450.GetBinContent(i) < 0:
				edgeHist450.SetBinContent(i,0.)
		
		### stack on bkg if chosen and set line style and color
		if stackSignal:		
			edgeHist450.Add(bkgHist.Clone())
		edgeHist450.SetLineColor(ROOT.kRed)
		edgeHist450.SetLineWidth(2)
		
		### second mass point
		EEHistSignal550, MMHistSignal550, EMHistSignal550 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_550_mneutralino_175",verbose=verbose)
		
		### normalization
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(550),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_550").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal550.Scale(EETriggerEff * scalingLumi)
		MMHistSignal550.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal550.Scale(EMuTriggerEff * scalingLumi * RSFOF)

		edgeHist550 = EEHistSignal550.Clone()
		edgeHist550.Add(MMHistSignal550.Clone())
		edgeHist550.Add(EMHistSignal550.Clone(),-1)
			
		for i in range(0,edgeHist550.GetNbinsX()):
			if edgeHist550.GetBinContent(i) < 0:
				edgeHist550.SetBinContent(i,0.)
		
		### stack on bkg if chosen and set line style and color
		if stackSignal:		
			edgeHist550.Add(bkgHist.Clone())
		edgeHist550.SetLineColor(ROOT.kRed)
		edgeHist550.SetLineWidth(2)
		edgeHist550.SetLineStyle(ROOT.kDashed)
		
		### third mass point
		EEHistSignal650, MMHistSignal650, EMHistSignal650 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_650_mneutralino_175",verbose=verbose)
		
		### normalization
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(650),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_650").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal650.Scale(EETriggerEff * scalingLumi)
		MMHistSignal650.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal650.Scale(EMuTriggerEff * scalingLumi * RSFOF)

		edgeHist650 = EEHistSignal650.Clone()
		edgeHist650.Add(MMHistSignal650.Clone())
		edgeHist650.Add(EMHistSignal650.Clone(),-1)
			
		for i in range(0,edgeHist650.GetNbinsX()):
			if edgeHist650.GetBinContent(i) < 0:
				edgeHist650.SetBinContent(i,0.)
				
		if stackSignal:
			edgeHist650.Add(bkgHist.Clone())
		edgeHist650.SetLineColor(ROOT.kRed)
		edgeHist650.SetLineWidth(2)
		edgeHist650.SetLineStyle(ROOT.kDotted)
		
		plot.cuts = cutsWithoutSignalScaleFactors
	
	### Add 3 points with mass edges at different positions		
	if differentEdgePositions:
		
		### Get the histogram for the normalization		
		denominatorFile = TFile("../SignalScan/T6bbllsleptonDenominatorHisto.root")
		denominatorHisto = TH2F(denominatorFile.Get("massScan"))
		
		### Take scale factors into account
		cutsWithoutSignalScaleFactors = plot.cuts
		plot.cuts = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*leptonFastSimScaleFactor1*leptonFastSimScaleFactor2*bTagWeight*(%s)"%plot.cuts

		### first mass point with an egde below the Z peak
		EEHistSignal75, MMHistSignal75, EMHistSignal75 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_175",verbose=verbose)
		
		### normalization
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal75.Scale(EETriggerEff * scalingLumi)
		MMHistSignal75.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal75.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		edgeHist75 = EEHistSignal75.Clone()
		edgeHist75.Add(MMHistSignal75.Clone())
		edgeHist75.Add(EMHistSignal75.Clone(),-1)
		
		### take into account that the OF subtraction might yield negative values	
		for i in range(0,edgeHist75.GetNbinsX()):
			if edgeHist75.GetBinContent(i) < 0:
				edgeHist75.SetBinContent(i,0.)
		
		### stack on bkg if chosen and set line style and color		
		if stackSignal:
			edgeHist75.Add(bkgHist.Clone())
		edgeHist75.SetLineColor(ROOT.kRed)
		edgeHist75.SetLineWidth(2)
		
		### second mass point with an egde just above the Z peak
		EEHistSignal125, MMHistSignal125, EMHistSignal125 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_225",verbose=verbose)
		
		### normalization
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(225))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal125.Scale(EETriggerEff * scalingLumi)
		MMHistSignal125.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal125.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		edgeHist125 = EEHistSignal125.Clone()
		edgeHist125.Add(MMHistSignal125.Clone())
		edgeHist125.Add(EMHistSignal125.Clone(),-1)
			
		for i in range(0,edgeHist125.GetNbinsX()):
			if edgeHist125.GetBinContent(i) < 0:
				edgeHist125.SetBinContent(i,0.)
				
		if stackSignal:
			edgeHist125.Add(bkgHist.Clone())
		edgeHist125.SetLineColor(ROOT.kRed)
		edgeHist125.SetLineWidth(2)
		edgeHist125.SetLineStyle(ROOT.kDashed)
		
		### Third mass point with a higher edge position
		EEHistSignal200, MMHistSignal200, EMHistSignal200 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_300",verbose=verbose)
		
		### normalization
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(300))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal200.Scale(EETriggerEff * scalingLumi)
		MMHistSignal200.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal200.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		edgeHist200 = EEHistSignal200.Clone()
		edgeHist200.Add(MMHistSignal200.Clone())
		edgeHist200.Add(EMHistSignal200.Clone(),-1)
			
		for i in range(0,edgeHist200.GetNbinsX()):
			if edgeHist200.GetBinContent(i) < 0:
				edgeHist200.SetBinContent(i,0.)
				
		if stackSignal:
			edgeHist200.Add(bkgHist.Clone())
		edgeHist200.SetLineColor(ROOT.kRed)
		edgeHist200.SetLineWidth(2)
		edgeHist200.SetLineStyle(ROOT.kDotted)
		
		plot.cuts = cutsWithoutSignalScaleFactors
				


	### get lines to mark the different mass regions
	lines = getLines(0, sfHist.GetBinContent(sfHist.GetMaximumBin())+10,xPos=[mllBins.lowMass.high,mllBins.onZ.low,mllBins.onZ.high, mllBins.highMass.low ])
	for line in lines:
		line.Draw()
		
	### Make the legend. Increase the size if signal is added
	if lowMassEdge:
		leg = TLegend(0.45, 0.4, 0.92, 0.91,"","brNDC")
	elif differentEdgePositions:
		leg = TLegend(0.55, 0.4, 0.95, 0.92,"","brNDC")
	else:
		leg = TLegend(0.55, 0.5, 0.95, 0.92,"","brNDC")
		
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if region == "inclusive":
		leg.AddEntry(legendHistDing,"Inclusive signal region","h")
	elif region == "central":
		leg.AddEntry(legendHistDing,"Central signal region","h")
	elif region == "forward":
		leg.AddEntry(legendHistDing,"Forward signal region","h")
	leg.AddEntry(sfHist,"Data","pe1")
	leg.AddEntry(bkgHistForLegend, "Flavor symmetric","f")
	leg.AddEntry(dyOnlyHist,"Z+jets", "f")
	leg.AddEntry(rareBGHist,"Other SM", "f")
	leg.AddEntry(errGraph,"Total uncertainty", "f")	
	
	if lowMassEdge:
		leg.AddEntry(legendHistDing,"Slepton signal model", "h")
		leg.AddEntry(edgeHist450,"m_{#tilde{b}} = 450 GeV, m_{#tilde{#chi}_{2}^{0}} = 175 GeV", "l")	
		leg.AddEntry(edgeHist550,"m_{#tilde{b}} = 550 GeV, m_{#tilde{#chi}_{2}^{0}} = 175 GeV", "l")	
		leg.AddEntry(edgeHist650,"m_{#tilde{b}} = 650 GeV, m_{#tilde{#chi}_{2}^{0}} = 175 GeV", "l")	
	
	if differentEdgePositions:
		leg.AddEntry(legendHistDing,"Slepton signal model, m_{#tilde{b}} = 500 GeV", "h")
		leg.AddEntry(edgeHist75,"75 GeV edge position", "l")	
		leg.AddEntry(edgeHist125,"125 GeV edge position", "l")	
		leg.AddEntry(edgeHist200,"200 GeV edge position", "l")	
	
	leg.Draw("same")
	
	### Draw the error band in the plot
	errGraph.Draw("SAME02")
	
	### plot the signal histograms
	if lowMassEdge:
		edgeHist450.Draw("samehist")
		edgeHist550.Draw("samehist")
		edgeHist650.Draw("samehist")
		
	if differentEdgePositions:
		edgeHist75.Draw("samehist")
		edgeHist125.Draw("samehist")
		edgeHist200.Draw("samehist")		
	
	## full background
	bkgHist.Draw("samehist")	
	
	### stack for DY component
	stack.Draw("samehist")
		
	sfHist.Draw("samepe1")
		
	plotPad.RedrawAxis()	

	### plot the ratio including the error band
	ratioPad.cd()
		
	ratioGraphs =  ratios.RatioGraph(sfHist,bkgHist, xMin=plot.firstBin, xMax=plot.lastBin,title="#frac{Data}{Prediction}  ",yMin=0.0,yMax=2,color=ROOT.kBlack,adaptiveBinning=1000)
	ratioGraphs.addErrorByHistograms( "rSFOF", histUp, histDown,color= myColors["MyBlue"],fillStyle=3001)			

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	
	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	ratioPad.RedrawAxis()
	
	### modify the plot name if signal is used
	nameModifier = ""

	if lowMassEdge:
		nameModifier += "_lowMassEdge"	
	if differentEdgePositions:
		nameModifier += "_differentEdgePositions"
	
	if stackSignal:
		nameModifier += "_stackedSignal"	
	
	hCanvas.Print("fig/mllResult_%s_%s_%s_SF%s.pdf"%(selection.name,runRange.label,bSelection,nameModifier))	
	
	

def makeResultPlot(path,selection,runRange,cmsExtra,lowMassEdge=False,differentEdgePositions=False,stackSignal=False,verbose=True):
	
	for bSelection in ["default","noBTags","geOneBTags"]:
	
		plot = getPlot(plotNames[bSelection])
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut			

		
		### Get the shape of the DY background from the DY control region
		
		### First fetch the DY background in the corresponding b-tag region
		plotDY = getPlot(plotNames[bSelection])
		
		if "Forward" in selection.name:
			plotDY.addRegion(getRegion("DrellYanControlForward"))
			region = "forward"
		elif "Central" in selection.name:
			plotDY.addRegion(getRegion("DrellYanControlCentral"))
			region = "central"
		else:		
			plotDY.addRegion(getRegion("DrellYanControl"))
			region = "inclusive"
		plotDY.cleanCuts()
		plotDY.cuts = plotDY.cuts % runRange.runCut		

		### The DY region without a b-tag region is necessary for the normalization
		plotDYScale = getPlot("mllPlotROutIn")
		
		if "Forward" in selection.name:
			plotDYScale.addRegion(getRegion("DrellYanControlForward"))
		elif "Central" in selection.name:
			plotDYScale.addRegion(getRegion("DrellYanControlCentral"))
		else:		
			plotDYScale.addRegion(getRegion("DrellYanControl"))
		plotDYScale.cleanCuts()
		plotDYScale.cuts = plotDYScale.cuts % runRange.runCut		
		
		### histograms in the signal region
		histEE, histMM, histEM = getHistograms(path,plot,runRange,verbose=verbose)
		histSF = histEE.Clone("histSF")
		histSF.Add(histMM.Clone())

		### histograms in the DY region and the corresponding btag selection 
		histEEDY, histMMDY, histEMDY = getHistograms(path,plotDY,runRange,verbose=verbose)
		histSFDY = histEEDY.Clone("histSFDY")
		histSFDY.Add(histMMDY.Clone())	

		### histograms in the DY region 
		histEEDYScale, histMMDYScale, histEMDYScale = getHistograms(path,plotDY,runRange,verbose=verbose)
		histSFDYScale = histEEDYScale.Clone("histSFDYScale")
		histSFDYScale.Add(histMMDYScale.Clone())	
		
		
		### Scale OF contribution by RSFOF 
		histOFSF = histEM.Clone("histOFSF")
		histOFSF.Scale(getattr(rSFOF,region).val)

		### Scale the DY histogramm in the b-tag region by the Z-prediction/(Z mass window in the histogramm for the normalization) 
		if region == "inclusive":
			histSFDY.Scale((getattr(zPredictions,bSelection).SF.central.val + getattr(zPredictions,bSelection).SF.forward.val) / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
		else:
			histSFDY.Scale(getattr(getattr(zPredictions,bSelection).SF,region).val / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
		
		### make the actual plot
		makePlot(histSF,histOFSF,selection,plot,runRange,region,cmsExtra,bSelection,path,histSFDY,lowMassEdge=lowMassEdge,differentEdgePositions=differentEdgePositions,stackSignal=stackSignal,verbose=verbose)
		



def main():
	
	

	parser = argparse.ArgumentParser(description='Result plots for the counting experiment.')
	
	parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False,
						  help="Switch verbose mode off. Do not show cut values and samples on the console whenever a histogram is created")								  			  	
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="add MC.")								  			  	
	parser.add_argument("-c", "--control", action="store_true", dest="control", default=False,
						  help="use control region.")								  			  	
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")		
	parser.add_argument("-l", "--lowMassEdge", action="store_true", dest="lowMassEdge", default=False,
						  help="add 13 TeV MC signals")	
	parser.add_argument("-d", "--differentEdgePositions", action="store_true", dest="differentEdgePositions", default=False,
						  help="add 13 TeV MC signals at different edge positions")	
	parser.add_argument("-s", "--stackSignal", dest="stackSignal", action="store_true", default=False,
						  help="stack the signal to the background if signal is plotted.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
						  					
	args = parser.parse_args()
	
	if args.quiet:
		verbose = False
	else:
		verbose = True

	if len(args.plots) == 0:
		args.plots = plotLists.default
	
	### At the moment, only 3 signals can be plotted at once (either 3 at low mass
	### or 3 at different positions). Otherwise the plots get too messy	
	if args.differentEdgePositions and args.lowMassEdge:
		print "Can not plot low mass edges and different edge positions into one plot."
		print "Plot and legend get too busy."
		print "Please choose one of them or adapt the tool."
		sys.exit()


	if not args.differentEdgePositions and not args.lowMassEdge and args.stackSignal:
		print "Stacked signal (-s) only makes sense if signal is added"
		print "Use -l for 3 low mass edges or -d for 3 different edge positions to do so"
		sys.exit()
		
	selections = []
	
	if args.control:
		
		selections.append(regionsToUse.rSFOF.central.name)	
		selections.append(regionsToUse.rSFOF.forward.name)		
	else:	
		selections.append(regionsToUse.signal.central.name)	
		selections.append(regionsToUse.signal.forward.name)	
	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPath	
	
	cmsExtra = "Private Work"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)	
			makeResultPlot(path,selection,runRange,cmsExtra,lowMassEdge=args.lowMassEdge,differentEdgePositions=args.differentEdgePositions,stackSignal=args.stackSignal,verbose=verbose)

main()



