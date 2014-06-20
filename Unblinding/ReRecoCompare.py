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
	
def readTreeFromFileReReco(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV23DileptonFinalTriggerTrees/%sDileptonTree"%(path, dileptonCombination))
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
def plotReRecoComparison(treeList1,treeList2,variable,additionalCut,nBins,firstBin,lastBin,labelX,labelY,suffix,log=False,signal=False):	


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

	EMuhistBlockA = ROOT.TH1F("hist1","hist1",nBins,firstBin,lastBin)
	EMuhistBlockB = ROOT.TH1F("hist2","hist2",nBins,firstBin,lastBin)

	for tree in treeList1:
		tempHist = createHistoFromTree(tree,  variable, additionalCut, nBins, firstBin, lastBin, -1)
		EMuhistBlockA.Add(tempHist)
	for tree in treeList2:
		tempHist = createHistoFromTree(tree,  variable, additionalCut, nBins, firstBin, lastBin, -1)
		EMuhistBlockB.Add(tempHist)
	#~ 
	#~ EMuhistBlockB.Scale(9.2/10.4)
	#~ print EMuhistBlockA.Integral()
	#~ print EMuhistBlockB.Integral()
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
	
	legend.AddEntry(EMuhistBlockA,"Default Reconstruction","p")	
	legend.AddEntry(EMuhistBlockB,"Jan22ReReco","p")
	#~ 
	latex = ROOT.TLatex()
	latex.SetTextSize(0.043)
	latex.SetTextFont(42)
	latex.SetNDC(True)
	latex.DrawLatex(0.13, 0.95, "CMS Preliminary,   #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 19.4-19.8 fb^{-1}")
	#~ 
		
	legend.Draw("same")
	
	ratioPad.cd()

	ratioGraphs =  ratios.RatioGraph(EMuhistBlockA,EMuhistBlockB, firstBin, lastBin,title="Prompt / ReReco",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kGreen+3,adaptiveBinning=0.25)

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	if signal:
		name = "ReReco_SignalRegion_%s_%s.pdf"
	else:
		name = "ReReco_Inclusive_%s_%s.pdf"
	if variable == "p4.M()":
		
		hCanvas.Print(name%(suffix,"Mll"))
	else:		
		hCanvas.Print(name%(suffix,variable))	
		hCanvas.Clear()	
	
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/home/jan/Trees/sw538v0476/"
	pathReReco = "/home/jan/Trees/sw538v0477/"
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
	
	#~ runCut = "runNr < 201657 && runNr > 198522 && (runNr == 199832 || runNr == 199834 || runNr == 199967 || runNr == 200160 || runNr == 200161 || runNr == 200174 || runNr == 200177 || runNr == 200178 || runNr == 200186 || runNr == 201191)"
	runCut = "runNr < 999999"

	#~ cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCut
	cuts = "weight*(chargeProduct < 0 && %s && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && %s && deltaR > 0.3 && %s && abs(eta1) < 2.4 && abs(eta2) < 2.4)"%(ptCut,etaCut,runCut)
	print cuts
	nEvents=-1
	
	lumi = 19.4
	

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
	SampleNameReReco = "MergedData_ReReco"
	
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

	#~ sfTree = eeTree.Clone("sfTree")
	#~ sfTree.Add(mmTree.Clone(""))
	#~ sfTreeReReco = eeTreeReReco.Clone("sfTree")
	#~ sfTreeReReco.Add(mmTreeReReco.Clone(""))
#~ 
	#~ sfTreeSignal = eeTreeSignal.Clone("sfTree")
	#~ sfTreeSignal.Add(mmTreeSignal.Clone(""))
	#~ sfTreeReRecoSignal = eeTreeReRecoSignal.Clone("sfTree")
	#~ sfTreeReRecoSignal.Add(mmTreeReRecoSignal.Clone(""))
	signalTreelist = [eeTreeSignal,mmTreeSignal]
	signalTreelistReReco = [eeTreeReRecoSignal,mmTreeReRecoSignal]
	treelist = [eeTree,mmTree]
	treelistReReco = [eeTreeReReco,mmTreeReReco]	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"p4.M()","",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_SF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"p4.M()",runCut,60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_SF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"nJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{Jets}","Events",suffix+"_SF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nJets",runCut,8,0,8,"N_{Jets}","Events",suffix+"_SF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"nBJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{B-Jets}","Events",suffix+"_SF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nBJets",runCut,8,0,8,"N_{B-Jets}","Events",suffix+"_SF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"nVertices","p4.M() > 20 && p4.M() < 70",50,0,50,"N_{Vertex}","Events",suffix+"_SF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nVertices",runCut,50,0,50,"N_{Vertex}","Events",suffix+"_SF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"met","p4.M() > 20 && p4.M() < 70",30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix+"_SF",signal=True)
	plotReRecoComparison(treelist,treelistReReco,"met",runCut,30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix+"_SF",signal=False,log=True)	
	
	signalTreelist = [emTreeSignal]
	signalTreelistReReco = [emTreeReRecoSignal]
	treelist = [emTree]
	treelistReReco = [emTreeReReco]
	
	plotReRecoComparison(signalTreelist ,signalTreelistReReco,"p4.M()","",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_OF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"p4.M()",runCut,60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_OF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist ,signalTreelistReReco,"nJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{Jets}","Events",suffix+"_OF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nJets",runCut,8,0,8,"N_{Jets}","Events",suffix+"_OF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist,signalTreelistReReco,"nBJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{B-Jets}","Events",suffix+"_OF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nBJets",runCut,8,0,8,"N_{B-Jets}","Events",suffix+"_OF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist ,signalTreelistReReco,"nVertices","p4.M() > 20 && p4.M() < 70",50,0,50,"N_{Vertex}","Events",suffix+"_OF",signal=True)	
	plotReRecoComparison(treelist,treelistReReco,"nVertices",runCut,50,0,50,"N_{Vertex}","Events",suffix+"_OF",signal=False,log=True)	
	plotReRecoComparison(signalTreelist ,signalTreelistReReco,"met","p4.M() > 20 && p4.M() < 70",30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix+"_OF",signal=True)
	plotReRecoComparison(treelist,treelistReReco,"met",runCut,30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix+"_OF",signal=False,log=True)	
	
	
	eeCountTree = eeTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	mmCountTree = mmTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	emCountTree = emTreeSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	eeCountTreeReReco = eeTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	mmCountTreeReReco = mmTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	emCountTreeReReco = emTreeReRecoSignal.CopyTree("p4.M() > 20 && p4.M() < 70")
	
	sfYield = eeCountTree.GetEntries() + mmCountTree.GetEntries()
	sfYieldReReco = eeCountTreeReReco.GetEntries() + mmCountTreeReReco.GetEntries()
	
	print sfYield, sfYieldReReco
	

	
	blockA = emCountTree.GetEntries()
	blockB = emCountTreeReReco.GetEntries()




	print blockA, blockB
	

	#~ met = 0
	#~ nJets = 0
	#~ mll = 0
	#~ pt = 0
	#~ other = 0
	#~ overlap = 0 
	#~ 
	#~ for ev in eeTreeSignal:
		#~ 
		#~ testTree = eeTreeReRecoSignal.CopyTree("eventNr == %d && lumiSec == %d && runNr == %d"%(ev.eventNr,ev.lumiSec,ev.runNr))
		#~ 
		#~ if testTree.GetEntries() == 1:
			#~ overlap = overlap +1
		#~ elif testTree.GetEntries() == 0:
			#~ testTree = eeTreeReReco.CopyTree("eventNr == %d && lumiSec == %d && runNr == %d"%(ev.eventNr,ev.lumiSec,ev.runNr))
			#~ if testTree.GetEntries() == 0:
				#~ other = other + 1
			#~ elif testTree.GetEntries() == 1:
				#~ for ev2 in testTree:
					#~ if ev2.p4.M() > 70 or ev2.p4.M() < 20:
						#~ mll = mll + 1
					#~ if ev2.pt1 < 20 or ev2.pt2 < 20:
						#~ pt = pt +1
					#~ if (ev2.met > 100 and ev2.nJets < 3) or (ev2.met > 150 and ev2.nJets < 2):
						#~ nJets = nJets +1
					#~ if (ev2.nJets >=3 and ev2.met < 100) or (ev2.met < 150 and ev2.nJets >= 2):
						#~ met = met +1 
						#~ 
	#~ print met, nJets, mll, pt, other, overlap					
		#~ if (ev.p4.M() > 20 and ev.p4.M() < 70 and ((ev.nJets >=2 and ev.met > 150) or (ev.nJets >=3 and ev.met > 100)) and ev.deltaR > 0.3 and ):
	
	

#~ 
#~ 
	print "In ReReco but not in Prompt OF :"
	for ev in emCountTreeReReco:
		found = False
		for ev2 in emCountTree:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
	print "In Prompt but not in ReReco OF :"
	for ev in emCountTree:
		found = False
		for ev2 in emCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
	print "In ReReco but not in Prompt EE :"
	for ev in eeCountTreeReReco:
		found = False
		for ev2 in eeCountTree:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr) or (ev.p4.M() < 20 or ev.p4.M() > 70):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
	print "In Prompt but not in ReReco EE :"
	for ev in eeCountTree:
		found = False
		for ev2 in eeCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr) or (ev.p4.M() < 20 or ev.p4.M() > 70):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
	print "In ReReco but not in Prompt MM :"
	for ev in mmCountTreeReReco:
		found = False
		for ev2 in mmCountTree:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr) or (ev.p4.M() < 20 or ev.p4.M() > 70):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
	print "In Prompt but not in ReReco MM :"
	for ev in mmCountTree:
		found = False
		for ev2 in mmCountTreeReReco:
			if (ev.runNr == ev2.runNr and ev.lumiSec == ev2.lumiSec and ev.eventNr == ev2.eventNr) or (ev.p4.M() < 20 or ev.p4.M() > 70):
				found = True
		if found == False:
			print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)


