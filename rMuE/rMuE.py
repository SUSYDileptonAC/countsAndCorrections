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
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import triggerEffs, rSFOF
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics
from locations import locations


def rMuEMeasure(eeHist,mumuHist):
	from math import sqrt
	result = {"vals":[],"errs":[]}
	for x in range(1,eeHist.GetNbinsX()+1):
		if mumuHist.GetBinContent(x) > 0 and eeHist.GetBinContent(x) > 0:
			val = sqrt(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x))	
			#~ err = 1./(0.5*val)*sqrt((sqrt(mumuHist.GetBinContent(x))/eeHist.GetBinContent(x))**2+(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x)**2*sqrt(eeHist.GetBinContent(x)))**2)
			err = 0.5*val*sqrt(1./float(eeHist.GetBinContent(x)) + 1./float(mumuHist.GetBinContent(x)) )
			result["vals"].append(val)
			result["errs"].append(err)
		else:
			result["vals"].append(0)
			result["errs"].append(0)
	return result



def rMuEFromSFOF(eeHist,mumuHist,emuHist,corr,corrErr):
	from math import sqrt
	result = {"up":[],"down":[]}
	resultErr = {"up":[],"down":[]}
	
	for x in range(1,eeHist.GetNbinsX()+1):
		sf = float(eeHist.GetBinContent(x) + mumuHist.GetBinContent(x))
		of = emuHist.GetBinContent(x)*corr
		if of > 0:
			rSFOF = sf/of
			if eeHist.GetBinContent(x) >0 or mumuHist.GetBinContent(x) >0:
				eemmPart = 1./(eeHist.GetBinContent(x)+mumuHist.GetBinContent(x))
			else: 
				eemmPart = 0.
			if emuHist.GetBinContent(x) >0:
				emPart = 1./emuHist.GetBinContent(x)
			else: 
				emPart = 0.
				
			relErrRSFOF = sqrt(eemmPart + emPart)
			if rSFOF >1.001:
				result["up"].append(rSFOF + sqrt(rSFOF**2-1) )
				result["down"].append(rSFOF - sqrt(rSFOF**2-1) )
				
				resultErr["up"].append(rSFOF*relErrRSFOF*(1+rSFOF/sqrt(rSFOF**2-1)))
				resultErr["down"].append(rSFOF*relErrRSFOF*(1-rSFOF/sqrt(rSFOF**2-1)))
			else:
				result["up"].append(rSFOF)
				result["down"].append(rSFOF)
				
				resultErr["up"].append(rSFOF*relErrRSFOF)
				resultErr["down"].append(rSFOF*relErrRSFOF)				
		else:
			result["up"].append(0)
			result["down"].append(0)
			
			resultErr["up"].append(0)
			resultErr["down"].append(0)			
		
	return result, resultErr

def getHistograms(path,plot,runRange,isMC,backgrounds,region,selection,EM=False):
	
	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")	
	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
			
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram	
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
		#~ histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram	
		#~ histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoMM.Scale(getattr(triggerEffs,region).effMM.val)
		
		if EM:
			histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram		
			
			#~ histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
			#~ histoEM.Scale(getattr(triggerEffs,region).effEM.val)
		
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		if EM:
			histoEM = getDataHist(plot,treesEM)
	
	if EM:
		return histoEE , histoMM, histoEM
	else:
		return histoEE , histoMM
		
def getHistogramsCorrected(path,plot,runRange,isMC,backgrounds,region,selection,EM=False):
	
	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
	
		
	baseCuts = plot.cuts
		
	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		if os.path.isfile("shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl"%(runRange.label)):
			correctionParameters = pickle.load(open("shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl"%(runRange.label),"rb"))
		else:
			print "shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl does not exist"%(runRange.label)
			print "Need to run with options -f and -m on trailingPt plot first"
			sys.exit()
		
		print correctionParameters["offset"]	
		print correctionParameters["falling"]	
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"],correctionParameters["falling"])	
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
		plot.cuts = baseCuts		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoMM.Scale(getattr(triggerEffs,region).effMM.val)
		
		if EM:
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"],correctionParameters["falling"])	
			histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
					
			#~ histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		### Change the ee cut if the pt correction is used
		if os.path.isfile("shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl"%(runRange.label)):
			correctionParameters = pickle.load(open("shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl"%(runRange.label),"rb"))
		else:
			print "shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl does not exist"%(runRange.label)
			print "Need to run with options -f on trailingPt plot first"
			sys.exit()
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"],correctionParameters["falling"])
			
		histoEE = getDataHist(plot,treesEE)
		
		plot.cuts = baseCuts
		histoMM = getDataHist(plot,treesMM)
		if EM:
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"],correctionParameters["falling"])	
			histoEM = getDataHist(plot,treesEM)
			
	if EM:
		return histoEE ,histoMM, histoEM
	else:
		return histoEE , histoMM

