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


def illustration(name):
	
	if "Forward" in name:
		label = "forward"
	else:
		if "Central" in name:
			label = "central"
		else:
			label = "inclusive"
	
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style = setTDRStyle()
	plotPad.UseCurrentStyle()		
	plotPad.Draw()	
	plotPad.cd()	
	hCanvas.DrawFrame(0,0,3,2,"; %s ; %s" %("r_{#mu e}","R_{SF/OF}"))	

	legend = TLegend(0.55, 0.18, 0.9, 0.525)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)


	x= array("f",[getattr(rMuE,label).val-getattr(rMuE,label).err, getattr(rMuE,label).val+getattr(rMuE,label).err]) 
   	y= array("f",[1.,1.])
   	ey= array("f",[1, 1])
   	ex= array("f",[0,0])
   	ge= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge.SetFillColor(ROOT.kGreen+3)
   	ge.SetLineColor(ROOT.kGreen+3)
   	ge.SetFillStyle(3001)
   	ge.Draw("SAME 3")	
	x= array("f",[0, 3]) 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	#~ y= array([rMuEs[region], rMuEs[region]],"f") # 1.237
   	y= array("f",[getattr(rSFOFFact,label).SF.val,getattr(rSFOFFact,label).SF.val])
   	ey= array("f",[getattr(rSFOFFact,label).SF.err, getattr(rSFOFFact,label).SF.err])
   	ex= array("f",[0.0,0.0])
   	ge2= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge2.SetFillColor(ROOT.kBlue-3)
   	ge2.SetLineColor(ROOT.kBlue-3)
   	ge2.SetFillStyle(3002)
   	ge2.Draw("SAME 3")	
	
	
	#~ print 0.5*((1+getattr(rMuE,label).val-1)+ 1./(1+getattr(rMuE,label).val-1))*getattr(rSFOFTrig,label).val
	#~ print getattr(rSFOFFact,label).SF.val
	#~ print 0.5*((getattr(rMuE,label).val-0.183218)+1./(getattr(rMuE,label).val-0.183218))*1.084055
	#~ print "0.5*((x-%f)+1./(x-%f))*%f"%(getattr(rMuE,label).val-1,getattr(rMuE,label).val-1,getattr(rSFOFTrig,label).val)
	#~ rSFOFLine = TF1("rSFOF%s"%label,"0.5*((x-%f)+1./(x-%f))*%f"%(getattr(rMuE,label).val-1,getattr(rMuE,label).val-1,getattr(rSFOFTrig,label).val),0.,3.)
	rSFOFLine = TF1("rSFOF%s"%label,"0.5*((x)+1./(x))*%f"%(getattr(rSFOFTrig,label).val),0.,3.)
	rSFOFLine.SetLineColor(ROOT.kRed)
	rSFOFLine.SetLineWidth(2)
	#~ rSFOFTrigUp = TF1("rSFOFUp%s"%label,"0.5*((x-%f)+1./(x-%f))*%f"%(getattr(rMuE,label).val-1,getattr(rMuE,label).val-1,getattr(rSFOFTrig,label).val+getattr(rSFOFTrig,label).err),0.,3.)
	rSFOFTrigUp = TF1("rSFOFUp%s"%label,"0.5*((x)+1./(x))*%f"%(getattr(rSFOFTrig,label).val+getattr(rSFOFTrig,label).err),0.,3.)
	rSFOFTrigUp.SetLineColor(ROOT.kBlack)
	rSFOFTrigUp.SetLineWidth(2)
	rSFOFTrigUp.SetLineStyle(ROOT.kDashed)
	#~ rSFOFTrigDown = TF1("rSFOFDown%s"%label,"0.5*((x-%f)+1./(x-%f))*%f"%(getattr(rMuE,label).val-1,getattr(rMuE,label).val-1,getattr(rSFOFTrig,label).val-getattr(rSFOFTrig,label).err),0.,3.)
	rSFOFTrigDown = TF1("rSFOFDown%s"%label,"0.5*((x)+1./(x))*%f"%(getattr(rSFOFTrig,label).val-getattr(rSFOFTrig,label).err),0.,3.)
	rSFOFTrigDown.SetLineColor(ROOT.kBlack)
	rSFOFTrigDown.SetLineWidth(2)
	rSFOFTrigDown.SetLineStyle(ROOT.kDashed)
	
	rmueline= ROOT.TF1("rmueline","%s"%getattr(rSFOFFact,label).SF.val,0, 3)
	rmueline.SetLineColor(ROOT.kBlue)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME") 

	line1 = ROOT.TLine(getattr(rMuE,label).val,0,getattr(rMuE,label).val,2)
	line1.Draw("Same")
	line1.SetLineWidth(2)
	line1.SetLineColor(ROOT.kGreen+3)
	legendHistDing = ROOT.TH1F()
	legendHistDing.SetFillColor(ROOT.kWhite)
	legend.AddEntry(legendHistDing,"Factorization method:","h")
	legend.AddEntry(rSFOFLine,"R_{SF/OF} (r_{#mu e})","l")
	legend.AddEntry(rSFOFTrigDown,"R_{SF/OF} (r_{#mu e}) #pm 1 #sigma on R_{T} ","l")
	legend.AddEntry(ge,"measured r_{#mu e} #pm 1 #sigma","fl")
	legend.AddEntry(ge2,"measured R_{SF/OF} #pm 1 #sigma","fl")
	
	legend.Draw("SAME")
	
	rSFOFLine.Draw("SAME")
	rSFOFTrigUp.Draw("SAME")
	rSFOFTrigDown.Draw("SAME")
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "%s dilepton selection"%label.title())	  	

	
	hCanvas.Print("fig/rMuEPropaganda_%s.pdf"%label)




