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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle, TFile
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, create2DHistoFromTree

from corrections import triggerEffs, rSFOF
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics
from locations import locations



def getRates(ev,sort):
	
	fileFake = TFile("fakeRates.root")
	filePrompt = TFile("promptRates.root")
	
	fakeHistE = fileFake.Get("fakeRateE")
	fakeHistM = fileFake.Get("fakeRateM")
	
	promptHistE = filePrompt.Get("promptRateE")
	promptHistM = filePrompt.Get("promptRateM")
	
	
	result = {}
	
	if sort == "MM":
		result["f1"] = fakeHistM.GetBinContent(fakeHistM.FindBin(ev.pt1,abs(ev.eta1)))
		result["f2"] = fakeHistM.GetBinContent(fakeHistM.FindBin(ev.pt2,abs(ev.eta2)))
		result["p1"] = promptHistM.GetBinContent(promptHistM.FindBin(ev.pt1,abs(ev.eta1)))
		result["p2"] = promptHistM.GetBinContent(promptHistM.FindBin(ev.pt2,abs(ev.eta2)))	
		#~ result["f1"] = 0.082
		#~ result["f2"] = 0.082
		#~ result["p1"] = 0.94
		#~ result["p2"] = 0.94	
	elif sort == "EE":
		result["f1"] = fakeHistE.GetBinContent(fakeHistE.FindBin(ev.pt1,abs(ev.eta1)))
		result["f2"] = fakeHistE.GetBinContent(fakeHistE.FindBin(ev.pt2,abs(ev.eta2)))
		result["p1"] = promptHistE.GetBinContent(promptHistE.FindBin(ev.pt1,abs(ev.eta1)))
		result["p2"] = promptHistE.GetBinContent(promptHistE.FindBin(ev.pt2,abs(ev.eta2)))	
		#~ result["f1"] = 0.112
		#~ result["f2"] = 0.112
		#~ result["p1"] = 0.88
		#~ result["p2"] = 0.88	
	elif sort == "EM":
		result["f1"] = fakeHistE.GetBinContent(fakeHistE.FindBin(ev.pt1,abs(ev.eta1)))
		result["f2"] = fakeHistM.GetBinContent(fakeHistM.FindBin(ev.pt2,abs(ev.eta2)))
		result["p1"] = promptHistE.GetBinContent(promptHistE.FindBin(ev.pt1,abs(ev.eta1)))
		result["p2"] = promptHistM.GetBinContent(promptHistM.FindBin(ev.pt2,abs(ev.eta2)))
		#~ result["f1"] = 0.112
		#~ result["f2"] = 0.082
		#~ result["p1"] = 0.88
		#~ result["p2"] = 0.94
		
	#~ result["p1"] = 1.0
	#~ result["p2"] = 1.0
	
	
	return result	
	


def getHistograms(path,plot,runRange):

	treesMu = readTrees(path,"","Fake","FakemuonIso")
	treesE = readTrees(path,"","Fake","FakeelectronIso")



	histoE = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
	histoM = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)

	for index, tree in treesMu.iteritems():
		histoM.Add(getDataHist(plot,treesMu,dataname=index))

	for index, tree in treesE.iteritems():
		histoE.Add(getDataHist(plot,treesE,dataname=index))

	
	return [histoE , histoM]
def get2DHistogramsPrompt(path,cut,binningPt,binningEta):

	treesMu = readTrees(path,"MuMu")
	treesE = readTrees(path,"EE")	
#
	histoE = ROOT.TH2F("","",len(binningPt)-1,array("f",binningPt),len(binningEta)-1,array("f",binningEta))
	histoM = ROOT.TH2F("","",len(binningPt)-1,array("f",binningPt),len(binningEta)-1,array("f",binningEta))

	for index, tree in treesMu.iteritems():
		if index == "MergedData_Loose":
			histoM.Add(create2DHistoFromTree(tree,"pt1","abs(eta1)",cut,len(binningPt)-1,binningPt[0],binningPt[-1],binning=binningPt,binning2=binningEta).Clone())
	for index, tree in treesE.iteritems():
		if index == "MergedData_Loose":	
			histoE.Add(create2DHistoFromTree(tree,"pt1","abs(eta1)",cut,len(binningPt)-1,binningPt[0],binningPt[-1],binning=binningPt,binning2=binningEta).Clone())

	print histoE.GetEntries()
	return [histoE , histoM]
	
