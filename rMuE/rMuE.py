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

def getHistograms(path,plot,runRange,isMC,backgrounds,region,EM=False):


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
		#~ histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		#~ histoMM.Scale(getattr(triggerEffs,region).effMM.val)
		
		if EM:
			histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
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

def centralValues(path,selection,runRange,isMC,backgrounds):

	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	#~ plot.cleanCuts()
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
	
	histEE, histMM = getHistograms(path,plot,runRange,isMC, backgrounds,region)
	
	nEE = histEE.Integral()
	nMM = histMM.Integral()
	
	rMuE= pow(nMM/nEE,0.5)

	rMuEStatErr = 0.5*rMuE*(1./nMM + 1./nEE)**0.5
	rMuESystErr= rMuE*relSyst
	

	result = {}
	result["nEE"] = nEE
	result["nMM"] = nMM
	result["rMuE"] = rMuE
	result["rMuEStatErr"] = rMuEStatErr
	result["rMuESystErr"] = rMuESystErr
	
	return result
	
	
def dependencies(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit):
	

	backgroundsTT = ["TTJets"]
	
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
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

		if isMC:
			histEE, histMM = getHistograms(path,plot,runRange,True, backgrounds,region)	
		else:
			histEE, histMM = getHistograms(path,plot,runRange,False, backgrounds,region)	
		histEEMC, histMMMC = getHistograms(path,plot,runRange,True, backgroundsTT,region)	
			
		
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
				#~ rMuE.SetBinError(i, 0.5*rMuE.GetBinContent(i)*pow(1./abs(histMM.GetBinContent(i)) + 1./abs(histEE.GetBinContent(i)), 0.5))
				rMuE.SetBinError(i, 0.5*pow( histMM.GetBinError(i)**2/(abs(histEE.GetBinContent(i))*abs(histMM.GetBinContent(i))) + histEE.GetBinError(i)**2*abs(histMM.GetBinContent(i))/abs(histEE.GetBinContent(i)**3), 0.5))
			if rMuEMC.GetBinContent(i) > 0:
				#~ rMuEMC.SetBinError(i, 0.5*rMuEMC.GetBinContent(i)*pow(1./abs(histMMMC.GetBinContent(i)) + 1./abs(histEEMC.GetBinContent(i)), 0.5))
				#~ rMuEMC.SetBinError(i, pow( pow(histMMMC.GetBinError(i)/histEEMC.GetBinContent(i),2) + pow(histEEMC.GetBinError(i)*histMMMC.GetBinContent(i)/(histEEMC.GetBinContent(i)**2),2), 0.5))
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
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		
		
		
		hCanvas.Print("fig/rMuE_%s_%s_%s_%s_RawInputs.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		
		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
		plotPad.DrawFrame(plot.firstBin,0.,plot.lastBin,2.5,"; %s; r_{#mue}" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

		

		if os.path.isfile("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label)):
			centralVals = pickle.load(open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"rb"))
		else:
			centralVals = centralValues(path,selection,runRange,isMC,backgrounds)
		
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
			
		leg = ROOT.TLegend(0.6,0.7,0.85,0.95)
		if not isMC:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "Data", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
			
		else:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "all MC", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
		if not isMC: 
			leg.AddEntry(rmueLine, "r_{#mu e} central value", "l")
		else:
			leg.AddEntry(rmueLine, "r_{#mu e} central value on MC", "l") 
		leg.AddEntry(ge,"syst. unc. of r_{#mu e}","f")

		leg.SetBorderSize(0)
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
		
				


		hCanvas.Print("fig/rMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	
	
def signalRegion(path,selection,plots,runRange,isMC,backgrounds,cmsExtra):
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

		
		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC, backgrounds,region,EM=True)	

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
			args.selection.append(regionsToUse.signal.central.name)	
			args.selection.append(regionsToUse.signal.forward.name)	
			args.selection.append(regionsToUse.signal.inclusive.name)		
		else:
			args.selection.append(regionsToUse.rMuE.central.name)	
			args.selection.append(regionsToUse.rMuE.forward.name)	
			args.selection.append(regionsToUse.rMuE.inclusive.name)
			
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
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds)
				if args.mc:
					outFilePkl = open("shelves/rMuE_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					outFilePkl = open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit)		
			if args.signalRegion:
				 signalRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra)	
				 
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rMuE_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves//rMuE_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())				 	

main()