### ---- Central ---- 

	#~ promptNotReRecoOF = [ [199319,612,803834699], [200245,194,218462398], [200519,330,452606536], [200519,476,615400908], [200525,476,629497262],
#~ [201097,95,56261321],
#~ [201097,164,180972123],
#~ [201115,20,35631352],
#~ [201196,97,83789552],
#~ [201229,11,20035259],
#~ [201173,238,204776331],
#~ [201278,398,555495628],
#~ [201625,572,784925104],
#~ [201625,693,913838993],  ]				
#~ 
	#~ rerecoNotPromptOF = [
#~ [201624,170,205283407],
#~ [200961,16,2287238],
#~ [198955,1200,1255920523],
#~ [199804,617,711125017],
#~ [199409,109,148027380],
#~ [201278,1287,1526273339],
#~ [201625,532,739936308],
#~ [199699,175,225967775],
#~ [201196,718,554011927],
#~ [199876,309,351914359],
#~ [199876,148,178195430],
#~ [199877,144,160733746],
#~ [201115,59,106577992],
#~ [201196,659,513929751],	
	#~ 
	#~ ]
	#~ 
	#~ rerecoNotPromptEE = [
#~ [199021,69,41161710],
#~ [198955,451,526688340],
#~ [199608,966,1097365158],
#~ [199960,99,71340078],
#~ [200042,167,143349949],
#~ [200244,575,749178915],
#~ [200525,971,1181603533],
#~ [201168,174,189598270],	]
#~ 
#~ 
	#~ promptNotReRecoEE = [