def get2DHistograms(path,cut,binningPt,binningEta):

	treesMu = readTrees(path,"","Fake","FakemuonIso")
	treesE = readTrees(path,"","Fake","FakeelectronIso")

	rmList = []
	for index, tree in treesMu.iteritems():
		if "DoubleElectron" in index:
			rmList.append(index)
	for index in rmList:
		del treesMu[index]
	rmList = []			
	for index, tree in treesE.iteritems():
		if "DoubleMu" in index:
			rmList.append(index)
	for index in rmList:
		del treesE[index]		
#
	histoE = ROOT.TH2F("","",len(binningPt)-1,array("f",binningPt),len(binningEta)-1,array("f",binningEta))
	histoM = ROOT.TH2F("","",len(binningPt)-1,array("f",binningPt),len(binningEta)-1,array("f",binningEta))

	for index, tree in treesMu.iteritems():
		histoM.Add(create2DHistoFromTree(tree,"pt","abs(eta)",cut,len(binningPt)-1,binningPt[0],binningPt[-1],binning=binningPt,binning2=binningEta).Clone())
	for index, tree in treesE.iteritems():
		histoE.Add(create2DHistoFromTree(tree,"pt","abs(eta)",cut,len(binningPt)-1,binningPt[0],binningPt[-1],binning=binningPt,binning2=binningEta).Clone())

	
	return [histoE , histoM]
	
def getHistogramsPrompt(path,plot,runRange):

	treesMu = readTrees(path,"MuMu")
	treesE = readTrees(path,"EE")

	histoM = getDataHist(plot,treesMu,dataname="MergedData_Loose")
	histoE = getDataHist(plot,treesE,dataname="MergedData_Loose")

	
	return [histoE , histoM]
	
	
def getTrees(path,plot):


	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
				
	
	for index, tree in treesEE.iteritems():
		if index == "MergedData_Loose":
			treeEE = tree	
	for index, tree in treesMM.iteritems():
		if index == "MergedData_Loose":
			treeMM = tree	
	for index, tree in treesEM.iteritems():
		if index == "MergedData_Loose":
			treeEM = tree	
	
	result = {}
	result["EE"] = treeEE.CopyTree(plot.cuts)
	result["MM"] = treeMM.CopyTree(plot.cuts)
	result["EM"] = treeEM.CopyTree(plot.cuts)
	return result

	
	
