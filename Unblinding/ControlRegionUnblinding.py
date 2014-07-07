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


def readTreeFromFile(path, dileptonCombination,Run2011=False,use532=False):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	if Run2011:
		result.Add("%s/cutsV18SignalHighPtFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	elif use532:		
		result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	else:		
		result.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")	
	return result
def readMCTreeFromFile(path,dileptonTrigger, dileptonCombination,Run2011=False):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	if Run2011:
		result.Add("%s/cutsV18SignalHighPtFinalTrees/%sDileptonTree"%(path, dileptonCombination))		
	else:
		result.Add("%s/cutsV23Dilepton%sFinalTrees/%sDileptonTree"%(path,dileptonTrigger, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")	
	return result
def readVectorTreeFromFile(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonVectorTree"%(path, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")
	return result

	
	
def totalNumberOfGeneratedEvents(path,Run2011=False):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path
	if Run2011:
			
		for sampleName, filePath in getFilePathsAndSampleNames(path,Run2011).iteritems():
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	else:
		for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
			#~ print filePath
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result
	
def readTrees(path, dileptonCombination,Run2011=False,use532 = False):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	if Run2011:
			
		for sampleName, filePath in getFilePathsAndSampleNames(path,Run2011=True).iteritems():
			
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination,Run2011=True)
		
	elif use532:
		
		for sampleName, filePath in getFilePathsAndSampleNames(path,use532=True).iteritems():
		
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination,use532=True)
	else:

		for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
	return result
def readTreesMC(path,dileptonTrigger, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readMCTreeFromFile(filePath,dileptonTrigger, dileptonCombination)
		
	return result
def readVectorTrees(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readVectorTreeFromFile(filePath, dileptonCombination)
		
	return result

	
def getFilePathsAndSampleNames(path,Run2011=False,use532 = False):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	if Run2011:
		for filePath in glob("%s/sw428*.root"%path):

			
			sampleName = match(".*sw428v.*\.cutsV18SignalHighPt.*\.(.*).root", filePath).groups()[0]			
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath		
	elif use532:
		for filePath in glob("%s/sw532*.root"%path):

			
			sampleName = match(".*sw532v.*\.processed.*\.(.*).root", filePath).groups()[0]				
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath		
	else:
		for filePath in glob("%s/sw538*.root"%path):
			
			sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]			
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath
	return result
	

class mainConfig:
	plotData = True
	plotMC	= True
	compareTTbar = False
	normalizeToData = False
	plotRatio = True
	plotSignal = False
	compare2011 = False
	compareSFvsOF = True
	compareEEvsMuMu = False
	compareSFvsOFFlavourSeperated = False
	useVectorTrees = False
	useTriggerEmulation = False 
	preselect = False
	produceReweighting = True
	plot2011 = False
	plot53X = False
	personalWork = False
	doTopReweighting = False
	
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
	path = "/home/jan/Trees/sw538v0475/"
	from sys import argv
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1
	import ratios

	
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	etaCut = etaCuts[argv[1]]
	suffix = argv[1]
	#~ cuts = "weight*(chargeProduct < 0 && %s && p4.M() < 70 && p4.M() > 20 && %s && nJets == 2 && met > 100 && met < 150 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%(ptCut,etaCut)
	cuts = "weight*(chargeProduct < 0 && %s && p4.M() < 101 && p4.M() > 81 && %s && ((met > 100 && nJets >= 3) ||  (met > 150 && nJets >=2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%(ptCut,etaCut)

	

	
	print cuts
	
	SampleNameBlockA = "MergedData_BlockA"
	SampleNameBlockB = "MergedData_BlockB_2Jets"
	path = "/home/jan/Trees/sw538v0476/"
	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")
	path = "/home/jan/Trees/sw532v0474/"
	EMutrees532 = readTrees(path, "EMu",use532=True)
	EEtrees532 = readTrees(path, "EE",use532=True)
	MuMutrees532 = readTrees(path, "MuMu",use532=True)
	for name, tree in EMutrees.iteritems():
		#~ print name
		if name == SampleNameBlockA:
			#~ fullTreeA = tree.Clone()
			eMuTreeA = tree.CopyTree(cuts)
		if name == SampleNameBlockB:
			#~ fullTreeB = tree.Clone()
			eMuTreeB = tree.CopyTree(cuts)
	for name, tree in EEtrees.iteritems():
		#~ print name
		if name == SampleNameBlockA:
			#~ fullTreeA = tree.Clone()
			eeTreeA = tree.CopyTree(cuts)
		if name == SampleNameBlockB:
			#~ fullTreeB = tree.Clone()
			eeTreeB = tree.CopyTree(cuts)
	for name, tree in MuMutrees.iteritems():
		#~ print name
		if name == SampleNameBlockA:
			#~ fullTreeA = tree.Clone()
			mmTreeA = tree.CopyTree(cuts)
		if name == SampleNameBlockB:
			#~ fullTreeB = tree.Clone()
			mmTreeB = tree.CopyTree(cuts)
		
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"p4.M()","",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix,signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"p4.M()","",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix,signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"p4.M()","nVertices < 11",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_LowPU",signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"p4.M()","nVertices < 11",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_LowPU",signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"p4.M()","11 <= nVertices && nVertices < 16",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_MidPU",signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"p4.M()","11 <= nVertices && nVertices < 16",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_MidPU",signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"p4.M()","16 <= nVertices",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_HighPU",signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"p4.M()","16 <= nVertices",60,0,300,"m_{ll} [GeV]","Events / 5 GeV",suffix+"_HighPU",signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"nJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{Jets}","Events",suffix,signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"nJets","",8,0,8,"N_{Jets}","Events",suffix,signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"nBJets","p4.M() > 20 && p4.M() < 70",8,0,8,"N_{B-Jets}","Events",suffix,signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"nBJets","",8,0,8,"N_{B-Jets}","Events",suffix,signal=False,log=True)	
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"nVertices","p4.M() > 20 && p4.M() < 70",50,0,50,"N_{Vertex}","Events",suffix,signal=True)	
	#~ plotBlockComparison(fullTreeA,fullTreeB,"nVertices","",50,0,50,"N_{Vertex}","Events",suffix,signal=False,log=True)	
	#~ 
	#~ plotBlockComparison(eMuTreeA,eMuTreeB,"met","p4.M() > 20 && p4.M() < 70",30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix,signal=True)
	#~ plotBlockComparison(fullTreeA,fullTreeB,"met","",30,0,300,"E_T^{miss} [GeV]","Events / 10 GeV",suffix,signal=False,log=True)	
	#~ 


	
	sfA = eeTreeA.GetEntries() + mmTreeB.GetEntries()
	ofA = eMuTreeA.GetEntries()
	sfB = eeTreeB.GetEntries() + mmTreeB.GetEntries()
	ofB = eMuTreeB.GetEntries()
	eeA = eeTreeA.GetEntries()
	eeB = eeTreeB.GetEntries()
	mmA = mmTreeA.GetEntries()
	mmB = mmTreeB.GetEntries()
	
	print "Block A"
	print "SF: %d (ee: %d mm: %d ) OF: %d"%(sfA,eeA,mmA,ofA)
	print "Block B"
	print "SF: %d (ee: %d mm: %d ) OF: %d"%(sfB,eeB,mmB,ofB)
	#~ print "ee events:"
	#~ for ev in eeTreeB:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
	#~ print "mm events:"
	#~ for ev in mmTreeB:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
	#~ print "em events:"
	#~ for ev in eMuTreeB:
		#~ print "%s:%s:%s"%(ev.runNr,ev.lumiSec,ev.eventNr)
	#~ 
	