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

from corrections import rSFOF, rEEOF, rMMOF
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations

### get the histograms from the ntuples for data or MC
def getHistograms(path,plot,runRange,isMC,backgrounds,verbose=True):
	
	### Add code to take the flavor-symmetric background contribution into account

	### fetch the trees
	treesEE = readTrees(path,"EE")
	treesMM = readTrees(path,"MuMu")
		
	
	### get the MC stack
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0,verbose=verbose).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0,verbose=verbose).theHistogram
		
	else:
		histoEE = getDataHist(plot,treesEE,verbose=verbose)
		histoMM = getDataHist(plot,treesMM,verbose=verbose)
	
	return histoEE , histoMM


### Routine to make the mass spectrum	
def plotMllSpectra(SFhist,runRange,selection,suffix,cmsExtra,additionalLabel):

	### Plot OF component in this routine as well
		
	SFhist.Rebin(5)
	
	### get canvas, pad and style
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
	
	SFhist.Draw("samepe")
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)	
	legend.AddEntry(SFhist,"%s events"%suffix,"p")
	legend.Draw("same")

	### make lines between the different regions
	line1 = ROOT.TLine(mllBins.lowMass.low,0,mllBins.lowMass.low,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(mllBins.lowMass.high,0,mllBins.lowMass.high,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(mllBins.onZ.low,0,mllBins.onZ.low,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(mllBins.onZ.high,0,mllBins.onZ.high,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5 = ROOT.TLine(mllBins.highMass.low,0,mllBins.highMass.low,SFhist.GetBinContent(SFhist.GetMaximumBin()))
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

	### Label in and out part
	Labelin = ROOT.TLatex()
	Labelin.SetTextAlign(12)
	Labelin.SetTextSize(0.04)
	Labelin.SetTextColor(ROOT.kRed+2)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.04)
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
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.21,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.21,yLabelPos,"%s"%(cmsExtra))
	
	plotPad.RedrawAxis()
	if additionalLabel is not "":
		hCanvas.Print("fig/rOutIn_NoLog_%s_%s_%s_%s.pdf"%(selection.name,suffix,runRange.label,additionalLabel))
	else:
		hCanvas.Print("fig/rOutIn_NoLog_%s_%s_%s.pdf"%(selection.name,suffix,runRange.label))
			
	
	
	### same in log plot
	hCanvas.Clear()
	
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()				
	

	
	plotPad.DrawFrame(mllBins.lowMass.low,1,300,SFhist.GetBinContent(SFhist.GetMaximumBin())*10,"; %s ; %s" %("m_{ll} [GeV]","Events / 5 GeV"))		
	
	plotPad.SetLogy()

	
	SFhist.Draw("samepe")
	legend.Draw("same")
	

	line1.SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2.SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3.SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4.SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5.SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	line5.Draw("same")
	Labelin.SetTextAngle(90)
	Labelin.DrawLatex(89.35,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"on Z")
	Labelout.SetTextAngle(90)
	Labelout.DrawLatex(47.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"low mass")
	Labelout.DrawLatex(75.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"below Z")
	Labelout.DrawLatex(109.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"above Z")
	Labelout.DrawLatex(150.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"high mass")
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
	
### routine to make some more detailed dependency studies beside the standard mass plots
### not very often used since the DY background outside the Z window is a minor background contribution	
def dependencies(path,selection,plots,runRange,mc,backgrounds,cmsExtra,verbose=True):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	legend = TLegend(0.6, 0.7, 0.9, 0.9)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)		
	
	for name in plots:
		hCanvas.Clear()
		
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	

		if not "Forward" in selection.name:
			relSyst = systematics.rOutIn.central.val
			if "Central" in selection.name:
				region = "central"
			else:
				region = "inclusive"
		else:	
			relSyst = systematics.rOutIn.forward.val
			region = "forward"	
		 
		if len(plot.binning) == 0:
			bins = [plot.firstBin+(plot.lastBin-plot.firstBin)/plot.nBins*i for i in range(plot.nBins+1)]
		else:
			bins = plot.binning
		rOutIn = {"LowMass":{"EE":[],"MM":[],"SF":[]},"HighMass":{"EE":[],"MM":[],"SF":[]},"BelowZ":{"EE":[],"MM":[],"SF":[]},"AboveZ":{"EE":[],"MM":[],"SF":[]}}
		rOutInErr = {"LowMass":{"EE":[],"MM":[],"SF":[]},"HighMass":{"EE":[],"MM":[],"SF":[]},"BelowZ":{"EE":[],"MM":[],"SF":[]},"AboveZ":{"EE":[],"MM":[],"SF":[]}}


		binningErrs	= []
		plotBinning = []
		for i in range(0,len(bins)-1):
			binningErrs.append((bins[i+1]-bins[i])/2)
			if i == 0:
				plotBinning.append((bins[i+1]-abs(bins[i]))/2)
			else:
				plotBinning.append(plotBinning[i-1]+(bins[i+1]-bins[i])/2+binningErrs[i-1])

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
				
			additionalLabel = "%s_%.2f_%.2f"%(plot.variable,bins[i],bins[i+1])
			centralVal = centralValues(path,selection,runRange,mc,backgrounds,cmsExtra,additionalLabel,verbose=verbose)
			for combination in ["EE","MM","SF"]:
				for region in ["LowMass","HighMass","BelowZ","AboveZ"]:
					rOutIn[region][combination].append(centralVal["rOutIn%s%s"%(region,combination)])
					rOutInErr[region][combination].append(centralVal["rOutIn%sErr%s"%(region,combination)])


			
			selection.cut = tmpCuts
		if mc:		
			if os.path.isfile("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label)):
				centralVals = pickle.load(open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"rb"))
			else:
				centralVals = centralValues(path,selection,runRange,mc,backgrounds,cmsExtra,verbose=verbose)					
		else:
			if os.path.isfile("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label)):
				centralVals = pickle.load(open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"rb"))
			else:
				centralVals = centralValues(path,selection,runRange,mc,backgrounds,cmsExtra,verbose=verbose)		
		
		for combination in ["EE","MM","SF"]:
			relSystSave = relSyst
			for region in ["LowMass","HighMass","BelowZ","AboveZ"]:
				relSyst = relSystSave	
				hCanvas = TCanvas("hCanvas", "Distribution", 800,800)

				plotPad = TPad("plotPad","plotPad",0,0,1,1)
				
				style=setTDRStyle()
				style.SetTitleYOffset(1.3)
				style.SetPadLeftMargin(0.16)		
				plotPad.UseCurrentStyle()
				plotPad.Draw()	
				plotPad.cd()
		
				plotPad.DrawFrame(plot.firstBin,0.0,plot.lastBin,0.15,"; %s ; %s" %(plot.xaxis,"R_{out/in}"))		
				
				
				bandX = array("f",[plot.firstBin,plot.lastBin])
				bandY = array("f",[centralVals["rOutIn%s%s"%(region,combination)],centralVals["rOutIn%s%s"%(region,combination)]])
				bandYErr = array("f",[centralVals["rOutIn%s%s"%(region,combination)]*relSyst,centralVals["rOutIn%s%s"%(region,combination)]*relSyst])
				bandXErr = array("f",[0,0])
				
				
				errorband = ROOT.TGraphErrors(2,bandX,bandY,bandXErr,bandYErr)
				errorband.GetYaxis().SetRangeUser(0.0,0.15)
				errorband.GetXaxis().SetRangeUser(-5,105)
				errorband.Draw("3same")
				errorband.SetFillColor(ROOT.kOrange-9)
				rOutInLine = ROOT.TLine(plot.firstBin,centralVals["rOutIn%s%s"%(region,combination)],plot.lastBin,centralVals["rOutIn%s%s"%(region,combination)])
				rOutInLine.SetLineStyle(ROOT.kDashed)
				rOutInLine.SetLineWidth(2)
				rOutInLine.Draw("same")

				
				
				
				binning = array("f",plotBinning)
				rOutInVals = array("f",rOutIn[region][combination])
				binningErrs = array("f",binningErrs)
				rOutInValsErrs = array("f",rOutInErr[region][combination])	
				graph = ROOT.TGraphErrors(len(binning),binning,rOutInVals,binningErrs,rOutInValsErrs)
				graph.Draw("Psame0")
				legend.Clear()

				if mc:
					legend.AddEntry(graph,"r_{out,in} MC","p")
				else:
					legend.AddEntry(graph,"r_{out,in} Data","p")
				legend.AddEntry(rOutInLine, "Mean r_{out,in} = %.3f"%centralVals["rOutIn%s%s"%(region,combination)],"l")
				legend.AddEntry(errorband, "Mean r_{out,in} #pm %d %%"%(relSyst*100),"f")
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
					
				latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
				

				latexCMS.DrawLatex(0.19,0.89,"CMS")
				if "Simulation" in cmsExtra:
					yLabelPos = 0.83	
				else:
					yLabelPos = 0.85	

				latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))		
					
				ROOT.gPad.RedrawAxis()
				if mc:
					hCanvas.Print("fig/rOutInSyst_%s_%s_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,region,combination,plot.additionalName))
				else:
					hCanvas.Print("fig/rOutInSyst_%s_%s_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,region,combination,plot.additionalName))

	
	

	
### routine to get the central values	
def centralValues(path,selection,runRange,isMC,backgrounds,cmsExtra,additionalLabel="",verbose=True):			
			

	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		

	
	if not "Forward" in selection.name:
		region = "central"
	else:		
		region = "forward"
		
	### Take flavor-symmetric background into account and add the other mass regions

	histEE, histMM = getHistograms(path,plot,runRange,isMC,backgrounds,verbose=verbose)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())
	
	### mass bins
	result = {}
	lowMassLow = mllBins.lowMass.low
	lowMassHigh = mllBins.lowMass.high
	peakLow = mllBins.onZ.low
	peakHigh = mllBins.onZ.high

	
	### results at the Z peak	
	result["peakEE"] = histEE.Integral(histEE.FindBin(peakLow+0.01),histEE.FindBin(peakHigh-0.01))
	result["peakMM"] = histMM.Integral(histMM.FindBin(peakLow+0.01),histMM.FindBin(peakHigh-0.01))
	result["peakSF"] = result["peakEE"] + result["peakMM"]

	### At low mass
	result["lowMassEE"] = histEE.Integral(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01))
	result["lowMassMM"] = histMM.Integral(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01))
	result["lowMassSF"] = result["lowMassEE"] + result["lowMassMM"]
	
	### Add other regions here

	for combination in ["EE","MM","SF"]:
		peak = result["peak%s"%combination]		
		peakErr = sqrt(result["peak%s"%combination])

		lowMass = result["lowMass%s"%combination]			
		lowMassErr = sqrt(result["lowMass%s"%combination])
				
		result["correctedPeak%s"%combination] = peak
		result["peakError%s"%combination] = peakErr

		result["correctedLowMass%s"%combination] = lowMass
		result["lowMassError%s"%combination] = lowMassErr
	
		rOutInLowMass =   lowMass / peak
		rOutInLowMassSystErr = rOutInLowMass*systematics.rOutIn.central.val
		rOutInLowMassErr = sqrt((lowMassErr/peak)**2 + (lowMass*peakErr/peak**2)**2)


		result["rOutInLowMass%s"%combination] = rOutInLowMass
		result["rOutInLowMassErr%s"%combination] = rOutInLowMassErr
		result["rOutInLowMassSyst%s"%combination] = rOutInLowMassSystErr
		
		saveLabel = additionalLabel
		tmpLabel = additionalLabel
		if isMC:
			tmpLabel += "_MC"

		additionalLabel = tmpLabel
		if combination == "EE":
			plotMllSpectra(histEE.Clone(),runRange,selection,combination,cmsExtra,additionalLabel)
		elif combination == "MM":	
			plotMllSpectra(histMM.Clone(),runRange,selection,combination,cmsExtra,additionalLabel)
		else:	
			plotMllSpectra(histSF.Clone(),runRange,selection,combination,cmsExtra,additionalLabel)
			

		additionalLabel = saveLabel
		




	return result