def promptRate(path,selection,plots,runRange,cmsExtra):

	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)	
		plot.cuts = plot.cuts % runRange.runCut	
		
	
		if "met" in name:
			plot.cuts = plot.cuts+"*(ht > 80 && id1 < 1.0 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106)"
		else:	
			plot.cuts = plot.cuts+"*(ht > 80 && id1 < 1.0 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106 && met < 20)"

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

		histsLoose = getHistogramsPrompt(path,plot,runRange)	
		if "met" in name:
			plot.cuts = plot.cuts+"*(ht > 80 && id1 < 0.15 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106)"
		else:	
			plot.cuts = plot.cuts+"*(ht > 80 && id1 < 0.15 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106 && met < 20)"
		

		histsTight= getHistogramsPrompt(path,plot,runRange)	
		
		
		for index, histLoose in enumerate(histsLoose):
			
			histTight = histsTight[index]
			
			print histTight.GetEntries(), histLoose.GetEntries()
			
			hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
			plotPad = TPad("plotPad","plotPad",0,0,1,1)
			
			style=setTDRStyle()
			plotPad.UseCurrentStyle()
			plotPad.Draw()	
			plotPad.cd()				
			logScale = plot.log
	
				
			plotPad.DrawFrame(plot.firstBin,0.5,plot.lastBin,1,"; %s ; %s" %(plot.xaxis,"prompt rate"))	
			
			
			
			fakeRate = TGraphAsymmErrors(histTight,histLoose,"cp")
			
		
			fakeRate.SetMarkerStyle(20)

			
			
			fakeRate.Draw("samep")

					
			latex = ROOT.TLatex()
			latex.SetTextSize(0.04)
			latex.SetNDC(True)

			legend = TLegend(0.55, 0.5, 0.95, 0.95)
			legend.SetFillStyle(0)
			legend.SetBorderSize(0)
			entryHist = TH1F()
			entryHist.SetFillColor(ROOT.kWhite)
			#~ legend.AddEntry(entryHist,selection.latex,"h")
			legend.AddEntry(fakeRate,"prompt rate","pe")

			
			#~ legend.Draw("same")
		



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
			if index == 0:
				hCanvas.Print("fig/promptRate_ele_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
			else:
				hCanvas.Print("fig/promptRate_mu_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
							
def fakeRate(path,selection,plots,runRange,cmsExtra):




	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)	
		plot.cuts = plot.cuts % runRange.runCut	
		
		if "Pt" in name:
			plot.variable = "pt"
		elif "Eta" in name:
			plot.variable = "eta"
			
			
		if "met" in name:
			plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 1.0"
		else:	
			plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 1.0 && met < 20"

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

		histsLoose = getHistograms(path,plot,runRange)	
		if "met" in name:
			plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 0.15"
		else:	
			plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 0.15 && met < 20 "
		

		histsTight= getHistograms(path,plot,runRange)	
		
		
		for index, histLoose in enumerate(histsLoose):
			
			histTight = histsTight[index]
			
			print histTight.GetEntries(), histLoose.GetEntries()
			
			hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
			plotPad = TPad("plotPad","plotPad",0,0,1,1)
			
			style=setTDRStyle()
			plotPad.UseCurrentStyle()
			plotPad.Draw()	
			plotPad.cd()				
			logScale = plot.log
	
				
			plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,1,"; %s ; %s" %(plot.xaxis,"fake rate"))	
			
			
			
			fakeRate = TGraphAsymmErrors(histTight,histLoose,"cp")
			
		
			fakeRate.SetMarkerStyle(20)

			
			
			fakeRate.Draw("samep")

					
			latex = ROOT.TLatex()
			latex.SetTextSize(0.04)
			latex.SetNDC(True)

			legend = TLegend(0.55, 0.825, 0.95, 0.95)
			legend.SetFillStyle(0)
			legend.SetBorderSize(0)
			entryHist = TH1F()
			entryHist.SetFillColor(ROOT.kWhite)
			#~ legend.AddEntry(entryHist,selection.latex,"h")
			legend.AddEntry(fakeRate,"fake rate","pe")

			
			#~ legend.Draw("same")
		



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
			if index == 0:
				hCanvas.Print("fig/fakeRate_ele_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
			else:
				hCanvas.Print("fig/fakeRate_mu_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))				
	


def fakeRateCentral(path,selection,plots,runRange,cmsExtra):


	f = TFile("fakeRates.root","RECREATE")

	ptBins = [20,25,30,10000]
	etaBins = [0,0.3,0.6,0.9,1.2,1.442,1.562,1.9,2.2,2.4]

	fakeRateE = ROOT.TH2F("fakeRateE","",len(ptBins)-1,array("f",ptBins),len(etaBins)-1,array("f",etaBins))
	fakeRateM = ROOT.TH2F("fakeRateM","",len(ptBins)-1,array("f",ptBins),len(etaBins)-1,array("f",etaBins))
	
	
	plot = getPlot("trailingPtPlot")
	plot.addRegion(selection)	
	plot.cuts = plot.cuts % runRange.runCut	
		

	plot.variable = "pt"
	


	plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 1.0 && met < 20 && pt < 35"

	histsLoose = get2DHistograms(path,plot.cuts,ptBins,etaBins)	

	plot.cuts = "abs(eta) < 2.4 && (abs(eta) < 1.4 || abs(eta) > 1.6) && ptJet1 > 50 && mT < 20 &&  nLept == 1 && pfIso < 0.15 && met < 20 && pt < 35"
	
	histsTight = get2DHistograms(path,plot.cuts,ptBins,etaBins)	

	
	
	histsTight[0].Divide(histsLoose[0])	
	histsTight[1].Divide(histsLoose[1])


	fakeRateE.Add(histsTight[0].Clone())
	fakeRateM.Add(histsTight[1].Clone())
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	style.SetPadRightMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	logScale = plot.log
		
	plotPad.DrawFrame(0.,0.,200,2.4,"; %s ; %s" %("trailing p_{T} [GeV]","trailing #eta"))	
	
	
	histsTight[0].Draw("samecolz")


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
	hCanvas.Print("fig/fakeRate_ele.pdf")	
			
	plotPad.DrawFrame(0.,0.,200,2.4,"; %s ; %s" %("trailing p_{T} [GeV]","trailing #eta"))	
	
	
	histsTight[1].Draw("samecolz")


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
	hCanvas.Print("fig/fakeRate_mu.pdf")			
		
	f.Write()
	f.Close()					




def promptRateCentral(path,selection,plots,runRange,cmsExtra):


	f = TFile("promptRates.root","RECREATE")

	ptBins = [20,25,30,35,40,50,60,70,10000]
	etaBins = [0,0.3,0.6,0.9,1.2,1.442,1.562,1.9,2.2,2.4]

	promptRateE = ROOT.TH2F("promptRateE","",len(ptBins)-1,array("f",ptBins),len(etaBins)-1,array("f",etaBins))
	promptRateM = ROOT.TH2F("promptRateM","",len(ptBins)-1,array("f",ptBins),len(etaBins)-1,array("f",etaBins))
	
	
	plot = getPlot("trailingPtPlot")
	plot.addRegion(selection)	
	plot.cuts = plot.cuts % runRange.runCut	
		

	#~ plot.variable = "pt1"
	



	plot.cuts = plot.cuts+"*(ht > 80 && id1 < 1.0 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106 && met < 20)"

	histsLoose = get2DHistogramsPrompt(path,plot.cuts,ptBins,etaBins)	

	plot.cuts = plot.cuts+"*(ht > 80 && id1 < 0.15 && id2 < 0.15 && nLightLeptons == 2 && p4.M() > 76 && p4.M() < 106 && met < 20)"
	
	histsTight = get2DHistogramsPrompt(path,plot.cuts,ptBins,etaBins)	

	
	
	histsTight[0].Divide(histsLoose[0])	
	histsTight[1].Divide(histsLoose[1])


	promptRateE.Add(histsTight[0].Clone())
	promptRateM.Add(histsTight[1].Clone())
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	style.SetPadRightMargin(0.2)
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	logScale = plot.log
		
	plotPad.DrawFrame(0.,0.,200,2.4,"; %s ; %s" %("trailing p_{T} [GeV]","trailing #eta"))	
	
	
	histsTight[0].Draw("samecolz")


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
	hCanvas.Print("fig/promptRate_ele.pdf")	
			
	plotPad.DrawFrame(0.,0.,200,2.4,"; %s ; %s" %("trailing p_{T} [GeV]","trailing #eta"))	
	
	
	histsTight[1].Draw("samecolz")


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
	hCanvas.Print("fig/promptRate_mu.pdf")			
		
	f.Write()
	f.Close()	




def nonPromptPrediction(path,selection,plots,runRange,cmsExtra):
	
	
	
	
	plot = getPlot("mllPlot")
	plot.addRegion(selection)	
	plot.cuts = plot.cuts % runRange.runCut	

	plot.cuts = plot.cuts+"*(id1 < 1.0 && id2 < 1.0)"
	
	print plot.cuts
	
	trees = getTrees(path,plot)
	

	combinations = ["EE","MM","EM"]
	result = {}
	for combination in combinations:
		nPP = 0
		nPF = 0
		nFP = 0
		nFF = 0
		nTT = 0
		nTL = 0
		nLT = 0
		nLL = 0
		for ev in trees[combination]:
			
			rates = getRates(ev,combination)
			if ev.id1 < 0.15 and ev.id2 < 0.15:
				nPP += (rates["f1"]-1)*(rates["f2"]-1)/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["p2"]
				nPF += (rates["f1"]-1)*(1-rates["p2"])/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["f2"]
				nFP += (1-rates["p1"])*(rates["f2"]-1)/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["p2"]
				nFF += (1-rates["p1"])*(1-rates["p2"])/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["f2"]
				nTT += 1
			elif ev.id1 < 0.15 and ev.id2 > 0.15:
				nPP += (rates["f1"]-1)*rates["f2"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["p2"]
				nPF += -(rates["f1"]-1)*rates["p2"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["f2"]
				nFP += rates["f2"]*(1-rates["p1"])/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["p2"]
				nFF += -(1-rates["p1"])*rates["p2"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["f2"]
				nTL += 1
			elif ev.id1 > 0.15 and ev.id2 < 0.15:
				nPP += (rates["f2"]-1)*rates["f1"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["p2"]
				nPF += rates["f1"]*(1-rates["p2"])/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["f2"]
				nFP += -rates["p1"]*(rates["f2"]-1)/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["p2"]
				nFF += -(1-rates["p2"])*rates["p1"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["f2"]#
				nLT += 1
			elif ev.id1 > 0.15 and ev.id2 > 0.15:
				nPP += rates["f2"]*rates["f1"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["p2"]
				nPF += -rates["f1"]*rates["p2"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["p1"]*rates["f2"]
				nFP += -rates["p1"]*rates["f2"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["p2"]
				nFF += rates["p2"]*rates["p1"]/((rates["f1"]-rates["p1"])*(rates["f2"]-rates["p2"]))*rates["f1"]*rates["f2"]
				nLL += 1
			#~ if ev.id1 < 0.15 and ev.id2 < 0.15:
				#~ nTT += 1
			#~ elif ev.id1 < 0.15 and ev.id2 > 0.15:
				#~ nPF += rates["f2"]/(1-rates["f2"])
				#~ nTL += 1
			#~ elif ev.id1 > 0.15 and ev.id2 < 0.15:
				#~ nFP += rates["f1"]/(1-rates["f1"])
				#~ nLT += 1
			#~ elif ev.id1 > 0.15 and ev.id2 > 0.15:
				#~ nFF += (rates["f1"]/(1-rates["f1"]))*(rates["f2"]/(1-rates["f2"]))
				#~ nLL += 1

		print "--------------------------"
		print nPP, nPF, nFP, nFF
		from math import sqrt
		nPPErr = sqrt(nTT)*nPP/nTT
		nPFErr = sqrt(nTT)*nPF/nTL
		nFPErr = sqrt(nTT)*nFP/nLT
		nFFErr = sqrt(nTT)*nFF/nLL
		
		nFake = nPF+nFP+nFF
		nFakeErr = nPFErr+nFPErr+nFFErr

		result[combination] = {"nPP":nPP,"nPPErr":nPPErr,"nPF":nPF,"nPFErr":nPFErr,"nFP":nFP,"nFPErr":nFPErr,"nFF":nFF,"nFFErr":nFFErr, "nTT":nTT,"nTL":nTL,"nLT":nLT,"nLL":nLL,"nFake":nFake,"nFakeErr":nFakeErr}
		
	outFilePkl = open("shelves/nonPrompt_%s_%s"%(selection.name,runRange.label),"w")
	pickle.dump(result, outFilePkl)
	outFilePkl.close()	
	
		
def main():



	parser = argparse.ArgumentParser(description='rMuE measurements.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")	
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	

	args = parser.parse_args()




	plots = plotLists.fake

	selections = ["Region"]	
			
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)		

	path = locations.fakeDataSetPath	

	#~ path = "/home/jan/Trees/sw538v0477"

	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
	else:
		cmsExtra = "Preliminary"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)

			#~ fakeRate(path,selection,plots,runRange,cmsExtra)
			#~ fakeRateCentral(path,selection,plots,runRange,cmsExtra)
	path = locations.dataSetPath	

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)

			#~ promptRate(path,selection,plots,runRange,cmsExtra)
			#~ promptRateCentral(path,selection,plots,runRange,cmsExtra)
	selections = ["SignalCentral","SignalForward"]		
			
	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)

			nonPromptPrediction(path,selection,plots,runRange,cmsExtra)

main()
