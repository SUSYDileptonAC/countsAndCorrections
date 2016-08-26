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

def dependencies(path,selection,plots,runRange,isMC,nonNormalized,backgrounds,cmsExtra,fit):
	for name in plots:
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


		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,nonNormalized, backgrounds,label)
		histRSFOF = histEE.Clone("histRSFOF")
		histRSFOF.Add(histMM.Clone())
		histRSFOF.Divide(histEM)			
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,300)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		style.SetTitleSize(0.1, "XYZ")
		style.SetTitleYOffset(0.35)
		style.SetTitleXOffset(0.7)
		style.SetPadLeftMargin(0.1)
		style.SetPadTopMargin(0.12)
		style.SetPadBottomMargin(0.17)
		plotPad.UseCurrentStyle()		
		plotPad.Draw()	
		plotPad.cd()	
					
	
		plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,3,"; %s ; %s" %(plot.xaxis,"SF/OF"))
		
		
		from ROOT import TH1F,kWhite
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.65,0.6,1,0.85)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")	


		zeroLine = ROOT.TLine(plot.firstBin, 1., plot.lastBin , 1.)
		zeroLine.SetLineWidth(1)
		zeroLine.SetLineColor(ROOT.kBlue)
		zeroLine.SetLineStyle(2)
		zeroLine.Draw("same")
		histRSFOF.SetLineColor(ROOT.kBlack)
		histRSFOF.SetMarkerColor(ROOT.kBlack)
		histRSFOF.SetMarkerStyle(20)
		histRSFOF.Draw("sameE0")


		legend.Draw("same")

		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(11)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexLumi = ROOT.TLatex()
		latexLumi.SetTextFont(42)
		latexLumi.SetTextAlign(31)
		latexLumi.SetTextSize(0.1)
		latexLumi.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.12)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.1)
		latexCMSExtra.SetNDC(True)	
		latexLumi.DrawLatex(0.95, 0.91, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.12,0.76,"CMS")
		if "Simulation" in cmsExtra and "Private Work" in cmsExtra:
			yLabelPos = 0.635	
		else:
			yLabelPos = 0.68	

		latexCMSExtra.DrawLatex(0.12,yLabelPos,"%s"%(cmsExtra))	


		if fit:
			fit = TF1("dataFit","pol1",0,plot.lastBin)
			fit.SetLineColor(ROOT.kBlack)
			histRSFOF.Fit("dataFit")		
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)	
			latex.SetNDC()	
			latex.DrawLatex(0.2, 0.25, "Fit: %.2f #pm %.2f %.5f #pm %.5f * %s"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1),plot.variable))


		
		if isMC:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	




def getHistograms(path,plot,runRange,isMC,nonNormalized,backgrounds,region=""):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	
	
	if isMC:
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			if nonNormalized:
				processes.append(Process(getattr(Backgrounds,background),eventCounts,normalized=False))
			else:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
	

	

