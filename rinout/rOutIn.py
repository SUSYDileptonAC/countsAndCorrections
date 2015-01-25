#!/usr/bin/env python

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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import systematics, rSFOF, rEEOF, rMMOF
import corrections



from locations import locations


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


	
def plotMllSpectra(SFhist,EMuhist,runRange,selection,suffix,cmsExtra):

		
	SFhist.Rebin(5)
	EMuhist.Rebin(5)

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	style.SetTitleYOffset(1.6)
	style.SetPadLeftMargin(0.19)		
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	

	
	plotPad.DrawFrame(20,0,300,SFhist.GetBinContent(SFhist.GetMaximumBin())*1.5,"; %s ; %s" %("m_{ll} [GeV]","Events / 5 GeV"))		

	
	SFhist.SetMarkerStyle(20)
	SFhist.SetMarkerColor(ROOT.kBlack)
	
	EMuhist.Draw("samehist")
	SFhist.Draw("samepe")
	EMuhist.SetFillColor(855)
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)	
	legend.AddEntry(SFhist,"%s events"%suffix,"p")
	legend.AddEntry(EMuhist,"OF events","f")
	legend.Draw("same")

	
	line1 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line5.SetLineColor(ROOT.kBlack)
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line5.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	line5.Draw("same")

	Labelin = ROOT.TLatex()
	Labelin.SetTextAlign(12)
	Labelin.SetTextSize(0.07)
	Labelin.SetTextColor(ROOT.kRed+2)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.07)
	Labelout.SetTextColor(ROOT.kBlack)	
	
	
	Labelin.DrawLatex(80.75,SFhist.GetBinContent(SFhist.GetMaximumBin())/1.5,"In")
	Labelout.DrawLatex(27.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/1.5,"Out")
	Labelout.DrawLatex(150.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/1.5,"Out")	
	
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.21,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.21,yLabelPos,"%s"%(cmsExtra))
	
	plotPad.RedrawAxis()
	hCanvas.Print("fig/rOutIn_NoLog_%s_%s_%s.pdf"%(selection.name,suffix,runRange.label))	
	
	
	
	hCanvas.Clear()
	
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	

	
	plotPad.DrawFrame(20,1,300,SFhist.GetBinContent(SFhist.GetMaximumBin())*10,"; %s ; %s" %("m_{ll} [GeV]","Events / 5 GeV"))		
	
	plotPad.SetLogy()

	
	EMuhist.Draw("samehist")
	SFhist.Draw("samepe")
	EMuhist.SetFillColor(855)
	legend.Draw("same")
	
	line1 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))	
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line5.SetLineColor(ROOT.kBlack)	
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line5.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	line5.Draw("same")
	Labelin.DrawLatex(81.35,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"In")
	Labelout.DrawLatex(27.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"Out")
	Labelout.DrawLatex(150.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"Out")
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra)) 	
	plotPad.RedrawAxis()
	hCanvas.Print("fig/rOutIn_%s_%s_%s.pdf"%(suffix,selection.name,runRange.label))	
	
	
