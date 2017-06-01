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
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics,  mllBins
import corrections



from locations import locations


def getHistograms(path,plot,runRange,isMC,backgrounds,region):

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
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		
		#~ histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		#~ histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		#~ histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.valMC)
		#~ histoMM.Scale(getattr(triggerEffs,region).effMM.valMC)	
		#~ histoEM.Scale(getattr(triggerEffs,region).effEM.valMC)				
		
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM


	
def plotMllSpectra(SFhist,EMuhist,runRange,selection,suffix,cmsExtra,additionalLabel):

		
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

	
	SFhist.SetMarkerStyle(20)
	SFhist.SetMarkerColor(ROOT.kBlack)
	
	#~ EMuhist.Draw("samehist")
	#~ SFhist.Draw("samepe")
	EMuhist.SetFillColor(855)
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)	
	legend.AddEntry(SFhist,"%s events"%suffix,"p")
	legend.AddEntry(EMuhist,"OF events","f")
	#~ legend.Draw("same")
	
	lines = {}
	massBins = ["mass20To60","mass60To86","onZ","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
	
	for mllBin in massBins:
		lines[mllBin] = ROOT.TLine(getattr(mllBins,mllBin).low,0,getattr(mllBins,mllBin).low,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		lines[mllBin].SetLineWidth(2)
		if mllBin == "onZ" or mllBin == "mass96To150":
			lines[mllBin].SetLineColor(ROOT.kRed+2)
		else:
			lines[mllBin].SetLineColor(ROOT.kBlack)
			
		lines[mllBin].Draw("same")


	Labelin = ROOT.TLatex()
	Labelin.SetTextAlign(12)
	Labelin.SetTextSize(0.025)
	Labelin.SetTextColor(ROOT.kRed+2)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.025)
	Labelout.SetTextColor(ROOT.kBlack)	
	
	
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
	
	
	hCanvas.Clear()
	
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	

	
	plotPad.DrawFrame(mllBins.mass20To60.low,0.1,500,SFhist.GetBinContent(SFhist.GetMaximumBin())*500,"; %s ; %s" %("m_{ll} [GeV]","Events / 5 GeV"))		
	
	plotPad.SetLogy()

	
	EMuhist.Draw("samehist")
	SFhist.Draw("samepe")
	legend.Draw("same")
	

	for mllBin in massBins:
		lines[mllBin].SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
		lines[mllBin].Draw("same")
		
	Labelin.SetTextAngle(90)
	Labelin.DrawLatex(91.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"on Z")
	Labelout.SetTextAngle(90)
	Labelout.DrawLatex(40.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"20-60 GeV")
	Labelout.DrawLatex(73.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"60-86 GeV")
	Labelout.DrawLatex(123.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"96-150 GeV")
	Labelout.DrawLatex(175.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"150-200 GeV")
	Labelout.DrawLatex(250.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"200-300 GeV")
	Labelout.DrawLatex(350.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"300-400 GeV")
	Labelout.DrawLatex(450.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"400+ GeV")
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.825	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra)) 	
	plotPad.RedrawAxis()
	if additionalLabel is not "":
		hCanvas.Print("fig/rOutIn_%s_%s_%s_%s.pdf"%(suffix,selection.name,runRange.label,additionalLabel))	
	else:
		hCanvas.Print("fig/rOutIn_%s_%s_%s.pdf"%(suffix,selection.name,runRange.label))	
	
	