def centralValues(path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra):


	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()

	plot.cuts = plot.cuts % runRange.runCut		

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


	histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,nonNormalized,backgrounds,label)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())

	histEESignal, histMMSignal, histEMSignal = getHistograms(path,plotSignal,runRange,isMC,nonNormalized,backgrounds,label)
	histSFSignal = histEESignal.Clone("histSFSignal")
	histSFSignal.Add(histMMSignal.Clone())
	result = {}
	

	lowMassLow = mllBins.lowMass.low
	lowMassHigh = mllBins.lowMass.high
	highMassLow = mllBins.highMass.low
	highMassHigh = mllBins.highMass.high
	
	highMassRSFOFLow = mllBins.highMassRSFOF.low
	highMassRSFOFHigh = mllBins.highMassRSFOF.high
	
	eeLowMassErr = ROOT.Double()
	eeLowMass = histEE.IntegralAndError(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01),eeLowMassErr)
	eeHighMassErr = ROOT.Double()
	eeHighMass = histEE.IntegralAndError(histEE.FindBin(highMassRSFOFLow+0.01),histEE.FindBin(highMassRSFOFHigh-0.01),eeHighMassErr)
	
	ee = eeLowMass + eeHighMass
	eeErr = (eeLowMassErr**2 + eeHighMassErr**2)**0.5
	
	mmLowMassErr = ROOT.Double()
	mmLowMass = histMM.IntegralAndError(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01),mmLowMassErr)
	mmHighMassErr = ROOT.Double()
	mmHighMass = histMM.IntegralAndError(histMM.FindBin(highMassRSFOFLow+0.01),histMM.FindBin(highMassRSFOFHigh-0.01),mmHighMassErr)
	
	mm = mmLowMass + mmHighMass
	mmErr = (mmLowMassErr**2 + mmHighMassErr**2)**0.5
	
	ofLowMassErr = ROOT.Double()
	ofLowMass = histEM.IntegralAndError(histEM.FindBin(lowMassLow+0.01),histEM.FindBin(lowMassHigh-0.01),ofLowMassErr)
	ofHighMassErr = ROOT.Double()
	ofHighMass = histEM.IntegralAndError(histEM.FindBin(highMassRSFOFLow+0.01),histEM.FindBin(highMassRSFOFHigh-0.01),ofHighMassErr)
	
	of = ofLowMass + ofHighMass
	ofErr = (ofLowMassErr**2 + ofHighMassErr**2)**0.5
	
	sf = ee + mm 
	sfLowMass = eeLowMass + mmLowMass 
	sfHighMass = eeHighMass + mmHighMass 
	sfErr = (eeErr**2 + mmErr**2)**0.5
	sfLowMassErr = (eeLowMassErr**2 + mmLowMassErr**2)**0.5
	sfHighMassErr = (eeHighMassErr**2 + mmHighMassErr**2)**0.5
	
	rsfof = float(sf)/float(of)
	rsfofErr = rsfof*(sfErr**2/sf**2+ofErr**2/of**2)**0.5
	rsfofLowMass = float(sfLowMass)/float(ofLowMass)
	rsfofLowMassErr = rsfofLowMass*(sfLowMassErr**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	rsfofHighMass = float(sfHighMass)/float(ofHighMass)
	rsfofHighMassErr = rsfofHighMass*(sfHighMassErr**2/sf**2+ofHighMassErr**2/of**2)**0.5
		
	rEEOF = float(ee)/float(of)
	rEEOFErr = rEEOF * (eeErr**2/ee**2 + ofErr**2/of**2)**0.5
	rEEOFLowMass = float(eeLowMass)/float(ofLowMass)
	rEEOFLowMassErr = rEEOFLowMass * (eeLowMassErr**2/eeLowMass**2 + ofLowMassErr**2/ofLowMass**2)**0.5
	rEEOFHighMass = float(eeHighMass)/float(ofHighMass)
	rEEOFHighMassErr = rEEOFHighMass * (eeHighMassErr**2/eeHighMass**2 + ofHighMassErr**2/ofHighMass**2)**0.5
	
	rMMOF = float(mm)/float(of)
	rMMOFErr = rMMOF * (mmErr**2/mm**2 + ofErr**2/of**2)**0.5
	rMMOFLowMass = float(mmLowMass)/float(ofLowMass)
	rMMOFLowMassErr = rMMOFLowMass * (mmLowMassErr**2/mmLowMass**2 + ofLowMassErr**2/ofLowMass**2)**0.5
	rMMOFHighMass = float(mmHighMass)/float(ofHighMass)
	rMMOFHighMassErr = rMMOFHighMass * (mmHighMassErr**2/mmHighMass**2 + ofHighMassErr**2/ofHighMass**2)**0.5
	
		
	
	result = {}
	result["EE"] = ee
	result["MM"] = mm
	result["SF"] = sf
	result["OF"] = of
	result["EELowMass"] = eeLowMass
	result["MMLowMass"] = mmLowMass
	result["SFLowMass"] = eeLowMass + mmLowMass
	result["OFLowMass"] = ofLowMass
	result["EEHighMass"] = eeHighMass
	result["MMHighMass"] = mmHighMass
	result["SFHighMass"] = eeHighMass + mmHighMass
	result["OFHighMass"] = ofHighMass
		
		
		
	result["rSFOF"] = rsfof
	result["rSFOFErr"] = rsfofErr
	result["rEEOF"] = rEEOF
	result["rEEOFErr"] = rEEOFErr
	result["rMMOF"] = rMMOF
	result["rMMOFErr"] = rMMOFErr
	
	result["rSFOFLowMass"] = sfLowMass / ofLowMass
	result["rSFOFErrLowMass"] = result["rSFOFLowMass"]*(sfLowMassErr**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	result["rEEOFLowMass"] = eeLowMass / ofLowMass
	result["rEEOFErrLowMass"] =  result["rEEOFLowMass"]*((eeLowMassErr**2)**0.5**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	result["rMMOFLowMass"] = mmLowMass / ofLowMass
	result["rMMOFErrLowMass"] =  result["rMMOFLowMass"]*((mmLowMassErr**2)**0.5**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	result["rSFOFHighMass"] = sfHighMass / ofHighMass
	result["rSFOFErrHighMass"] = result["rSFOFHighMass"]*(sfHighMassErr**2/sfHighMass**2+ofHighMassErr**2/ofHighMass**2)**0.5
	result["rEEOFHighMass"] = eeHighMass / ofHighMass
	result["rEEOFErrHighMass"] =  result["rEEOFHighMass"]*((eeHighMassErr**2)**0.5**2/sfHighMass**2+ofHighMassErr**2/ofHighMass**2)**0.5
	result["rMMOFHighMass"] = mmHighMass / ofHighMass
	result["rMMOFErrHighMass"] =  result["rMMOFHighMass"]*((mmHighMassErr**2)**0.5**2/sfHighMass**2+ofHighMassErr**2/ofHighMass**2)**0.5

	if isMC:
		
		eeLowMassErrSignal = ROOT.Double()
		eeLowMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(lowMassLow+0.01),histEESignal.FindBin(lowMassHigh-0.01),eeLowMassErrSignal)
		eeHighMassErrSignal = ROOT.Double()
		eeHighMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(highMassRSFOFLow+0.01),histEESignal.FindBin(highMassRSFOFHigh-0.01),eeHighMassErrSignal)
		
		eeSignal = eeLowMassSignal + eeHighMassSignal
		eeErrSignal = (eeLowMassErrSignal**2 + eeHighMassErrSignal**2)**0.5
		
		mmLowMassErrSignal = ROOT.Double()
		mmLowMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(lowMassLow+0.01),histMMSignal.FindBin(lowMassHigh-0.01),mmLowMassErrSignal)
		mmHighMassErrSignal = ROOT.Double()
		mmHighMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(highMassRSFOFLow+0.01),histMMSignal.FindBin(highMassRSFOFHigh-0.01),mmHighMassErrSignal)
		
		mmSignal = mmLowMassSignal + mmHighMassSignal
		mmErrSignal = (mmLowMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
		
		ofLowMassErrSignal = ROOT.Double()
		ofLowMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(lowMassLow+0.01),histEMSignal.FindBin(lowMassHigh-0.01),ofLowMassErrSignal)
		ofHighMassErrSignal = ROOT.Double()
		ofHighMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(highMassRSFOFLow+0.01),histEMSignal.FindBin(highMassRSFOFHigh-0.01),ofHighMassErrSignal)
		
		ofSignal = ofLowMassSignal + ofHighMassSignal
		ofErrSignal = (ofLowMassErrSignal**2 + ofHighMassErrSignal**2)**0.5
		 
		sfSignal = eeSignal + mmSignal 
		sfLowMassSignal = eeLowMassSignal + mmLowMassSignal
		sfHighMassSignal = eeHighMassSignal + mmHighMassSignal
		sfErrSignal = (eeErrSignal**2 + mmErrSignal**2)**0.5
		sfLowMassErrSignal = (eeLowMassErrSignal**2 + mmLowMassErrSignal**2)**0.5
		sfHighMassErrSignal = (eeHighMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
		
		rsfofSignal = float(sfSignal)/float(ofSignal)	
		rsfofErrSignal = rsfofSignal*(sfErrSignal**2/sfSignal**2+ofErrSignal**2/ofSignal**2)**0.5
		rsfofLowMassSignal = float(sfLowMassSignal)/float(ofLowMassSignal)
		rsfofLowMassErrSignal = rsfofLowMassSignal*(sfLowMassErrSignal**2/sfLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		rsfofHighMassSignal = float(sfHighMassSignal)/float(ofHighMassSignal)
		rsfofHighMassErrSignal = rsfofHighMassSignal*(sfHighMassErrSignal**2/sfHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		
		rEEOFSignal = float(eeSignal)/float(ofSignal)
		rEEOFErrSignal = rEEOFSignal * (eeErrSignal**2/eeSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
		rEEOFLowMassSignal = float(eeLowMassSignal)/float(ofLowMassSignal)
		rEEOFLowMassErrSignal = rEEOFLowMassSignal * (eeLowMassErrSignal**2/eeLowMassSignal**2 + ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		rEEOFHighMassSignal = float(eeHighMassSignal)/float(ofHighMassSignal)
		rEEOFHighMassErrSignal = rEEOFHighMassSignal * (eeHighMassErrSignal**2/eeHighMassSignal**2 + ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		
		rMMOFSignal = float(mmSignal)/float(ofSignal)
		rMMOFErrSignal = rMMOFSignal * (mmErrSignal**2/mmSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
		rMMOFLowMassSignal = float(mmLowMassSignal)/float(ofLowMassSignal)
		rMMOFLowMassErrSignal = rMMOFLowMassSignal * (mmLowMassErrSignal**2/mmLowMassSignal**2 + ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		rMMOFHighMassSignal = float(mmHighMassSignal)/float(ofHighMassSignal)
		rMMOFHighMassErrSignal = rMMOFHighMassSignal * (mmHighMassErrSignal**2/mmHighMassSignal**2 + ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5

		transferFaktor = rsfofSignal/rsfof
		transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
		transferFaktor = rsfofSignal/rsfof
		transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
		transferFaktorEE = rEEOFSignal/rEEOF
		transferFaktorEEErr = transferFaktorEE*((rEEOFErr/rEEOF)**2+(rEEOFErrSignal/rEEOFSignal)**2)**0.5
		transferFaktorMM = rMMOFSignal/rMMOF
		transferFaktorMMErr = transferFaktorMM*((rMMOFErr/rMMOF)**2+(rMMOFErrSignal/rMMOFSignal)**2)**0.5
		
		transferFaktorLowMass = rsfofLowMassSignal/rsfofLowMass
		transferFaktorLowMassErr = transferFaktorLowMass*((rsfofLowMassErr/rsfofLowMass)**2+(rsfofLowMassErrSignal/rsfofLowMassSignal)**2)**0.5
		transferFaktorEELowMass = rEEOFLowMassSignal/rEEOFLowMass
		transferFaktorEELowMassErr = transferFaktorEELowMass*((rEEOFLowMassErr/rEEOFLowMass)**2+(rEEOFLowMassErrSignal/rEEOFLowMassSignal)**2)**0.5
		transferFaktorMMLowMass = rMMOFLowMassSignal/rMMOFLowMass
		transferFaktorMMLowMassErr = transferFaktorMMLowMass*((rMMOFLowMassErr/rMMOFLowMass)**2+(rMMOFLowMassErrSignal/rMMOFLowMassSignal)**2)**0.5
		
		transferFaktorHighMass = rsfofHighMassSignal/rsfofHighMass
		transferFaktorHighMassErr = transferFaktorHighMass*((rsfofHighMassErr/rsfofHighMass)**2+(rsfofHighMassErrSignal/rsfofHighMassSignal)**2)**0.5
		transferFaktorEEHighMass = rEEOFHighMassSignal/rEEOFHighMass
		transferFaktorEEHighMassErr = transferFaktorEEHighMass*((rEEOFHighMassErr/rEEOFHighMass)**2+(rEEOFHighMassErrSignal/rEEOFHighMassSignal)**2)**0.5
		transferFaktorMMHighMass = rMMOFHighMassSignal/rMMOFHighMass
		transferFaktorMMHighMassErr = transferFaktorMMHighMass*((rMMOFHighMassErr/rMMOFHighMass)**2+(rMMOFHighMassErrSignal/rMMOFHighMassSignal)**2)**0.5
		
		result["EESignal"] = eeSignal
		result["MMSignal"] = mmSignal
		result["SFSignal"] = sfSignal
		result["OFSignal"] = ofSignal
		result["EELowMassSignal"] = eeLowMassSignal
		result["MMLowMassSignal"] = mmLowMassSignal
		result["SFLowMassSignal"] = eeLowMassSignal + mmLowMassSignal
		result["OFLowMassSignal"] = ofLowMassSignal
		result["EEHighMassSignal"] = eeHighMassSignal
		result["MMHighMassSignal"] = mmHighMassSignal
		result["SFHighMassSignal"] = eeHighMassSignal + mmHighMassSignal
		result["OFHighMassSignal"] = ofHighMassSignal
		
		
		
		result["rSFOFSignal"] = rsfofSignal
		result["rSFOFErrSignal"] = rsfofErrSignal
		result["rEEOFSignal"] = rEEOFSignal
		result["rEEOFErrSignal"] = rEEOFErrSignal
		result["rMMOFSignal"] = rMMOFSignal
		result["rMMOFErrSignal"] = rMMOFErrSignal
		
		result["rSFOFLowMassSignal"] = sfLowMassSignal / ofLowMassSignal
		result["rSFOFErrLowMassSignal"] = result["rSFOFLowMassSignal"]*(sfLowMassErrSignal**2/sfLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		result["rEEOFLowMassSignal"] = eeLowMassSignal / ofLowMassSignal
		result["rEEOFErrLowMassSignal"] =  result["rEEOFLowMassSignal"]*(eeLowMassErrSignal**2/eeLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		result["rMMOFLowMassSignal"] = mmLowMassSignal / ofLowMassSignal
		result["rMMOFErrLowMassSignal"] =  result["rMMOFLowMassSignal"]*(mmLowMassErrSignal**2/mmLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		result["rSFOFHighMassSignal"] = sfHighMassSignal / ofHighMassSignal
		result["rSFOFErrHighMassSignal"] = result["rSFOFHighMassSignal"]*(sfHighMassErrSignal**2/sfHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		result["rEEOFHighMassSignal"] = eeHighMassSignal / ofHighMassSignal
		result["rEEOFErrHighMassSignal"] =  result["rEEOFHighMassSignal"]*(eeHighMassErrSignal**2/eeHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		result["rMMOFHighMassSignal"] = mmHighMassSignal / ofHighMassSignal
		result["rMMOFErrHighMassSignal"] =  result["rMMOFHighMassSignal"]*(mmHighMassErrSignal**2/mmHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		
		result["transfer"] = transferFaktor
		result["transferErr"] = transferFaktorErr
		result["transferEE"] = transferFaktorEE
		result["transferEEErr"] = transferFaktorEEErr
		result["transferMM"] = transferFaktorMM
		result["transferMMErr"] = transferFaktorMMErr
	
		result["transferLowMass"] = transferFaktorLowMass
		result["transferLowMassErr"] = transferFaktorLowMassErr
		result["transferEELowMass"] = transferFaktorEELowMass
		result["transferEELowMassErr"] = transferFaktorEELowMassErr
		result["transferMMLowMass"] = transferFaktorMMLowMass
		result["transferMMLowMassErr"] = transferFaktorMMLowMassErr
		result["transferHighMass"] = transferFaktorHighMass
		result["transferHighMassErr"] = transferFaktorHighMassErr
		result["transferEEHighMass"] = transferFaktorEEHighMass
		result["transferEEHighMassErr"] = transferFaktorEEHighMassErr
		result["transferMMHighMass"] = transferFaktorMMHighMass
		result["transferMMHighMassErr"] = transferFaktorMMHighMassErr
	
	return result
	
	
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
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")			
	parser.add_argument("-f", "--fit", action="store_true", dest="fit", default= False,
						  help="do dependecy fit")	
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
			

	path = locations.dataSetPath
		
	cmsExtra = "Private Work"
	if args.mc:
		cmsExtra = "#splitline{Private Work}{Simulation}"


	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)

			if args.central:
				
				centralVal = centralValues(path,selection,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra)
				if args.mc:
					outFilePkl = open("shelves/rSFOF_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					outFilePkl = open("shelves/rSFOF_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra,args.fit)		
				
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rSFOF_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves//rSFOF_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())					
main()
