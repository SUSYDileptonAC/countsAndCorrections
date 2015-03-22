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

import numpy


import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rSFOFFact, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins

from locations import locations

def getHistograms(path,plot,runRange,isMC,backgrounds,region=""):

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
		histoEE.Scale(getattr(triggerEffs,region).effEE.val)
		histoEE.Scale(getattr(triggerEffs,region).effMM.val)	
		histoEM.Scale(getattr(triggerEffs,region).effEM.val)
			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
def getUncert(sf,of,factorUncert):

		result = (sf + of + (of*factorUncert)**2)**0.5
		return result
		
def lumiDependency(path,plotName,selection,runRange,cmsExtra):


	plot = getPlot(plotName)
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		


	label =""
	if "Forward" in selection.name:
		label = "forward"
	elif "Central" in selection.name:
		label = "central"
	else:		
		label = "inclusive"	

	corr = getattr(rSFOF,label).val
	corrUncert = getattr(rSFOF,label).err	

	runCuts = [[190645,194643],[194644,195868],[195915,198955],[198969,200075],[200091,201669],[201671,202972],[202973,205344],[205515,206512],[206513,207491],[207492,208686]]
	#~ runCuts = [[190645,194897]]

	#~ xValues = [2,4,6,8,10,12,14,16,18,19.4]
	xValues = [1,3,5,7,9,11,13,15,17,18.7]
	xValuesUncert = [1,1,1,1,1,1,1,1,1,0.7]
	
	yValues = []
	yValuesUncert = []
	yValuesBTagged = []
	yValuesUncertBTagged = []
	yValuesBVeto = []
	yValuesUncertBVeto = []
	
	sfList = []
	ofList = []
	
	sfValuesUncert = []
	ofValuesUncert = []
	
	sfListBTagged = []
	ofListBTagged = []
	
	sfValuesUncertBTagged = []
	ofValuesUncertBTagged = []
	
	sfListBVeto = []
	ofListBVeto = []
	
	sfValuesUncertBVeto = []
	ofValuesUncertBVeto = []
	
	eeList = []
	mmList = []
	
	eeValuesUncert = []
	mmValuesUncert = []
	
	
	
	
	cuts = plot.cuts	

	for cutPair in runCuts:
		plot.cuts = plot.cuts + "*(runNr >= %d && runNr <= %d)"%(runCuts[0][0],cutPair[1])
		
		eeHist, mmHist, emHist = getHistograms(path,plot,runRange,False,[],label)
		
		plot.cuts = cuts
		plot.cuts = plot.cuts + "*(runNr >= %d && runNr <= %d)"%(runCuts[0][0],cutPair[1]) +  "*(nBJets == 0)"
		
		eeHistBVeto, mmHistBVeto, emHistBVeto = getHistograms(path,plot,runRange,False,[],label)
		
		plot.cuts = cuts
		plot.cuts = plot.cuts + "*(runNr >= %d && runNr <= %d)"%(runCuts[0][0],cutPair[1]) +  "*(nBJets >= 1)"
		
		eeHistBTagged, mmHistBTagged, emHistBTagged = getHistograms(path,plot,runRange,False,[],label)

		plot.cuts = cuts
				
		ee = eeHist.Integral() 
		mm = mmHist.Integral() 
		sf = eeHist.Integral() + mmHist.Integral()
		of = emHist.Integral()*corr
		eeBTagged = eeHistBTagged.Integral() 
		mmBTagged = mmHistBTagged.Integral() 
		sfBTagged = eeHistBTagged.Integral() + mmHistBTagged.Integral()
		ofBTagged = emHistBTagged.Integral()
		eeBVeto = eeHistBVeto.Integral() 
		mmBVeto = mmHistBVeto.Integral() 
		sfBVeto = eeHistBVeto.Integral() + mmHistBVeto.Integral()
		ofBVeto = emHistBVeto.Integral()
		
		yValues.append(sf-of)
		yValuesUncert.append(getUncert(sf,of,corrUncert))
		sfList.append(sf)
		ofList.append(of)
		sfValuesUncert.append(sf**0.5)
		ofValuesUncert.append((of+(of*corrUncert)**2)**0.5)
		yValuesBTagged.append(sfBTagged-ofBTagged)
		yValuesUncertBTagged.append(getUncert(sfBTagged,ofBTagged,corrUncert))
		sfListBTagged.append(sfBTagged)
		ofListBTagged.append(ofBTagged)
		sfValuesUncertBTagged.append(sfBTagged**0.5)
		ofValuesUncertBTagged.append(ofBTagged**0.5)	
		yValuesBVeto.append(sfBVeto-ofBVeto)
		yValuesUncertBVeto.append(getUncert(sfBVeto,ofBVeto,corrUncert))
		sfListBVeto.append(sfBVeto)
		ofListBVeto.append(ofBVeto)
		sfValuesUncertBVeto.append(sfBVeto**0.5)
		ofValuesUncertBVeto.append(ofBVeto**0.5)
		eeList.append(ee)
		mmList.append(mm)
		eeValuesUncert.append(ee**0.5)
		mmValuesUncert.append(mm**0.5)		

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style = setTDRStyle()
	style.SetTitleYOffset(1.25)
	plotPad.UseCurrentStyle()		
	plotPad.Draw()	
	plotPad.cd()	

	legend = TLegend(0.19, 0.5, 0.55, 0.85)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)

	#~ if label == "forward":
		#~ hCanvas.DrawFrame(0,-20,20,200,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
		#~ 
	#~ else:	
	
	yMax = sfList[-1]+150
	yMin = min(min(yValues)-max(yValuesUncert)*1.25,-10)
	hCanvas.DrawFrame(0,yMin,20,yMax,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
	
	zeroLine = ROOT.TLine(0, 0., 20 , 0.)
	zeroLine.SetLineWidth(1)
	zeroLine.SetLineColor(ROOT.kBlue)
	zeroLine.SetLineStyle(2)
	zeroLine.Draw("same")	
	
	arg2 = numpy.array(xValues,"d")
	arg4 = numpy.array(xValuesUncert,"d")

	arg3 = numpy.array(yValues,"d")
	arg5 = numpy.array(yValuesUncert,"d")	
	
	sfArray = numpy.array(sfList,"d")
	ofArray = numpy.array(ofList,"d")
	sfUncertArray = numpy.array(sfValuesUncert,"d")
	ofUncertArray = numpy.array(ofValuesUncert,"d")

	arg3BTagged = numpy.array(yValuesBTagged,"d")
	arg5BTagged = numpy.array(yValuesUncertBTagged,"d")	
		
	sfArrayBTagged = numpy.array(sfListBTagged,"d")
	ofArrayBTagged = numpy.array(ofListBTagged,"d")
	sfUncertArrayBTagged = numpy.array(sfValuesUncertBTagged,"d")
	ofUncertArrayBTagged = numpy.array(ofValuesUncertBTagged,"d")

	arg3BVeto = numpy.array(yValuesBVeto,"d")
	arg5BVeto = numpy.array(yValuesUncertBVeto,"d")	
		
	sfArrayBVeto = numpy.array(sfListBVeto,"d")
	ofArrayBVeto = numpy.array(ofListBVeto,"d")
	sfUncertArrayBVeto = numpy.array(sfValuesUncertBVeto,"d")
	ofUncertArrayBVeto = numpy.array(ofValuesUncertBVeto,"d")

	eeArray = numpy.array(eeList,"d")
	mmArray = numpy.array(mmList,"d")
	eeUncertArray = numpy.array(eeValuesUncert,"d")
	mmUncertArray = numpy.array(mmValuesUncert,"d")
	

	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graph = ROOT.TGraphErrors(10,arg2,arg3,arg4,arg5)
	graphSF = ROOT.TGraphErrors(10,arg2,sfArray,arg4,sfUncertArray)
	graphOF = ROOT.TGraphErrors(10,arg2,ofArray,arg4,ofUncertArray)

	graphBTagged = ROOT.TGraphErrors(10,arg2,arg3BTagged,arg4,arg5BTagged)

	graphSFBTagged = ROOT.TGraphErrors(10,arg2,sfArrayBTagged,arg4,sfUncertArrayBTagged)

	graphOFBTagged = ROOT.TGraphErrors(10,arg2,ofArrayBTagged,arg4,ofUncertArrayBTagged)

	graphBVeto = ROOT.TGraphErrors(10,arg2,arg3BVeto,arg4,arg5BVeto)
	graphSFBVeto = ROOT.TGraphErrors(10,arg2,sfArrayBVeto,arg4,sfUncertArrayBVeto)
	graphOFBVeto = ROOT.TGraphErrors(10,arg2,ofArrayBVeto,arg4,ofUncertArrayBVeto)

	graphEE = ROOT.TGraphErrors(10,arg2,eeArray,arg4,eeUncertArray)
	graphMM = ROOT.TGraphErrors(10,arg2,mmArray,arg4,mmUncertArray)
	graph.Draw("Psame")
	graphSF.Draw("Psame")
	graphSF.SetLineColor(ROOT.kRed)
	graphSF.SetMarkerColor(ROOT.kRed)
	graphOF.Draw("Psame")
	graphOF.SetLineColor(ROOT.kBlue)
	graphOF.SetMarkerColor(ROOT.kBlue)
	
	
	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if "Signal" in selection.name:
		legend.AddEntry(legendHistDing,"Signal region %s"%label,"h")	
	else:
		legend.AddEntry(legendHistDing,"Control region %s"%label,"h")	
	
	legend.AddEntry(graphSF,"Same Flavour","p")	
	legend.AddEntry(graphOF,"Prediction from Opposite Flavour","p")	
	legend.AddEntry(graph,"N_{SF}-N_{prediction}","p")	

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


	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.89,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.82	
	else:
		yLabelPos = 0.85	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	
	hCanvas.Print("fig/YieldvsLumi_%s"%(plot.filename%runRange.label))
	#~ if label == "forward":
		#~ hCanvas.DrawFrame(0,-20,20,200,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
		#~ 
	#~ else:	
	yMax = sfListBTagged[-1]+150
	yMin = min(min(yValuesBTagged)-max(yValuesUncertBTagged)*1.25,-10)
	hCanvas.DrawFrame(0,yMin,20,yMax,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
	zeroLine.Draw("same")
	legend.Clear()
	graphBTagged.Draw("Psame")
	graphSFBTagged.Draw("Psame")
	graphSFBTagged.SetLineColor(ROOT.kRed)
	graphSFBTagged.SetMarkerColor(ROOT.kRed)
	graphOFBTagged.Draw("Psame")
	graphOFBTagged.SetLineColor(ROOT.kBlue)
	graphOFBTagged.SetMarkerColor(ROOT.kBlue)
	
		

	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if "Signal" in selection.name:
		legend.AddEntry(legendHistDing,"Signal region %s - b tagged"%label,"h")	
	else:
		legend.AddEntry(legendHistDing,"Control region %s - b tagged"%label,"h")		
	
	legend.AddEntry(graphSFBTagged,"Same Flavour","p")	
	legend.AddEntry(graphOFBTagged,"Opposite Flavour","p")	
	legend.AddEntry(graphBTagged,"N_{SF}-N_{OF}","p")	

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

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.89,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.82	
	else:
		yLabelPos = 0.85	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	hCanvas.Print("fig/YieldvsLumi_BTagged_%s"%(plot.filename%runRange.label))
	
	#~ if label == "forward":
		#~ hCanvas.DrawFrame(0,-20,20,200,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
		#~ 
	#~ else:	
	yMax = sfListBVeto[-1]+150
	yMin = min(min(yValuesBVeto)-max(yValuesUncertBVeto)*1.25,-10)
	hCanvas.DrawFrame(0,yMin,20,yMax,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
	zeroLine.Draw("same")
	legend.Clear()
	graphBVeto.Draw("Psame")
	graphSFBVeto.Draw("Psame")
	graphSFBVeto.SetLineColor(ROOT.kRed)
	graphSFBVeto.SetMarkerColor(ROOT.kRed)
	graphOFBVeto.Draw("Psame")
	graphOFBVeto.SetLineColor(ROOT.kBlue)
	graphOFBVeto.SetMarkerColor(ROOT.kBlue)
	
		
	
	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if "Signal" in selection.name:
		legend.AddEntry(legendHistDing,"Signal region %s - b veto"%label,"h")	
	else:
		legend.AddEntry(legendHistDing,"Control region %s - b veto"%label,"h")	
	
	legend.AddEntry(graphSFBVeto,"Same Flavour","p")	
	legend.AddEntry(graphOFBVeto,"Opposite Flavour","p")	
	legend.AddEntry(graphBVeto,"N_{SF}-N_{OF}","p")	
	#~ legend.AddEntry(graph,"SF - OF","p")	
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
	
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.89,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.82	
	else:
		yLabelPos = 0.85	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	hCanvas.Print("fig/YieldvsLumi_BVeto_%s"%(plot.filename%runRange.label))
def main():	
	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-l", "--lowMass", action="store_true", dest="lowMass", default=False,
						  help="plot low mass dependency")
	parser.add_argument("-o", "--highMass", action="store_true", dest="highMass", default=False,
						  help="plot high mass dependency")
	parser.add_argument("-c", "--control", action="store_true", dest="control", default=False,
						  help="use control region")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	

	args = parser.parse_args()


	plotName = ""
	if args.lowMass:
		plotName = "mllPlotLowMass"
	elif args.highMass:
		plotName = "mllPlotHighMass"	
	selections = []	
	if args.control:
		selections.append(regionsToUse.rSFOF.central.name)	
		selections.append(regionsToUse.rSFOF.forward.name)	
		selections.append(regionsToUse.rSFOF.inclusive.name)	
	else:
		selections.append(regionsToUse.signal.central.name)	
		selections.append(regionsToUse.signal.forward.name)	
		selections.append(regionsToUse.signal.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPath	


	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
	else:
		cmsExtra = "Preliminary"
	print cmsExtra
	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)
			
			lumiDependency(path,plotName,selection,runRange,cmsExtra)			

				
main()						
