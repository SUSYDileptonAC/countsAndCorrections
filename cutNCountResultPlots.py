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

		
	
def getSignalMCHistograms(path,plot,runRange,sampleName):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")

	histoEE = getDataHist(plot,treesEE,dataname = sampleName)
	histoMM = getDataHist(plot,treesMM,dataname = sampleName)
	histoEM = getDataHist(plot,treesEM,dataname = sampleName)

	return histoEE , histoMM, histoEM
	
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

def getErrHist(plot,combination,bSelection,region,ofHist,dyHist,rSFOFErr):
	
	if combination == "SF":
		localZPred = getattr(zPredictions,bSelection).SF
		localROutIn = rOutIn
	elif combination == "EE":
		localZPred = getattr(zPredictions,bSelection).EE
		localROutIn = rOutInEE
	elif combination == "MM":
		localZPred = getattr(zPredictions,bSelection).MM
		localROutIn = rOutInMM
	
	hist = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histUp = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histDown = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	graph = TGraphAsymmErrors()
	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinContent(i,1)
		hist.SetBinError(i,ofHist.GetBinContent(i)*rSFOFErr)
	if dyHist is not None:
		for i in range(hist.FindBin(mllBins.lowMass.low+0.01),hist.FindBin(mllBins.lowMass.high-0.01)):
			
			if region == "inclusive":
				zErrCentral = (((localZPred.central.err*localROutIn.lowMass.central.val)**2 + (localZPred.central.val*localROutIn.lowMass.central.err)**2)**0.5) / (localZPred.central.val*localROutIn.lowMass.central.val) * dyHist.GetBinContent(i)
				zErrForward = (((localZPred.forward.err*localROutIn.lowMass.forward.val)**2 + (localZPred.forward.val*localROutIn.lowMass.forward.err)**2)**0.5) / (localZPred.forward.val*localROutIn.lowMass.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward
			else:
				zErr = (((getattr(localZPred,region).err*getattr(localROutIn.lowMass,region).val)**2 + (getattr(localZPred,region).val*getattr(localROutIn.lowMass,region).err)**2)**0.5) / ((getattr(localZPred,region).val*getattr(localROutIn.lowMass,region).val)) * dyHist.GetBinContent(i)
							
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 
			
		for i in range(hist.FindBin(mllBins.highMass.low+0.01),hist.FindBin(plot.lastBin-0.01)+1):
			if region == "inclusive":
				zErrCentral = (((localZPred.central.err*localROutIn.highMass.central.val)**2 + (localZPred.central.val*localROutIn.highMass.central.err)**2)**0.5) / (localZPred.central.val*localROutIn.highMass.central.val) * dyHist.GetBinContent(i)
				zErrForward = (((localZPred.forward.err*localROutIn.highMass.forward.val)**2 + (localZPred.forward.val*localROutIn.highMass.forward.err)**2)**0.5) / (localZPred.forward.val*localROutIn.highMass.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward		
			
			else:
				zErr = (((getattr(localZPred,region).err*getattr(localROutIn.highMass,region).val)**2 + (getattr(localZPred,region).val*getattr(localROutIn.highMass,region).err)**2)**0.5) / ((getattr(localZPred,region).val*getattr(localROutIn.highMass,region).val)) * dyHist.GetBinContent(i)
			
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 
			
		for i in range(hist.FindBin(mllBins.onZ.low+0.01),hist.FindBin(mllBins.onZ.high-0.01)):
			if region == "inclusive":
				zErrCentral = (localZPred.central.err / localZPred.central.val) * dyHist.GetBinContent(i)
				zErrForward = (localZPred.forward.err / localZPred.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward


			
			else:
				zErr = (getattr(localZPred,region).err / getattr(localZPred,region).val) * dyHist.GetBinContent(i) 
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 

		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),dyHist.GetBinContent(i) + ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5)			
		for i in range(1,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) - hist.GetBinError(i))
			if dyHist.GetBinContent(i) + ofHist.GetBinContent(i) > 0:			
				hist.SetBinError(i,hist.GetBinError(i) / (dyHist.GetBinContent(i) + ofHist.GetBinContent(i)))
			else:
				hist.SetBinError(i,1.2)
	else:
		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5)	
		for i in range(1,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,ofHist.GetBinContent(i) - hist.GetBinError(i))			
			if ofHist.GetBinContent(i) > 0:
				hist.SetBinError(i,hist.GetBinError(i) / (ofHist.GetBinContent(i)))
			else:
				hist.SetBinError(i,0)
	return graph, histUp, histDown

