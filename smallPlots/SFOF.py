import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)


etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"(((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)))",
			"BothEndcap":"abs(eta1) > 1.6 && abs(eta2) > 1.6",
			"Inclusive":"abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6))"
			}


def readTreeFromFile(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	return result
def readTreeFromFileV22(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	return result
	
def getFilePathsAndSampleNames(path):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	for filePath in glob("%s/sw538*.root"%path):
		sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		result[sampleName] = filePath
	return result
	
def totalNumberOfGeneratedEvents(path):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	return result
	
def readTrees(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
	return result
	
def readTreesV22(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFileV22(filePath, dileptonCombination)
		
	return result
	
	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	result = TH1F(name, "", nBins, firstBin, lastBin)
	result.Sumw2()
	tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	return result
	
	
def setTDRStyle():
	from ROOT import TStyle
	from ROOT import kWhite
	from ROOT import kTRUE
	tdrStyle =  TStyle("tdrStyle","Style for P-TDR")
	
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(kWhite)
	# For the canvas:
	tdrStyle.SetCanvasBorderMode(0)
	tdrStyle.SetCanvasColor(kWhite)
	tdrStyle.SetCanvasDefH(600) #Height of canvas
	tdrStyle.SetCanvasDefW(600)#Width of canvas
	tdrStyle.SetCanvasDefX(0)  #POsition on screen
	tdrStyle.SetCanvasDefY(0)
	
	# For the Pad:
	tdrStyle.SetPadBorderMode(0)
	# tdrStyle->SetPadBorderSize(Width_t size = 1);
	tdrStyle.SetPadColor(kWhite)
	tdrStyle.SetPadGridX(0)
	tdrStyle.SetPadGridY(0)
	tdrStyle.SetGridColor(0)
	tdrStyle.SetGridStyle(3)
	tdrStyle.SetGridWidth(1)
	
	# For the frame:
	tdrStyle.SetFrameBorderMode(0)
	tdrStyle.SetFrameBorderSize(1)
	tdrStyle.SetFrameFillColor(0)
	tdrStyle.SetFrameFillStyle(0)
	tdrStyle.SetFrameLineColor(1)
	tdrStyle.SetFrameLineStyle(1)
	tdrStyle.SetFrameLineWidth(1)
	
	# For the histo:
	# tdrStyle->SetHistFillColor(1);
	# tdrStyle->SetHistFillStyle(0);
	tdrStyle.SetHistLineColor(1)
	tdrStyle.SetHistLineStyle(0)
	tdrStyle.SetHistLineWidth(1)
	# tdrStyle->SetLegoInnerR(Float_t rad = 0.5);
	# tdrStyle->SetNumberContours(Int_t number = 20);
	
	tdrStyle.SetEndErrorSize(2)
	#  tdrStyle->SetErrorMarker(20);
	tdrStyle.SetErrorX(0.)
	
	tdrStyle.SetMarkerStyle(20)
	
	#For the fit/function:
	tdrStyle.SetOptFit(1)
	tdrStyle.SetFitFormat("5.4g")
	tdrStyle.SetFuncColor(2)
	tdrStyle.SetFuncStyle(1)
	tdrStyle.SetFuncWidth(1)
	
	#For the date:
	tdrStyle.SetOptDate(0)
	# tdrStyle->SetDateX(Float_t x = 0.01);
	# tdrStyle->SetDateY(Float_t y = 0.01);
	
	# For the statistics box:
	tdrStyle.SetOptFile(0)
	tdrStyle.SetOptStat("emr") # To display the mean and RMS:   SetOptStat("mr");
	tdrStyle.SetStatColor(kWhite)
	tdrStyle.SetStatFont(42)
	tdrStyle.SetStatFontSize(0.025)
	tdrStyle.SetStatTextColor(1)
	tdrStyle.SetStatFormat("6.4g")
	tdrStyle.SetStatBorderSize(1)
	tdrStyle.SetStatH(0.1)
	tdrStyle.SetStatW(0.15)
	# tdrStyle->SetStatStyle(Style_t style = 100.1);
	# tdrStyle->SetStatX(Float_t x = 0);
	# tdrStyle->SetStatY(Float_t y = 0);
	
	# Margins:
	tdrStyle.SetPadTopMargin(0.05)
	tdrStyle.SetPadBottomMargin(0.13)
	tdrStyle.SetPadLeftMargin(0.15)
	tdrStyle.SetPadRightMargin(0.05)
	
	# For the Global title:
	tdrStyle.SetOptTitle(0)
	tdrStyle.SetTitleFont(42)
	tdrStyle.SetTitleColor(1)
	tdrStyle.SetTitleTextColor(1)
	tdrStyle.SetTitleFillColor(10)
	tdrStyle.SetTitleFontSize(0.05)
	# tdrStyle->SetTitleH(0); # Set the height of the title box
	# tdrStyle->SetTitleW(0); # Set the width of the title box
	# tdrStyle->SetTitleX(0); # Set the position of the title box
	# tdrStyle->SetTitleY(0.985); # Set the position of the title box
	# tdrStyle->SetTitleStyle(Style_t style = 100.1);
	# tdrStyle->SetTitleBorderSize(2);
	
	# For the axis titles:
	tdrStyle.SetTitleColor(1, "XYZ")
	tdrStyle.SetTitleFont(42, "XYZ")
	tdrStyle.SetTitleSize(0.06, "XYZ")
	# tdrStyle->SetTitleXSize(Float_t size = 0.02); # Another way to set the size?
	# tdrStyle->SetTitleYSize(Float_t size = 0.02);
	tdrStyle.SetTitleXOffset(0.9)
	tdrStyle.SetTitleYOffset(1.2)
	# tdrStyle->SetTitleOffset(1.1, "Y"); # Another way to set the Offset
	
	# For the axis labels:
	tdrStyle.SetLabelColor(1, "XYZ")
	tdrStyle.SetLabelFont(42, "XYZ")
	tdrStyle.SetLabelOffset(0.007, "XYZ")
	tdrStyle.SetLabelSize(0.05, "XYZ")
	
	# For the axis:
	tdrStyle.SetAxisColor(1, "XYZ")
	tdrStyle.SetStripDecimals(kTRUE)
	tdrStyle.SetTickLength(0.03, "XYZ")
	tdrStyle.SetNdivisions(408, "XYZ")
	
	#~ tdrStyle->SetNdivisions(510, "XYZ");
	tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
	tdrStyle.SetPadTickY(1)
	
	# Change for log plots:
	tdrStyle.SetOptLogx(0)
	tdrStyle.SetOptLogy(0)
	tdrStyle.SetOptLogz(0)
	
	# Postscript options:
	tdrStyle.SetPaperSize(20.,20.);
	# tdrStyle->SetLineScalePS(Float_t scale = 3);
	# tdrStyle->SetLineStyleString(Int_t i, const char* text);
	# tdrStyle->SetHeaderPS(const char* header);
	# tdrStyle->SetTitlePS(const char* pstitle);
	
	#tdrStyle->SetBarOffset(Float_t baroff = 0.5);
	#tdrStyle->SetBarWidth(Float_t barwidth = 0.5);
	#tdrStyle->SetPaintTextFormat(const char* format = "g");
	tdrStyle.SetPalette(1)
	#tdrStyle->SetTimeOffset(Double_t toffset);
	#tdrStyle->SetHistMinimumZero(kTRUE);
	
	
	
	
	ROOT.gROOT.ForceStyle()
	
	tdrStyle.cd()


def plotBlockComparison(treeBlockA,treeBlockB,variable,additionalCut,nBins,firstBin,lastBin,labelX,labelY,suffix,log=False,signal=False):	


	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	setTDRStyle()		
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()	

	legend = TLegend(0.7, 0.55, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	

	
	

	minMll = 20

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



	
	EMuhistBlockA = createHistoFromTree(treeBlockA,  variable, additionalCut, nBins, firstBin, lastBin, -1)

	EMuhistBlockB = createHistoFromTree(treeBlockB,  variable, additionalCut, nBins, firstBin, lastBin, -1)
	
	EMuhistBlockB.Scale(9.2/10.4)
	print EMuhistBlockA.Integral()
	print EMuhistBlockB.Integral()
	EMuhistBlockA.SetMarkerStyle(21)
	EMuhistBlockB.SetMarkerStyle(22)
	EMuhistBlockA.SetMarkerColor(ROOT.kGreen+3)
	EMuhistBlockB.SetMarkerColor(ROOT.kBlack)
	EMuhistBlockA.SetLineColor(ROOT.kGreen+3)
	EMuhistBlockB.SetLineColor(ROOT.kBlack)
	
	if log: 
		yMin=0.1
		yMax = max(EMuhistBlockA.GetBinContent(EMuhistBlockA.GetMaximumBin()),EMuhistBlockB.GetBinContent(EMuhistBlockB.GetMaximumBin()))*10
		plotPad.SetLogy()
	else: 
		yMin=0
		yMax = max(EMuhistBlockA.GetBinContent(EMuhistBlockA.GetMaximumBin()),EMuhistBlockB.GetBinContent(EMuhistBlockB.GetMaximumBin()))*1.5
	hCanvas.DrawFrame(firstBin,yMin,lastBin,yMax,"; %s ; %s" %(labelX,labelY))

	EMuhistBlockA.Draw("samep")
	EMuhistBlockB.Draw("samep")
	
	legend.AddEntry(EMuhistBlockA,"First 9.2 fb^{-1}","p")	
	legend.AddEntry(EMuhistBlockB,"Second 10.4 fb^{-1} scaled","p")
	#~ 
	latex = ROOT.TLatex()
	latex.SetTextSize(0.043)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.95, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 9.2-10.4 fb^{-1}")
	#~ 
		
	legend.Draw("same")
	
	ratioPad.cd()

	ratioGraphs =  ratios.RatioGraph(EMuhistBlockA,EMuhistBlockB, firstBin, lastBin,title="Bl. A / Bl. B",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kGreen+3,adaptiveBinning=0.25)

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	if signal:
		name = "OFUnblinding_SignalRegion_%s_%s.pdf"
	else:
		name = "OFUnblinding_Inclusive_%s_%s.pdf"
	if variable == "p4.M()":
		
		hCanvas.Print(name%(suffix,"Mll"))
	else:		
		hCanvas.Print(name%(suffix,variable))	
		hCanvas.Clear()
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw7412v1001Trigger/"
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

	from defs import getRegion, getPlot, getRunRange, Backgrounds

	from setTDRStyle import setTDRStyle
	from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

	from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rSFOFFact, triggerEffs
	from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
	import corrections

	from ROOT import TGraphAsymmErrors

	from locations import locations

	import ratios
	
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	cuts = "weight*(chargeProduct < 0 && %s  && abs(eta1) < 2.4 && abs(eta2) < 2.4  && p4.M() > 20 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)))"%(ptCut)


	SampleName = "TT_Powheg"
	runRange = getRunRange("Run2015_25ns")
	
	plot = getPlot("mllPlot")
	selection = getRegion("SignalInclusive")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut			
	
	eventCounts = totalNumberOfGeneratedEvents(path)
	processes = [Process(getattr(Backgrounds,"TT_Powheg"),eventCounts)]

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")


	histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
	histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
	histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
	#~ histoEE.Scale(getattr(triggerEffs,"central").effEE.valMC)
	#~ histoMM.Scale(getattr(triggerEffs,"central").effMM.valMC)	
	#~ histoEM.Scale(getattr(triggerEffs,"central").effEM.valMC)	



	histoSF = histoEE.Clone()
	histoSF.Add(histoMM)

		
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	setTDRStyle()		
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()

	legend = TLegend(0.7, 0.55, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	
	
	
	yMin=0
	yMax = 19
	plotPad.DrawFrame(20,yMin,300,yMax,"; %s ; %s" %("m_{ll}","N_{events} / 5 GeV"))
	ROOT.gStyle.SetOptStat(0)
	
	histoSF.SetFillColor(ROOT.kBlue+1)
	histoEM.SetLineColor(ROOT.kBlack)
	histoEM.SetLineWidth(3)
	histoSF.SetLineColor(ROOT.kBlue+1)
	fakeHist = ROOT.TH1F()
	fakeHist.SetLineColor(ROOT.kWhite)
	legend.SetHeader("t#bar{t} Simulation")
	legend.AddEntry(histoSF,"SF","f")
	legend.AddEntry(histoEM,"OF","l")
	
	histoEM.Scale(1.034)
	
	
	histoSF.Draw("samehist")
	histoEM.Draw("samehist")
	legend.Draw("same")
	

	#~ line2.Draw("same")

	
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
	
	#~ latex.DrawLatex(0.95, 0.96, "(8 TeV)")
	cmsExtra = "#splitline{Simulation}{Private Work}"

	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))
	
	latexCentral = ROOT.TLatex()
	latexCentral.SetTextFont(42)
	latexCentral.SetTextAlign(31)
	latexCentral.SetTextSize(0.07)
	latexCentral.SetNDC(True)	
	#~ latexCentral.DrawLatex(0.4,0.45,"Central")
	latexForward = ROOT.TLatex()
	latexForward.SetTextFont(42)
	latexForward.SetTextAlign(31)
	latexForward.SetTextSize(0.07)
	latexForward.SetNDC(True)	
	#~ latexForward.DrawLatex(0.88,0.45,"Forward")
	
	
	ratioPad.cd()
	#~ ratioGraphs =  ratios.RatioGraph(datahist,drawStack.theHistogram, xMin=mainConfig.plot.firstBin, xMax=mainConfig.plot.lastBin,title="Data / MC",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=0.25)

	ratioGraphs =  ratios.RatioGraph(histoSF,histoEM, plot.firstBin, plot.lastBin,title="SF / OF",yMin=0.5,yMax=1.5,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=0.25)
	
	x= array("f",[plot.firstBin, plot.lastBin]) 
	y= array("f", [1.0,1.0]) 
	ex= array("f", [0.,0.])
	ey= array("f", [0.014,0.014])
	ge= ROOT.TGraphErrors(2, x, y, ex, ey)
	ge.SetFillColor(ROOT.kBlue+2)
	ge.SetFillStyle(3001)
	ge.SetLineColor(ROOT.kWhite)

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)	
	ge.Draw("SAME 3")
#~ 
	line2 = ROOT.TLine(0.3,0,0.3,2)
	line2.SetLineColor(ROOT.kBlue+3)
	line2.SetLineWidth(2)
	line2.SetLineStyle(2)

	#~ line2.Draw("same")


	hCanvas.Print("SFOF.pdf")
