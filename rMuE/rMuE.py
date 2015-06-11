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

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

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

def getHistograms(path,source,modifier,plot,runRange,isMC,backgrounds,region,iso,EM=False):


	treesEE = readTrees(path,"EE",source = source,modifier= modifier)
	treesEM = readTrees(path,"EMu",source = source,modifier= modifier)
	treesMM = readTrees(path,"MuMu",source = source,modifier= modifier)
		
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
			
	
		if "not_isolated" in iso:
			flavor_independent_cuts = plot.cuts
			prompt_cuts = "(%s) && (abs(motherPdgId1) == 11 || abs(motherPdgId1) == 15 || motherPdgId1 == 23 || abs(motherPdgId1) == 24) && (abs(motherPdgId2) == 11 || abs(motherPdgId2) == 15 || motherPdgId2 == 23 || abs(motherPdgId2) == 24)"%plot.cuts
			nonIsoCutsEE = "(%s) && d01 < 0.02 && d02 < 0.02 && dZ1 < 0.1 && dZ2 < 0.1 && abs(deltaEtaSuperClusterTrackAtVtx1) < 0.007 && abs(deltaEtaSuperClusterTrackAtVtx2) < 0.007 && abs(deltaPhiSuperClusterTrackAtVtx1) < 0.07 && abs(deltaPhiSuperClusterTrackAtVtx2) < 0.07 && sigmaIetaIeta1 < 0.01 && sigmaIetaIeta2 < 0.01 && hadronicOverEm1 < 0.12 && hadronicOverEm2 < 0.12 && eOverP1 < 0.05 && eOverP2 < 0.05 && missingHits1 < 2 && missingHits2 < 2"%prompt_cuts
			nonIsoCutsEMu = "(%s) && d01 < 0.02 && d02 < 0.02 && dZ1 < 0.1 && dZ2 < 0.1 && abs(deltaEtaSuperClusterTrackAtVtx1) < 0.007 && abs(deltaPhiSuperClusterTrackAtVtx1) < 0.07 && sigmaIetaIeta1 < 0.01 && hadronicOverEm1 < 0.12 && eOverP1 < 0.05 && missingHits1 < 2 && globalMuon2 == 1 && trackerMuon2 == 1 && pfMuon2 == 1 && trackChi22 < 10 && numberOfValidMuonHits2 > 0 && numberOfMatchedStations2 > 1 && numberOfValidPixelHits2 > 0 && trackerLayersWithMeasurement2 > 5"%prompt_cuts
			nonIsoCutsMuMu = "(%s) && d01 < 0.02 && d02 < 0.02 && dZ1 < 0.1 && dZ2 < 0.1 && globalMuon1 == 1  && globalMuon2 == 1 && trackerMuon1 == 1 && trackerMuon2 == 1 && pfMuon1 == 1 && pfMuon2 == 1 && trackChi21 < 10 && trackChi22 < 10 && numberOfValidMuonHits1 > 0 && numberOfValidMuonHits2 > 0 && numberOfMatchedStations1 > 1 && numberOfMatchedStations2 > 1 && numberOfValidPixelHits1 > 0 && numberOfValidPixelHits2 > 0 && trackerLayersWithMeasurement1 > 5 && trackerLayersWithMeasurement2 > 5"%prompt_cuts
		
		
			plot.cuts = nonIsoCutsEE
			histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram
			
			plot.cuts = nonIsoCutsMuMu		
			histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
			
			histoEE.Scale(getattr(triggerEffs,region).effEE.val)
			histoMM.Scale(getattr(triggerEffs,region).effMM.val)
			
			if EM:
				plot.cuts = nonIsoCutsEMu
				histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
				histoEM.Scale(getattr(triggerEffs,region).effEM.val)
				
			plot.cuts = flavor_independent_cuts

	
		else:
			
			eventCounts = totalNumberOfGeneratedEvents(path,source)	
			processes = []
			for background in backgrounds:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
			
			histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
			histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
			histoEE.Scale(getattr(triggerEffs,region).effEE.val)
			histoMM.Scale(getattr(triggerEffs,region).effMM.val)
			
			if EM:
				histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
				histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		if EM:
			histoEM = getDataHist(plot,treesEM)
	
	if EM:
		return histoEE , histoMM, histoEM
	else:
		return histoEE , histoMM

