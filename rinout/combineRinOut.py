import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)


etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"(((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && 1.6 < TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4)",
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
	for filePath in glob("%s/sw532*.root"%path):
		sampleName = match(".*sw532v.*\.processed.*\.(.*).root", filePath).groups()[0]
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
	print path
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
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

def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

corrections = {"MergedData":{"Barrel":{"EE":[0.45,0.03],"MM":[0.55,0.03],"SF":[1.00,0.04]},"Endcap":{"EE":[0.48,0.06],"MM":[0.63,0.07],"SF":[1.11,0.07]}},
	"MergedData_BlockA":{"Barrel":{"EE":[0.47,0.03],"MM":[0.54,0.04],"SF":[1.02,0.05]},"Endcap":{"EE":[0.43,0.06],"MM":[0.57,0.08],"SF":[1.04,0.08]}},
    "MergedData_BlockB":{"Barrel":{"EE":[0.43,0.03],"MM":[0.56,0.04],"SF":[1.00,0.05]},"Endcap":{"EE":[0.53,0.07],"MM":[0.70,0.09],"SF":[1.18,0.09]}},}

	
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw532v0474/"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1
	from helpers import *	
	from defs import Backgrounds
	import defs	
	suffixA = argv[1] + "_" + argv[2] + "_BlockA"
	suffixB = argv[1] + "_" + argv[2] + "_BlockB"
	suffix = argv[1] + "_" + argv[2] + "_" + argv[3]
	useMC = False
	if len(argv) > 4:
		useMC = True
		suffix = suffix + "_MC"


	
	blockApickle = loadPickles("shelves/rInOut_Data_%s.pkl"%suffixA)
	blockBpickle = loadPickles("shelves/rInOut_Data_%s.pkl"%suffixB)






		
	nllPredictionScale	= corrections["MergedData"][argv[1]][argv[2]][0]	
	nllPredictionScaleErr	= corrections["MergedData"][argv[1]][argv[2]][1]	
		
		
	
	result = {}


	peak = blockApickle["peakSF"] + blockBpickle["peakSF"] - (blockApickle["peakOF"] + blockBpickle["peakOF"])*nllPredictionScale 
	peakError = sqrt(sqrt(blockApickle["peakSF"] + blockBpickle["peakSF"])**2 + sqrt((blockApickle["peakOF"] + blockBpickle["peakOF"])*nllPredictionScale)**2 + sqrt((blockApickle["peakOF"] + blockBpickle["peakOF"])*nllPredictionScaleErr*nllPredictionScale)**2 )
	continuum = blockApickle["continuumSF"] + blockBpickle["continuumSF"] - (blockApickle["continuumOF"] + blockBpickle["continuumOF"])*nllPredictionScale 
	continuumError =  sqrt(sqrt(blockApickle["continuumSF"] + blockBpickle["continuumSF"])**2 + sqrt((blockApickle["continuumOF"] + blockBpickle["continuumOF"])*nllPredictionScale)**2 + sqrt((blockApickle["continuumOF"] + blockBpickle["continuumOF"])*nllPredictionScaleErr*nllPredictionScale)**2 )
	result["peakSF"] = blockApickle["peakSF"] + blockBpickle["peakSF"]
	result["peakOF"] = blockApickle["peakOF"] + blockBpickle["peakOF"]
	result["continuumSF"] =blockApickle["continuumSF"] + blockBpickle["continuumSF"] 
	result["continuumOF"] = blockApickle["continuumOF"] + blockBpickle["continuumOF"]

		
	result["peak"] = peak
	result["peakError"] = peakError
	result["continuum"] = continuum
	result["continuumError"] = continuumError
	result["correction"] = 	nllPredictionScale
	result["correctionErr"] = 	nllPredictionScaleErr
	
	Rinout =   continuum / peak

	ErrRinoutSyst = Rinout*0.25

	ErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
	print "R_{in,out} = %f \pm %f (stat.) \pm \%f (syst) "%(Rinout,ErrRinout,ErrRinoutSyst) 	
	ErrRinoutTotal = sqrt(ErrRinoutSyst**2 + ErrRinout**2)

	result["rInOut"] = Rinout
	result["rInOutErr"] = ErrRinout
	result["rInOutSyst"] = ErrRinoutSyst

	if not useMC:
		outFilePkl = open("shelves/rInOut_Data_%s.pkl"%suffix,"w")
	else:
		outFilePkl = open("shelves/rInOut_MC_%s.pkl"%suffix,"w")
	pickle.dump(result, outFilePkl)
	outFilePkl.close()	
	