def getHistogramsCorrectedShifted(path,plot,runRange,isMC,backgrounds,region,selection,EM=False):


	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")	
		
	baseCuts = plot.cuts		
	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		if os.path.isfile("shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl"%(runRange.label)):
			correctionParameters = pickle.load(open("shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl"%(runRange.label),"rb"))
		else:
			print "shelves/rMuE_correctionParameters_ZPeakControl_%s_MC.pkl does not exist"%(runRange.label)
			print "Need to run with options -f and -m on trailingPt plot first"
			sys.exit()
		
		offsetError = (systematics.rMuE.inclusive.val**2 + (correctionParameters["offsetErr"]/correctionParameters["offset"])**2)**0.5
		fallingError = (systematics.rMuE.inclusive.val**2 + (correctionParameters["fallingErr"]/correctionParameters["falling"])**2)**0.5
		
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"]*(1+offsetError),correctionParameters["falling"]*(1+fallingError))
		histoEEUp = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"]*(1-offsetError),correctionParameters["falling"]*(1-fallingError))			
		histoEEDown = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
		#~ histoEEUp.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoEEDown.Scale(getattr(triggerEffs,region).effEE.val)
		
		if EM:
			plot.cuts = baseCuts
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"]*(1+offsetError),correctionParameters["falling"]*(1+fallingErr))	
			histoEMUp = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram

			plot.cuts = baseCuts
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"]*(1-offsetError),correctionParameters["falling"]*(1-fallingError))	
			histoEMDown = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
			#~ histoEMUp.Scale(getattr(triggerEffs,region).effEM.val)
			#~ histoEMDown.Scale(getattr(triggerEffs,region).effEM.val)
		
	else:
		### Change the ee cut if the pt correction is used
		if os.path.isfile("shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl"%(runRange.label)):
			correctionParameters = pickle.load(open("shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl"%(runRange.label),"rb"))
		else:
			print "shelves/rMuE_correctionParameters_ZPeakControl_%s.pkl does not exist"%(runRange.label)
			print "Need to run with options -f on trailingPt plot first"
			sys.exit()
			
		offsetError = (systematics.rMuE.inclusive.val**2 + (correctionParameters["offsetErr"]/correctionParameters["offset"])**2)**0.5
		fallingError = (systematics.rMuE.inclusive.val**2 + (correctionParameters["fallingErr"]/correctionParameters["falling"])**2)**0.5
		
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"]*(1+offsetError),correctionParameters["falling"]*(1+fallingError))	
		histoEEUp = getDataHist(plot,treesEE)
		
		plot.cuts = baseCuts
		plot.cuts = "(%s)*pow((%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.)),2)"%(baseCuts,correctionParameters["offset"]*(1-offsetError),correctionParameters["falling"]*(1-fallingError))	
		histoEEDown = getDataHist(plot,treesEE)
		
		if EM:
			plot.cuts = baseCuts
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"]*(1+offsetError),correctionParameters["falling"]*(1+fallingError))	
			histoEMUp = getDataHist(plot,treesEM)
	
			plot.cuts = baseCuts
			plot.cuts = "(%s)*(%s+%s*pow(((pt1 > pt2)*pt2 + (pt2 > pt1)*pt1),-1.))"%(baseCuts,correctionParameters["offset"]*(1-offsetError),correctionParameters["falling"]*(1-fallingError))	
			histoEMDown = getDataHist(plot,treesEM)
	
	if EM:
		return histoEEUp ,histoEEDown , histoEMUp, histoEMDown
	else:
		return histoEEUp ,histoEEDown