def main():



	parser = argparse.ArgumentParser(description='R(out/in) measurements.')
	
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
						  help="calculate R(out/in) central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()



	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.rOutIn
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.rOutIn.central.name)	
		args.selection.append(regionsToUse.rOutIn.forward.name)	
		args.selection.append(regionsToUse.rOutIn.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	


	path = locations.dataSetPath
	
	if args.quiet:
		verbose = False
	else:
		verbose = True


	cmsExtra = "Private Work"
	if args.mc:
		cmsExtra = "#splitline{Private Work}{Simulation}"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)


			### Calculate central values for r_Out/In and store them in .pkl files
			if args.central:
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,cmsExtra,verbose=verbose)
				if args.mc:
					outFilePkl = open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rOutIn_%s_%s_MC.pkl created"%(selection.name,runRange.label)
				else:
					outFilePkl = open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"w")
					print "shelves/rOutIn_%s_%s.pkl created"%(selection.name,runRange.label)
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
			
			### make more detailed dependency plots	
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,verbose=verbose)	
			
			### copy .pkl files to frameWorkBase/shelves to be used by other tools	 
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rOutIn_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					print "shelves/rOutIn_%s_%s_MC.pkl copied to central repository"%(selection.name,runRange.label)		
				else:	
					bashCommand = "cp shelves/rOutIn_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
					print "shelves/rOutIn_%s_%s.pkl copied to central repository"%(selection.name,runRange.label)
				process = subprocess.Popen(bashCommand.split())				 					 	
	

main()