def plotSystematics(EEtrees,MuMutrees,EMutrees,suffix,Rinout,Simulation=False,highMass=False):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
	sampleName = "MergedData"
	
	if Simulation:
		sampleName = "ZJets_madgraph_Summer12"
		sampleName2 = "AStar_madgraph_Summer12"
	
	minMll = 20
	maxMll = 70
	if highMass:
		minMll = 120
		maxMll = 1000

	nBins = 1500
	firstBin = 0
	lastBin = 300


	legend = TLegend(0.65, 0.65, 0.98, 0.90)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)

	Cutlabel = ROOT.TLatex()
	Cutlabel.SetTextAlign(12)
	Cutlabel.SetTextSize(0.03)
	Labelin = ROOT.TLatex()
	Labelin.SetTextAlign(12)
	Labelin.SetTextSize(0.07)
	Labelin.SetTextColor(ROOT.kRed+2)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.07)
	Labelout.SetTextColor(ROOT.kBlack)
	
	
	metRange = 6
	metBinsUp=[10,20,30,40,60,100]
	metBinsDown=[0,10,20,30,40,60]	
	Rinout2Jets = []
	ErrRinout2Jets = []	
	nJets=2
	
	#~ cuts = "weight*(chargeProduct < 0 && %s && met < %d && met > %d && nJets == %d && runNr <= 196531 && deltaR > 0.3 && abs(eta1)<2.4 && abs(eta2)<2.4)"
	cuts = "weight*(chargeProduct < 0 && %s && met < %d && met > %d && nJets == %d  && deltaR > 0.3 && %s )"

	
	for index in range (0,metRange):
		addHist = None
		legend.Clear()
		for name, tree in EEtrees.iteritems():
			if name == sampleName:
				EEhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
		
		if addHist != None:
			EEhist.Add(addHist.Clone())
		addHist = None			
		for name, tree in MuMutrees.iteritems():
			if name == sampleName:
				MuMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
		if addHist != None:
			MuMuhist.Add(addHist.Clone())		
		addHist = None
		for name, tree in EMutrees.iteritems():
			if name == sampleName:

				EMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)		
		
		if addHist != None:
			EMuhist.Add(addHist.Clone())			
		
		if argv[2] == "SF":		
			SFhist = EEhist.Clone()
			SFhist.Add(MuMuhist.Clone())
		elif argv[2] == "EE":
			SFhist = EEhist.Clone()
		else:
			SFhist = MuMuhist.Clone()
			



			#SFhist.Add(EMuhist,-1)
		
		peak = (SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))- EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))*nllPredictionScale) 
		peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101+0.01))*nllPredictionScale)**2)
		continuum = (SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)) - EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale )
		continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(maxMll+0.01),SFhist.FindBin(maxMll)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale)**2) 
		localRinout =   continuum / peak			
		localErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)


		Rinout2Jets.append(localRinout)
		ErrRinout2Jets.append(localErrRinout)
		
		
		SFhist.Rebin(25)
		EMuhist.Rebin(25)
		SFhist.Draw("")
		SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
		SFhist.GetYaxis().SetTitle("Events / 5 GeV")
		EMuhist.Draw("samehist")
		#EMuhist.SetLineColor(ROOT.kRed)
		EMuhist.SetFillColor(855)
		legend.AddEntry(SFhist,"SF events","p")
		legend.AddEntry(EMuhist,"OF events","f")
		legend.Draw("same")
		hCanvas.SetLogy()
			
		line1 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line2 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line5 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line1.SetLineColor(ROOT.kBlack)
		line2.SetLineColor(ROOT.kBlack)
		line5.SetLineColor(ROOT.kBlack)
		line3.SetLineColor(ROOT.kRed+2)
		line4.SetLineColor(ROOT.kRed+2)
		line1.SetLineWidth(2)
		line2.SetLineWidth(2)
		line3.SetLineWidth(2)
		line4.SetLineWidth(2)
		line5.SetLineWidth(2)
		line1.Draw("same")
		line2.Draw("same")
		line3.Draw("same")
		line4.Draw("same")
		line5.Draw("same")
		Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"In")
		Labelout.DrawLatex(32.5,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Labelout.DrawLatex(150,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > 20 GeV}{ %d GeV < met < %d GeV, nJets ==%d}" %(metBinsDown[index],metBinsUp[index],nJets))
			#~ Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
			#~ Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
			#~ Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20(10) GeV}{MET < 100 GeV, nJets ==3}")
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True) 
			
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
		cmsExtra = "Preliminary"
		if Simulation:
			cmsExtra = "Simulation"
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 			
			
		if highMass:	
			hCanvas.Print("fig/Rinout_highMass_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		else:
			hCanvas.Print("fig/Rinout_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		
	hCanvas.Clear()			
	hCanvas.SetLogy(0)		
	
	
	
	arg6 = numpy.array([-5,105],"d")
	arg7 = numpy.array([Rinout,Rinout],"d")
	arg8 = numpy.array([0,0],"d")
	arg9 = numpy.array([Rinout*0.25,Rinout*0.25],"d")
	
	errorband = ROOT.TGraphErrors(2,arg6,arg7,arg8,arg9)
	errorband.GetYaxis().SetRangeUser(0.0,0.15)
	errorband.GetXaxis().SetRangeUser(-5,105)
	errorband.GetXaxis().SetTitle("E_{T}^{miss} [GeV]")
	errorband.GetYaxis().SetTitle("r_{out,in}")
	errorband.Draw("A3")
	errorband.SetFillColor(ROOT.kOrange-9)
	rinoutLine = ROOT.TLine(-5,Rinout,105,Rinout)
	rinoutLine.SetLineStyle(ROOT.kDashed)
	rinoutLine.SetLineWidth(2)
	rinoutLine.Draw("same")

	METvalues =[5,15,25,35,50,80]
	METErrors =[5,5,5,5,10,20]
	arg2 = numpy.array(METvalues,"d")
	arg3 = numpy.array(Rinout2Jets,"d")
	arg4 = numpy.array(METErrors,"d")
	arg5 = numpy.array(ErrRinout2Jets,"d")	
	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graph2jet = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graph2jet.Draw("Psame0")
	legend.Clear()
	#legend.AddEntry(graph1jet,"NJets==1","p")
	if argv[3] == "MC":
		legend.AddEntry(graph2jet,"r_{out,in} MC","p")
	else:
		legend.AddEntry(graph2jet,"r_{out,in} Data","p")
	#legend.AddEntry(graph3jet,"NJets==3","p")
	legend.AddEntry(rinoutLine, "Mean r_{out,in} = %.3f"%Rinout,"l")
	legend.AddEntry(errorband, "Mean r_{out,in} #pm 25%","f")
	legend.Draw("same")


	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if argv[3] == "MC":
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 		
		
	ROOT.gPad.RedrawAxis()
	if highMass:		
		hCanvas.Print("fig/RinoutSystMET_highMass_Full2012_%s.pdf"%suffix)
	else:
		hCanvas.Print("fig/RinoutSystMET_Full2012_%s.pdf"%suffix)

	RinoutMET100 = []
	ErrRinoutMET100 = []	
	
	for nJets in range (0,6):

		legend.Clear()
		addHist = None 
		for name, tree in EEtrees.iteritems():
			if name == sampleName:
				EEhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)	
		if addHist != None:
			EEhist.Add(addHist.Clone())
		addHist = None
		for name, tree in MuMutrees.iteritems():
			if name == sampleName:
				MuMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)				
		if addHist != None:
			MuMuhist.Add(addHist.Clone())
		addHist = None		
		for name, tree in EMutrees.iteritems():
			if name == sampleName:
				EMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)				
		if addHist != None:
			EMuhist.Add(addHist.Clone())
						
		if argv[2] == "SF":		
			SFhist = EEhist.Clone()
			SFhist.Add(MuMuhist.Clone())
		elif argv[2] == "EE":
			SFhist = EEhist.Clone()
		else:
			SFhist = MuMuhist.Clone()
			
		peak = (SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))- EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))*nllPredictionScale) 
		peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101+0.01))*nllPredictionScale)**2)
		continuum = (SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)) - EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale )
		continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale)**2) 
		localRinout =   continuum / peak			
			
			#localRinout = SFhist.Integral(SFhist.FindBin(15),SFhist.FindBin(70)) / SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101))
		localErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
		print localRinout
		print localErrRinout

		RinoutMET100.append(localRinout)
		ErrRinoutMET100.append(localErrRinout)	
		
		SFhist.Rebin(25)
		EMuhist.Rebin(25)
		SFhist.Draw("")
		SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
		SFhist.GetYaxis().SetTitle("Events / 5 GeV")
		EMuhist.Draw("samehist")
		#EMuhist.SetLineColor(ROOT.kRed)
		EMuhist.SetFillColor(855)
		legend.AddEntry(SFhist,"SF events","p")
		legend.AddEntry(EMuhist,"OF events","f")
		legend.Draw("same")
		hCanvas.SetLogy()
			
		line1 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line2 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line5 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))		
		line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line1.SetLineColor(ROOT.kBlack)
		line2.SetLineColor(ROOT.kBlack)
		line5.SetLineColor(ROOT.kBlack)
		line3.SetLineColor(ROOT.kRed+2)
		line4.SetLineColor(ROOT.kRed+2)
		line1.SetLineWidth(2)
		line2.SetLineWidth(2)
		line3.SetLineWidth(2)
		line4.SetLineWidth(2)
		line5.SetLineWidth(2)
		line1.Draw("same")
		line2.Draw("same")
		line3.Draw("same")
		line4.Draw("same")
		line5.Draw("same")
		Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"In")
		Labelout.DrawLatex(150,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Labelout.DrawLatex(32.5,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")		
		Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > 20 GeV}{ %d GeV < met < %d GeV, nJets ==%d}" %(0,100,nJets))
			#~ Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
			#~ Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
			#~ Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20(10) GeV}{MET < 100 GeV, nJets ==3}")
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True) 
			
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
		cmsExtra = "Preliminary"
		if Simulation:
			cmsExtra = "Simulation"
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 
			
		if highMass:	
			hCanvas.Print("fig/Rinout_highMass_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))		
		else:
			hCanvas.Print("fig/Rinout_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		
	hCanvas.Clear()
	hCanvas.SetLogy(0)	
	arg6 = numpy.array([-0.5,6.5],"d")
	arg7 = numpy.array([Rinout,Rinout],"d")
	arg8 = numpy.array([0,0],"d")
	arg9 = numpy.array([Rinout*0.25,Rinout*0.25],"d")
	
	errorband = ROOT.TGraphErrors(2,arg6,arg7,arg8,arg9)
	errorband.GetYaxis().SetRangeUser(0.0,0.15)
	errorband.GetXaxis().SetRangeUser(-0.5,6.5)
	errorband.GetXaxis().SetTitle("N_{Jets}")
	errorband.GetYaxis().SetTitle("r_{out,in}")
	errorband.Draw("A3")
	errorband.SetFillColor(ROOT.kOrange-9)
	rinoutLine = ROOT.TLine(-0.5,Rinout,6.5,Rinout)
	rinoutLine.SetLineStyle(ROOT.kDashed)
	rinoutLine.SetLineWidth(2)
	rinoutLine.Draw("same")

	METvalues =[0.5,1.5,2.5,3.5,4.5,5.5]
	METErrors =[0.5,0.5,0.5,0.5,0.5,0.5]
	arg2 = numpy.array(METvalues,"d")
	arg3 = numpy.array(RinoutMET100,"d")
	arg4 = numpy.array(METErrors,"d")
	arg5 = numpy.array(ErrRinoutMET100,"d")	
	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graphMET100 = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graphMET100.Draw("Psame0")
	legend.Clear()
	#legend.AddEntry(graph1jet,"NJets==1","p")
	if argv[3] == "MC":
		legend.AddEntry(graphMET100,"r_{out,in} MC","p")
	else:
		legend.AddEntry(graphMET100,"r_{out,in} Data","p")
	#legend.AddEntry(graph3jet,"NJets==3","p")
	legend.AddEntry(rinoutLine, "Mean r_{out,in} = %.3f"%Rinout,"l")
	legend.AddEntry(errorband, "Mean r_{out,in} #pm 25%","f")
	legend.Draw("same")
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if argv[3] == "MC":
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 
	ROOT.gPad.RedrawAxis()
	if highMass:		
		hCanvas.Print("fig/RinoutSystNJets_highMass_Full2012_%s.pdf"%suffix)
	else:		
		hCanvas.Print("fig/RinoutSystNJets_Full2012_%s.pdf"%suffix)
	
	

	
	
def centralValues(path,selection,runRange,isMC,backgrounds,cmsExtra):			
			

	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		

	
	if not "Forward" in selection.name:
		region = "central"
	else:		
		region = "forward"


	histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,backgrounds)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())
	result = {}
	print histEE.GetNbinsX()
	lowMassLow = 20
	lowMassHigh = 70
	peakLow = 81
	peakHigh = 101
	highMassLow = 120
	highMassHigh = 1000

		
	result["peakEE"] = histEE.Integral(histEE.FindBin(peakLow+0.01),histEE.FindBin(peakHigh-0.01))
	result["peakMM"] = histMM.Integral(histMM.FindBin(peakLow+0.01),histMM.FindBin(peakHigh-0.01))
	result["peakSF"] = result["peakEE"] + result["peakMM"]
	result["peakOF"] = histEM.Integral(histEM.FindBin(peakLow+0.01),histEM.FindBin(peakHigh-0.01))
	result["lowMassEE"] = histEE.Integral(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01))
	result["lowMassMM"] = histMM.Integral(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01))
	result["lowMassSF"] = result["lowMassEE"] + result["lowMassMM"]
	result["lowMassOF"] = histEM.Integral(histEM.FindBin(lowMassLow),histEM.FindBin(lowMassHigh-0.01))
	result["highMassEE"] = histEE.Integral(histEE.FindBin(highMassLow+0.01),histEE.FindBin(highMassHigh))
	result["highMassMM"] = histMM.Integral(histMM.FindBin(highMassLow+0.01),histMM.FindBin(highMassHigh))
	result["highMassSF"] = result["highMassEE"] + result["highMassMM"]
	result["highMassOF"] = histEM.Integral(histEM.FindBin(highMassLow+0.01),histEM.FindBin(highMassHigh))

		
	for combination in ["EE","MM","SF"]:
		corr = getattr(corrections,"r%sOF"%combination).central.val
		corrErr = getattr(corrections,"r%sOF"%combination).central.err
		peak = result["peak%s"%combination] - result["peakOF"]*corr			
		peakErr = sqrt(result["peak%s"%combination] + (sqrt(result["peakOF"])*corr)**2 + (sqrt(result["peakOF"])*corr*corrErr)**2)
		lowMass = result["lowMass%s"%combination] - result["lowMassOF"]*corr			
		lowMassErr = sqrt(result["lowMass%s"%combination] + (sqrt(result["lowMassOF"])*corr)**2 + (sqrt(result["lowMassOF"])*corr*corrErr)**2)
		highMass = result["highMass%s"%combination] - result["highMassOF"]*corr			
		highMassErr = sqrt(result["highMass%s"%combination] + (sqrt(result["highMassOF"])*corr)**2 + (sqrt(result["highMassOF"])*corr*corrErr)**2)			
		result["correctedPeak%s"%combination] = peak
		result["peakError%s"%combination] = peakErr
		result["correctedLowMass%s"%combination] = lowMass
		result["lowMassError%s"%combination] = lowMassErr
		result["correctedHighMass%s"%combination] = highMass
		result["highMassError%s"%combination] = highMassErr
		result["correction"] = 	corr
		result["correctionErr"] = 	corrErr
	
		rOutInLowMass =   lowMass / peak
		rOutInHighMass = highMass / peak
		rOutInLowMassSystErr = rOutInLowMass*0.25
		rOutInHighMassSystErr = rOutInHighMass*0.25
		rOutInLowMassErr = sqrt((lowMassErr/peak)**2 + (lowMass*peakErr/peak**2)**2)
		rOutInHighMassErr = sqrt((highMassErr/peak)**2 + (highMass*peakErr/peak**2)**2)

		result["rOutInLowMass%s"%combination] = rOutInLowMass
		result["rOutInLowMassErr%s"%combination] = rOutInLowMassErr
		result["rOutInLowMassSyst%s"%combination] = rOutInLowMassSystErr
		result["rOutInHighMass%s"%combination] = rOutInHighMass
		result["rOutInHighMassErr%s"%combination] = rOutInHighMassErr
		result["rOutInHighMassSyst%s"%combination] = rOutInHighMassSystErr

		if combination == "EE":
			plotMllSpectra(histEE.Clone(),histEM.Clone(),runRange,selection,combination,cmsExtra)
		elif combination == "MM":	
			plotMllSpectra(histMM.Clone(),histEM.Clone(),runRange,selection,combination,cmsExtra)
		else:	
			plotMllSpectra(histSF.Clone(),histEM.Clone(),runRange,selection,combination,cmsExtra)







	return result
def main():



	parser = argparse.ArgumentParser(description='R(out/in) measurements.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , nargs=1, default=["DrellYanControl"],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", nargs=1, default="Full2012",
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate R(out/in) central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")		
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	

					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = ["Rare","SingleTop","TTJets_SpinCorrelations","Diboson","DrellYanTauTau","DrellYan"]
	if len(args.plots) == 0:
		args.plots = ["nJetsPlotRMuE","nBJetsPlotRMuE","leadingPtPlotRMuE","trailigPtPlotRMuE","trailigPtPlotRMuELeading30","mllPlotRMuE","htPlotRMuE","metPlotRMuE","nVtxPlotRMuE","tralingEtaPlotRMuE","deltaRPlotRMuE"]
	
	runRange = getRunRange(args.runRange)
	
	
	selection = getRegion(args.selection[0])

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



	if args.central:
		centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,cmsExtra)
		if args.mc:
			outFilePkl = open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
		else:
			outFilePkl = open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"w")
		pickle.dump(centralVal, outFilePkl)
		outFilePkl.close()
		
	if args.dependencies:
		 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit)		
	

main()
