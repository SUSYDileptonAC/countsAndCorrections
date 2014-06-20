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
	print path
	for filePath in glob("%s/sw538*.root"%path):
		print filePath
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
	
	
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw538v0475/"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1
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
	data = False
	if argv[2] == "Data":
		data = True
	#~ cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCut
	cuts = "weight*(chargeProduct < 0 && %s && p4.M() > 81 && p4.M() < 101 && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && deltaR > 0.3  )"%(ptCut,etaCut)
	nEvents=-1
	
	lumi = 10.4
	

	minMll = 20
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	ROOT.gStyle.SetOptStat(0)
	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")
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
	nBins = 196
	firstBin = 20
	lastBin = 1000
	
	if data:
		SampleName = "MergedData_BlockB"
	else: 
		SampleName = "TTJets_MGDecays_Trigger_madgraph_Summer12"
	
	for name, tree in EEtrees.iteritems():
		if name == SampleName:
			EEhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			#~ eeTree = tree.CopyTree(cuts)
			eeTreeFull = tree.Clone()
	for name, tree in MuMutrees.iteritems():
		if name == SampleName:
			MuMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			#~ mumuTree = tree.CopyTree(cuts)
			mumuTreeFull = tree.Clone()
	for name, tree in EMutrees.iteritems():
		if name == SampleName:
			EMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
			#~ emuTree = tree.CopyTree(cuts)
			emuTreeFull = tree.Clone()
		
	#~ sfHist = EEhist.Clone("sfhist")
	#~ sfHist.Add(MuMuhist.Clone(""))
	#~ 
	#~ EMuhist.SetMarkerStyle(21)
	#~ sfHist.SetMarkerStyle(22)
	#~ EMuhist.SetMarkerColor(ROOT.kGreen+3)
	#~ sfHist.SetMarkerColor(ROOT.kBlack)
	#~ 
	#~ 
	#~ hCanvas.DrawFrame(20,0,300,100,"; %s ; %s" %("m_{ll} [GeV]","Events / 5 GeV"))
#~ 
	#~ EMuhist.Draw("samep")
	#~ sfHist.Draw("samep")
	#~ 
	#~ legend.AddEntry(EMuhist,"SF Block B","p")	
	#~ legend.AddEntry(sfHist,"OF Block B","p")	
	#~ legend.Draw("same")
	#~ 
	#~ ratioPad.cd()
#~ 
	#~ ratioGraphs =  ratios.RatioGraph(sfHist,EMuhist, xMin=20, xMax=300,title="SF / oF",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kGreen+3,adaptiveBinning=100000)
#~ 
	#~ ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	#~ 
	#~ hCanvas.Print("Unblinding_Zpeak.pdf")
	#~ 
#~ 
	#~ sf = sfHist.Integral()
	#~ of = EMuhist.Integral()
#~ 
	#~ print sf, of
	
	#~ for ev in eeTree:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
	#~ print "----------------------------"
	#~ for ev in mumuTree:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
	#~ print "----------------------------"
	#~ for ev in emuTree:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
		
	missingEE = [
[206594,232,334869087],
[198272,173,164780462],
[198230,103,119666328],
[198212,37,21383792]]	
	missingMM = [
[204544,31,46712204],
[208428,68,78721385],
[206512,123,104441745],
[198269,105,170520480],
[198269,90,148386713],
[208307,17,26326494],
[198230,26,31715163]]

	#~ for ev in eeTreeFull:
		#~ for event in missingEE:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.runNr == event[2]:
				#~ print "MET: %.1f nJets: %d mll %.1f pt1: %.1f pt2: %.1f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
#~ 
	#~ for ev in mumuTreeFull:
		#~ for event in missingMM:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.runNr == event[2]:
				#~ print "MET: %.1f nJets: %d mll %.1f pt1: %.1f pt2: %.1f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
	
	for ev in missingEE:
		tempTree = eeTreeFull.CopyTree("runNr == %d && lumiSec == %d && pt1 > 20 && pt2 > 20"%(ev[0],ev[1]))
		print ev
		print "found %d matching events"%tempTree.GetEntries()
	for ev in missingMM:
		tempTree = mumuTreeFull.CopyTree("runNr == %d && lumiSec == %d && pt1 > 20 && pt2 > 20"%(ev[0],ev[1]))
		print ev
		print "found %d matching events"%tempTree.GetEntries()