def centralValues(path,selection,runRange,isMC,backgrounds,corrected):

	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	#~ plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut	
	plot.cuts = plot.cuts.replace("mll","p4.M()")
	plot.variable = plot.variable.replace("mll","p4.M()")
	plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")	
	if 	plot.variable == "pt":
		plot.variable = plot.variable.replace("pt","p4.Pt()")
	#~ plot.cuts = plot.cuts.replace("genWeight*weight*","")
	#~ plot.cuts = plot.cuts.replace("leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*","")
	#~ plot.cuts = plot.cuts.replace("weight*","")
	#~ plot.cuts = plot.cuts.replace("pt","p4.Pt()")

	
	if not "Forward" in selection.name:
		relSyst = systematics.rMuE.central.val
		if "Central" in selection.name:
			region = "central"
		else:
			region = "inclusive"
	else:	
		relSyst = systematics.rMuE.forward.val
		region = "forward"
	
	if corrected:
		histEE , histMM = getHistogramsCorrected(path,plot,runRange,isMC, backgrounds,region,selection)
		histEEUp, histEEDown = getHistogramsCorrectedShifted(path,plot,runRange,isMC, backgrounds,region,selection)
	else:
		histEE , histMM = getHistograms(path,plot,runRange,isMC, backgrounds,region,selection)
	
	nEE = histEE.Integral()
	nMM = histMM.Integral()
	
	rMuE= pow(nMM/nEE,0.5)
	
	if corrected:
		nEEUp = histEEUp.Integral()
		nEEDown = histEEDown.Integral()
		rMuEUp= pow(nMM/nEEUp,0.5)
		rMuEDown= pow(nMM/nEEDown,0.5)
		rMuESystErrUp= abs(rMuE-rMuEUp)
		rMuESystErrDown= abs(rMuE-rMuEDown)

	rMuEStatErr = 0.5*rMuE*(1./nMM + 1./nEE)**0.5
	rMuESystErr= rMuE*relSyst
	
	

	result = {}
	result["nEE"] = nEE
	result["nMM"] = nMM
	result["rMuE"] = rMuE
	result["rMuEStatErr"] = rMuEStatErr
	result["rMuESystErrOld"] = rMuESystErr
	if corrected:
		result["nEEUp"] = nEEUp
		result["nEEDown"] = nEEDown
		result["rMuEUp"] = rMuEUp
		result["rMuEDown"] = rMuEDown
		result["rMuESystErrUp"] = rMuESystErrUp
		result["rMuESystErrDown"] = rMuESystErrDown
		
	return result
	
	