def getLines(yMin,yMax, xPos = [70.,81., 101]):
	from ROOT import TLine, kGray
	result = []
	for x in xPos:
		result.append(TLine(x, yMin, x,yMax))
		result[-1].SetLineWidth(1)
		result[-1].SetLineColor(kGray+2)
		result[-1].SetLineStyle(2)
	return result

	
def makePlot(sfHist,ofHist,selection,plot,runRange,region,cmsExtra,combination,bSelection,path,dyHist=None,edgeShape=False,edgeShapeMC=False,differentEdgePositions=False):

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
		#~ if edgeShape or edgeShapeMC or differentEdgePositions: 
			#~ yMax = yMax*1.75 
		#~ else:
			#~ yMax = yMax*2.
						
	else: 
		yMax = plot.yMax
					
	
	plotPad.DrawFrame(plot.firstBin,0,plot.lastBin, yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	#set overflow bin
	print sfHist.GetBinContent(sfHist.GetNbinsX()), sfHist.GetBinContent(sfHist.GetNbinsX()+1)
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
	
	dyOnlyHist = dyHist.Clone("dyOnlyHist")
	dyOnlyHist.Scale(getattr(getattr(OnlyZPredictions,bSelection).SF,region).val / getattr(getattr(zPredictions,bSelection).SF,region).val)
	
	rareBGHist = dyHist.Clone("rareBGHist")
	rareBGHist.Scale(getattr(getattr(OtherPredictions,bSelection).SF,region).val / getattr(getattr(zPredictions,bSelection).SF,region).val)
	
	rareBGHist.SetLineColor(ROOT.kViolet+2)
	rareBGHist.SetFillColor(ROOT.kViolet+2)
	
	from ROOT import THStack
	
	stack = THStack()
	stack.Add(rareBGHist)	
	stack.Add(dyOnlyHist)
	
	bkgHistForLegend = bkgHist.Clone("bkgHistForLegend")
	bkgHistForLegend.SetLineColor(ROOT.kBlue+3)
	bkgHistForLegend.SetFillColor(ROOT.kWhite)
	bkgHistForLegend.SetLineWidth(2)
	

	
	
	
		
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
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	





	
	if combination == "SF":
		rSFOFErr = getattr(rSFOF,region).err
	elif combination == "EE":
		rSFOFErr = getattr(rEEOF,region).err
	elif combination == "MM":
		rSFOFErr = getattr(rMMOF,region).err
	
	errGraph, histUp, histDown = getErrHist(plot,combination,bSelection,region,ofHist,dyHist,rSFOFErr)
	errGraph.SetFillColor(myColors["MyBlueOverview"])
	errGraph.SetFillStyle(3001)
	#~ errGraph.SetLineColor(myColors["MyDarkBlue"])
	#~ errGraph.SetMarkerColor(myColors["MyDarkBlue"])
	

	if edgeShape:
		
		edgeFile = ROOT.TFile("edgeShape.root","READ")
		edgeHist = ROOT.TH1F()
		edgeHist = edgeFile.Get("edgeHist300__inv")
		edgeHist.Scale(1./edgeHist.Integral())
		
		edgeHist500 = edgeFile.Get("edgeHist500__inv")
		edgeHist500.Scale(1./edgeHist500.Integral())
		
		edgeHist700 = edgeFile.Get("edgeHist700__inv")
		edgeHist700.Scale(1./edgeHist700.Integral())

		
		edgeHist.Scale(61)
		edgeHist.Add(bkgHist.Clone())
		edgeHist.SetLineColor(ROOT.kRed)		
		edgeHist.SetLineWidth(2)	
		
		
		edgeHist500.Scale(86)
		edgeHist500.Add(bkgHist.Clone())
		edgeHist500.SetLineColor(ROOT.kRed)		
		edgeHist500.SetLineWidth(2)		
		edgeHist500.SetLineStyle(ROOT.kDashed)
		
		edgeHist700.Scale(117)
		edgeHist700.Add(bkgHist.Clone())
		edgeHist700.SetLineColor(ROOT.kRed)		
		edgeHist700.SetLineStyle(ROOT.kDotted)		
		edgeHist700.SetLineWidth(2)	

	if edgeShapeMC:
		
		denominatorFile = TFile("../SignalScan/T6bbllsleptonDenominatorHisto.root")
		denominatorHisto = TH2F(denominatorFile.Get("massScan"))
		
		cutsWithoutSignalScaleFactors = plot.cuts
		plot.cuts = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*leptonFastSimScaleFactor1*leptonFastSimScaleFactor2*(%s)"%plot.cuts
		
		if "Central" in selection.name:
			EETriggerEff = 0.945
			EMuTriggerEff = 0.937
			MuMuTriggerEff = 0.929
			RSFOF = 1.032
		elif "Forward" in selection.name:
			EETriggerEff = 0.943
			EMuTriggerEff = 0.938
			MuMuTriggerEff = 0.916
			RSFOF = 1.092
		else:
			EETriggerEff = 0.949
			EMuTriggerEff = 0.921811
			MuMuTriggerEff = 0.929178
			RSFOF = 1.05

		EEHistSignal450, MMHistSignal450, EMHistSignal450 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_450_mneutralino_175")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(450),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_450").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal450.Scale(EETriggerEff * scalingLumi)
		MMHistSignal450.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal450.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist450 = EEHistSignal450.Clone()
			edgeHist450.Add(MMHistSignal450.Clone())
			edgeHist450.Add(EMHistSignal450.Clone(),-1)
		if combination == "EE":
			edgeHist450 = EEHistSignal450.Clone()
			edgeHist450.Add(EMHistSignal450.Clone(),-0.5)
		if combination == "MM":
			edgeHist450 = MMHistSignal450.Clone()
			edgeHist450.Add(EMHistSignal450.Clone(),-0.5)
			
		for i in range(0,edgeHist450.GetNbinsX()):
			if edgeHist450.GetBinContent(i) < 0:
				edgeHist450.SetBinContent(i,0.)
				
		edgeHist450.Add(bkgHist.Clone())
		edgeHist450.SetLineColor(ROOT.kRed)
		edgeHist450.SetLineWidth(2)
		
		EEHistSignal550, MMHistSignal550, EMHistSignal550 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_550_mneutralino_175")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(550),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_550").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal550.Scale(EETriggerEff * scalingLumi)
		MMHistSignal550.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal550.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist550 = EEHistSignal550.Clone()
			edgeHist550.Add(MMHistSignal550.Clone())
			edgeHist550.Add(EMHistSignal550.Clone(),-1)
		if combination == "EE":
			edgeHist550 = EEHistSignal550.Clone()
			edgeHist550.Add(EMHistSignal550.Clone(),-0.5)
		if combination == "MM":
			edgeHist550 = MMHistSignal550.Clone()
			edgeHist550.Add(EMHistSignal550.Clone(),-0.5)
			
		for i in range(0,edgeHist550.GetNbinsX()):
			if edgeHist550.GetBinContent(i) < 0:
				edgeHist550.SetBinContent(i,0.)
				
		edgeHist550.Add(bkgHist.Clone())
		edgeHist550.SetLineColor(ROOT.kRed)
		edgeHist550.SetLineWidth(2)
		edgeHist550.SetLineStyle(ROOT.kDashed)
		
		EEHistSignal650, MMHistSignal650, EMHistSignal650 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_650_mneutralino_175")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(650),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_650").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal650.Scale(EETriggerEff * scalingLumi)
		MMHistSignal650.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal650.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist650 = EEHistSignal650.Clone()
			edgeHist650.Add(MMHistSignal650.Clone())
			edgeHist650.Add(EMHistSignal650.Clone(),-1)
		if combination == "EE":
			edgeHist650 = EEHistSignal650.Clone()
			edgeHist650.Add(EMHistSignal650.Clone(),-0.5)
		if combination == "MM":
			edgeHist650 = MMHistSignal650.Clone()
			edgeHist650.Add(EMHistSignal650.Clone(),-0.5)
			
		for i in range(0,edgeHist650.GetNbinsX()):
			if edgeHist650.GetBinContent(i) < 0:
				edgeHist650.SetBinContent(i,0.)
				
		edgeHist650.Add(bkgHist.Clone())
		edgeHist650.SetLineColor(ROOT.kRed)
		edgeHist650.SetLineWidth(2)
		edgeHist650.SetLineStyle(ROOT.kDotted)
		
		plot.cuts = cutsWithoutSignalScaleFactors
			
	if differentEdgePositions:
				
		denominatorFile = TFile("T6bbllsleptonDenominatorHisto.root")
		denominatorHisto = TH2F(denominatorFile.Get("massScan"))
		
		cutsWithoutSignalScaleFactors = plot.cuts
		plot.cuts = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*leptonFastSimScaleFactor1*leptonFastSimScaleFactor2*(%s)"%plot.cuts
		
		if "Central" in selection.name:
			EETriggerEff = triggerEffs.central.effEE.val
			EMuTriggerEff = triggerEffs.central.effEM.val
			MuMuTriggerEff = triggerEffs.central.effMM.val
			RSFOF = rSFOF.central.val
		elif "Forward" in selection.name:
			EETriggerEff = triggerEffs.forward.effEE.val
			EMuTriggerEff = triggerEffs.forward.effEM.val
			MuMuTriggerEff = triggerEffs.forward.effMM.val
			RSFOF = rSFOF.forward.val
		else:
			EETriggerEff = triggerEffs.inclusive.effEE.val
			EMuTriggerEff = triggerEffs.inclusive.effEM.val
			MuMuTriggerEff = triggerEffs.inclusive.effMM.val
			RSFOF = rSFOF.inclusive.val

		EEHistSignal75, MMHistSignal75, EMHistSignal75 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_175")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(175))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal75.Scale(EETriggerEff * scalingLumi)
		MMHistSignal75.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal75.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist75 = EEHistSignal75.Clone()
			edgeHist75.Add(MMHistSignal75.Clone())
			edgeHist75.Add(EMHistSignal75.Clone(),-1)
		if combination == "EE":
			edgeHist75 = EEHistSignal75.Clone()
			edgeHist75.Add(EMHistSignal75.Clone(),-0.5)
		if combination == "MM":
			edgeHist75 = MMHistSignal75.Clone()
			edgeHist75.Add(EMHistSignal75.Clone(),-0.5)
			
		for i in range(0,edgeHist75.GetNbinsX()):
			if edgeHist75.GetBinContent(i) < 0:
				edgeHist75.SetBinContent(i,0.)
				
		edgeHist75.Add(bkgHist.Clone())
		edgeHist75.SetLineColor(ROOT.kRed)
		edgeHist75.SetLineWidth(2)
		
		EEHistSignal125, MMHistSignal125, EMHistSignal125 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_225")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(225))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal125.Scale(EETriggerEff * scalingLumi)
		MMHistSignal125.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal125.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist125 = EEHistSignal125.Clone()
			edgeHist125.Add(MMHistSignal125.Clone())
			edgeHist125.Add(EMHistSignal125.Clone(),-1)
		if combination == "EE":
			edgeHist125 = EEHistSignal125.Clone()
			edgeHist125.Add(EMHistSignal125.Clone(),-0.5)
		if combination == "MM":
			edgeHist125 = MMHistSignal125.Clone()
			edgeHist125.Add(EMHistSignal125.Clone(),-0.5)
			
		for i in range(0,edgeHist125.GetNbinsX()):
			if edgeHist125.GetBinContent(i) < 0:
				edgeHist125.SetBinContent(i,0.)
				
		edgeHist125.Add(bkgHist.Clone())
		edgeHist125.SetLineColor(ROOT.kRed)
		edgeHist125.SetLineWidth(2)
		edgeHist125.SetLineStyle(ROOT.kDashed)
		
		EEHistSignal200, MMHistSignal200, EMHistSignal200 = getSignalMCHistograms(path,plot,runRange,"T6bbllslepton_msbottom_500_mneutralino_300")
		
		denominator = denominatorHisto.GetBinContent(denominatorHisto.GetXaxis().FindBin(500),denominatorHisto.GetYaxis().FindBin(300))		
		xsection = getattr(sbottom_masses, "m_b_500").cross_section13TeV			
		scalingLumi = runRange.lumi*xsection/denominator
		
		EEHistSignal200.Scale(EETriggerEff * scalingLumi)
		MMHistSignal200.Scale(MuMuTriggerEff * scalingLumi)
		EMHistSignal200.Scale(EMuTriggerEff * scalingLumi * RSFOF)
		
		if combination == "SF":
			edgeHist200 = EEHistSignal200.Clone()
			edgeHist200.Add(MMHistSignal200.Clone())
			edgeHist200.Add(EMHistSignal200.Clone(),-1)
		if combination == "EE":
			edgeHist200 = EEHistSignal200.Clone()
			edgeHist200.Add(EMHistSignal200.Clone(),-0.5)
		if combination == "MM":
			edgeHist200 = MMHistSignal200.Clone()
			edgeHist200.Add(EMHistSignal200.Clone(),-0.5)
			
		for i in range(0,edgeHist200.GetNbinsX()):
			if edgeHist200.GetBinContent(i) < 0:
				edgeHist200.SetBinContent(i,0.)
				
		edgeHist200.Add(bkgHist.Clone())
		edgeHist200.SetLineColor(ROOT.kRed)
		edgeHist200.SetLineWidth(2)
		edgeHist200.SetLineStyle(ROOT.kDotted)
		
		plot.cuts = cutsWithoutSignalScaleFactors
				


	lines = getLines(0, sfHist.GetBinContent(sfHist.GetMaximumBin())+10,xPos=[mllBins.lowMass.high,mllBins.onZ.low,mllBins.onZ.high, mllBins.highMass.low ])
	for line in lines:
		line.Draw()
	if edgeShape or edgeShapeMC:
		leg = TLegend(0.45, 0.4, 0.92, 0.91,"","brNDC")
	elif differentEdgePositions:
		leg = TLegend(0.55, 0.4, 0.95, 0.92,"","brNDC")
	else:
		leg = TLegend(0.55, 0.4, 0.95, 0.92,"","brNDC")
		
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
	#~ leg.AddEntry(bkgHist, "Total background","l")
	leg.AddEntry(bkgHistForLegend, "Flavor symmetric","f")
	#~ leg.AddEntry(dyHist,"Drell-Yan", "f")
	leg.AddEntry(dyOnlyHist,"Z+jets", "f")
	leg.AddEntry(rareBGHist,"Other SM", "f")
	leg.AddEntry(errGraph,"Total uncertainty", "f")	
	
	if edgeShape:
		leg.AddEntry(legendHistDing,"Scaled 8 TeV signal fit:", "h")	
		leg.AddEntry(edgeHist,"m_{#tilde{b}} = 300 GeV hypothesis", "l")	
		leg.AddEntry(edgeHist500,"m_{#tilde{b}} = 500 GeV hypothesis", "l")	
		leg.AddEntry(edgeHist700,"m_{#tilde{b}} = 700 GeV hypothesis", "l")	
	
	if edgeShapeMC:
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
	
	errGraph.Draw("SAME02")
	
	if edgeShape:		
		edgeHist.Draw("samehist")	
		edgeHist500.Draw("samehist")	
		edgeHist700.Draw("samehist")
		
	if edgeShapeMC:
		edgeHist450.Draw("samehist")
		edgeHist550.Draw("samehist")
		edgeHist650.Draw("samehist")
		
	if differentEdgePositions:
		edgeHist75.Draw("samehist")
		edgeHist125.Draw("samehist")
		edgeHist200.Draw("samehist")
	
	
	bkgHist.Draw("samehist")	
	
	
	stack.Draw("samehist")	
	sfHist.Draw("samepe1")






		
	plotPad.RedrawAxis()	


	ratioPad.cd()
		
	ratioGraphs =  ratios.RatioGraph(sfHist,bkgHist, xMin=plot.firstBin, xMax=plot.lastBin,title="#frac{Data}{Prediction}  ",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=1000)
	ratioGraphs.addErrorByHistograms( "rSFOF", histUp, histDown,color= myColors["MyBlue"],fillStyle=3001)			

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	
	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	ratioPad.RedrawAxis()

	if edgeShape:
		hCanvas.Print("fig/mllResult_%s_%s_%s_%s_edgeShape.pdf"%(selection.name,runRange.label,bSelection,combination))	
	elif edgeShapeMC:
		hCanvas.Print("fig/mllResult_%s_%s_%s_%s_edgeShapeMC.pdf"%(selection.name,runRange.label,bSelection,combination))	
	elif differentEdgePositions:
		hCanvas.Print("fig/mllResult_%s_%s_%s_%s_edgeShapeMC_differentEdgePositions.pdf"%(selection.name,runRange.label,bSelection,combination))	
	else:
		hCanvas.Print("fig/mllResult_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,bSelection,combination))	
	
	
		


def makeResultPlot(path,selection,runRange,cmsExtra,edgeShape=False,edgeShapeMC=False,differentEdgePositions=False):
	
	for bSelection in ["default","noBTags","geOneBTags"]:
	
		plot = getPlot(plotNames[bSelection])
		plot.addRegion(selection)
		plot.cleanCuts()
		plot.cuts = plot.cuts % runRange.runCut			

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

		plotDYScale = getPlot("mllPlotROutIn")
		
		if "Forward" in selection.name:
			plotDYScale.addRegion(getRegion("DrellYanControlForward"))
		elif "Central" in selection.name:
			plotDYScale.addRegion(getRegion("DrellYanControlCentral"))
		else:		
			plotDYScale.addRegion(getRegion("DrellYanControl"))
		plotDYScale.cleanCuts()
		plotDYScale.cuts = plotDYScale.cuts % runRange.runCut		
		
		
		histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[])
		histSF = histEE.Clone("histSF")
		histSF.Add(histMM.Clone())

		histEEDY, histMMDY, histEMDY = getHistograms(path,plotDY,runRange,False,[])
		histSFDY = histEEDY.Clone("histSFDY")
		histSFDY.Add(histMMDY.Clone())	

		histEEDYScale, histMMDYScale, histEMDYScale = getHistograms(path,plotDY,runRange,False,[])
		histSFDYScale = histEEDYScale.Clone("histSFDYScale")
		histSFDYScale.Add(histMMDYScale.Clone())	
		
		
		histOFSF = histEM.Clone("histOFSF")
		histOFEE = histEM.Clone("histOFEE")
		histOFMM = histEM.Clone("histOFMM")
		histOFSF.Scale(getattr(rSFOF,region).val)
		histOFEE.Scale(getattr(rEEOF,region).val)
		histOFMM.Scale(getattr(rMMOF,region).val)

		if region == "inclusive":
			histSFDY.Scale((getattr(zPredictions,bSelection).SF.central.val + getattr(zPredictions,bSelection).SF.forward.val) / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
			histEEDY.Scale((getattr(zPredictions,bSelection).EE.central.val + getattr(zPredictions,bSelection).EE.forward.val) / histEEDYScale.Integral(histEEDYScale.FindBin(81),histEEDYScale.FindBin(101)))
			histMMDY.Scale((getattr(zPredictions,bSelection).MM.central.val + getattr(zPredictions,bSelection).MM.forward.val) / histMMDYScale.Integral(histMMDYScale.FindBin(81),histMMDYScale.FindBin(101)))
		else:
			histSFDY.Scale(getattr(getattr(zPredictions,bSelection).SF,region).val / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
			histEEDY.Scale(getattr(getattr(zPredictions,bSelection).EE,region).val / histEEDYScale.Integral(histEEDYScale.FindBin(81),histEEDYScale.FindBin(101)))
			histMMDY.Scale(getattr(getattr(zPredictions,bSelection).MM,region).val / histMMDYScale.Integral(histMMDYScale.FindBin(81),histMMDYScale.FindBin(101)))
		
		makePlot(histSF,histOFSF,selection,plot,runRange,region,cmsExtra,"SF",bSelection,path,histSFDY,edgeShape=edgeShape,edgeShapeMC=edgeShapeMC,differentEdgePositions=differentEdgePositions)
		makePlot(histEE,histOFEE,selection,plot,runRange,region,cmsExtra,"EE",bSelection,path,histEEDY,edgeShape=edgeShape,edgeShapeMC=edgeShapeMC,differentEdgePositions=differentEdgePositions)
		makePlot(histMM,histOFMM,selection,plot,runRange,region,cmsExtra,"MM",bSelection,path,histMMDY,edgeShape=edgeShape,edgeShapeMC=edgeShapeMC,differentEdgePositions=differentEdgePositions)




def main():
	
	

	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")								  			  	
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="add MC.")								  			  	
	parser.add_argument("-c", "--control", action="store_true", dest="control", default=False,
						  help="use control region.")								  			  	
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-e", "--edgeShape", action="store_true", dest="edgeShape", default=False,
						  help="add 8 TeV excess shape.")	
	parser.add_argument("-s", "--edgeShapeMC", action="store_true", dest="edgeShapeMC", default=False,
						  help="add 13 TeV MC signals")	
	parser.add_argument("-D", "--differentEdgePositions", action="store_true", dest="differentEdgePositions", default=False,
						  help="add 13 TeV MC signals at different edge positions")	
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
						  					
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.rSFOF
	if len(args.plots) == 0:
		args.plots = plotLists.default


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
	
	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
	else:
		#~ cmsExtra = "Preliminary"
		cmsExtra = ""

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)	
			makeResultPlot(path,selection,runRange,cmsExtra,edgeShape=args.edgeShape,edgeShapeMC=args.edgeShapeMC,differentEdgePositions=args.differentEdgePositions)

main()



