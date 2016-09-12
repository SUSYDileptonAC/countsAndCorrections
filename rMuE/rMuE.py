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


### get the histograms from the ntuples for data or MC
def getHistograms(path,plot,runRange,isMC,backgrounds,region,verbose=True,EM=False):


	### fetch the trees
	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	
	### get the MC stack
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,verbose=verbose).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,verbose=verbose).theHistogram
		
		if EM:
			histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0,verbose=verbose).theHistogram		
			
	### or histogram
	else:
		histoEE = getDataHist(plot,treesEE,verbose=verbose)
		histoMM = getDataHist(plot,treesMM,verbose=verbose)
		if EM:
			histoEM = getDataHist(plot,treesEM,verbose=verbose)
	
	if EM:
		return histoEE , histoMM, histoEM
	else:
		return histoEE , histoMM

### calculate the central r_MuE values
def centralValues(path,selection,runRange,isMC,backgrounds,verbose=True):

	### get the plot and region selection
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	plot.cuts = plot.cuts % runRange.runCut		


	### fetch the systematics
	if not "Forward" in selection.name:
		relSyst = systematics.rMuE.central.val
		if "Central" in selection.name:
			region = "central"
		else:
			region = "inclusive"
	else:	
		relSyst = systematics.rMuE.forward.val
		region = "forward"
	
	### get the histograms
	histEE, histMM = getHistograms(path,plot,runRange,isMC, backgrounds,region,verbose=verbose)
	
	nEE = histEE.Integral()
	nMM = histMM.Integral()
	
	###calculate the ratio and the uncertainties
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
	
	
def dependencies(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit,verbose=True):
	
	### make dependency plots, use ttbar MC for comparison both when plotting
	### data and all MC

	backgroundsTT = ["TT_Powheg"]
	
	### loop over the plots
	for name in plots:
		### Get plot and region
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	

		### get systematics
		if not "Forward" in selection.name:
			relSyst = systematics.rMuE.central.val
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			relSyst = systematics.rMuE.forward.val
			region = "forward"

		### fetch histograms
		if isMC:
			histEE, histMM = getHistograms(path,plot,runRange,True, backgrounds,region,verbose=verbose)	
		else:
			histEE, histMM = getHistograms(path,plot,runRange,False, backgrounds,region,verbose=verbose)	
		histEEMC, histMMMC = getHistograms(path,plot,runRange,True, backgroundsTT,region,verbose=verbose)	
			
		### create canvas, pad, set style, latex labels ...
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
		



		### make ratio histogram
		rMuE = histMM.Clone("rMuE")
		rMuE.Divide(histEE)
		rMuEMC = histMMMC.Clone("rMuEMC")
		rMuEMC.Divide(histEEMC)
		
		### take the square root (since r_mu = sqrt(N_mumu/N_ee)
		### and propagate the uncertainties
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



		### make a plot of the input (ee and mumu events)
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
		
			
		### Plot r_MuE
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

		### fetch the central value from existing file or calculate it if non-existent
		if os.path.isfile("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label)):
			centralVals = pickle.load(open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"rb"))
		else:
			centralVals = centralValues(path,selection,runRange,isMC,backgrounds)

		### draw a line for the central value and an error band around it
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
		
		### Draw ratio and legend
		rMuEMC.Draw("hist E1P SAME")
			
		leg = ROOT.TLegend(0.6,0.7,0.85,0.93)
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
		
	
		### Try a fit if there seems to be a linear dependency on mll
		### Rewrite this part if you see any dependency on another variable
		### and want to correct it
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
	
		
		# Draw arrows for the gap in eta between 1.4 and 1.6
		
		if "eta" in plot.variable:
			yMin = 0.95
			yMax = 1.2
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


		hCanvas.Print("fig/rMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	

		### Calculate 0.5*(rMuE + rMuE^-1) which is the quantity that goes into R_SFOF
		### and the corresponding uncertainty
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
		
		plotPad.Draw()	
		plotPad.cd()	
		plotPad.DrawFrame(plot.firstBin,0.95,plot.lastBin,1.2,"; %s; 0.5(r_{#mue} + 1/r_{#mue})" %plot.xaxis)
		gStyle.SetErrorX(0.5)

		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))


		### Draw line and uncertainty band again
		x= array("f",[plot.firstBin, plot.lastBin]) 
		y= array("f", [0.5*(centralVals["rMuE"]+1./centralVals["rMuE"]),0.5*(centralVals["rMuE"]+1./centralVals["rMuE"])]) 
		ex= array("f", [0.,0.])
		ey= array("f", [0.5*(1. - (1./(centralVals["rMuE"]**2)))*centralVals["rMuESystErr"],0.5*(1. - (1./(centralVals["rMuE"]**2)))*centralVals["rMuESystErr"]])
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
			
		leg = ROOT.TLegend(0.6,0.7,0.85,0.93)
		if not isMC:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "Data", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
			
		else:
			rMuE.Draw("hist E1P SAME")			
			leg.AddEntry(rMuE, "all MC", "p")
			leg.AddEntry(rMuEMC,"t#bar{t} MC","p")
		if not isMC: 
			leg.AddEntry(rmueLine, "central value", "l")
		else:
			leg.AddEntry(rmueLine, "central value on MC", "l") 
		leg.AddEntry(ge,"syst. unc. of r_{#mu e}","f")

		leg.SetBorderSize(0)
		leg.SetLineWidth(2)
		leg.SetTextAlign(22)
		
	
		
		### fit dependency on mll, or change for other variables
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
	
		
		# Gap in eta again
		
		if "eta" in plot.variable:
			yMin = 0.95
			yMax = 1.2
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
		
				


		hCanvas.Print("fig/rSFOFFromRMuE_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
	
	
def main():



	parser = argparse.ArgumentParser(description='rMuE measurements.')
	
	parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", default=False,
						  help="Switch verbose mode off. Do not show cut values and samples on the console whenever a histogram is created")
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
		args.selection.append(regionsToUse.rMuE.central.name)	
		args.selection.append(regionsToUse.rMuE.forward.name)	
		args.selection.append(regionsToUse.rMuE.inclusive.name)
			
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)		

	path = locations.dataSetPath
	
	if args.quiet:
		verbose = False
	else:
		verbose = True		

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

			### calculate central values for r_MuE and store them in a .pkl file
			if args.central:
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,verbose=verbose)
				if args.mc:
					outFilePkl = open("shelves/rMuE_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rMuE_%s_%s_MC.pkl created"%(selection.name,runRange.label)
				else:
					outFilePkl = open("shelves/rMuE_%s_%s.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rMuE_%s_%s.pkl created"%(selection.name,runRange.label)
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
			
			### plot dependencies	
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit,verbose=verbose)
			
			### copy .pkl file to frameWorkBase/shelves	 to be used later on by other tools
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rMuE_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)	
					print "shelves/rMuE_%s_%s_MC.pkl copied to central repository"%(selection.name,runRange.label)	
				else:	
					bashCommand = "cp shelves//rMuE_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)	
					print "shelves/rMuE_%s_%s.pkl copied to central repository"%(selection.name,runRange.label)
				process = subprocess.Popen(bashCommand.split())				 	

main()