#~ [201602,155,157360436],
#~ [201625,378,557281409],
#~ [198954,224,264505030],
#~ [198955,1298,1334649389],
#~ [199608,387,465311942],
#~ [199699,527,619538870],
#~ [199739,97,66211793],
#~ [199876,213,250307616],
#~ [199877,33,37864981],
#~ [200091,744,881746145],
#~ [200473,848,904188235],
#~ [200991,1026,1212741455],
#~ [201115,23,42627312],
#~ [201168,43,48546689],	
	#~ 
	#~ ]
	#~ 
	#~ rerecoNotPromptMM = [
#~ [199608,440,527675572],
#~ [199319,894,1121158128],
#~ [200041,690,830804191],
#~ [198969,699,839961535],
#~ [198969,482,614309194],
#~ [199021,463,569403420],
#~ [199409,168,230339699],
#~ [201602,228,288454210],
#~ [200075,90,42333764],
#~ [200991,615,776380582],
#~ [201168,96,107760541],
#~ [201278,380,530725227],
#~ [201625,355,528369012],	
	#~ ]
	#~ 
	#~ promptNotReRecoMM = [
	#~ 
#~ [198955,794,893568723],
#~ [199319,565,754425242],
#~ [199428,463,563539913],
#~ [199608,164,175875059],
#~ [199752,224,276784903],
#~ [199804,228,250989834],
#~ [199804,424,493597499],
#~ [199877,343,364637397],
#~ [200245,341,369345746],
#~ [201097,472,634707124],
#~ [201196,3,2511168],
#~ [201625,777,1005894809],	
	#~ 
	#~ 
	#~ ]