def centralValues(source,modifier,path,selection,runRange,isMC,backgrounds,ptCut,iso):

	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	#~ plot.cleanCuts()
	if ptCut != "pt2020":
		pt_Cut = getattr(theCuts.ptCuts,ptCut)
		plot.cuts = plot.cuts.replace("pt1 > 20 && pt2 > 20",pt_Cut.cut)
	plot.cuts = plot.cuts % runRange.runCut		


	
	if not "Forward" in selection.name:
		relSyst = systematics.rMuE.central.val
		if "Central" in selection.name:
			region = "central"
		else:
			region = "inclusive"
	else:	
		relSyst = systematics.rMuE.forward.val
		region = "forward"
	
	histEE, histMM = getHistograms(path,source,modifier,plot,runRange,isMC, backgrounds,region,iso)
	
	nEE = histEE.Integral()
	nMM = histMM.Integral()
	
	rMuE= pow(nMM/nEE,0.5)

	#~ rMuEStatErr = pow( pow(nMM**0.5/nEE,2) + pow(nEE**0.5*nMM/(nEE**2),2), 0.5)
	rMuEStatErr = 0.5*rMuE*pow( 1./nMM + 1./nEE, 0.5)
	rMuESystErr= rMuE*relSyst
	

	result = {}
	result["nEE"] = nEE
	result["nMM"] = nMM
	result["rMuE"] = rMuE
	result["rMuEStatErr"] = rMuEStatErr
	result["rMuESystErr"] = rMuESystErr
	
	return result
	
	
