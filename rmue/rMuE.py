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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import systematics, triggerEffs

from locations import locations

def getHistograms(path,plot,runRange,isMC,backgrounds,region):


	treesEE = readTrees(path,"EE")
	treesMM = readTrees(path,"MuMu")	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		histoEE.Scale(getattr(triggerEffs,region).effMM.val)
			
		
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
	
	return histoEE , histoMM

def centralValues(path,selection,runRange,isMC,backgrounds):

	plot = getPlot("mllPlot")
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
	
	histEE, histMM = getHistograms(path,plot,runRange,isMC, backgrounds,region)
	
	nEE = histEE.Integral()
	nMM = histMM.Integral()
	
	rMuE= pow(nMM/nEE,0.5)

	rMuEStatErr = pow( pow(nMM**0.5/nEE,2) + pow(nEE**0.5*nMM/(nEE**2),2), 0.5)
	rMuESystErr= rMuE*relSyst
	

	result = {}
	result["nEE"] = nEE
	result["nMM"] = nMM
	result["rMuE"] = rMuE
	result["rMuEStatErr"] = rMuEStatErr
	result["rMuESystErr"] = rMuESystErr
	
	return result
	
	
def dependencies(path,selection,plots,runRange,isMC,backgrounds,cmsExtra):
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


		histEE, histMM = getHistograms(path,plot,runRange,False, backgrounds,region)	
		histEEMC, histMMMC = getHistograms(path,plot,runRange,True, backgrounds,region)	
			
		
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
			rMuE.SetBinContent(i, pow(rMuE.GetBinContent(i),0.5))
			rMuEMC.SetBinContent(i, pow(rMuEMC.GetBinContent(i),0.5))
			if rMuE.GetBinContent(i) > 0:
				rMuE.SetBinError(i, pow( pow(histMM.GetBinContent(i)**0.5/histEE.GetBinContent(i),2) + pow(histEE.GetBinContent(i)**0.5*histMM.GetBinContent(i)/(histEE.GetBinContent(i)**2),2), 0.5))
			if rMuEMC.GetBinContent(i) > 0:
				rMuEMC.SetBinError(i, pow( pow(histMMMC.GetBinError(i)/histEEMC.GetBinContent(i),2) + pow(histEEMC.GetBinError(i)*histMMMC.GetBinContent(i)/(histEEMC.GetBinContent(i)**2),2), 0.5))

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
		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
		
		
		
		hCanvas.Print("fig/rMuE_%s_%s_%s_%s_RawInputs.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		
		hCanvas.Clear()
		ROOT.gPad.SetLogy(0)

		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()
		plotPad.UseCurrentStyle()
		
		plotPad.Draw()	
		plotPad.cd()	
		plotPad.DrawFrame(plot.firstBin,0.8,plot.lastBin,1.7,"; %s; r_{#mue}" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.89,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.82	
		else:
			yLabelPos = 0.85	

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
		if not isMC: 
			leg.AddEntry(rmueLine, "r_{#mu e} central value", "l")
		else:
			leg.AddEntry(rmueLine, "r_{#mu e} central value on MC", "l") 
		leg.AddEntry(ge,"syst. unc. of r_{#mu e}","f")

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
		
				


		hCanvas.Print("fig/rMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	
		
	
def main():



	parser = argparse.ArgumentParser(description='Trigger efficiency measurements.')
	
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
						  help="calculate effinciecy central values")
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
		centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds)
		if args.mc:
			outFilePkl = open("shelves/rMuE_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
		else:
			outFilePkl = open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"w")
		pickle.dump(centralVal, outFilePkl)
		outFilePkl.close()
		
	if args.dependencies:
		 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra)		

main()