#~ ### ---- Forward ---- 
#~ 

	#~ rerecoNotPromptOF = [
#~ [201062,89,47509787],
#~ [201173,500,406012656],
#~ [200525,789,978268841],
#~ [201278,330,461229015],
#~ [200976,154,112344849],
#~ [200041,794,950246680],
#~ [199754,965,896598114],
#~ [200075,517,616777901],
	#~ ]
	#~ promptNotReRecoOF = [
#~ [199336,50,50647446],
#~ [199436,273,190712449],
#~ [199875,279,360281348],
#~ [200473,958,1005624398],
#~ [200473,277,276576077],
#~ [200519,358,484798412],
#~ [201196,740,568470430],
#~ [201278,1725,1883270763],
#~ [201625,630,847024317],
	#~ ]
	#~ rerecoNotPromptEE = [
#~ [201278,1743,1896344595],
	#~ ]
	#~ promptNotReRecoEE = [
#~ [200041,554,681203523],
#~ [200075,263,301044436],
#~ [200369,45,51346195],
	#~ ]
	#~ 
	#~ rerecoNotPromptMM = [
#~ [199356,177,162994764],
#~ [199409,758,898831232],
#~ [200600,356,514199849],
#~ [200991,555,702485686],
#~ [201173,477,389143433],
	#~ ]
	#~ promptNotReRecoMM = [
#~ [199409,227,308053002],
#~ [201624,91,55651911],
	#~ ]
#~ 
#~ 
	#~ print "events in Prompt Reco with are not in ReReco OF"					
	#~ for ev in emTreeReReco:
		#~ for event in promptNotReRecoOF:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in emTreeSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
	#~ print "events in ReReco with are not in PromptReco OF"
	#~ for ev in emTree:
		#~ for event in rerecoNotPromptOF:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in emTreeReRecoSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
	#~ print "events in Prompt Reco with are not in ReReco EE"					
	#~ for ev in eeTreeReReco:
		#~ for event in promptNotReRecoEE:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in eeTreeSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
	#~ print "events in ReReco with are not in PromptReco EE"
	#~ for ev in eeTree:
		#~ for event in rerecoNotPromptEE:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in eeTreeReRecoSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
	#~ print "events in Prompt Reco with are not in ReReco MM"					
	#~ for ev in mmTreeReReco:
		#~ for event in promptNotReRecoMM:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in mmTreeSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
	#~ print "events in ReReco with are not in PromptReco MM"
	#~ for ev in mmTree:
		#~ for event in rerecoNotPromptMM:
			#~ if ev.runNr == event[0] and ev.lumiSec == event[1] and ev.eventNr == event[2]:
				#~ print "%d:%d:%d"%(event[0],event[1],event[2])
				#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev.met,ev.nJets,ev.p4.M(),ev.pt1,ev.pt2)
				#~ for ev2 in mmTreeReRecoSignal:
					#~ if ev2.runNr == event[0] and ev2.lumiSec == event[1] and ev2.eventNr == event[2]:
						#~ print "MET: %.2f nJets: %d mll %.2f pt1: %.2f pt2: %.2f"%(ev2.met,ev2.nJets,ev2.p4.M(),ev2.pt1,ev2.pt2)
						#~ 
						#~ 
	#~ 