def dependencies(source,modifier,path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit,ptCut,iso):
	
	#~ backgrounds = ["TTJets_SpinCorrelations"]
	backgrounds = ["TTJets"]
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()
		if ptCut != "pt2020":
			pt_Cut = getattr(theCuts.ptCuts,ptCut)
			plot.cuts = plot.cuts.replace("pt1 > 20 && pt2 > 20",pt_Cut.cut)
			pt_label = pt_Cut.label
		else:
			pt_label = "p_{T} > 20 GeV"		
		plot.cuts = plot.cuts % runRange.runCut	

		if not "Forward" in selection.name:
			relSyst = systematics.rMuE.central.val
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			relSyst = systematics.rMuE.forward.val
			region = "forward"
			
		if "MiniIsoEffAreaIso" in source:
			iso_label = "mini iso cone, eff. area corrected"
		elif "MiniIsoDeltaBetaIso" in source:
			iso_label = "mini iso cone, #Delta#beta corrected"
		elif "MiniIsoPFWeights" in source:
			iso_label = "mini iso cone, PF weights"
		elif "EffAreaIso" in source:
			iso_label = "R=0.3 cone, eff. area corrected"
		elif "DeltaBetaIso" in source:
			iso_label = "R=0.3 cone, #Delta#beta corrected"


		#~ histEE, histMM = getHistograms(path,plot,runRange,False, backgrounds,region)	
		histEEMC, histMMMC = getHistograms(path,source,modifier,plot,runRange,True, backgrounds,region,iso)	
			
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
				
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(11)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexLumi = ROOT.TLatex()
		latexLumi.SetTextFont(42)
		latexLumi.SetTextAlign(31)
		latexLumi.SetTextSize(0.04)
		latexLumi.SetNDC(True)
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
		



		#~ rMuE = histMM.Clone("rMuE")
		#~ rMuE.Divide(histEE)
		rMuEMC = histMMMC.Clone("rMuEMC")
		rMuEMC.Divide(histEEMC)
		
		#~ for i in range(1, rMuE.GetNbinsX()+1):
		for i in range(1, rMuEMC.GetNbinsX()+1):
			#~ rMuE.SetBinContent(i, pow(rMuE.GetBinContent(i),0.5))
			rMuEMC.SetBinContent(i, pow(rMuEMC.GetBinContent(i),0.5))
			#~ if rMuE.GetBinContent(i) > 0:
				#~ rMuE.SetBinError(i, pow( pow(histMM.GetBinContent(i)**0.5/histEE.GetBinContent(i),2) + pow(histEE.GetBinContent(i)**0.5*histMM.GetBinContent(i)/(histEE.GetBinContent(i)**2),2), 0.5))
			if rMuEMC.GetBinContent(i) > 0:
				#~ rMuEMC.SetBinError(i, pow( pow(histMMMC.GetBinError(i)/histEEMC.GetBinContent(i),2) + pow(histEEMC.GetBinError(i)*histMMMC.GetBinContent(i)/(histEEMC.GetBinContent(i)**2),2), 0.5))
				#~ rMuEMC.SetBinError(i, 0.5*rMuEMC.GetBinContent(i)*pow( pow(histEEMC.GetBinError(i)/histEEMC.GetBinContent(i),2) + pow(histMMMC.GetBinError(i)/histMMMC.GetBinContent(i),2), 0.5))
				rMuEMC.SetBinError(i, 0.5*rMuEMC.GetBinContent(i)*pow( 1./histEEMC.GetBinContent(i) + 1./histMMMC.GetBinContent(i), 0.5))

		rMuEMC.SetMarkerStyle(21)
		rMuEMC.SetLineColor(ROOT.kGreen-2) 
		rMuEMC.SetMarkerColor(ROOT.kGreen-2) 
		

		#~ rMuE.SetMarkerStyle(20)
		#~ rMuE.SetLineColor(ROOT.kBlack) 
		#~ rMuE.SetMarkerColor(ROOT.kBlack) 



		plotPad.DrawFrame(plot.firstBin,1,plot.lastBin,histMMMC.GetBinContent(histMMMC.GetMaximumBin())*10,"; %s; N_{Events}" %plot.xaxis)
		#~ plotPad.DrawFrame(plot.firstBin,1,plot.lastBin,histMM.GetBinContent(histMM.GetMaximumBin())*10,"; %s; N_{Events}" %plot.xaxis)
		
		legend = ROOT.TLegend(0.65,0.7,0.9,0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)	
		#~ legend.AddEntry(histMM,"#mu#mu events","p")
		#~ legend.AddEntry(histEE,"ee events","p")
		legend.AddEntry(histMMMC,"#mu#mu events","p")
		legend.AddEntry(histEEMC,"ee events","p")
		#~ histMM.SetMarkerColor(ROOT.kRed)
		#~ histMM.SetLineColor(ROOT.kRed)
		#~ histMM.SetMarkerStyle(20)
		#~ histEE.SetMarkerStyle(21)
		#~ histMM.Draw("samepe")
		#~ histEE.Draw("samepe")
		histMMMC.SetMarkerColor(ROOT.kRed)
		histMMMC.SetLineColor(ROOT.kRed)
		histMMMC.SetMarkerStyle(20)
		histEEMC.SetMarkerStyle(21)
		histMMMC.Draw("samepe")
		histEEMC.Draw("samepe")
		legend.Draw("same")
		ROOT.gPad.SetLogy(1)
		
		#~ latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
		if iso:
			latex.DrawLatex(0.25, 0.3, "not isolated")
		latex.DrawLatex(0.25, 0.2, pt_label)
		latex.DrawLatex(0.25, 0.25, selection.latex)
		latex.DrawLatex(0.35, 0.65, iso_label)
		
