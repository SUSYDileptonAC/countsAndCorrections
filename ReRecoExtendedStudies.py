import ROOT
import numpy as np

from math import sqrt
attic = []

import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

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
	
def readTreeFromFileReReco(path, dileptonCombination):
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
def getFilePathsAndSampleNamesReReco(path):
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
def readTreesReReco(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print (path)
	for sampleName, filePath in getFilePathsAndSampleNamesReReco(path).iteritems():
		
		result[sampleName] = readTreeFromFileReReco(filePath, dileptonCombination)
		
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
	tdrStyle.SetPadLeftMargin(0.2)
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
	tdrStyle.SetTitleYOffset(1.5)
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
	
labels = {"met":["#Delta MET_{x,y} [GeV]","Events / 0.5 GeV","DeltaMET"],"ptMu":["#Delta p_{T}^{#mu} [GeV]","Events / 0.05 GeV","DeltaPtMu"],"ptEle":["#Delta p_{T}^{ele} [GeV]","Events / 0.05 GeV","DeltaPtEle"],"mllEE":["#Delta m_{ee} [GeV]","Events / 0.05 GeV","DeltaMllEE"],"overlay":["#Delta m_{ll} [GeV]","Events / 0.05 GeV","MllOveraly"],"mllMM":["#Delta m_{#mu#mu} [GeV]","Events / 0.05 GeV","DeltaMllMM"],"mllEM":["#Delta m_{e#mu} [GeV]","Events / 0.05 GeV","DeltaMllEM"],"jetPt":["#Delta p_{T}^{first two jets} [GeV]","Events / 0.5 GeV","DeltaJetPt"]}	
	
def plotResolutionHist(hist,name,firstBin,lastBin,suffix,log=False,signal=True):	


	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()		
	plotPad.UseCurrentStyle()
	plotPad.Draw()
	plotPad.cd()

	legend = TLegend(0.7, 0.55, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	

	
	

	#~ plotPad.SetOptStat(0)
	ROOT.gStyle.SetOptStat(0)
	#~ ROOT.gStyle.SetOptFit(0)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.03)
	Labelout.SetNDC(True)
	Labelout.SetTextColor(ROOT.kBlack)



	
	if log: 
		yMin=0.1
		yMax = hist.GetBinContent(hist.GetMaximumBin())*10
		plotPad.SetLogy()
	else: 
		yMin=0
		yMax = hist.GetBinContent(hist.GetMaximumBin())*1.5
	hCanvas.DrawFrame(firstBin,yMin,lastBin,yMax,"; %s ; %s" %(labels[name][0],labels[name][1]))

	gaus = TF1("gauss","gaus",firstBin,lastBin)

	hist.Fit("gauss")
	hCanvas.DrawFrame(firstBin,yMin,lastBin,yMax,"; %s ; %s" %(labels[name][0],labels[name][1]))
	
	hist.Draw("samepe")
	Labelout.DrawLatex(0.3,0.85,"Gauss: mean = %.2f#pm%.2f, #sigma = %.2f#pm%.2f, #Chi^{2}/N_{dof} = %.2f"%(gaus.GetParameter(1),gaus.GetParError(1),gaus.GetParameter(2),gaus.GetParError(2),gaus.GetChisquare()/gaus.GetNDF()))
	#~ legend.AddEntry(EMuhistBlockA,"Prompt Reco RunC","p")	
	#~ legend.AddEntry(EMuhistBlockB,"Jan22 ReReco RunC","p")
	#~ 
	latex = ROOT.TLatex()
	latex.SetTextSize(0.043)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.95, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 19.4-19.8 fb^{-1}")
	#~ 
		
	#~ legend.Draw("same")
	
	if signal:
		if log:
		
			plotName = "ReRecoResolution_SignalRegion_%s_%s_Log.pdf"
		else:	
			plotName = "ReRecoResolution_SignalRegion_%s_%s.pdf"
		
	else:
		if log:
			plotName = "ReRecoResolution_Inclusive_%s_%s_Log.pdf"
		else:	
			plotName = "ReRecoResolution_Inclusive_%s_%s.pdf"

	hCanvas.Print(plotName%(suffix,labels[name][2]))	
	hCanvas.Clear()	
def plotOverlay(histEE,histMM,histEM,name,firstBin,lastBin,suffix,log=False,signal=True):	


	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	setTDRStyle()		

	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	setTDRStyle()		
	plotPad.UseCurrentStyle()
	plotPad.Draw()
	plotPad.cd()	
	
	legend = TLegend(0.7, 0.55, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	

	
	


	ROOT.gStyle.SetOptStat(0)
	Labelout = ROOT.TLatex()
	Labelout.SetTextAlign(12)
	Labelout.SetTextSize(0.03)
	Labelout.SetNDC(True)
	Labelout.SetTextColor(ROOT.kBlack)



	
	if log: 
		yMin=0.1
		yMax = histMM.GetBinContent(histMM.GetMaximumBin())*10
		plotPad.SetLogy()
	else: 
		yMin=0
		yMax = histMM.GetBinContent(histMM.GetMaximumBin())*1.5
	hCanvas.DrawFrame(firstBin,yMin,lastBin,yMax,"; %s ; %s" %(labels[name][0],labels[name][1]))

	#~ gaus = TF1("gauss","gaus",firstBin,lastBin)
#~ 
	#~ hist.Fit("gauss")
	#~ hCanvas.DrawFrame(firstBin,yMin,lastBin,yMax,"; %s ; %s" %(labels[name][0],labels[name][1]))
	#~ 
	histEE.Draw("samepe")
	histEE.SetMarkerStyle(21)
	histEE.SetMarkerColor(ROOT.kRed+2)
	histEE.SetLineColor(ROOT.kRed+2)
	histMM.Draw("samepe")
	histMM.SetMarkerStyle(22)
	histMM.SetMarkerColor(ROOT.kBlue-1)
	histMM.SetLineColor(ROOT.kBlue-1)
	histEM.Draw("samepe")
	histEM.SetMarkerStyle(23)
	#~ Labelout.DrawLatex(0.3,0.85,"Gauss: mean = %.2f, #sigma = %.2f, #Chi^{2}/N_{dof} = %.2f"%(gaus.GetParameter(1),gaus.GetParameter(2),gaus.GetChisquare()/gaus.GetNDF()))
	legend.AddEntry(histEE,"ee events","p")	
	legend.AddEntry(histMM,"#mu#mu events","p")	
	legend.AddEntry(histEM,"e#mu events","p")	
	#~ legend.AddEntry(EMuhistBlockB,"Jan22 ReReco RunC","p")
	#~ 
	latex = ROOT.TLatex()
	latex.SetTextSize(0.043)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.95, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 19.4-19.8 fb^{-1}")
	#~ 
		
	legend.Draw("same")
	

	if signal:
		if log:
		
			plotName = "ReRecoResolution_SignalRegion_%s_%s_Log.pdf"
		else:	
			plotName = "ReRecoResolution_SignalRegion_%s_%s.pdf"
		
	else:
		if log:
			plotName = "ReRecoResolution_Inclusive_%s_%s_Log.pdf"
		else:	
			plotName = "ReRecoResolution_Inclusive_%s_%s.pdf"

	hCanvas.Print(plotName%(suffix,labels[name][2]))	
	hCanvas.Clear()	
	
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw538v0477/"
	pathReReco = "/home/jan/Trees/sw538v0478/"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1, TH2F, TF1
	import ratios
	
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
	
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	etaCut = etaCuts[argv[1]]
	suffix = argv[1]
	
	#~ runCut = "runNr < 201657 && runNr > 198522 && !(runNr == 199832 || runNr == 199834 || runNr == 199967 || runNr == 200160 || runNr == 200161 || runNr == 200174 || runNr == 200177 || runNr == 200178 || runNr == 200186 || runNr == 201191)"
	runCut = "runNr < 999999"

	#~ cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCut
	cuts = "weight*(chargeProduct < 0 && %s && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && deltaR > 0.3 && %s && abs(eta1) < 2.4 && abs(eta2) < 2.4)"%(ptCut,etaCut,runCut)
	print cuts
	nEvents=-1
	
	lumi = 9.2
	

	minMll = 20
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	ROOT.gStyle.SetOptStat(0)
	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")
	EMutreesReReco = readTreesReReco(pathReReco, "EMu")
	EEtreesReReco = readTreesReReco(pathReReco, "EE")
	MuMutreesReReco = readTreesReReco(pathReReco, "MuMu")
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
	nBins = 56
	firstBin = 20
	lastBin = 300
	
	SampleName = "MergedData"
	SampleNameReReco = "MergedData"
	print EEtrees
	for name, tree in EEtrees.iteritems():
		if name == SampleName:
			EEhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			eeTreeSignal = tree.CopyTree(cuts)			
			eeTree = tree.Clone()			
	for name, tree in MuMutrees.iteritems():
		if name == SampleName:
			MuMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			mmTreeSignal = tree.CopyTree(cuts)
			mmTree = tree.Clone()
	for name, tree in EMutrees.iteritems():
		if name == SampleName:
			EMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			emTreeSignal = tree.CopyTree(cuts)
			emTree = tree.Clone()

	for name, tree in EEtreesReReco.iteritems():
		if name == SampleNameReReco:
			EEhistReReco = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			eeTreeReRecoSignal = tree.CopyTree(cuts)		
			eeTreeReReco = tree.Clone()		
	for name, tree in MuMutreesReReco.iteritems():
		if name == SampleNameReReco:
			mmTreeReRecoSignal = tree.CopyTree(cuts)
			mmTreeReReco = tree.Clone()
			MuMuhistReReco = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)		
	for name, tree in EMutreesReReco.iteritems():
		if name == SampleNameReReco:
			EMuhistReReco = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			emTreeReRecoSignal = tree.CopyTree(cuts)
			emTreeReReco = tree.Clone()

	eeCountTree = eeTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	mmCountTree = mmTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	emCountTree = emTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	eeCountTreeReReco = eeTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	mmCountTreeReReco = mmTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	emCountTreeReReco = emTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	


	metHist = TH1F("metHist","metHist",200,-50,50)
	ptHistMu = TH1F("ptHistMu","ptHistMu",200,-5,5)
	ptHistEle = TH1F("ptHistEle","ptHistEle",200,-5,5)
	mllHistEE = TH1F("mllHistEE","mllHistEE",200,-5,5)
	mllHistEM = TH1F("mllHistEM","mllHistEM",200,-5,5)
	mllHistMM = TH1F("mllHistMM","mllHistMM",200,-5,5)
	jetPtHist = TH1F("jetPtHist","jetPtHist",200,-50,50)
	
	for ev in eeCountTree:
		for ev2 in eeCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr):
				print "Filling"
				metHist.Fill(ev2.vMet.Px()-ev.vMet.Px())
				metHist.Fill(ev2.vMet.Py()-ev.vMet.Py())
				ptHistEle.Fill(ev2.pt1 - ev.pt1)
				ptHistEle.Fill(ev2.pt2 - ev.pt2)
				mllHistEE.Fill(ev2.p4.M() - ev.p4.M())
				jetPtHist.Fill(ev2.jet1pt - ev.jet1pt)
				jetPtHist.Fill(ev2.jet2pt - ev.jet2pt)
				
	for ev in mmCountTree:
		for ev2 in mmCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr):
				metHist.Fill(ev2.vMet.Px()-ev.vMet.Px())
				metHist.Fill(ev2.vMet.Py()-ev.vMet.Py())
				ptHistMu.Fill(ev2.pt1 - ev.pt1)
				ptHistMu.Fill(ev2.pt2 - ev.pt2)
				mllHistMM.Fill(ev2.p4.M() - ev.p4.M())
				jetPtHist.Fill(ev2.jet1pt - ev.jet1pt)
				jetPtHist.Fill(ev2.jet2pt - ev.jet2pt)				
				
	for ev in emCountTree:
		for ev2 in emCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr):
				metHist.Fill(ev2.vMet.Px()-ev.vMet.Px())
				metHist.Fill(ev2.vMet.Py()-ev.vMet.Py())
				ptHistEle.Fill(ev2.pt1 - ev.pt1)
				ptHistMu.Fill(ev2.pt2 - ev.pt2)
				mllHistEM.Fill(ev2.p4.M() - ev.p4.M())
				jetPtHist.Fill(ev2.jet1pt - ev.jet1pt)
				jetPtHist.Fill(ev2.jet2pt - ev.jet2pt)				
		
	
	
	
	plotResolutionHist(metHist,"met",-50,50,suffix,log=False)
	plotResolutionHist(ptHistEle,"ptEle",-5,5,suffix,log=False)
	plotResolutionHist(ptHistMu,"ptMu",-5,5,suffix,log=False)
	plotOverlay(mllHistEE,mllHistMM,mllHistEM,"overlay",-5,5,suffix,log=False)	
	plotResolutionHist(mllHistEE,"mllEE",-5,5,suffix,log=False)
	plotResolutionHist(mllHistEM,"mllEM",-5,5,suffix,log=False)
	plotResolutionHist(mllHistMM,"mllMM",-5,5,suffix,log=False)
	plotResolutionHist(jetPtHist,"jetPt",-50,50,suffix,log=False)
	
	plotResolutionHist(metHist,"met",-50,50,suffix,log=True)
	plotResolutionHist(ptHistEle,"ptEle",-5,5,suffix,log=True)
	plotResolutionHist(ptHistMu,"ptMu",-5,5,suffix,log=True)
	plotOverlay(mllHistEE,mllHistMM,mllHistEM,"overlay",-5,5,suffix,log=True)	
	plotResolutionHist(mllHistEE,"mllEE",-5,5,suffix,log=True)
	plotResolutionHist(mllHistEM,"mllEM",-5,5,suffix,log=True)
	plotResolutionHist(mllHistMM,"mllMM",-5,5,suffix,log=True)
	plotResolutionHist(jetPtHist,"jetPt",-50,50,suffix,log=True)
