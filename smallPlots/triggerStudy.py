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
	result.Add("%s/cutsV25DileptonMiniAODTriggerFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	return result
def readTreeFromFileTrigger(path,trigger, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV25DileptonMiniAODTriggerHLT%sFinalTrees/%sDileptonTree"%(path,trigger, dileptonCombination))	
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
	for filePath in glob("%s/sw74*.root"%path):
		sampleName = match(".*sw74.*\.cutsV25DileptonMiniAODTrigger.*\.(.*).root", filePath).groups()[0]
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
def readTreesTrigger(path,trigger, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFileTrigger(filePath,trigger, dileptonCombination)
		
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



if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw74XUnprocessed/"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1
	import ratios

	
	ptCut = "(pt1 > 20 && pt2 > 30 || pt1 > 30 && pt2 > 20)"
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	cuts = "(chargeProduct < 0 && %s  && abs(eta1) < 2.4 && abs(eta2) < 2.4 && p4.M()>20 && deltaR > 0.3  && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)))"%(ptCut)


	SampleName = "TTJets_aMCatNLO_FXFX_Spring15_25ns"

	

	eeTrees = readTrees(path, "EE")	
	mmTrees = readTrees(path, "MuMu")	
	emTrees = readTrees(path, "EMu")	
	eeTreesTrigger = readTreesTrigger(path,"DiEle", "EE")	
	mmTreesTrigger = readTreesTrigger(path,"DiMu", "MuMu")	
	emTreesTrigger = readTreesTrigger(path,"MuEG", "EMu")
	
	variables = {"mll":"p4.M()","leadingPt":"(pt1 > pt2)*pt1 + (pt2 > pt1)*pt2","trailingPt":"(pt1 > pt2)*pt2 + (pt2 > pt1)*pt1"}
	xLables = {"mll":"m_{ll} [GeV]","leadingPt":"p_{T}^{leading}","trailingPt":"p_{T}^{trailing}"}
	
	for var in ["mll","leadingPt","trailingPt"]:	
		for name, tree in eeTrees.iteritems():
			if name == SampleName:
				eeHist = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)
				#~ eeHist.Scale(1./tree.GetEntries())
		for name, tree in mmTrees.iteritems():
			if name == SampleName:
				mmHist = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)
				#~ mmHist.Scale(1./tree.GetEntries())
		for name, tree in emTrees.iteritems():
			if name == SampleName:
				emHist = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)
				
		for name, tree in eeTreesTrigger.iteritems():
			if name == SampleName:
				eeHistTrigger = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)
				#~ eeHist.Scale(1./tree.GetEntries())
		for name, tree in mmTreesTrigger.iteritems():
			if name == SampleName:
				mmHistTrigger = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)
				#~ mmHist.Scale(1./tree.GetEntries())
		for name, tree in emTreesTrigger.iteritems():
			if name == SampleName:
				emHistTrigger = createHistoFromTree(tree, variables[var], cuts, 56, 20, 300, nEvents = -1)

		effEE = ROOT.TGraphAsymmErrors(eeHistTrigger,eeHist,"cp")
		effEM = ROOT.TGraphAsymmErrors(emHistTrigger,emHist,"cp")
		effMM = ROOT.TGraphAsymmErrors(mmHistTrigger,mmHist,"cp")

		effEE.SetMarkerStyle(20)
		effEM.SetMarkerStyle(21)
		effMM.SetMarkerStyle(22)
		effEE.SetMarkerColor(ROOT.kBlack)
		effEM.SetMarkerColor(ROOT.kBlue)
		effMM.SetMarkerColor(ROOT.kRed)
		effEE.SetLineColor(ROOT.kBlack)
		effEM.SetLineColor(ROOT.kBlue)
		effMM.SetLineColor(ROOT.kRed)

		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		setTDRStyle()		
		plotPad.UseCurrentStyle()
		plotPad.Draw()	
		

		legend = TLegend(0.7, 0.5, 0.95, 0.75)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)
		
		
		
		yMin=0
		yMax = max(eeHist.GetBinContent(eeHist.GetMaximumBin()),emHist.GetBinContent(mmHist.GetMaximumBin()))*1.5
		hCanvas.DrawFrame(0,0.5,300,1,"; %s ; %s" %(xLables[var],"trigger efficiency"))
		ROOT.gStyle.SetOptStat(0)
		
		eeHist.SetLineColor(ROOT.kRed)
		eeHist.SetLineStyle(2)
		eeHist.SetLineWidth(2)
		#~ eeHist.SetLineColor(ROOT.kRed)
		fakeHist = ROOT.TH1F()
		fakeHist.SetLineColor(ROOT.kWhite)
		#~ legend.SetHeader("t#bar{t} Simulation")
		legend.AddEntry(effEE,"ee","p")
		legend.AddEntry(effMM,"#mu#mu","p")
		legend.AddEntry(effEM,"e#mu","p")
		
		
		effEE.Draw("samepe")
		effEM.Draw("samepe")
		effMM.Draw("samepe")
		legend.Draw("same")
		line1 = ROOT.TLine(0.3,0,0.3,yMax)
		line2 = ROOT.TLine(1.6,0,1.6,yMax)
		line1.SetLineColor(ROOT.kBlue+3)
		line2.SetLineColor(ROOT.kBlue+3)

		line1.SetLineWidth(2)
		line2.SetLineWidth(2)
		line1.SetLineStyle(2)
		line2.SetLineStyle(2)

		#~ line1.Draw("same")
		#~ line2.Draw("same")

		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		#latexCMS.SetTextAlign(31)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		#latexCMSExtra.SetTextAlign(31)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)		
		
		latex.DrawLatex(0.95, 0.96, "(13 TeV)")
		cmsExtra = "Simulation Private Work"

		latexCMS.DrawLatex(0.15,0.955,"CMS")
		latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))				
					
			#~ else:
				#~ latexCMS.DrawLatex(0.19,0.89,"CMS")
				#~ latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra))	
		#~ 
		
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
		
		



		hCanvas.Print("triggerEffs_%s.pdf"%var)