#~ 
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		
		
		
		hCanvas.Print("fig/rMuE_%s_%s_%s_%s_%s_%s_RawInputs.pdf"%(selection.name,source,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))	
		
		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
		plotPad.DrawFrame(plot.firstBin,0.7,plot.lastBin,1.6,"; %s; r_{#mue}" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		#~ latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
		if iso:
			latex.DrawLatex(0.25, 0.3, "not isolated")
		latex.DrawLatex(0.25, 0.2, pt_label)
		latex.DrawLatex(0.25, 0.25, selection.latex)
		latex.DrawLatex(0.35, 0.65, iso_label)
		

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

		

		#~ if os.path.isfile("shelves/rMuE_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut)):
			#~ centralVals = pickle.load(open("shelves/rMuE_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut),"rb"))
		#~ else:
		centralVals = centralValues(source,modifier,path,selection,runRange,isMC,backgrounds,ptCut,iso)
		
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
		
		
		rMuEMC.Draw("hist E1P SAME")
			
		leg = ROOT.TLegend(0.55,0.7,0.925,0.95)
		if not isMC:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "Data", "p")
		if "DiLeptonTrigger" in source:
			leg.AddEntry(rMuEMC,"t#bar{t} MC, Dilepton Trigger","p")
		elif "Reweighted" in source:
			leg.AddEntry(rMuEMC,"t#bar{t} MC, Reweighted","p")
		else:
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
		if not isMC: 
			leg.AddEntry(rmueLine, "r_{#mu e} central value", "l")
		else:
			leg.AddEntry(rmueLine, "r_{#mu e} central value on MC", "l") 
		leg.AddEntry(ge,"syst. unc. of r_{#mu e}","f")

		leg.SetBorderSize(0)
		leg.SetFillStyle(0)
		leg.SetLineWidth(2)
		leg.SetTextAlign(22)
		
	
		if fit:
			fit = TF1("dataFit","pol1",0,300)
			fit.SetLineColor(ROOT.kGreen+3)
			fitMC = TF1("mcFit","pol1",0,300)
			fitMC.SetLineColor(ROOT.kBlue+3)
			rMuE.Fit("dataFit")
			rMuEMC.Fit("mcFit")			
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)	
			latex.SetNDC()	
			latex.DrawLatex(0.2, 0.25, "Fit on data: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))
			latex.DrawLatex(0.2, 0.20, "Fit on MC:   %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fitMC.GetParameter(0),fitMC.GetParError(0),fitMC.GetParameter(1),fitMC.GetParError(1)))			
	
		
		# Pfeile
		
		if "eta" in plot.variable:
			yMin = 0.8
			yMax = 1.6
			lineU1 = ROOT.TLine(1.4, yMin, 1.4, yMax-0.2)
			lineU1.SetLineColor(ROOT.kBlue-3)
			lineU1.SetLineWidth(2)
			lineU1.Draw("")
			lineU2 = ROOT.TLine(1.6, yMin, 1.6, yMax-0.2)
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

			lineE = ROOT.TLine(2.4, yMin, 2.4, yMax-0.2) #3.5 -> 1.7
			lineE.SetLineColor(ROOT.kRed-3)
			lineE.SetLineWidth(2)
			lineE.Draw("")

		hCanvas.RedrawAxis()
		leg.Draw("SAME")
		ROOT.gPad.RedrawAxis()
		hCanvas.Update()	
		
				


		hCanvas.Print("fig/rMuE_%s_%s_%s_%s_%s_%s.pdf"%(selection.name,source,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))	


def dependenciesPU(source,path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit,ptCut,iso):
		
	backgrounds = ["TTJets","TTJets_PU4BX50","TTJets_PU30BX50"]
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()
		if ptCut != "pt2020":
			pt_Cut = getattr(theCuts.ptCuts,ptCut)
			plot.cuts = plot.cuts.replace("pt1 > 20 && pt2 > 20",pt_Cut.cut)
			pt_label = pt_Cut.label
		else:
			pt_label = "p_{T} > 20 GeV"	
		plot.cuts = plot.cuts % runRange.runCut	

		if not "Forward" in selection.name:
			relSyst = systematics.rMuE.central.val
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			relSyst = systematics.rMuE.forward.val
			region = "forward"


		histos = {}
		
		for background in backgrounds:
			BG = []
			BG.append(background)
			histos["histEEMC_%s"%(background)],histos["histMMMC_%s"%(background)] = getHistograms(path,source,plot,runRange,True, BG,region,iso)
				
			
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
				
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(11)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexLumi = ROOT.TLatex()
		latexLumi.SetTextFont(42)
		latexLumi.SetTextAlign(31)
		latexLumi.SetTextSize(0.04)
		latexLumi.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)		

		#~ intlumi = ROOT.TLatex()
		#~ intlumi.SetTextAlign(12)
		#~ intlumi.SetTextSize(0.03)
		#~ intlumi.SetNDC(True)					
		


		for background in backgrounds:
			BG_sample = getattr(Backgrounds,background)
			histos["rMuEMC_%s"%(background)] = histos["histMMMC_%s"%(background)].Clone("rMuEMC_%s"%(background))
			histos["rMuEMC_%s"%(background)].Divide(histos["histEEMC_%s"%(background)])
			histos["rMuEMC_%s"%(background)].SetLineColor(BG_sample.linecolor)
			histos["rMuEMC_%s"%(background)].SetMarkerColor(BG_sample.linecolor)
			histos["rMuEMC_%s"%(background)].SetMarkerStyle(21)

		
			for i in range(1, histos["rMuEMC_%s"%(background)].GetNbinsX()+1):
				histos["rMuEMC_%s"%(background)].SetBinContent(i, pow(histos["rMuEMC_%s"%(background)].GetBinContent(i),0.5))
				if histos["rMuEMC_%s"%(background)].GetBinContent(i) > 0:
					histos["rMuEMC_%s"%(background)].SetBinError(i, 0.5*histos["rMuEMC_%s"%(background)].GetBinError(i)*pow( 1./histos["histEEMC_%s"%(background)].GetBinContent(i) + 1./histos["histMMMC_%s"%(background)].GetBinContent(i), 0.5))
		
		

		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
		plotPad.DrawFrame(plot.firstBin,0.7,plot.lastBin,1.6,"; %s; r_{#mue}" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
		latex.DrawLatex(0.25, 0.2, pt_label)
		latex.DrawLatex(0.25, 0.25, selection.latex)
		

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

		
#~ 
		#~ if os.path.isfile("shelves/rMuE_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut)):
			#~ centralVals = pickle.load(open("shelves/rMuE_%s_%s_%s.pkl"%(selection.name,source,runRange.label,ptCut),"rb"))
		#~ else:
			#~ centralVals = centralValues(source,path,selection,runRange,isMC,backgrounds,ptCut)

		
		#~ rmueLine= ROOT.TF1("rmueline","%f"%centralVals["rMuE"],plot.firstBin,plot.lastBin)
		#~ rmueLine.SetLineColor(ROOT.kOrange+3)
		#~ rmueLine.SetLineWidth(3)
		#~ rmueLine.SetLineStyle(2)
		#~ rmueLine.Draw("SAME")

		
		leg = ROOT.TLegend(0.6,0.7,0.95,0.95)
		for background in backgrounds:
			BG_sample = getattr(Backgrounds,background)
			histos["rMuEMC_%s"%(background)].Draw("hist E1P SAME")
			if "DileptonTrigger" in source:
				leg.AddEntry(histos["rMuEMC_%s"%(background)],BG_sample.label+" Dilepton Trigger","p")
			else:
				leg.AddEntry(histos["rMuEMC_%s"%(background)],BG_sample.label,"p")
		
		#~ leg.AddEntry(rmueLine, "r_{#mu e} central value on MC", "l") 

		leg.SetFillStyle(0)
		leg.SetBorderSize(0)
		leg.SetLineWidth(2)
		leg.SetTextAlign(22)
		
	

		# Pfeile
		
		if "eta" in plot.variable:
			yMin = 0.8
			yMax = 1.6
			lineU1 = ROOT.TLine(1.4, yMin, 1.4, yMax-0.2)
			lineU1.SetLineColor(ROOT.kBlue-3)
			lineU1.SetLineWidth(2)
			lineU1.Draw("")
			lineU2 = ROOT.TLine(1.6, yMin, 1.6, yMax-0.2)
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

			lineE = ROOT.TLine(2.4, yMin, 2.4, yMax-0.2) #3.5 -> 1.7
			lineE.SetLineColor(ROOT.kRed-3)
			lineE.SetLineWidth(2)
			lineE.Draw("")

		hCanvas.RedrawAxis()
		leg.Draw("SAME")
		ROOT.gPad.RedrawAxis()
		hCanvas.Update()	
		
				


		hCanvas.Print("fig/rMuE_PUStudy_%s_%s_%s_%s_%s_%s.pdf"%(selection.name,source,runRange.label,plot.variablePlotName,plot.additionalName,ptCut))	
	
	
def signalRegion(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,iso):
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

		
		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC, backgrounds,region,iso,EM=True)	

		rMuEMeasured = rMuEMeasure(histEE,histMM)	
		rMuE, rMuEUncert = rMuEFromSFOF(histEE,histMM,histEM,corr,corrErr)
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		plotPad = TPad("plotPad","plotPad",0,0,1,1)
		
		style=setTDRStyle()
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		plotPad.cd()				
		
		plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,5,"; %s ; %s" %(plot.xaxis,"r_{#mu e}"))			
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
			centralVals = centralValues(path,getRegion(centralName),runRange,False,backgrounds,iso)
		
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
		legend.AddEntry(graphHigh,"r_{#mu e} = N_{SF}/N_{OF} + #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
		legend.AddEntry(graphLow,"r_{#mu e} = N_{SF}/N_{OF} - #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
		legend.AddEntry(rmueLine,"r_{#mu e} from Z peak","l")
		legend.AddEntry(ge,"Syst. Uncert. of r_{#mu e}","f")
		legend.AddEntry(graphMeasured,"r_{#mu e} = #sqrt{N_{#mu#mu}/N_{ee}} in SF signal region","p")
		
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
	parser.add_argument("-P", "--pileUp", dest="pileUp", action="store_true", default=False,
						  help="make pile up studies.")
	parser.add_argument("-i", "--nonIsolated", dest="nonIsolated", action="store_true", default=False,
						  help="use base trees without isolation requirement.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-C", "--ptCut",action="store", dest="ptCut", default="pt2515",
						  help="modify the pt cuts")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")
	parser.add_argument("-l", "--dilepton", action="store_true", dest="dilepton", default=False,
						  help="use dilepton triggers as baseline.")
	parser.add_argument("-e", "--effectiveArea", action="store_true", dest="effectiveArea", default=False,
						  help="use effective area PU corrections.")	
	parser.add_argument("-D", "--deltaBeta", action="store_true", dest="deltaBeta", default=False,
						  help="use delta beta PU corrections.")	
	parser.add_argument("-R", "--constantConeSize", action="store_true", dest="constantConeSize", default=False,
						  help="use constant cone of R=0.3 for iso.")	
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
			args.selection.append(regionsToUse.signal.central.name)	
			args.selection.append(regionsToUse.signal.forward.name)	
			args.selection.append(regionsToUse.signal.inclusive.name)		
		else:
			args.selection.append(regionsToUse.rMuE.central.name)	
			args.selection.append(regionsToUse.rMuE.forward.name)	
			args.selection.append(regionsToUse.rMuE.inclusive.name)
			
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)
	
	if args.dilepton:
		source = "DiLeptonTrigger"
		modifier = "DiLeptonTrigger"
	else:
		source = ""		
		modifier = ""		

	if args.nonIsolated:
		if args.dilepton:
			path = locations.baseTreesTriggerDataSetPath
			iso = "not_isolated_DiLeptonTrigger"
			source = "baseTreesDiLeptonTrigger"
		else:
			path = locations.baseTreesDataSetPath	
			iso = "not_isolated"
			source = "baseTrees"	
	else:	
		path = locations.dataSetPath
		iso = ""
		
	if args.constantConeSize:
		if args.effectiveArea:
			source = "EffAreaIso%s"%source
		elif args.deltaBeta:
			source = "DeltaBetaIso%s"%source
		else:
			print "Constant cone size (option -R) can only be used in combination with effective area (-e) or delta beta (-D) pileup corrections."
			print "Using default miniIso cone with PF weights instead"
	else:
		if args.effectiveArea:
			source = "MiniIsoEffAreaIso%s"%source
		elif args.deltaBeta:
			source = "MiniIsoDeltaBetaIso%s"%source
		else:
			source = "MiniIsoPFWeights%s"%source


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
				centralVal = centralValues(source,modifier,path,selection,runRange,args.mc,args.backgrounds,args.ptCut,iso)
				if args.mc:
					if args.nonIsolated:
						outFilePkl = open("shelves/rMuE_%s_%s_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label,args.ptCut,iso),"w")
					else:
						outFilePkl = open("shelves/rMuE_%s_%s_%s_%s_MC.pkl"%(selection.name,source,runRange.label,args.ptCut),"w")
				else:
					outFilePkl = open("shelves/rMuE_%s_%s_%s_%s.pkl"%(selection.name,source,runRange.label,args.ptCut),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(source,modifier,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit,args.ptCut,iso)		
			if args.pileUp:
				 dependenciesPU(source,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit,args.ptCut,iso)		
			if args.signalRegion:
				 signalRegion(source,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.ptCut,iso)	
				 
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rMuE_%s_%s_%s_%s_MC.pkl %s/shelves"%(selection.name,source,runRange.label,args.ptCut,pathes.basePath)		
				else:	
					bashCommand = "cp shelves//rMuE_%s_%s_%s_%s.pkl %s/shelves"%(selection.name,source,runRange.label,args.ptCut,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())				 	

main()
