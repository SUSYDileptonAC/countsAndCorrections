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

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, triggerEffs, rSFOFDirect
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations



def dependencies(source,modifier,path,selection,plots,runRange,isMC,nonNormalized,backgrounds,cmsExtra,fit,ptCut):
	pathMC = locations.dataSetPathMC
	if isMC:
		backgrounds = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
	#~ backgroundsTTbar = ["TT_Powheg"]
	backgroundsTTbar = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()
	
		plot.cuts = plot.cuts % runRange.runCut	
		
		#~ plot.cuts = plot.cuts.replace("p4.M()","mll")
		#~ plot.variable = plot.variable.replace("p4.M()","mll")
		plot.cuts = plot.cuts.replace("mll","p4.M()")
		plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
		plot.variable = plot.variable.replace("mll","p4.M()")
		#~ plot.cuts = plot.cuts.replace("p4.Pt()","pt")
		#~ plot.cuts = plot.cuts.replace("metFilterSummary > 0 &&","")
		#~ plot.cuts = plot.cuts.replace("genWeight*weight*","")
		#~ plot.cuts = plot.cuts.replace("weight*","")
		#~ plot.variable = plot.variable.replace("p4.Pt()","pt")
		
		if "Forward" in selection.name:
			label = "forward"
		elif "Central" in selection.name:
			label = "central"
		else:		
			label = "inclusive"
		
		if isMC:	
			if os.path.isfile("shelves/rSFOF_Control_%s_MC.pkl"%(runRange.label)):
				centralVals = pickle.load(open("shelves/rSFOF_Control_%s_MC.pkl"%(runRange.label),"rb"))
			else:
				centralVals = centralValues(source,modifier,path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra)
		else:	
			if os.path.isfile("shelves/rSFOF_Control_%s.pkl"%(runRange.label)):
				centralVals = pickle.load(open("shelves/rSFOF_Control_%s.pkl"%(runRange.label),"rb"))
			else:
				centralVals = centralValues(source,modifier,path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra)
	
		if os.path.isfile("shelves/rSFOF_Control_%s_MC.pkl"%(runRange.label)):
			centralValsTTbar = pickle.load(open("shelves/rSFOF_Control_%s_MC.pkl"%(runRange.label),"rb"))
		else:
			centralValsTTbar = centralValues(source,modifier,path,selection,runRange,True,nonNormalized,backgroundsTTbar,cmsExtra)

		print plot.cuts
		histEE, histMM, histEM = getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized, backgrounds,label)
		histRSFOF = histEE.Clone("histRSFOF")
		histRSFOF.Add(histMM.Clone())
		histRSFOF.Divide(histEM)				
		histEE.Divide(histEM)				
		histMM.Divide(histEM)
		
		histEETTbar, histMMTTbar, histEMTTbar = getHistograms(path,source,modifier,plot,runRange,True,nonNormalized, backgroundsTTbar,label)				
		histRSFOFTTbar = histEETTbar.Clone("histRSFOFTTbar")
		histRSFOFTTbar.Add(histMMTTbar.Clone())
		histRSFOFTTbar.Divide(histEMTTbar)				
		histEETTbar.Divide(histEMTTbar)				
		histMMTTbar.Divide(histEMTTbar)				
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		plotPad.UseCurrentStyle()		
		plotPad.Draw()	
		plotPad.cd()	
					
	
		plotPad.DrawFrame(plot.firstBin,0.8,plot.lastBin,1.8,"; %s ; %s" %(plot.xaxis,"SF/OF"))
		gStyle.SetErrorX(0.5)
		
		
		from ROOT import TH1F,kWhite
			


		zeroLine = ROOT.TLine(plot.firstBin, 1., plot.lastBin , 1.)
		zeroLine.SetLineWidth(1)
		zeroLine.SetLineColor(ROOT.kBlack)
		zeroLine.SetLineStyle(2)
		zeroLine.Draw("same")
		
		
		if isMC:
			err = rSFOFDirect.inclusive.errMC
		else:
			err = rSFOFDirect.inclusive.err
			
		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [centralVals["rSFOF"],centralVals["rSFOF"]]) 
		#~ y= array("f", [centralValsTTbar["rSFOF"],centralValsTTbar["rSFOF"]]) 
		ex= array("f", [0.,0.])
		ey= array("f", [err,err])
						
		ge= ROOT.TGraphErrors(2, x, y, ex, ey)
		ge.SetFillColor(ROOT.kOrange-9)
		ge.SetFillStyle(1001)
		ge.SetLineColor(ROOT.kWhite)
		ge.Draw("SAME 3")		
		
		rsfofLine= ROOT.TF1("rsfofline","%f"%centralVals["rSFOF"],plot.firstBin,plot.lastBin)
		rsfofLine.SetLineColor(ROOT.kOrange+3)
		rsfofLine.SetLineWidth(3)
		rsfofLine.SetLineStyle(2)
		rsfofLine.Draw("SAME")
		
		rsfofLineTTbar= ROOT.TF1("rsfoflineTTbar","%f"%centralValsTTbar["rSFOF"],plot.firstBin,plot.lastBin)
		#~ rsfofLineTTbar.SetLineColor(ROOT.kGreen-2)
		rsfofLineTTbar.SetLineColor(ROOT.kBlack)
		rsfofLineTTbar.SetLineWidth(3)
		rsfofLineTTbar.SetLineStyle(2)
		rsfofLineTTbar.Draw("SAME")
		
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.4,0.55,0.92,0.92)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")
		#~ if isMC:
			#~ legend.AddEntry(histRSFOF, "All MC", "p")
		if not isMC:
			legend.AddEntry(histRSFOF, "Data", "p")
		
		legend.AddEntry(histRSFOFTTbar,"MC","p")
		#~ if isMC:
			#~ legend.AddEntry(rsfofLine, "R_{SF/OF} centr. val. contr. region: All MC", "l")
		if not isMC:
			legend.AddEntry(rsfofLine, "R_{SF/OF} centr. val. contr. region", "l")
		legend.AddEntry(rsfofLineTTbar, "R_{SF/OF} centr. val. contr. region: MC", "l")
		legend.AddEntry(ge,"syst. unc. of R_{SF/OF}","f")
		
		
		
		histRSFOF.SetLineColor(ROOT.kBlack)
		histRSFOF.SetMarkerColor(ROOT.kBlack)
		histRSFOF.SetMarkerStyle(20)
		if not isMC:
			histRSFOF.Draw("hist E1P SAME")
		
		histRSFOFTTbar.SetMarkerStyle(21)
		#~ histRSFOFTTbar.SetLineColor(ROOT.kGreen-2) 
		#~ histRSFOFTTbar.SetMarkerColor(ROOT.kGreen-2)
		histRSFOFTTbar.SetLineColor(ROOT.kBlack) 
		histRSFOFTTbar.SetMarkerColor(ROOT.kBlack)
		
		histRSFOFTTbar.Draw("hist E1P SAME") 
		
		legend.Draw("same")

		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
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
		#latexCMSExtra.SetTextAlign(31)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)	
		latexLumi.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra and "Private Work" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	


		if fit:
			fit = TF1("dataFit","pol1",0,300)
			fit.SetLineColor(ROOT.kBlack)
			histRSFOF.Fit("dataFit")		
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)	
			latex.SetNDC()	
			latex.DrawLatex(0.2, 0.25, "Fit: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))


		ROOT.gPad.RedrawAxis()
		hCanvas.Update()
		
		if isMC:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	




def getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized,backgrounds,region=""):

	treesEE = readTrees(path,"EE",source = source,modifier= modifier)
	treesEM = readTrees(path,"EMu",source = source,modifier= modifier)
	treesMM = readTrees(path,"MuMu",source = source,modifier= modifier)
		
	
	
	if isMC:
		#~ print path, source, modifier
		eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)	
		processes = []
		for background in backgrounds:
			if nonNormalized:
				processes.append(Process(getattr(Backgrounds,background),eventCounts,normalized=False))
			else:
				processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,useTriggerEmulation=True,).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,useTriggerEmulation=True).theHistogram
		#~ 
		#~ histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		#~ histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		#~ histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram
						#~ 
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val/getattr(triggerEffs,region).effEE.valMC)
		#~ histoMM.Scale(getattr(triggerEffs,region).effMM.val/getattr(triggerEffs,region).effMM.valMC)	
		#~ histoEM.Scale(getattr(triggerEffs,region).effEM.val/getattr(triggerEffs,region).effEM.valMC)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
	

	

