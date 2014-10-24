import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)


etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"(((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2))) && abs(eta1) < 2.4 && abs(eta2) < 2.4",
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
def readTreeFromFileDoubleMu(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV23DileptonDoubleMuFinalTrees/%sDileptonTree"%(path, dileptonCombination))
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
	#~ print path
	for filePath in glob("%s/sw538*.root"%path):
		#~ print filePath
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
	#~ print (path)
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
	tdrStyle.SetPadLeftMargin(0.13)
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
	tdrStyle.SetTitleYOffset(1.1)
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
	
def getUncert(sf,of,factorUncert):

		result = (sf + of + (of*factorUncert)**2)**0.5
		return result
		
if (__name__ == "__main__"):
	setTDRStyle()
	#~ path = "missing16JanEvent.cutsV23DileptonDoubleMu.AOD.root"
	path = "/home/jan/Trees/sw538v0476/sw538v0476.processed.MergedData.root"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1, TGraphErrors
	import ratios
	from messageLogger import messageLogger as log
	import numpy


	#~ (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20) && chargeProduct==-1 && (runNr < 207833 || runNr > 208307) && (runNr > 201678 || (runNr >= 198022 && runNr <= 198523) || runNr == 201671 || runNr == 201669 || runNr == 201668 || runNr == 201658 || runNr == 201657 || runNr == 200976 || runNr == 200961 || (runNr == 200229 && (lumiSec == 532 || lumiSec == 533)) || (runNr == 199812 && (lumiSec >= 182 && lumiSec <= 186)) || runNr == 190782 || runNr == 190895 || runNr == 190906 || runNr == 190945 || runNr == 190949 || runNr == 190646 || runNr == 190659 || runNr == 190679 || runNr == 190688 || runNr == 190702 || runNr == 190703 || runNr == 190706 || runNr == 190707 || runNr == 190708 || runNr == 190733 || runNr == 190736 || (runNr == 191271 && lumiSec >= 159) || runNr == 193192 || runNr == 193193 || runNr == 194631 || (runNr == 195540 && lumiSec <=120) || runNr == 201191) && not(runNr == 190705 && ((lumiSec >= 66 && lumiSec <= 76) || (lumiSec >=78 && lumiSec < 80))) && not(runNr == 190705 && ((lumiSec >= 66 && lumiSec <= 76) || (lumiSec >=78 && lumiSec < 80))) && not(runNr == 191830 && (lumiSec >= 243 && lumiSec <= 244)) && not(runNr == 194115 && (lumiSec >= 732 && lumiSec <= 818)) && not(runNr == 194223 && (lumiSec >= 9 && lumiSec <= 51)) && not(runNr == 195016 && ((lumiSec >= 252 && lumiSec <= 253) || (lumiSec >=561 && lumiSec < 562))) && not(runNr == 195774 && lumiSec == 138) && not(runNr == 195918 && lumiSec == 45)
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)


	setTDRStyle()		
	

	legend = TLegend(0.7, 0.55, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	etaCut = etaCuts[argv[1]]
	suffix = argv[1]	
	label = "Central"
	if suffix == "Endcap":
		label = "Forward"
	treeOF = readTreeFromFile(path, "EMu").CopyTree("nJets >=2 && met > 100")
	treeEE = readTreeFromFile(path, "EE").CopyTree("nJets >=2 && met > 100")
	treeMM = readTreeFromFile(path, "MuMu").CopyTree("nJets >=2 && met > 100")
#~ 

	nBins = 10000
	firstBin = 0
	lastBin = 1000

	
	lumi = 19.4
	

	minMll = 20
	legend = TLegend(0.15, 0.7, 0.6, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	legend.SetTextFont(42)
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
	
	variable = "p4.M()"
	
	#~ sfList = [98,108,94,104,79,86,87,81,84,34]
	#~ ofList = [78,65,60,73,70,87,75,78,89,35]
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
	
	factor = 1.0
	factorUncert = 0.04
	if suffix == "Endcap":
		factor = 1.11
		factorUncert = 0.07
	for cutPair in runCuts:
		cuts = "weight*(chargeProduct < 0 && %s && p4.M() > 20 && p4.M() < 70 && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && runNr >= %d && runNr <= %d && deltaR > 0.3)"%(ptCut,etaCut,runCuts[0][0],cutPair[1])
		cutsBTagged = "weight*(chargeProduct < 0 && %s && p4.M() > 20 && p4.M() < 70 && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && runNr >= %d && runNr <= %d && deltaR > 0.3 && nBJets >= 1)"%(ptCut,etaCut,cutPair[0],cutPair[1])
		cutsBVeto = "weight*(chargeProduct < 0 && %s && p4.M() > 20 && p4.M() < 70 && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && runNr >= %d && runNr <= %d && deltaR > 0.3 && nBJets == 0)"%(ptCut,etaCut,cutPair[0],cutPair[1])
		eeHist = createHistoFromTree(treeEE,  variable, cuts, nBins, firstBin, lastBin, -1)
		mmHist = createHistoFromTree(treeMM,  variable, cuts, nBins, firstBin, lastBin, -1)
		emHist = createHistoFromTree(treeOF,  variable, cuts, nBins, firstBin, lastBin, -1)
		eeHistBTagged = createHistoFromTree(treeEE,  variable, cutsBTagged, nBins, firstBin, lastBin, -1)
		mmHistBTagged = createHistoFromTree(treeMM,  variable, cutsBTagged, nBins, firstBin, lastBin, -1)
		emHistBTagged = createHistoFromTree(treeOF,  variable, cutsBTagged, nBins, firstBin, lastBin, -1)
		eeHistBVeto = createHistoFromTree(treeEE,  variable, cutsBVeto, nBins, firstBin, lastBin, -1)
		mmHistBVeto = createHistoFromTree(treeMM,  variable, cutsBVeto, nBins, firstBin, lastBin, -1)
		emHistBVeto = createHistoFromTree(treeOF,  variable, cutsBVeto, nBins, firstBin, lastBin, -1)
		
		ee = eeHist.Integral() 
		mm = mmHist.Integral() 
		sf = eeHist.Integral() + mmHist.Integral()
		of = emHist.Integral()*factor
		eeBTagged = eeHistBTagged.Integral() 
		mmBTagged = mmHistBTagged.Integral() 
		sfBTagged = eeHistBTagged.Integral() + mmHistBTagged.Integral()
		ofBTagged = emHistBTagged.Integral()
		eeBVeto = eeHistBVeto.Integral() 
		mmBVeto = mmHistBVeto.Integral() 
		sfBVeto = eeHistBVeto.Integral() + mmHistBVeto.Integral()
		ofBVeto = emHistBVeto.Integral()
		print ee, mm, sf, of, getUncert(sf,of,factorUncert)
		
		yValues.append(sf-of)
		yValuesUncert.append(getUncert(sf,of,factorUncert))
		sfList.append(sf)
		ofList.append(of)
		sfValuesUncert.append(sf**0.5)
		ofValuesUncert.append((of+(of*factorUncert)**2)**0.5)
		print "hallo1"		
		yValuesBTagged.append(sfBTagged-ofBTagged)
		yValuesUncertBTagged.append(getUncert(sfBTagged,ofBTagged,factorUncert))
		sfListBTagged.append(sfBTagged)
		ofListBTagged.append(ofBTagged)
		sfValuesUncertBTagged.append(sfBTagged**0.5)
		ofValuesUncertBTagged.append(ofBTagged**0.5)	
		print "hallo2"	
		yValuesBVeto.append(sfBVeto-ofBVeto)
		yValuesUncertBVeto.append(getUncert(sfBVeto,ofBVeto,factorUncert))
		sfListBVeto.append(sfBVeto)
		ofListBVeto.append(ofBVeto)
		sfValuesUncertBVeto.append(sfBVeto**0.5)
		ofValuesUncertBVeto.append(ofBVeto**0.5)
		print "hallo3"		
		eeList.append(ee)
		mmList.append(mm)
		eeValuesUncert.append(ee**0.5)
		mmValuesUncert.append(mm**0.5)		
	#~ for i in range(0,10):
#~ 
		#~ 
		#~ sf = sfList[i]
		#~ of = ofList[i]
		#~ print sf, of, getUncert(sf,of)
		#~ yValues.append(sf-of)
		#~ yValuesUncert.append(getUncert(sf,of))
		#~ sfValuesUncert.append(sf**0.5)
		#~ ofValuesUncert.append(of**0.5)
	if suffix == "Endcap":
		hCanvas.DrawFrame(0,-20,20,200,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
		
	else:	
		hCanvas.DrawFrame(0,-20,20,1000,"; %s ; %s" %("integrated luminosity [fb^{-1}]","Events"))
	arg2 = numpy.array(xValues,"d")
	arg4 = numpy.array(xValuesUncert,"d")
	print "hallo4"
	print yValues
	arg3 = numpy.array(yValues,"d")
	arg5 = numpy.array(yValuesUncert,"d")	
	print sfList
	print ofList	
	sfArray = numpy.array(sfList,"d")
	ofArray = numpy.array(ofList,"d")
	sfUncertArray = numpy.array(sfValuesUncert,"d")
	ofUncertArray = numpy.array(ofValuesUncert,"d")
	print "hallo5"
	print yValuesBTagged
	print yValuesUncertBTagged
	arg3BTagged = numpy.array(yValuesBTagged,"d")
	arg5BTagged = numpy.array(yValuesUncertBTagged,"d")	
		
	sfArrayBTagged = numpy.array(sfListBTagged,"d")
	ofArrayBTagged = numpy.array(ofListBTagged,"d")
	sfUncertArrayBTagged = numpy.array(sfValuesUncertBTagged,"d")
	ofUncertArrayBTagged = numpy.array(ofValuesUncertBTagged,"d")
	print "hallo6"
	arg3BVeto = numpy.array(yValuesBVeto,"d")
	arg5BVeto = numpy.array(yValuesUncertBVeto,"d")	
		
	sfArrayBVeto = numpy.array(sfListBVeto,"d")
	ofArrayBVeto = numpy.array(ofListBVeto,"d")
	sfUncertArrayBVeto = numpy.array(sfValuesUncertBVeto,"d")
	ofUncertArrayBVeto = numpy.array(ofValuesUncertBVeto,"d")
	print "hallo7"
	eeArray = numpy.array(eeList,"d")
	mmArray = numpy.array(mmList,"d")
	eeUncertArray = numpy.array(eeValuesUncert,"d")
	mmUncertArray = numpy.array(mmValuesUncert,"d")
	

	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graph = ROOT.TGraphErrors(10,arg2,arg3,arg4,arg5)
	graphSF = ROOT.TGraphErrors(10,arg2,sfArray,arg4,sfUncertArray)
	graphOF = ROOT.TGraphErrors(10,arg2,ofArray,arg4,ofUncertArray)
	print "hallo8"
	graphBTagged = ROOT.TGraphErrors(10,arg2,arg3BTagged,arg4,arg5BTagged)
	print "hallo33"
	graphSFBTagged = ROOT.TGraphErrors(10,arg2,sfArrayBTagged,arg4,sfUncertArrayBTagged)
	print "hallo44"
	graphOFBTagged = ROOT.TGraphErrors(10,arg2,ofArrayBTagged,arg4,ofUncertArrayBTagged)
	print "hallo22"
	graphBVeto = ROOT.TGraphErrors(10,arg2,arg3BVeto,arg4,arg5BVeto)
	graphSFBVeto = ROOT.TGraphErrors(10,arg2,sfArrayBVeto,arg4,sfUncertArrayBVeto)
	graphOFBVeto = ROOT.TGraphErrors(10,arg2,ofArrayBVeto,arg4,ofUncertArrayBVeto)
	print "hallo9"
	graphEE = ROOT.TGraphErrors(10,arg2,eeArray,arg4,eeUncertArray)
	graphMM = ROOT.TGraphErrors(10,arg2,mmArray,arg4,mmUncertArray)
	graph.Draw("Psame")
	graphSF.Draw("Psame")
	graphSF.SetLineColor(ROOT.kRed)
	graphSF.SetMarkerColor(ROOT.kRed)
	graphOF.Draw("Psame")
	graphOF.SetLineColor(ROOT.kBlue)
	graphOF.SetMarkerColor(ROOT.kBlue)
	
	print "hallo10"	
	#~ graphEE.Draw("Psame")
	#~ graphEE.SetLineColor(ROOT.kGreen+3)
	#~ graphEE.SetMarkerColor(ROOT.kGreen+3)
	#~ graphMM.Draw("Psame")
	#~ graphMM.SetLineColor(ROOT.kGreen-2)
	#~ graphMM.SetMarkerColor(ROOT.kGreen-2)	
	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	legend.AddEntry(legendHistDing,"Signal Region %s"%label,"h")	
	
	legend.AddEntry(graphSF,"Same Flavour","p")	
	legend.AddEntry(graphOF,"Prediction from Opposite Flavour","p")	
	legend.AddEntry(graph,"N_{SF}-N_{prediction}","p")	
	#~ legend.AddEntry(graph,"SF - OF","p")	
	legend.Draw("same")
	
	
	
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
	latex.DrawLatex(0.98, 0.96, "%s fb^{-1} (8 TeV)"%("19.4",))
	

	cmsExtra = "Unpublished"		
	latexCMS.DrawLatex(0.15,0.955,"CMS")
	latexCMSExtra.DrawLatex(0.28,0.955,"%s"%(cmsExtra))	
	
	
	hCanvas.Print("YieldvsLumi_%s.pdf"%suffix)
	
	hCanvas.DrawFrame(0,-20,11,150,"; %s ; %s" %("# lumi block","Events / approx. 2fb^{-1}"))
	legend.Clear()
	graphBTagged.Draw("Psame")
	graphSFBTagged.Draw("Psame")
	graphSFBTagged.SetLineColor(ROOT.kRed)
	graphSFBTagged.SetMarkerColor(ROOT.kRed)
	graphOFBTagged.Draw("Psame")
	graphOFBTagged.SetLineColor(ROOT.kBlue)
	graphOFBTagged.SetMarkerColor(ROOT.kBlue)
	
		
	#~ graphEE.Draw("Psame")
	#~ graphEE.SetLineColor(ROOT.kGreen+3)
	#~ graphEE.SetMarkerColor(ROOT.kGreen+3)
	#~ graphMM.Draw("Psame")
	#~ graphMM.SetLineColor(ROOT.kGreen-2)
	#~ graphMM.SetMarkerColor(ROOT.kGreen-2)	
	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	legend.AddEntry(legendHistDing,"Signal Region %s - b-Tagged"%suffix,"h")		
	
	legend.AddEntry(graphSFBTagged,"Same Flavour","p")	
	legend.AddEntry(graphOFBTagged,"Opposite Flavour","p")	
	legend.AddEntry(graphBTagged,"N_{SF}-N_{OF}","p")	
	#~ legend.AddEntry(graph,"SF - OF","p")	
	legend.Draw("same")
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.96, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")
	
	hCanvas.Print("YieldvsLumi_BTagged_%s.pdf"%suffix)
	
	hCanvas.DrawFrame(0,-20,11,150,"; %s ; %s" %("# lumi block","Events / approx. 2fb^{-1}"))
	legend.Clear()
	graphBVeto.Draw("Psame")
	graphSFBVeto.Draw("Psame")
	graphSFBVeto.SetLineColor(ROOT.kRed)
	graphSFBVeto.SetMarkerColor(ROOT.kRed)
	graphOFBVeto.Draw("Psame")
	graphOFBVeto.SetLineColor(ROOT.kBlue)
	graphOFBVeto.SetMarkerColor(ROOT.kBlue)
	
		
	#~ graphEE.Draw("Psame")
	#~ graphEE.SetLineColor(ROOT.kGreen+3)
	#~ graphEE.SetMarkerColor(ROOT.kGreen+3)
	#~ graphMM.Draw("Psame")
	#~ graphMM.SetLineColor(ROOT.kGreen-2)
	#~ graphMM.SetMarkerColor(ROOT.kGreen-2)	
	
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	legend.AddEntry(legendHistDing,"Signal Region %s - b-Veto"%suffix,"h")		
	
	legend.AddEntry(graphSFBVeto,"Same Flavour","p")	
	legend.AddEntry(graphOFBVeto,"Opposite Flavour","p")	
	legend.AddEntry(graphBVeto,"N_{SF}-N_{OF}","p")	
	#~ legend.AddEntry(graph,"SF - OF","p")	
	legend.Draw("same")
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.96, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 19.4 fb^{-1}")
	
	hCanvas.Print("YieldvsLumi_BVeto_%s.pdf"%suffix)
	
