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

import ratios


from locations import locations






def doPlot(source,modifier,path,selection,plots,runRange,isMC,backgrounds,cmsExtra):
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()

		plot.cuts = plot.cuts % runRange.runCut	

		if "Forward" in selection.name:
			label = "forward"
		elif "Central" in selection.name:
			label = "central"
		else:		
			label = "inclusive"


		histsEE, histsMM, histsEM = getHistograms(path,source,modifier,plot,runRange,isMC, backgrounds,label)
		
		histsSF = []
		
		for hist in histsEE:
			histsSF.append(hist.Clone())
		for index, hist in enumerate(histsMM):
			histsSF[index].Add(hist.Clone())
			
			
			
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
		ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		ratioPad.UseCurrentStyle()
		plotPad.Draw()	
		ratioPad.Draw()	
		plotPad.cd()

		logScale = plot.log
		if plot.variable == "met" or plot.variable == "type1Met" or plot.variable == "tcMet" or plot.variable == "caloMet" or plot.variable == "mht":
			logScale = True
		
		if logScale == True:
			plotPad.SetLogy()					
		
		yMax = histsSF[0].GetBinContent(histsSF[0].GetMaximumBin())
		if plot.yMax == 0:
			if logScale:
				yMax = yMax*1000
			else:
				yMax = yMax*1.5
							
		else: yMax = plot.yMax
		
		plotPad.DrawFrame(plot.firstBin,0.1,plot.lastBin,yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))



		
		
		from ROOT import TH1F,kWhite
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.5,0.6,0.95,0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")	


		for index, hist in enumerate(histsSF):
			
			hist.SetLineColor(ROOT.kBlue+2*index)
			#~ hist.SetLineStyle(1+2*index)

			hist.Draw("samehist")
			legend.AddEntry(hist,backgrounds[index],"l")	
		#~ legend.AddEntry(histEE,"R_{EE/OF}","p")	
		#~ legend.AddEntry(histMM,"R_{MM/OF}","p")	


		legend.Draw("same")

		
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


		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

		#~ if fit:
			#~ fit = TF1("dataFit","pol1",0,300)
			#~ fit.SetLineColor(ROOT.kBlack)
			#~ histRSFOF.Fit("dataFit")		
			#~ 
			#~ latex = ROOT.TLatex()
			#~ latex.SetTextSize(0.035)	
			#~ latex.SetNDC()	
			#~ latex.DrawLatex(0.2, 0.25, "Fit: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))


		ratioPad.cd()		
		ratioGraphs =  ratios.RatioGraph(histsSF[1],histsSF[0], xMin=plot.firstBin, xMax=plot.lastBin,title="X / Madgraph",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlue+2,adaptiveBinning=0.25)
		ratioGraphs2 =  ratios.RatioGraph(histsSF[2],histsSF[0], xMin=plot.firstBin, xMax=plot.lastBin,title="X / Madgraph",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlue+4,adaptiveBinning=0.25)
		ratioGraphs3 =  ratios.RatioGraph(histsSF[3],histsSF[0], xMin=plot.firstBin, xMax=plot.lastBin,title="X / Madgraph",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlue+6,adaptiveBinning=0.25)

		ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
		ratioGraphs2.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)
		ratioGraphs3.draw(ROOT.gPad,False,False,True,chi2Pos=0.8)


		hCanvas.Print("fig/ttbarCompare_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	





def getHistograms(path,source,modifier,plot,runRange,isMC,backgrounds,region=""):

	treesEE = readTrees(path,"EE",source = source,modifier= modifier)
	treesEM = readTrees(path,"EMu",source = source,modifier= modifier)
	treesMM = readTrees(path,"MuMu",source = source,modifier= modifier)
		
	
	histosEE = []
	histosMM = []
	histosEM = []

		#~ print path, source, modifier
	eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)	
	processes = []
	for background in backgrounds:
		processes = []

		processes.append(Process(getattr(Backgrounds,background),eventCounts))
		
		histosEE.append(TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram)		
		histosMM.append(TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram)
		histosEM.append(TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram)
						

			

	
	return histosEE , histosMM, histosEM
	
	

	


	
	
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
		args.backgrounds = ["TTJets_Madgraph","TTJets_aMCatNLO","TT_aMCatNLO","TT_Powheg"]
	if len(args.plots) == 0:
		args.plots = plotLists.default
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.signal.central.name)	
		args.selection.append(regionsToUse.signal.forward.name)	
		args.selection.append(regionsToUse.signal.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPathTrigger
	
	if args.dilepton:
		source = "DiLeptonTrigger"
		modifier = "DiLeptonTrigger"
	else:
		source = ""		
		modifier = ""	
		
	print args.selection
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
			
				
			doPlot(source,modifier,path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra)

		
main()