def dependencies(source,modifier,path,selection,plots,runRange,isMC,nonNormalized,backgrounds,cmsExtra,fit,ptCut):
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

		if "Forward" in selection.name:
			label = "forward"
		elif "Central" in selection.name:
			label = "central"
		else:		
			label = "inclusive"


		histEE, histMM, histEM = getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized, backgrounds,label)
		histRSFOF = histEE.Clone("histRSFOF")
		histRSFOF.Add(histMM.Clone())
		histRSFOF.Divide(histEM)				
		histEE.Divide(histEM)				
		histMM.Divide(histEM)				
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,300)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		#~ style.SetTitleYOffset(0.70)
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
		histEE.SetLineColor(ROOT.kBlue)
		histEE.SetMarkerColor(ROOT.kBlue)
		histEE.SetMarkerStyle(20)
		#~ histEE.Draw("sameE0")
		histMM.SetLineColor(ROOT.kRed)
		histMM.SetMarkerColor(ROOT.kRed)
		histMM.SetMarkerStyle(20)
		#~ histMM.Draw("sameE0")


		#~ legend.AddEntry(histRSFOF,"R_{SF/OF}","pe")	
		#~ legend.AddEntry(histEE,"R_{EE/OF}","p")	
		#~ legend.AddEntry(histMM,"R_{MM/OF}","p")	


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
		#latexCMS.SetTextAlign(31)
		latexCMS.SetTextSize(0.12)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		#latexCMSExtra.SetTextAlign(31)
		latexCMSExtra.SetTextSize(0.1)
		latexCMSExtra.SetNDC(True)	
		latexLumi.DrawLatex(0.95, 0.91, "%s fb^{-1} (13 TeV)"%runRange.printval)
		#~ latexLumi.DrawLatex(0.95, 0.96, "(13 TeV)")
		
		#~ latex.DrawLatex(0.25, 0.2, pt_label)
		#~ latex.DrawLatex(0.25, 0.25, selection.latex)
		

		latexCMS.DrawLatex(0.12,0.76,"CMS")
		if "Simulation" in cmsExtra and "Private Work" in cmsExtra:
			yLabelPos = 0.635	
		else:
			yLabelPos = 0.68	

		latexCMSExtra.DrawLatex(0.12,yLabelPos,"%s"%(cmsExtra))	


		if fit:
			fit = TF1("dataFit","pol1",0,300)
			fit.SetLineColor(ROOT.kBlack)
			histRSFOF.Fit("dataFit")		
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)	
			latex.SetNDC()	
			latex.DrawLatex(0.2, 0.25, "Fit: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))


		
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
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram
						
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoEE.Scale(getattr(triggerEffs,region).effMM.val)	
		#~ histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
	

	

def centralValues(source,modifier,path,selection,runRange,isMC,nonNormalized,backgrounds,cmsExtra):


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


	histEE, histMM, histEM = getHistograms(path,source,modifier,plot,runRange,isMC,nonNormalized,backgrounds,label)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())

	histEESignal, histMMSignal, histEMSignal = getHistograms(path,source,modifier,plotSignal,runRange,isMC,nonNormalized,backgrounds,label)
	histSFSignal = histEESignal.Clone("histSFSignal")
	histSFSignal.Add(histMMSignal.Clone())
	result = {}
	

	lowMassLow = mllBins.lowMass.low
	lowMassHigh = mllBins.lowMass.high
	peakLow = mllBins.onZ.low
	peakHigh = mllBins.onZ.high
	highMassLow = mllBins.highMass.low
	highMassHigh = mllBins.highMass.high
		

	eeLowMassErr = ROOT.Double()
	eeLowMass = histEE.IntegralAndError(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01),eeLowMassErr)
	eeHighMassErr = ROOT.Double()
	eeHighMass = histEE.IntegralAndError(histEE.FindBin(highMassLow+0.01),histEE.FindBin(highMassHigh-0.01),eeHighMassErr)
	
	ee = eeLowMass + eeHighMass
	eeErr = (eeLowMassErr**2 + eeHighMassErr**2)**0.5
	
	mmLowMassErr = ROOT.Double()
	mmLowMass = histMM.IntegralAndError(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01),mmLowMassErr)
	mmHighMassErr = ROOT.Double()
	mmHighMass = histMM.IntegralAndError(histMM.FindBin(highMassLow+0.01),histMM.FindBin(highMassHigh-0.01),mmHighMassErr)
	
	mm = mmLowMass + mmHighMass
	mmErr = (mmLowMassErr**2 + mmHighMassErr**2)**0.5
	
	ofLowMassErr = ROOT.Double()
	ofLowMass = histEM.IntegralAndError(histEM.FindBin(lowMassLow+0.01),histEM.FindBin(lowMassHigh-0.01),ofLowMassErr)
	ofHighMassErr = ROOT.Double()
	ofHighMass = histEM.IntegralAndError(histEM.FindBin(highMassLow+0.01),histEM.FindBin(highMassHigh-0.01),ofHighMassErr)
	
	of = ofLowMass + ofHighMass
	ofErr = (ofLowMassErr**2 + ofHighMassErr**2)**0.5

	
	sf = ee + mm 
	sfLowMass = eeLowMass + mmLowMass 
	sfHighMass = eeHighMass + mmHighMass 
	sfErr = (eeErr**2 + mmErr**2)**0.5
	sfLowMassErr = (eeLowMassErr**2 + mmLowMassErr**2)**0.5
	sfHighMassErr = (eeHighMassErr**2 + mmHighMassErr**2)**0.5

	eeLowMassErrSignal = ROOT.Double()
	eeLowMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(lowMassLow+0.01),histEESignal.FindBin(lowMassHigh-0.01),eeLowMassErrSignal)
	eeHighMassErrSignal = ROOT.Double()
	eeHighMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(highMassLow+0.01),histEESignal.FindBin(highMassHigh-0.01),eeHighMassErrSignal)
	
	eeSignal = eeLowMassSignal + eeHighMassSignal
	eeErrSignal = (eeLowMassErrSignal**2 + eeHighMassErrSignal**2)**0.5
	
	mmLowMassErrSignal = ROOT.Double()
	mmLowMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(lowMassLow+0.01),histMMSignal.FindBin(lowMassHigh-0.01),mmLowMassErrSignal)
	mmHighMassErrSignal = ROOT.Double()
	mmHighMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(highMassLow+0.01),histMMSignal.FindBin(highMassHigh-0.01),mmHighMassErrSignal)
	
	mmSignal = mmLowMassSignal + mmHighMassSignal
	mmErrSignal = (mmLowMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
	
	ofLowMassErrSignal = ROOT.Double()
	ofLowMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(lowMassLow+0.01),histEMSignal.FindBin(lowMassHigh-0.01),ofLowMassErrSignal)
	ofHighMassErrSignal = ROOT.Double()
	ofHighMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(highMassLow+0.01),histEMSignal.FindBin(highMassHigh-0.01),ofHighMassErrSignal)
	
	ofSignal = ofLowMassSignal + ofHighMassSignal
	ofErrSignal = (ofLowMassErrSignal**2 + ofHighMassErrSignal**2)**0.5

	
	sfSignal = eeSignal + mmSignal 
	sfLowMassSignal = eeLowMassSignal + mmLowMassSignal
	sfHighMassSignal = eeHighMassSignal + mmHighMassSignal
	sfErrSignal = (eeErrSignal**2 + mmErrSignal**2)**0.5
	sfLowMassErrSignal = (eeLowMassErrSignal**2 + mmLowMassErrSignal**2)**0.5
	sfHighMassErrSignal = (eeHighMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
		
	
	rsfof = float(sf)/float(of)
	rsfofErr = rsfof*(sfErr**2/sf**2+ofErr**2/of**2)**0.5
	rsfofLowMass = float(sfLowMass)/float(ofLowMass)
	rsfofLowMassErr = rsfof*(sfLowMassErr**2/sfLowMass**2+ofLowMassErr**2/ofLowMass**2)**0.5
	rsfofHighMass = float(sfHighMass)/float(ofHighMass)
	rsfofHighMassErr = rsfof*(sfHighMassErr**2/sf**2+ofHighMassErr**2/of**2)**0.5
	
	rsfofSignal = float(sfSignal)/float(ofSignal)	
	rsfofErrSignal = rsfofSignal*(sfErrSignal**2/sfSignal**2+ofErrSignal**2/ofSignal**2)**0.5
	rsfofLowMassSignal = float(sfLowMassSignal)/float(ofLowMassSignal)
	if sfLowMassSignal > 0 and ofLowMassSignal > 0:
		rsfofLowMassErrSignal = rsfofLowMassSignal*(sfLowMassErrSignal**2/sfLowMassSignal**2+ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
	else:
		rsfofLowMassErrSignal = 0
	rsfofHighMassSignal = float(sfHighMassSignal)/float(ofHighMassSignal)
	rsfofHighMassErrSignal = rsfofHighMassSignal*(sfHighMassErrSignal**2/sfHighMassSignal**2+ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
	
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
	
	rEEOFSignal = float(eeSignal)/float(ofSignal)
	rEEOFErrSignal = rEEOFSignal * (eeErrSignal**2/eeSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
	rEEOFLowMassSignal = float(eeLowMassSignal)/float(ofLowMassSignal)
	if eeLowMassSignal > 0 and ofLowMassSignal > 0:
		rEEOFLowMassErrSignal = rEEOFLowMassSignal * (eeLowMassErrSignal**2/eeLowMassSignal**2 + ofLowMassErrSignal**2/ofLowMassSignal**2)**0.5
	else:
		rEEOFLowMassErrSignal = 0
	rEEOFHighMassSignal = float(eeHighMassSignal)/float(ofHighMassSignal)
	rEEOFHighMassErrSignal = rEEOFHighMassSignal * (eeHighMassErrSignal**2/eeHighMassSignal**2 + ofHighMassErrSignal**2/ofHighMassSignal**2)**0.5
	
	rMMOF = float(mm)/float(of)
	rMMOFErr = rMMOF * (mmErr**2/mm**2 + ofErr**2/of**2)**0.5
	rMMOFLowMass = float(mmLowMass)/float(ofLowMass)
	rMMOFLowMassErr = rMMOFLowMass * (mmLowMassErr**2/mmLowMass**2 + ofLowMassErr**2/ofLowMass**2)**0.5
	rMMOFHighMass = float(mmHighMass)/float(ofHighMass)
	rMMOFHighMassErr = rMMOFHighMass * (mmHighMassErr**2/mmHighMass**2 + ofHighMassErr**2/ofHighMass**2)**0.5
	
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
	
	result["rSFOF"] = rsfof
	result["rSFOFErr"] = rsfofErr
	result["rEEOF"] = rEEOF
	result["rEEOFErr"] = rEEOFErr
	result["rMMOF"] = rMMOF
	result["rMMOFErr"] = rMMOFErr
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
	parser.add_argument("-i", "--illustrate", action="store_true", dest="illustrate", default=False,
						  help="plot dependency illustrations.")	
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
			

	path = locations.dataSetPathTrigger
	
	if args.dilepton:
		source = "DiLeptonTrigger"
		modifier = "DiLeptonTrigger"
	else:
		source = ""		
		modifier = ""	
		
	#~ if args.constantConeSize:
		#~ if args.effectiveArea:
			#~ source = "EffAreaIso%s"%source
		#~ elif args.deltaBeta:
			#~ source = "DeltaBetaIso%s"%source
		#~ else:
			#~ print "Constant cone size (option -R) can only be used in combination with effective area (-e) or delta beta (-D) pileup corrections."
			#~ print "Using default miniIso cone with PF weights instead"
	#~ else:
		#~ if args.effectiveArea:
			#~ source = "MiniIsoEffAreaIso%s"%source
		#~ elif args.deltaBeta:
			#~ source = "MiniIsoDeltaBetaIso%s"%source
		#~ else:
			#~ source = "MiniIsoPFWeights%s"%source	


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
				
			if args.illustrate:
				illustration(selectionName)
				
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rSFOF_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves//rSFOF_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())					
main()