def dependencies(path,selection,plots,runRange,mc,backgrounds,cmsExtra):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	legend = TLegend(0.6, 0.7, 0.9, 0.9)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)
	
	#~ massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","edgeMass","highMassOld","highMass","lowMass"]		
	massBins = ["edgeMass","highMassOld"]		
	
	for name in plots:
		print name
		hCanvas.Clear()
		
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	
		plot.cuts = plot.cuts.replace("mll","p4.M()")
		plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
		plot.cuts = plot.cuts.replace("MT2 > 80 &&","")
		plot.variable = plot.variable.replace("mll","p4.M()")
		if 	plot.variable == "pt":
			plot.variable = plot.variable.replace("pt","p4.Pt()")

		 
		if len(plot.binning) == 0:
			bins = [plot.firstBin+(plot.lastBin-plot.firstBin)/plot.nBins*i for i in range(plot.nBins+1)]
		else:
			bins = plot.binning
		print bins
		rOutIn = {}
		rOutInErr = {}
		rOutInMC = {}
		rOutInMCErr = {}
		for massBin in massBins:
			#~ rOutIn[massBin] ={"EE":[],"MM":[],"SF":[]}
			#~ rOutInErr[massBin] ={"EE":[],"MM":[],"SF":[]}
			rOutIn[massBin] ={"SF":[]}
			rOutInErr[massBin] ={"SF":[]}
			rOutInMC[massBin] ={"SF":[]}
			rOutInMCErr[massBin] ={"SF":[]}


		binningErrs	= []
		plotBinning = []
		for i in range(0,len(bins)-1):
			binningErrs.append((bins[i+1]-bins[i])/2)
			if i == 0:
				plotBinning.append((bins[i+1]-abs(bins[i]))/2)
			else:
				plotBinning.append(plotBinning[i-1]+(bins[i+1]-bins[i])/2+binningErrs[i-1])

			print plotBinning
			tmpCuts = selection.cut 
			cuts = selection.cut.split("&&")
			cutsUp = [] 
			cutsDown = [] 
			cutsEqual = []
			for cut in cuts:
				if "%s >"%plot.variable in cut:
					cutsUp.append(cut+ "&&")
				elif "%s <"%plot.variable in cut:
					cutsDown.append(cut+ "&&")
				elif "%s =="%plot.variable in cut:
					cutsEqual.append(cut+ "&&")
			for cut in cutsUp:
				selection.cut = selection.cut.replace(cut,"")		
			for cut in cutsDown:
				selection.cut = selection.cut.replace(cut,"")		
			for cut in cutsEqual:
				selection.cut = selection.cut.replace(cut,"")		
			
			selection.cut = selection.cut + " && %s > %f && %s < %f"%(plot.variable,bins[i],plot.variable,bins[i+1]) + " && %s"%runRange.runCut
			selection.cut.replace("&& &&","&&")
			print selection.cut
				
			additionalLabel = "%s_%.2f_%.2f"%(plot.variable,bins[i],bins[i+1])
			centralVal = centralValues(path,selection,runRange,False,backgrounds,cmsExtra,additionalLabel)
			centralValMC = centralValues(path,selection,runRange,True,backgrounds,cmsExtra,additionalLabel)
			
			
			outFilePkl = open("shelves/rOutIn_%s_%s_%s.pkl"%(selection.name,runRange.label,additionalLabel),"w")
			pickle.dump(centralVal, outFilePkl)
			outFilePkl.close()

			outFilePklMC = open("shelves/rOutIn_%s_%s_%s_MC.pkl"%(selection.name,runRange.label,additionalLabel),"w")
			pickle.dump(centralValMC, outFilePklMC)
			outFilePklMC.close()
				
			print additionalLabel
			##~ for combination in ["EE","MM","SF"]:
			for combination in ["SF"]:
				for region in massBins:
					if region in ["edgeMass","highMassOld"]:
						rOutIn[region][combination].append(centralVal["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
						rOutInErr[region][combination].append(centralVal["rOutIn_%s_NoMT2Cut_Err%s"%(region,combination)])
						rOutInMC[region][combination].append(centralValMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
						rOutInMCErr[region][combination].append(centralValMC["rOutIn_%s_NoMT2Cut_Err%s"%(region,combination)])
					else:
						rOutIn[region][combination].append(centralVal["rOutIn_%s_%s"%(region,combination)])
						rOutInErr[region][combination].append(centralVal["rOutIn_%s_Err%s"%(region,combination)])
						rOutInMC[region][combination].append(centralValMC["rOutIn_%s_%s"%(region,combination)])
						rOutInMCErr[region][combination].append(centralValMC["rOutIn_%s_Err%s"%(region,combination)])


			
			selection.cut = tmpCuts

								
		if os.path.isfile("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label)):
			centralVals = pickle.load(open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"rb"))
		else:
			centralVals = centralValues(path,selection,runRange,False,backgrounds,cmsExtra)	
		if os.path.isfile("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label)):
			centralValsMC = pickle.load(open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"rb"))
		else:
			centralValsMC = centralValues(path,selection,runRange,True,backgrounds,cmsExtra)		
		
		#~ for combination in ["EE","MM","SF"]:
		for combination in ["SF"]:
			
			for region in massBins:
				if region == "edgeMass" or region == "highMassOld":
					relSyst = systematics.rOutIn.old.val
					ymax = 0.25	
				elif region == "mass20To60":
					relSyst = systematics.rOutIn.massBelow150.val
					ymax = 0.25	
				elif region == "mass96To150" or region == "mass60To86":
					relSyst = systematics.rOutIn.massBelow150.val	
					ymax = 0.4
				elif region == "lowMass" or region == "highMass":
					relSyst = systematics.rOutIn.old.val	
					ymax = 0.4
				elif region == "mass150To200":
					relSyst = systematics.rOutIn.massAbove150.val
					ymax = 0.05
				else:
					relSyst = systematics.rOutIn.massAbove150.val
					ymax = 0.03
					
				hCanvas = TCanvas("hCanvas", "Distribution", 800,800)

				plotPad = TPad("plotPad","plotPad",0,0,1,1)
				
				style=setTDRStyle()
				style.SetTitleYOffset(1.3)
				style.SetPadLeftMargin(0.16)		
				plotPad.UseCurrentStyle()
				plotPad.Draw()	
				plotPad.cd()
				
				
		
				plotPad.DrawFrame(plot.firstBin,0.0,plot.lastBin,ymax,"; %s ; %s" %(plot.xaxis,"R_{out/in}"))		
				
				
				bandX = array("f",[plot.firstBin,plot.lastBin])
				if region in ["edgeMass","highMassOld"]:
					bandY = array("f",[centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]])
					bandYErr = array("f",[centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]*relSyst,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]*relSyst])
				else:
					bandY = array("f",[centralVals["rOutIn_%s_%s"%(region,combination)],centralVals["rOutIn_%s_%s"%(region,combination)]])
					bandYErr = array("f",[centralVals["rOutIn_%s_%s"%(region,combination)]*relSyst,centralVals["rOutIn_%s_%s"%(region,combination)]*relSyst])
				bandXErr = array("f",[0,0])
				
				
				errorband = ROOT.TGraphErrors(2,bandX,bandY,bandXErr,bandYErr)
				errorband.GetYaxis().SetRangeUser(0.0,0.15)
				errorband.GetXaxis().SetRangeUser(-5,105)
				errorband.Draw("3same")
				errorband.SetFillColor(ROOT.kOrange-9)
				if region in ["edgeMass","highMassOld"]:
					rOutInLine = ROOT.TLine(plot.firstBin,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],plot.lastBin,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
				else:
					rOutInLine = ROOT.TLine(plot.firstBin,centralVals["rOutIn_%s_%s"%(region,combination)],plot.lastBin,centralVals["rOutIn_%s_%s"%(region,combination)])
				rOutInLine.SetLineStyle(ROOT.kDashed)
				rOutInLine.SetLineWidth(2)
				rOutInLine.Draw("same")
				
				if region in ["edgeMass","highMassOld"]:
					rOutInLineMC = ROOT.TLine(plot.firstBin,centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],plot.lastBin,centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
				else:
					rOutInLineMC = ROOT.TLine(plot.firstBin,centralValsMC["rOutIn_%s_%s"%(region,combination)],plot.lastBin,centralValsMC["rOutIn_%s_%s"%(region,combination)])
				rOutInLineMC.SetLineStyle(ROOT.kDashed)
				rOutInLineMC.SetLineWidth(2)
				rOutInLineMC.SetLineColor(ROOT.kGreen-2)
				rOutInLineMC.Draw("same")

				
				
				
				binning = array("f",plotBinning)
				binningErrs = array("f",binningErrs)
				
				rOutInVals = array("f",rOutIn[region][combination])
				rOutInValsErrs = array("f",rOutInErr[region][combination])	
				graph = ROOT.TGraphErrors(len(binning),binning,rOutInVals,binningErrs,rOutInValsErrs)
				graph.Draw("Psame0")
				
				rOutInValsMC = array("f",rOutInMC[region][combination])
				rOutInValsMCErrs = array("f",rOutInMCErr[region][combination])	
				graphMC = ROOT.TGraphErrors(len(binning),binning,rOutInValsMC,binningErrs,rOutInValsMCErrs)
				graphMC.SetLineColor(ROOT.kGreen-2) 
				graphMC.SetMarkerColor(ROOT.kGreen-2) 
				graphMC.Draw("Psame0")
				
				legend.Clear()

				
				legend.AddEntry(graphMC,"R_{out,in} MC","p")
				legend.AddEntry(graph,"R_{out,in} Data","p")
				if region in ["edgeMass","highMassOld"]:
					legend.AddEntry(rOutInLine, "Mean R_{out,in} Data = %.3f"%centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],"l")
					legend.AddEntry(rOutInLineMC, "Mean R_{out,in} MC = %.3f"%centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],"l")
				else:
					legend.AddEntry(rOutInLine, "Mean R_{out,in} Data = %.3f"%centralVals["rOutIn_%s_%s"%(region,combination)],"l")
					legend.AddEntry(rOutInLineMC, "Mean R_{out,in} MC = %.3f"%centralValsMC["rOutIn_%s_%s"%(region,combination)],"l")
				legend.AddEntry(errorband, "Mean r_{out,in} Data #pm %d %%"%(relSyst*100),"f")
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
				
				latexLabel = ROOT.TLatex()
				latexLabel.SetTextSize(0.03)	
				latexLabel.SetNDC()
				
				if region == "edgeMass":
					latexLabel.DrawLatex(0.6, 0.5, "mass 20-70 GeV")
				if region == "highMassOld":
					latexLabel.DrawLatex(0.6, 0.5, "mass > 101 GeV")
				else:
					latexLabel.DrawLatex(0.6, 0.5, region)
					
				latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
				

				latexCMS.DrawLatex(0.19,0.89,"CMS")
				yLabelPos = 0.85	

				latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))		
					
				ROOT.gPad.RedrawAxis()
				hCanvas.Print("fig/rOutInSyst_%s_%s_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,region,combination,plot.additionalName))

	
	

	
	
def centralValues(path,selection,runRange,isMC,backgrounds,cmsExtra,additionalLabel=""):			
	
	massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","edgeMass","highMassOld","lowMassOld","highMass","lowMass"]
	
	if "Forward" in selection.name:
		region = "forward"
	elif "Central" in selection.name:
		region = "central"
	else:		
		region = "inclusive"		

	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut	
	plot.cuts = plot.cuts.replace("mll","p4.M()")
	plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
	if additionalLabel != "":
		plot.cuts = plot.cuts.replace("MT2 > 80 &&","")
	plot.variable = plot.variable.replace("mll","p4.M()")	
	if 	plot.variable == "pt":
		plot.variable = plot.variable.replace("pt","p4.Pt()")
		
	print plot.cuts

	plotNoMT2Cut = getPlot("mllPlotROutIn")
	plotNoMT2Cut.addRegion(selection)
	plotNoMT2Cut.cleanCuts()
	plotNoMT2Cut.cuts = plotNoMT2Cut.cuts % runRange.runCut	
	plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("mll","p4.M()")
	plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("pt > 25","p4.Pt() > 25")
	plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("MT2 > 80 &&","")
	plotNoMT2Cut.variable = plotNoMT2Cut.variable.replace("mll","p4.M()")
	if 	plotNoMT2Cut.variable == "pt":
		plotNoMT2Cut.variable = plotNoMT2Cut.variable.replace("pt","p4.Pt()")

	histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,backgrounds,region)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())
	
	histEENoMT2Cut, histMMNoMT2Cut, histEMNoMT2Cut = getHistograms(path,plotNoMT2Cut,runRange,isMC,backgrounds,region)
	histSFNoMT2Cut = histEENoMT2Cut.Clone("histSFNoMT2Cut")
	histSFNoMT2Cut.Add(histMMNoMT2Cut.Clone())
	
	result = {}
	
	peakLow = mllBins.onZ.low
	peakHigh = mllBins.onZ.high
	
	result["peak_EE"] = histEE.Integral(histEE.FindBin(peakLow+0.01),histEE.FindBin(peakHigh-0.01))
	result["peak_MM"] = histMM.Integral(histMM.FindBin(peakLow+0.01),histMM.FindBin(peakHigh-0.01))
	result["peak_SF"] = result["peak_EE"] + result["peak_MM"]
	result["peak_OF"] = histEM.Integral(histEM.FindBin(peakLow+0.01),histEM.FindBin(peakHigh-0.01))
	
	result["peak_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(peakLow+0.01),histEENoMT2Cut.FindBin(peakHigh-0.01))
	result["peak_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(peakLow+0.01),histMMNoMT2Cut.FindBin(peakHigh-0.01))
	result["peak_NoMT2Cut_SF"] = result["peak_NoMT2Cut_EE"] + result["peak_NoMT2Cut_MM"]
	result["peak_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(peakLow+0.01),histEMNoMT2Cut.FindBin(peakHigh-0.01))
	
	for massBin in massBins:
		lowerEdge = getattr(mllBins,massBin).low
		upperEdge = getattr(mllBins,massBin).high
		
		result[massBin+"_EE"] = histEE.Integral(histEE.FindBin(lowerEdge+0.01),histEE.FindBin(upperEdge-0.01))
		result[massBin+"_MM"] = histMM.Integral(histMM.FindBin(lowerEdge+0.01),histMM.FindBin(upperEdge-0.01))
		result[massBin+"_OF"] = histEM.Integral(histEM.FindBin(lowerEdge+0.01),histEM.FindBin(upperEdge-0.01))
		result[massBin+"_SF"] = result[massBin+"_EE"]+result[massBin+"_MM"]
		
		result[massBin+"_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(lowerEdge+0.01),histEENoMT2Cut.FindBin(upperEdge-0.01))
		result[massBin+"_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(lowerEdge+0.01),histMMNoMT2Cut.FindBin(upperEdge-0.01))
		result[massBin+"_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(lowerEdge+0.01),histEMNoMT2Cut.FindBin(upperEdge-0.01))
		result[massBin+"_NoMT2Cut_SF"] = result[massBin+"_NoMT2Cut_EE"]+result[massBin+"_NoMT2Cut_MM"]


	#~ for combination in ["EE","MM","SF"]:
	for combination in ["SF"]:
		if isMC:
			corr = getattr(corrections,"r%sOF"%combination).central.valMC
			corrErr = getattr(corrections,"r%sOF"%combination).central.errMC
		else:
			corr = getattr(corrections,"r%sOF"%combination).central.val
			corrErr = getattr(corrections,"r%sOF"%combination).central.err
		peak = result["peak_%s"%combination] - result["peak_OF"]*corr			
		#~ peakErr = sqrt(result["peak%s"%combination] + (sqrt(result["peakOF"])*corr)**2 + (sqrt(result["peakOF"])*corr*corrErr)**2)

		peakErr = sqrt(result["peak_%s"%combination] + result["peak_OF"]*corr**2 + (result["peak_OF"]*corrErr)**2)
		
		peakNoMT2Cut = result["peak_NoMT2Cut_%s"%combination] - result["peak_NoMT2Cut_OF"]*corr			
		peakNoMT2CutErr = sqrt(result["peak_NoMT2Cut_%s"%combination] + result["peak_NoMT2Cut_OF"]*corr**2 + (result["peak_NoMT2Cut_OF"]*corrErr)**2)
		
		result["corrected_peak_%s"%combination] = peak
		result["peak_Error%s"%combination] = peakErr
		
		result["corrected_peak_NoMT2Cut_%s"%combination] = peakNoMT2Cut
		result["peak_NoMT2Cut_Error%s"%combination] = peakNoMT2CutErr
		
		result["correction"] = 	corr
		result["correctionErr"] = 	corrErr

		for massBin in massBins:
			if massBin == "mass150To200" or massBin  == "mass200To300" or massBin  == "mass300To400" or massBin  == "mass400":
				relSyst = systematics.rOutIn.massAbove150.val		
			elif massBin == "mass20To60" or massBin  == "mass60To86" or massBin  == "mass96To150":
				relSyst = systematics.rOutIn.massBelow150.val
			else:
				relSyst = systematics.rOutIn.old.val
					
			corrYield =  result[massBin+"_"+combination] - result[massBin+"_"+"OF"]*corr			
			corrYieldErr = sqrt(result[massBin+"_"+combination] + result[massBin+"_OF"]*corr**2 + (result[massBin+"_OF"]*corrErr)**2)
			
			result["corrected_"+massBin+"_"+combination] = corrYield
			result[massBin+"_Error"+combination] = corrYieldErr
			
			corrYieldNoMT2Cut =  result[massBin+"_NoMT2Cut_"+combination] - result[massBin+"_NoMT2Cut_"+"OF"]*corr			
			corrYieldNoMT2CutErr = sqrt(result[massBin+"_NoMT2Cut_"+combination] + result[massBin+"_NoMT2Cut_OF"]*corr**2 + (result[massBin+"_NoMT2Cut_OF"]*corrErr)**2)
			
			result["corrected_"+massBin+"_NoMT2Cut_"+combination] = corrYieldNoMT2Cut
			result[massBin+"_NoMT2Cut_Error"+combination] = corrYieldNoMT2CutErr
			
	
			rOutIn = corrYield / peak
			rOutInSystErr = rOutIn * relSyst
			rOutInErr = sqrt( (corrYieldErr/peak)**2 + (corrYield*peakErr/peak**2)**2 )

			rOutInNoMT2Cut = corrYieldNoMT2Cut / peakNoMT2Cut
			rOutInNoMT2CutSystErr = rOutInNoMT2Cut * relSyst
			rOutInNoMT2CutErr = sqrt( (corrYieldNoMT2CutErr/peakNoMT2Cut)**2 + (corrYieldNoMT2Cut*peakNoMT2CutErr/peakNoMT2Cut**2)**2 )
			
			result["rOutIn_"+massBin+"_"+combination] = rOutIn
			result["rOutIn_"+massBin+"_"+"Err"+combination] = rOutInErr
			result["rOutIn_"+massBin+"_"+"Syst"+combination] = rOutInSystErr

			result["rOutIn_"+massBin+"_NoMT2Cut_"+combination] = rOutInNoMT2Cut
			result["rOutIn_"+massBin+"_NoMT2Cut_"+"Err"+combination] = rOutInNoMT2CutErr
			result["rOutIn_"+massBin+"_NoMT2Cut_"+"Syst"+combination] = rOutInNoMT2CutSystErr

		
		saveLabel = additionalLabel
		tmpLabel = additionalLabel
		if isMC:
			tmpLabel += "_MC"

		histEMToPlot = histEM.Clone()
		histEMToPlot.Scale(corr)
		additionalLabel = tmpLabel
		if combination == "EE":
			plotMllSpectra(histEE.Clone(),histEMToPlot,runRange,selection,combination,cmsExtra,additionalLabel)
		elif combination == "MM":	
			plotMllSpectra(histMM.Clone(),histEMToPlot,runRange,selection,combination,cmsExtra,additionalLabel)
		else:	
			plotMllSpectra(histSF.Clone(),histEMToPlot,runRange,selection,combination,cmsExtra,additionalLabel)
			

		additionalLabel = saveLabel
		




	return result
def main():



	parser = argparse.ArgumentParser(description='R(out/in) measurements.')
	
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
						  help="calculate R(out/in) central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")		
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.rOutIn
	if len(args.selection) == 0:
		#~ args.selection.append(regionsToUse.rOutIn.central.name)	
		#~ args.selection.append(regionsToUse.rOutIn.forward.name)	
		args.selection.append(regionsToUse.rOutIn.inclusive.name)	
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


			if args.central:
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,cmsExtra)
				if args.mc:
					outFilePkl = open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					outFilePkl = open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra)	
				 
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rOutIn_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves/rOutIn_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())				 					 	
	

main()