def dependencies(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit,corrected):
	

	pathMC = locations.dataSetPathMC
	if isMC:
		backgroundsMC = ["TT_Powheg"]
	else:
		#~ backgroundsMC = ["TT_Powheg","DrellYan"]
		backgroundsMC = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		print plot.cuts
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	
		plot.cuts = plot.cuts.replace("mll","p4.M()")
		plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
		plot.variable = plot.variable.replace("mll","p4.M()")
		if 	plot.variable == "pt":
			plot.variable = plot.variable.replace("pt","p4.Pt()")
		
		#~ plot.cuts = plot.cuts.replace("genWeight*weight*","")
		#~ plot.cuts = plot.cuts.replace("leptonScaleFactor1*leptonFullSimScaleFactor2*","")
		#~ plot.cuts = plot.cuts.replace("weight*","")
		print plot.cuts

		if not "Forward" in selection.name:
			relSyst = systematics.rMuE.central.val
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			relSyst = systematics.rMuE.forward.val
			region = "forward"

		if corrected:
			if isMC:
				histEE, histMM = getHistogramsCorrected(pathMC,plot,runRange,True, backgrounds,region,selection)	
			else:
				histEE, histMM = getHistogramsCorrected(path,plot,runRange,False, backgrounds,region,selection)		
			histEEMC, histMMMC = getHistogramsCorrected(pathMC,plot,runRange,True, backgroundsMC,region,selection)	
		else:
			if isMC:
				histEE, histMM = getHistograms(pathMC,plot,runRange,True, backgrounds,region,selection)	
			else:
				histEE, histMM = getHistograms(path,plot,runRange,False, backgrounds,region,selection)	
			histEEMC, histMMMC = getHistograms(pathMC,plot,runRange,True, backgroundsMC,region,selection)	
		
		if corrected:
			plot.additionalName = "corrected"
			
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
				
			
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

		intlumi = ROOT.TLatex()
		intlumi.SetTextAlign(12)
		intlumi.SetTextSize(0.03)
		intlumi.SetNDC(True)
		
		latexLabel = ROOT.TLatex()
		latexLabel.SetTextSize(0.03)	
		latexLabel.SetNDC()					
		



		rMuE = histMM.Clone("rMuE")
		rMuE.Divide(histEE)
		rMuEMC = histMMMC.Clone("rMuEMC")
		rMuEMC.Divide(histEEMC)			
		
		
		for i in range(1, rMuE.GetNbinsX()+1):
			if rMuE.GetBinContent(i) > 0:
				rMuE.SetBinContent(i, pow(rMuE.GetBinContent(i),0.5))
			if rMuEMC.GetBinContent(i) > 0:
				rMuEMC.SetBinContent(i, pow(rMuEMC.GetBinContent(i),0.5))
			if rMuE.GetBinContent(i) > 0:
				rMuE.SetBinError(i, 0.5*pow( histMM.GetBinError(i)**2/(abs(histEE.GetBinContent(i))*abs(histMM.GetBinContent(i))) + histEE.GetBinError(i)**2*abs(histMM.GetBinContent(i))/abs(histEE.GetBinContent(i)**3), 0.5))
			if rMuEMC.GetBinContent(i) > 0:
				rMuEMC.SetBinError(i, 0.5*pow( histMMMC.GetBinError(i)**2/(abs(histEEMC.GetBinContent(i))*abs(histMMMC.GetBinContent(i))) + histEEMC.GetBinError(i)**2*abs(histMMMC.GetBinContent(i))/abs(histEEMC.GetBinContent(i)**3), 0.5))
								

		
		rMuEMC.SetMarkerStyle(21)
		rMuEMC.SetLineColor(ROOT.kGreen-2) 
		rMuEMC.SetMarkerColor(ROOT.kGreen-2) 
		

		rMuE.SetMarkerStyle(20)
		rMuE.SetLineColor(ROOT.kBlack) 
		rMuE.SetMarkerColor(ROOT.kBlack) 



		plotPad.DrawFrame(plot.firstBin,1,plot.lastBin,histMM.GetBinContent(histMM.GetMaximumBin())*10,"; %s; N_{Events}" %plot.xaxis)
		
		legend = ROOT.TLegend(0.65,0.7,0.9,0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)	
		legend.AddEntry(histMM,"#mu#mu events","p")
		legend.AddEntry(histEE,"ee events","p")
		histMM.SetMarkerColor(ROOT.kRed)
		histMM.SetLineColor(ROOT.kRed)
		histMM.SetMarkerStyle(20)
		histEE.SetMarkerStyle(21)
		histMM.Draw("samepe")
		histEE.Draw("samepe")
		legend.Draw("same")
		ROOT.gPad.SetLogy(1)
		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		
		latexLabel.DrawLatex(0.2, 0.3, selection.labelSubRegion)
		if corrected:
			latexLabel.DrawLatex(0.2, 0.23, "lepton p_{T} corrected")
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		#~ if "Simulation" in cmsExtra:
			#~ yLabelPos = 0.81	
		#~ else:
			#~ yLabelPos = 0.84	
		yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		
		
		if isMC:
			hCanvas.Print("fig/rMuE_%s_%s_%s_%s_RawInputs_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/rMuE_%s_%s_%s_%s_RawInputs.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		
		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()
		if corrected:	
			plotPad.DrawFrame(plot.firstBin,0.25,plot.lastBin,2.,"; %s; r_{#mu/e}^{corr.}" %plot.xaxis)
		else:	
			plotPad.DrawFrame(plot.firstBin,0.,plot.lastBin,2.5,"; %s; r_{#mu/e}" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		#~ if "Simulation" in cmsExtra:
			#~ yLabelPos = 0.81	
		#~ else:
			#~ yLabelPos = 0.84	
		yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

		if os.path.isfile("shelves/rMuE_%s_%s_%s.pkl"%(selection.name,runRange.label,plot.additionalName)):
			centralVals = pickle.load(open("shelves/rMuE_%s_%s_%s.pkl"%(selection.name,runRange.label,plot.additionalName),"rb"))
		else:
			centralVals = centralValues(path,selection,runRange,isMC,backgrounds,corrected)

		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [centralVals["rMuE"],centralVals["rMuE"]]) 
		ex= array("f", [0.,0.])
		ey= array("f", [centralVals["rMuE"]*systematics.rMuE.inclusive.val,centralVals["rMuE"]*systematics.rMuE.inclusive.val])
		ge= ROOT.TGraphErrors(2, x, y, ex, ey)
		ge.SetFillColor(ROOT.kOrange-9)
		ge.SetFillStyle(1001)
		ge.SetLineColor(ROOT.kWhite)
		if not fit:
			ge.Draw("SAME 3")
		
		rmueLine= ROOT.TF1("rmueline","%f"%centralVals["rMuE"],plot.firstBin,plot.lastBin)
		rmueLine.SetLineColor(ROOT.kOrange+3)
		rmueLine.SetLineWidth(3)
		rmueLine.SetLineStyle(2)
		rmueLine.Draw("SAME")
		
		
		rMuEMC.Draw("hist E1P SAME")
			
		leg = ROOT.TLegend(0.6,0.7,0.85,0.95)
		if not isMC:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "Data", "p")
			leg.AddEntry(rMuEMC,"MC","p")
			if corrected:
				leg.AddEntry(rmueLine, "r^{corr.}_{#mu/e} central value", "l")
			else:
				leg.AddEntry(rmueLine, "r_{#mu/e} central value", "l")
			
		else:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "all MC", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
			if corrected:
				leg.AddEntry(rmueLine, "r^{corr.}_{#mu/e} central value on MC", "l") 
			else:
				leg.AddEntry(rmueLine, "r_{#mu/e} central value on MC", "l") 
			
		if not fit:
			if corrected:
				leg.AddEntry(ge,"syst. unc. of r^{corr.}_{#mu/e}","f")
			else:
				leg.AddEntry(ge,"syst. unc. of r_{#mu/e}","f")

		leg.SetBorderSize(0)
		leg.SetLineWidth(2)
		leg.SetTextAlign(22)
		
		latexLabel.DrawLatex(0.2, 0.3, selection.labelSubRegion)
		if corrected:
			latexLabel.DrawLatex(0.2, 0.23, "lepton p_{T} corrected")
			
		
	
		if fit:
			if "trailingPt" in name:
			#~ if "leadingPt" in name:
				fit = TF1("dataFit","[0]+[1]*pow(x,-1)",20,200)
				fit.SetParameter(0,1)
				fit.SetParLimits(0,0.8,1.5)
				fit.SetParameter(1,10)
				fit.SetParLimits(1,0,1000)
				fit.SetLineColor(ROOT.kBlack)
				fitMC = TF1("mcFit","[0]+[1]*pow(x,-1)",20,200)
				fitMC.SetLineColor(ROOT.kGreen-2)
				fitMC.SetParameter(0,1)
				fitMC.SetParLimits(0,0.5,2)
				fitMC.SetParameter(1,10)
				fitMC.SetParLimits(1,0,1000)
				rMuE.Fit("dataFit")
				rMuEMC.Fit("mcFit")
				
				fit.Draw("same l")		
				fitMC.Draw("same l")			
				
				latexFit = ROOT.TLatex()
				latexFit.SetTextSize(0.025)	
				latexFit.SetNDC()
				if not isMC:	
					latexFit.DrawLatex(0.2, 0.23, "Fit on data: (%.2f #pm %.2f) + (%.2f #pm %.2f) * p_{T}^{-1})"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))
					latexFit.DrawLatex(0.2, 0.18, "Fit on MC:   (%.2f #pm %.2f) + (%.2f #pm %.2f) * p_{T}^{-1})"%(fitMC.GetParameter(0),fitMC.GetParError(0),fitMC.GetParameter(1),fitMC.GetParError(1)))
				else:	
					latexFit.DrawLatex(0.2, 0.23, "Fit on all MC: (%.2f #pm %.2f) + (%.2f #pm %.2f) * p_{T}^{-1})"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))
					latexFit.DrawLatex(0.2, 0.18, "Fit on ttbar MC:   (%.2f #pm %.2f) + (%.2f #pm %.2f) * p_{T}^{-1})"%(fitMC.GetParameter(0),fitMC.GetParError(0),fitMC.GetParameter(1),fitMC.GetParError(1)))
								
				
				### Only store the fit parameters when not using the pt corrected cuts
				### Otherwise things get screwed up
				if not corrected:
					correctionParameters = {}
					correctionParameters["offset"] = fit.GetParameter(0)
					correctionParameters["offsetErr"] = fit.GetParError(0)
					correctionParameters["falling"] = fit.GetParameter(1)
					correctionParameters["fallingErr"] = fit.GetParError(1)
				
					if isMC:
						outFilePkl = open("shelves/rMuE_correctionParameters_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
					else:
						outFilePkl = open("shelves/rMuE_correctionParameters_%s_%s.pkl"%(selection.name,runRange.label),"w")
					pickle.dump(correctionParameters, outFilePkl)			
	
		
		# Pfeile
		
		if "eta" in plot.variable:
			yMin = 0.7
			yMax = 1.5
			lineU1 = ROOT.TLine(1.4, yMin, 1.4, yMax)
			lineU1.SetLineColor(ROOT.kBlue-3)
			lineU1.SetLineWidth(2)
			lineU1.Draw("")
			lineU2 = ROOT.TLine(1.6, yMin, 1.6, yMax)
			lineU2.SetLineColor(ROOT.kBlue-3)
			lineU2.SetLineWidth(2)
			lineU2.Draw("")
			arrow1=ROOT.TArrow(1.55,1.3,1.6,1.3,0.01,"<|")
			arrow1.SetFillColor(ROOT.kBlue-3)
			arrow1.SetLineColor(ROOT.kBlue-3)
			arrow1.SetLineWidth(3)
			arrow1.Draw("")
			arrow2=ROOT.TArrow(1.4,1.3,1.45,1.3,0.01,"|>")
			arrow2.SetFillColor(ROOT.kBlue-3)
			arrow2.SetLineColor(ROOT.kBlue-3)
			arrow2.SetLineWidth(3)
			arrow2.Draw("")

			lineE = ROOT.TLine(2.4, yMin, 2.4, yMax) #3.5 -> 1.7
			lineE.SetLineColor(ROOT.kRed-3)
			lineE.SetLineWidth(2)
			lineE.Draw("")

		hCanvas.RedrawAxis()
		leg.Draw("SAME")
		ROOT.gPad.RedrawAxis()
		hCanvas.Update()	
		
				
		if isMC:
			if fit and "trailingPt" in name:
				hCanvas.Print("fig/rMuE_%s_%s_%s_%s_MC_fit.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
			else:
				hCanvas.Print("fig/rMuE_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
		else:
			if fit and "trailingPt" in name:	
				hCanvas.Print("fig/rMuE_%s_%s_%s_%s_fit.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
			else:	
				hCanvas.Print("fig/rMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	

		for i in range(1, rMuE.GetNbinsX()+1):
			if rMuE.GetBinContent(i) > 0:
				rMuE.SetBinError(i, 0.5*(1. - (1./rMuE.GetBinContent(i)**2))*rMuE.GetBinError(i))
			if rMuEMC.GetBinContent(i) > 0:
				rMuEMC.SetBinError(i, 0.5*(1. - (1./rMuEMC.GetBinContent(i)**2))*rMuEMC.GetBinError(i))			
			if rMuE.GetBinContent(i) > 0:
				rMuE.SetBinContent(i, 0.5*(rMuE.GetBinContent(i)+ 1./rMuE.GetBinContent(i)))
			if rMuEMC.GetBinContent(i) > 0:
				rMuEMC.SetBinContent(i, 0.5*(rMuEMC.GetBinContent(i)+ 1./rMuEMC.GetBinContent(i)))


		rMuEMC.SetMarkerStyle(21)
		rMuEMC.SetLineColor(ROOT.kGreen-2) 
		rMuEMC.SetMarkerColor(ROOT.kGreen-2) 
		

		rMuE.SetMarkerStyle(20)
		rMuE.SetLineColor(ROOT.kBlack) 
		rMuE.SetMarkerColor(ROOT.kBlack) 

		
		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		plotPad.SetLeftMargin(0.2)
		
		plotPad.Draw()	
		plotPad.cd()
		if corrected:	
			plotPad.DrawFrame(plot.firstBin,0.975,plot.lastBin,1.1,"; %s; 0.5(r^{corr.}_{#mu/e} + 1/r^{corr.}_{#mu/e})" %plot.xaxis)
		else:
			plotPad.DrawFrame(plot.firstBin,0.95,plot.lastBin,1.2,"; %s; 0.5(r_{#mu/e} + 1/r_{#mu/e})" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.23,0.88,"CMS")
		#~ if "Simulation" in cmsExtra:
			#~ yLabelPos = 0.81	
		#~ else:
			#~ yLabelPos = 0.84	
		yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.23,yLabelPos,"%s"%(cmsExtra))
		
		latexLabel.DrawLatex(0.25, 0.65, selection.labelSubRegion)
		if corrected:
			latexLabel.DrawLatex(0.25, 0.58, "lepton p_{T} corrected")


		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [0.5*(centralVals["rMuE"]+1./centralVals["rMuE"]),0.5*(centralVals["rMuE"]+1./centralVals["rMuE"])]) 
		ex= array("f", [0.,0.])
		if corrected:
			erry = max(abs(0.5*(centralVals["rMuE"] + 1./centralVals["rMuE"] - centralVals["rMuEUp"] - 1./centralVals["rMuEUp"])),abs(0.5*(centralVals["rMuE"] + 1./centralVals["rMuE"] - centralVals["rMuEDown"] - 1./centralVals["rMuEDown"])))
			#~ ey= array("f", [abs(0.5*(centralVals["rMuE"] + 1./centralVals["rMuE"] - centralVals["rMuE"]*(1+systematics.rMuE.inclusive.val) - 1./(centralVals["rMuE"]*(1+systematics.rMuE.inclusive.val)))),abs(0.5*(centralVals["rMuE"] + 1./centralVals["rMuE"] - centralVals["rMuE"]*(1+systematics.rMuE.inclusive.val) - 1./(centralVals["rMuE"]*(1+systematics.rMuE.inclusive.val))))])
			ey= array("f", [erry,erry])
		else:
			ey= array("f", [0.5*(1. - (1./(centralVals["rMuE"]**2)))*centralVals["rMuESystErrOld"],0.5*(1. - (1./(centralVals["rMuE"]**2)))*centralVals["rMuESystErrOld"]])
		ge= ROOT.TGraphErrors(2, x, y, ex, ey)
		ge.SetFillColor(ROOT.kOrange-9)
		ge.SetFillStyle(1001)
		ge.SetLineColor(ROOT.kWhite)
		ge.Draw("SAME 3")
		
		rmueLine= ROOT.TF1("rmueline","%f"%(0.5*(centralVals["rMuE"]+1./centralVals["rMuE"])),plot.firstBin,plot.lastBin)
		rmueLine.SetLineColor(ROOT.kOrange+3)
		rmueLine.SetLineWidth(3)
		rmueLine.SetLineStyle(2)
		rmueLine.Draw("SAME")
		
		
		rMuEMC.Draw("hist E1P SAME")
			
		leg = ROOT.TLegend(0.6,0.7,0.85,0.95)
		if not isMC:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "Data", "p")
			leg.AddEntry(rMuEMC,"MC","p")
			
		else:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "all MC", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
		if not isMC: 
			leg.AddEntry(rmueLine, "central value", "l")
		else:
			leg.AddEntry(rmueLine, "central value on MC", "l")
		if corrected: 
			leg.AddEntry(ge,"syst. unc. of r^{corr.}_{#mu/e}","f")
		else: 
			leg.AddEntry(ge,"syst. unc. of r_{#mu/e}","f")

		leg.SetBorderSize(0)
		leg.SetLineWidth(2)
		leg.SetTextAlign(22)
		
		
		# Pfeile
		
		if "eta" in plot.variable:
			yMin = 0.975
			yMax = 1.05
			lineU1 = ROOT.TLine(1.4, yMin, 1.4, yMax)
			lineU1.SetLineColor(ROOT.kBlue-3)
			lineU1.SetLineWidth(2)
			lineU1.Draw("")
			lineU2 = ROOT.TLine(1.6, yMin, 1.6, yMax)
			lineU2.SetLineColor(ROOT.kBlue-3)
			lineU2.SetLineWidth(2)
			lineU2.Draw("")
			arrow1=ROOT.TArrow(1.55,1.3,1.6,1.3,0.01,"<|")
			arrow1.SetFillColor(ROOT.kBlue-3)
			arrow1.SetLineColor(ROOT.kBlue-3)
			arrow1.SetLineWidth(3)
			arrow1.Draw("")
			arrow2=ROOT.TArrow(1.4,1.3,1.45,1.3,0.01,"|>")
			arrow2.SetFillColor(ROOT.kBlue-3)
			arrow2.SetLineColor(ROOT.kBlue-3)
			arrow2.SetLineWidth(3)
			arrow2.Draw("")

			lineE = ROOT.TLine(2.4, yMin, 2.4, yMax) #3.5 -> 1.7
			lineE.SetLineColor(ROOT.kRed-3)
			lineE.SetLineWidth(2)
			lineE.Draw("")

		hCanvas.RedrawAxis()
		leg.Draw("SAME")
		ROOT.gPad.RedrawAxis()
		hCanvas.Update()	
		
				
		if isMC:
			hCanvas.Print("fig/rSFOFFromRMuE_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))
		else:	
			hCanvas.Print("fig/rSFOFFromRMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	
	
def signalRegion(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,corrected):
	plots = ["mllPlotRMuESignal"]
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		#~ plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	

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

		
		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC, backgrounds,region,selection,corrected,EM=True)	

		rMuEMeasured = rMuEMeasure(histEE,histMM)	
		rMuE, rMuEUncert = rMuEFromSFOF(histEE,histMM,histEM,corr,corrErr)
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		
		style=setTDRStyle()
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()				
		
		plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,5,"; %s ; %s" %(plot.xaxis,"r_{#mu/e}"))			
		latex = ROOT.TLatex()
		latex.SetTextSize(0.04)
		latex.SetNDC(True)

		
		if "Central" in selection.name:
			centralName = "ZPeakControlCentral"
		elif "Forward" in selection.name:
			centralName = "ZPeakControlForward"
		else:
			centralName = "ZPeakControl"
		
		if os.path.isfile("shelves/rMuE_%s_%s.pkl"%(centralName,runRange.label)):
			centralVals = pickle.load(open("shelves/rMuE_%s_%s.pkl"%(centralName,runRange.label),"rb"))
		else:
			centralVals = centralValues(path,getRegion(centralName),runRange,False,backgrounds)
		
		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [centralVals["rMuE"],centralVals["rMuE"]]) 
		ex= array("f", [0.,0.])
		ey= array("f", [centralVals["rMuESystErr"],centralVals["rMuESystErr"]])
		ge= ROOT.TGraphErrors(2, x, y, ex, ey)
		ge.SetFillColor(ROOT.kOrange-9)
		ge.SetFillStyle(1001)
		ge.SetLineColor(ROOT.kWhite)
		ge.Draw("SAME 3")
		
		rmueLine= ROOT.TF1("rmueline","%f"%centralVals["rMuE"],plot.firstBin,plot.lastBin)
		rmueLine.SetLineColor(ROOT.kOrange+3)
		rmueLine.SetLineWidth(3)
		rmueLine.SetLineStyle(2)
		rmueLine.Draw("SAME")	
				
		
	
		arrayRMuEHigh = array("f",rMuE["up"])
		arrayRMuELow = array("f",rMuE["down"])
		arrayRMuEMeasured = array("f",rMuEMeasured["vals"])
		arrayRMuEHighUncert = array("f",rMuEUncert["up"])
		arrayRMuELowUncert = array("f",rMuEUncert["down"])
		arrayRMuEMeasuredUncert = array("f",rMuEMeasured["errs"])
		xValues = []
		xValuesUncert = []

		for x in range(0,histEE.GetNbinsX()):	
			xValues.append(plot.firstBin+ (plot.lastBin-plot.firstBin)/plot.nBins + x*((plot.lastBin-plot.firstBin)/plot.nBins))
			xValuesUncert.append(0)

		
		arrayXValues = array("f",xValues)
		arrayXValuesUncert = array("f",xValuesUncert)

		
		graphHigh = ROOT.TGraphErrors(histEE.GetNbinsX(),arrayXValues,arrayRMuEHigh,arrayXValuesUncert,arrayRMuEHighUncert)
		graphLow = ROOT.TGraphErrors(histEE.GetNbinsX(),arrayXValues,arrayRMuELow,arrayXValuesUncert,arrayRMuEHighUncert)
		graphMeasured = ROOT.TGraphErrors(histEE.GetNbinsX(),arrayXValues,arrayRMuEMeasured,arrayXValuesUncert,arrayRMuEMeasuredUncert)
		
		
		graphHigh.SetMarkerStyle(21)
		graphLow.SetMarkerStyle(22)
		graphMeasured.SetMarkerStyle(23)
		graphHigh.SetMarkerColor(ROOT.kRed)
		graphLow.SetMarkerColor(ROOT.kBlue)
		graphHigh.SetLineColor(ROOT.kRed)
		graphLow.SetLineColor(ROOT.kBlue)
		
		graphHigh.Draw("sameEP0")
		graphLow.Draw("sameEP0")
		graphMeasured.Draw("sameEP0")
		
		
		
		
		legend = TLegend(0.5, 0.6, 0.95, 0.95)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		entryHist = TH1F()
		entryHist.SetFillColor(ROOT.kWhite)
		legend.AddEntry(entryHist,selection.latex,"h")
		legend.AddEntry(graphHigh,"r_{#mu/e} = N_{SF}/N_{OF} + #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
		legend.AddEntry(graphLow,"r_{#mu/e} = N_{SF}/N_{OF} - #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
		legend.AddEntry(rmueLine,"r_{#mu/e} from Z peak","l")
		legend.AddEntry(ge,"Syst. Uncert. of r_{#mu/e}","f")
		legend.AddEntry(graphMeasured,"r_{#mu/e} = #sqrt{N_{#mu#mu}/N_{ee}} in SF signal region","p")
		
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

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))		
		
		plotPad.RedrawAxis()
		if isMC:
			hCanvas.Print("fig/rMuESignal_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
		else:	
			hCanvas.Print("fig/rMuESignal_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
	
def main():



	parser = argparse.ArgumentParser(description='rMuE measurements.')
	
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
	parser.add_argument("-C", "--corrected", action="store_true", dest="corrected", default=False,
						  help="Use cuts corrected for rMuE dependency on trailing lepton pt")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")	
	parser.add_argument("-z", "--signalRegion", action="store_true", dest="signalRegion", default= False,
						  help="make rMuE in signal region plot")	
	parser.add_argument("-f", "--fit", action="store_true", dest="fit", default= False,
						  help="do dependecy fit")	
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.rMuE
	if len(args.selection) == 0:
		
		if args.signalRegion:
			#~ args.selection.append(regionsToUse.signal.central.name)	
			#~ args.selection.append(regionsToUse.signal.forward.name)	
			args.selection.append(regionsToUse.signal.inclusive.name)		
		else:
			#~ args.selection.append(regionsToUse.rMuE.central.name)	
			#~ args.selection.append(regionsToUse.rMuE.forward.name)	
			args.selection.append(regionsToUse.rMuE.inclusive.name)
			
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)		

	path = locations.dataSetPath
	print path
	

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

			if args.central:
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,args.corrected)
				if args.mc:
					if args.corrected:
						outFilePkl = open("shelves/rMuE_%s_%s_MC_corrected.pkl"%(selection.name,runRange.label),"w")
					else:
						outFilePkl = open("shelves/rMuE_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					if args.corrected:
						outFilePkl = open("shelves/rMuE_%s_%s_corrected.pkl"%(selection.name,runRange.label),"w")
					else:
						outFilePkl = open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit,args.corrected)		
			if args.signalRegion:
				 signalRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.corrected)	
				 
			if args.write:
				import subprocess
				if args.mc:
					if args.corrected:
						bashCommand = "cp shelves/rMuE_correctionParameters_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					else:		
						bashCommand = "cp shelves/rMuE_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:
					if args.corrected:	
						bashCommand = "cp shelves/rMuE_correctionParameters_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					else:
						bashCommand = "cp shelves/rMuE_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())				 	

main()