def centralValues(source,modifier,path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra):


	#~ plot = getPlot("mllPlotRSFOFCentralVal")
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	plot.cleanCuts()

	plot.cuts = plot.cuts % runRange.runCut
	#~ plot.cuts = plot.cuts.replace("p4.M()","mll")
	#~ plot.variable = plot.variable.replace("p4.M()","mll")
	#~ plot.cuts = plot.cuts.replace("p4.Pt()","pt")
	#~ plot.cuts = plot.cuts.replace("metFilterSummary > 0 &&","")
	#~ plot.cuts = plot.cuts.replace("triggerSummary > 0 &&","")
	#~ plot.cuts = plot.cuts.replace("genWeight*weight*","")
	#~ plot.cuts = plot.cuts.replace("weight*","")
	#~ plot.variable = plot.variable.replace("p4.Pt()","pt")	
	
	plot.cuts = plot.cuts.replace("mll","p4.M()")
	plot.variable = plot.variable.replace("mll","p4.M()")
	plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
	#~ plot.variable = plot.variable.replace("pt","p4.Pt()")	

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
	#~ plotSignal.cuts = plotSignal.cuts.replace("p4.M()","mll")
	#~ plotSignal.variable = plotSignal.variable.replace("p4.M()","mll")	
	#~ plotSignal.cuts = plotSignal.cuts.replace("p4.Pt()","pt")
	#~ plotSignal.cuts = plotSignal.cuts.replace("metFilterSummary > 0 &&","")
	#~ plotSignal.cuts = plotSignal.cuts.replace("triggerSummary > 0 &&","")
	#~ plotSignal.cuts = plot.cuts.replace("genWeight*weight*","")
	#~ plotSignal.cuts = plot.cuts.replace("weight*","")
	#~ plotSignal.variable = plotSignal.variable.replace("p4.Pt()","pt")
	
	plotSignal.cuts = plotSignal.cuts.replace("mll","p4.M()")
	plotSignal.variable = plotSignal.variable.replace("mll","p4.M()")
	plotSignal.variable = plotSignal.variable.replace("pt > 25","p4.Pt() > 25")	

	
	tempCut = plot.cuts
	#~ plot.cuts = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && (mll>20 && mll < 70)")
	plot.cuts = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && (p4.M()>20 && p4.M() < 70)")
	
	#~ print plot.cuts

	histEELow, histMMLow, histEMLow = getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized,backgrounds,label)
	histSFLow = histEELow.Clone("histSFLow")
	histSFLow.Add(histMMLow.Clone())
	
	plot.cuts = tempCut
	#~ plot.cuts = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && mll>110")
	plot.cuts = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && p4.M()>110")
	#~ plot.cuts = plot.cuts+"&& (mll>110)"
	
	histEEHigh, histMMHigh, histEMHigh = getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized,backgrounds,label)
	histSFHigh = histEEHigh.Clone("histSFHigh")
	histSFHigh.Add(histMMHigh.Clone())
	
	plot.cuts = tempCut

	if isMC:
		tempCut = plotSignal.cuts
		
		#~ plotSignal.cuts = plotSignal.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && (mll>20 && mll < 70)")
		plotSignal.cuts = plotSignal.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && (p4.M()>20 && p4.M() < 70)")
		histEESignalLow, histMMSignalLow, histEMSignalLow = getHistograms(path,source,modifier,plotSignal,runRange,isMC,nonNormalized,backgrounds,label)
		histSFSignalLow = histEESignalLow.Clone("histSFSignalLow")
		histSFSignalLow.Add(histMMSignalLow.Clone())
		
		plotSignal.cuts = tempCut
		#~ plotSignal.cuts = plotSignal.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && mll>110")
		plotSignal.cuts = plotSignal.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && p4.M()>110")
		histEESignalHigh, histMMSignalHigh, histEMSignalHigh = getHistograms(path,source,modifier,plotSignal,runRange,isMC,nonNormalized,backgrounds,label)
		histSFSignalHigh = histEESignalHigh.Clone("histSFSignalHigh")
		histSFSignalHigh.Add(histMMSignalHigh.Clone())
		
		plotSignal.cuts = tempCut
	
	result = {}
			

	eeLowMassErr = ROOT.Double()
	#~ eeLowMass = histEELow.IntegralAndError(plot.firstBin,plot.lastBin,eeLowMassErr)
	eeLowMass = histEELow.IntegralAndError(histEELow.GetXaxis().FindBin(plot.firstBin),histEELow.GetXaxis().FindBin(plot.lastBin)-1,eeLowMassErr)
	eeHighMassErr = ROOT.Double()
	eeHighMass = histEEHigh.IntegralAndError(histEEHigh.GetXaxis().FindBin(plot.firstBin),histEEHigh.GetXaxis().FindBin(plot.lastBin)-1,eeHighMassErr)
	
	ee = eeLowMass + eeHighMass
	eeErr = (eeLowMassErr**2 + eeHighMassErr**2)**0.5
	
	mmLowMassErr = ROOT.Double()
	mmLowMass = histMMLow.IntegralAndError(histMMLow.GetXaxis().FindBin(plot.firstBin),histMMLow.GetXaxis().FindBin(plot.lastBin)-1,mmLowMassErr)
	mmHighMassErr = ROOT.Double()
	mmHighMass = histMMHigh.IntegralAndError(histMMHigh.GetXaxis().FindBin(plot.firstBin),histMMHigh.GetXaxis().FindBin(plot.lastBin)-1,mmHighMassErr)
	
	mm = mmLowMass + mmHighMass
	mmErr = (mmLowMassErr**2 + mmHighMassErr**2)**0.5
	
	ofLowMassErr = ROOT.Double()
	ofLowMass = histEMLow.IntegralAndError(histEMLow.GetXaxis().FindBin(plot.firstBin),histEMLow.GetXaxis().FindBin(plot.lastBin)-1,ofLowMassErr)
	ofHighMassErr = ROOT.Double()
	ofHighMass = histEMHigh.IntegralAndError(histEMHigh.GetXaxis().FindBin(plot.firstBin),histEMHigh.GetXaxis().FindBin(plot.lastBin)-1,ofHighMassErr)
	
	of = ofLowMass + ofHighMass
	ofErr = (ofLowMassErr**2 + ofHighMassErr**2)**0.5

	
	sf = ee + mm 
	sfLowMass = eeLowMass + mmLowMass 
	sfHighMass = eeHighMass + mmHighMass 
	sfErr = (eeErr**2 + mmErr**2)**0.5
	sfLowMassErr = (eeLowMassErr**2 + mmLowMassErr**2)**0.5
	sfHighMassErr = (eeHighMassErr**2 + mmHighMassErr**2)**0.5	
	
	print sf
	
	rsfof = float(sf)/float(of)
	rsfofErr = rsfof*(sfErr**2/sf**2+ofErr**2/of**2)**0.5
	rsfofLowMass = float(sfLowMass)/float(ofLowMass)
	rsfofLowMassErr = rsfofLowMass*(sfLowMassErr**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	rsfofHighMass = float(sfHighMass)/float(ofHighMass)
	rsfofHighMassErr = rsfofHighMass*(sfHighMassErr**2/sf**2+ofHighMassErr**2/of**2)**0.5
	
	
	rEEOF = float(ee)/float(of)
	if ee > 0 and of > 0:
		rEEOFErr = rEEOF * (eeErr**2/ee**2 + ofErr**2/of**2)**0.5
	else:
		rEEOFErr = 0
	rEEOFLowMass = float(eeLowMass)/float(ofLowMass)
	if eeLowMass > 0 and ofLowMass > 0:
		rEEOFLowMassErr = rEEOFLowMass * (eeLowMassErr**2/eeLowMass**2 + ofLowMassErr**2/ofLowMass**2)**0.5
	else:
		rEEOFLowMassErr = 0
	rEEOFHighMass = float(eeHighMass)/float(ofHighMass)
	if eeHighMass > 0 and ofHighMass > 0:
		rEEOFHighMassErr = rEEOFHighMass * (eeHighMassErr**2/eeHighMass**2 + ofHighMassErr**2/ofHighMass**2)**0.5
	else:
		rEEOFHighMassErr = 0	
	
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
		
	result["rSFOF"] = rsfof
	result["rSFOFErr"] = rsfofErr
	result["rEEOF"] = rEEOF
	result["rEEOFErr"] = rEEOFErr
	result["rMMOF"] = rMMOF
	result["rMMOFErr"] = rMMOFErr	

	
	if isMC:
		
		
		eeLowMassErrSignal = ROOT.Double()
		eeLowMassSignal = histEESignalLow.IntegralAndError(histEESignalLow.GetXaxis().FindBin(plotSignal.firstBin),histEESignalLow.GetXaxis().FindBin(plotSignal.lastBin)-1,eeLowMassErr)
		eeHighMassErrSignal = ROOT.Double()
		eeHighMassSignal = histEESignalHigh.IntegralAndError(histEESignalHigh.GetXaxis().FindBin(plotSignal.firstBin),histEESignalHigh.GetXaxis().FindBin(plotSignal.lastBin)-1,eeHighMassErr)
		
		eeSignal = eeLowMassSignal + eeHighMassSignal
		eeErrSignal = (eeLowMassErrSignal**2 + eeHighMassErrSignal**2)**0.5
		
		mmLowMassErrSignal = ROOT.Double()
		mmLowMassSignal = histMMSignalLow.IntegralAndError(histMMSignalLow.GetXaxis().FindBin(plotSignal.firstBin),histMMSignalLow.GetXaxis().FindBin(plotSignal.lastBin)-1,mmLowMassErr)
		mmHighMassErrSignal = ROOT.Double()
		mmHighMassSignal = histMMSignalHigh.IntegralAndError(histMMSignalHigh.GetXaxis().FindBin(plotSignal.firstBin),histMMSignalHigh.GetXaxis().FindBin(plotSignal.lastBin)-1,mmHighMassErr)
		
		mmSignal = mmLowMassSignal + mmHighMassSignal
		mmErrSignal = (mmLowMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
		
		ofLowMassErrSignal = ROOT.Double()
		ofLowMassSignal = histEMSignalLow.IntegralAndError(histEMSignalLow.GetXaxis().FindBin(plotSignal.firstBin),histEMSignalLow.GetXaxis().FindBin(plotSignal.lastBin)-1,ofLowMassErr)
		ofHighMassErrSignal = ROOT.Double()
		ofHighMassSignal = histEMSignalHigh.IntegralAndError(histEMSignalHigh.GetXaxis().FindBin(plotSignal.firstBin),histEMSignalHigh.GetXaxis().FindBin(plotSignal.lastBin)-1,ofHighMassErr)
		
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
		if sfLowMassSignal > 0 and ofLowMassSignal > 0:
			rsfofLowMassErrSignal = rsfofLowMassSignal*(sfLowMassErrSignal**2/sfLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			rsfofLowMassErrSignal = 0
		rsfofHighMassSignal = float(sfHighMassSignal)/float(ofHighMassSignal)
		rsfofHighMassErrSignal = rsfofHighMassSignal*(sfHighMassErrSignal**2/sfHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		
		rEEOFSignal = float(eeSignal)/float(ofSignal)
		rEEOFErrSignal = rEEOFSignal * (eeErrSignal**2/eeSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
		rEEOFLowMassSignal = float(eeLowMassSignal)/float(ofLowMassSignal)
		if eeLowMassSignal > 0 and ofLowMassSignal > 0:
			rEEOFLowMassErrSignal = rEEOFLowMassSignal * (eeLowMassErrSignal**2/eeLowMassSignal**2 + ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			rEEOFLowMassErrSignal = 0
		rEEOFHighMassSignal = float(eeHighMassSignal)/float(ofHighMassSignal)
		rEEOFHighMassErrSignal = rEEOFHighMassSignal * (eeHighMassErrSignal**2/eeHighMassSignal**2 + ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
	
		rMMOFSignal = float(mmSignal)/float(ofSignal)
		rMMOFErrSignal = rMMOFSignal * (mmErrSignal**2/mmSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
		rMMOFLowMassSignal = float(mmLowMassSignal)/float(ofLowMassSignal)
		if mmLowMassSignal > 0 and ofLowMassSignal > 0:
			rMMOFLowMassErrSignal = rMMOFLowMassSignal * (mmLowMassErrSignal**2/mmLowMassSignal**2 + ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			rMMOFLowMassErrSignal = 0
		rMMOFHighMassSignal = float(mmHighMassSignal)/float(ofHighMassSignal)
		rMMOFHighMassErrSignal = rMMOFHighMassSignal * (mmHighMassErrSignal**2/mmHighMassSignal**2 + ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5	
		
		transferFaktor = rsfofSignal/rsfof
		transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
		if rEEOF > 0:
			transferFaktorEE = rEEOFSignal/rEEOF
		else:
			transferFaktorEE = 0
		if rEEOF > 0 and rEEOFSignal > 0:
			transferFaktorEEErr = transferFaktorEE*((rEEOFErr/rEEOF)**2+(rEEOFErrSignal/rEEOFSignal)**2)**0.5
		else:
			transferFaktorEEErr = 0
		transferFaktorMM = rMMOFSignal/rMMOF
		transferFaktorMMErr = transferFaktorMM*((rMMOFErr/rMMOF)**2+(rMMOFErrSignal/rMMOFSignal)**2)**0.5
		
		transferFaktorLowMass = rsfofLowMassSignal/rsfofLowMass
		if rsfofLowMass > 0 and rsfofLowMassSignal > 0:
			transferFaktorLowMassErr = transferFaktorLowMass*((rsfofLowMassErr/rsfofLowMass)**2+(rsfofLowMassErrSignal/rsfofLowMassSignal)**2)**0.5
		else:
			transferFaktorLowMassErr = 0
		if rEEOFLowMass > 0:
			transferFaktorEELowMass = rEEOFLowMassSignal/rEEOFLowMass
		else:
			transferFaktorEELowMass = 0
		if rEEOFLowMass > 0 and rEEOFLowMassSignal > 0:
			transferFaktorEELowMassErr = transferFaktorEELowMass*((rEEOFLowMassErr/rEEOFLowMass)**2+(rEEOFLowMassErrSignal/rEEOFLowMassSignal)**2)**0.5
		else:
			transferFaktorEELowMassErr = 0
		transferFaktorMMLowMass = rMMOFLowMassSignal/rMMOFLowMass
		if rMMOFLowMass > 0 and rMMOFLowMassSignal > 0:
			transferFaktorMMLowMassErr = transferFaktorMMLowMass*((rMMOFLowMassErr/rMMOFLowMass)**2+(rMMOFLowMassErrSignal/rMMOFLowMassSignal)**2)**0.5
		else:
			transferFaktorMMLowMassErr = 0
		
		transferFaktorHighMass = rsfofHighMassSignal/rsfofHighMass
		transferFaktorHighMassErr = transferFaktorHighMass*((rsfofHighMassErr/rsfofHighMass)**2+(rsfofHighMassErrSignal/rsfofHighMassSignal)**2)**0.5
		if rEEOFHighMass > 0:
			transferFaktorEEHighMass = rEEOFHighMassSignal/rEEOFHighMass
		else:
			transferFaktorEEHighMass = 0
		if rEEOFHighMass > 0 and rEEOFHighMassSignal > 0:
			transferFaktorEEHighMassErr = transferFaktorEEHighMass*((rEEOFHighMassErr/rEEOFHighMass)**2+(rEEOFHighMassErrSignal/rEEOFHighMassSignal)**2)**0.5
		else:
			transferFaktorEEHighMassErr = 0
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
		
		result["rSFOFLowMassSignal"] = sfLowMassSignal / ofLowMassSignal
		if sfLowMassSignal > 0 and ofLowMassSignal > 0:
			result["rSFOFErrLowMassSignal"] = result["rSFOFLowMassSignal"]*(sfLowMassErrSignal**2/sfLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			result["rSFOFErrLowMassSignal"] = 0
		result["rEEOFLowMassSignal"] = eeLowMassSignal / ofLowMassSignal
		if eeLowMassSignal > 0 and ofLowMassSignal > 0:
			result["rEEOFErrLowMassSignal"] =  result["rEEOFLowMassSignal"]*(eeLowMassErrSignal**2/eeLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			result["rEEOFErrLowMassSignal"] = 0
		result["rMMOFLowMassSignal"] = mmLowMassSignal / ofLowMassSignal
		if mmLowMassSignal > 0 and ofLowMassSignal > 0:
			result["rMMOFErrLowMassSignal"] =  result["rMMOFLowMassSignal"]*(mmLowMassErrSignal**2/mmLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
		else:
			result["rMMOFErrLowMassSignal"] = 0
			
		result["rSFOFHighMassSignal"] = sfHighMassSignal / ofHighMassSignal
		result["rSFOFErrHighMassSignal"] = result["rSFOFHighMassSignal"]*(sfHighMassErrSignal**2/sfHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		result["rEEOFHighMassSignal"] = eeHighMassSignal / ofHighMassSignal
		result["rEEOFErrHighMassSignal"] =  result["rEEOFHighMassSignal"]*(eeHighMassErrSignal**2/eeHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		result["rMMOFHighMassSignal"] = mmHighMassSignal / ofHighMassSignal
		result["rMMOFErrHighMassSignal"] =  result["rMMOFHighMassSignal"]*(mmHighMassErrSignal**2/mmHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
		
		result["rSFOFSignal"] = rsfofSignal
		result["rSFOFErrSignal"] = rsfofErrSignal
		result["rEEOFSignal"] = rEEOFSignal
		result["rEEOFErrSignal"] = rEEOFErrSignal
		result["rMMOFSignal"] = rMMOFSignal
		result["rMMOFErrSignal"] = rMMOFErrSignal
		
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
	parser.add_argument("-f", "--fit", action="store_true", dest="fit", default= False,
						  help="do dependecy fit")	
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
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
		#~ args.selection.append(regionsToUse.rSFOF.central.name)	
		#~ args.selection.append(regionsToUse.rSFOF.forward.name)	
		args.selection.append(regionsToUse.rSFOF.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	if args.mc:
		#~ path = locations.dataSetPathNLL
		path = locations.dataSetPath
	else:
		#~ path = locations.dataSetPathNLL
		path = locations.dataSetPath
	
	if args.dilepton:
		source = "DiLeptonTrigger"
		modifier = "DiLeptonTrigger"
	else:
		source = ""		
		modifier = ""	
		


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
				
				centralVal = centralValues(source,modifier,path,selection,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra)
				if args.mc:
					outFilePkl = open("shelves/rSFOF_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					outFilePkl = open("shelves/rSFOF_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(source,modifier,path,selection,args.plots,runRange,args.mc,args.nonNormalized,args.backgrounds,cmsExtra,args.fit,args.ptCut)		
				
				
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rSFOF_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves/rSFOF_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())					
main()
