import ROOT
import numpy 
from math import sqrt

attic = []

ROOT.gStyle.SetOptStat(0)

etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"(abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4",
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
	tdrStyle.SetPadLeftMargin(0.16)
	tdrStyle.SetPadRightMargin(0.02)
	
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
	
	
def plotMllSpectra(SFhist,EMuHist,suffix,Simulation=False):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	SFhist.Rebin(25)
	EMuhist.Rebin(25)
	SFhist.GetXaxis().SetRangeUser(15,300)
	SFhist.Draw("")
	SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
	SFhist.GetYaxis().SetTitle("Events / 5 GeV")
	EMuhist.Draw("samehist")
	#EMuhist.SetLineColor(855)
	EMuhist.SetFillColor(855)
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
	ROOT.gStyle.SetOptStat(0)	
	legend.AddEntry(SFhist,"%s events"%argv[2],"p")
	legend.AddEntry(EMuhist,"OF events","f")
	legend.Draw("same")
	#hCanvas.SetLogy()
	
	line1 = ROOT.TLine(minMll,0,minMll,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line5.SetLineColor(ROOT.kRed+2)
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line5.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	line5.Draw("same")
	
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
	
	
	Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
	Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
	Labelout.DrawLatex(150.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")	
	Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20 GeV}{MET < 50 GeV, nJets >=2}")
	
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if Simulation:
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 
	
	
	hCanvas.Print("fig/Rinout_NoLog_%s.pdf"%suffix)
	hCanvas.Clear()
	hCanvas.SetLogy()
	ROOT.gStyle.SetTitleYOffset(0.9)
	ROOT.gStyle.SetPadLeftMargin(0.13)
	SFhist.Draw("")
	SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
	SFhist.GetYaxis().SetTitle("Events / 5 GeV")
	EMuhist.Draw("samehist")
	#EMuhist.SetLineColor(855)
	EMuhist.SetFillColor(855)
	#legend.AddEntry(SFhist,"SF events","p")
	#legend.AddEntry(EMuhist,"OF events","f")
	legend.Draw("same")
	#hCanvas.SetLogy()
	
	line1 = ROOT.TLine(minMll,0,minMll,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line5 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))	
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line5.SetLineColor(ROOT.kBlack)	
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line5.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	line5.Draw("same")
	Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/12,"In")
	Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/12,"Out")
	Labelout.DrawLatex(150.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/12,"Out")
	Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/10,"#splitline{p_{T}^{lepton} > 20 GeV}{MET < 50 GeV, nJets >=2}")
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if Simulation:
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 	
	hCanvas.Print("fig/Rinout_%s.pdf"%suffix)		
	
	
def plotSystematics(EEtrees,MuMutrees,EMutrees,suffix,Rinout,Simulation=False,highMass=False):
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
	sampleName = "MergedData"
	
	if Simulation:
		sampleName = "ZJets_madgraph_Summer12"
		sampleName2 = "AStar_madgraph_Summer12"
	
	minMll = 20
	maxMll = 70
	if highMass:
		minMll = 120
		maxMll = 1000

	nBins = 1500
	firstBin = 0
	lastBin = 300


	legend = TLegend(0.65, 0.65, 0.98, 0.90)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
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
	
	
	metRange = 6
	metBinsUp=[10,20,30,40,60,100]
	metBinsDown=[0,10,20,30,40,60]	
	Rinout2Jets = []
	ErrRinout2Jets = []	
	nJets=2
	
	#~ cuts = "weight*(chargeProduct < 0 && %s && met < %d && met > %d && nJets == %d && runNr <= 196531 && deltaR > 0.3 && abs(eta1)<2.4 && abs(eta2)<2.4)"
	cuts = "weight*(chargeProduct < 0 && %s && met < %d && met > %d && nJets == %d  && deltaR > 0.3 && %s )"

	
	for index in range (0,metRange):
		addHist = None
		legend.Clear()
		for name, tree in EEtrees.iteritems():
			if name == sampleName:
				EEhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
		
		if addHist != None:
			EEhist.Add(addHist.Clone())
		addHist = None			
		for name, tree in MuMutrees.iteritems():
			if name == sampleName:
				MuMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
		if addHist != None:
			MuMuhist.Add(addHist.Clone())		
		addHist = None
		for name, tree in EMutrees.iteritems():
			if name == sampleName:

				EMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,metBinsUp[index],metBinsDown[index],nJets,etaCut), nBins, firstBin, lastBin)		
		
		if addHist != None:
			EMuhist.Add(addHist.Clone())			
		
		if argv[2] == "SF":		
			SFhist = EEhist.Clone()
			SFhist.Add(MuMuhist.Clone())
		elif argv[2] == "EE":
			SFhist = EEhist.Clone()
		else:
			SFhist = MuMuhist.Clone()
			



			#SFhist.Add(EMuhist,-1)
		
		peak = (SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))- EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))*nllPredictionScale) 
		peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101+0.01))*nllPredictionScale)**2)
		continuum = (SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)) - EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale )
		continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(maxMll+0.01),SFhist.FindBin(maxMll)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale)**2) 
		localRinout =   continuum / peak			
		localErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)


		Rinout2Jets.append(localRinout)
		ErrRinout2Jets.append(localErrRinout)
		
		
		SFhist.Rebin(25)
		EMuhist.Rebin(25)
		SFhist.Draw("")
		SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
		SFhist.GetYaxis().SetTitle("Events / 5 GeV")
		EMuhist.Draw("samehist")
		#EMuhist.SetLineColor(ROOT.kRed)
		EMuhist.SetFillColor(855)
		legend.AddEntry(SFhist,"SF events","p")
		legend.AddEntry(EMuhist,"OF events","f")
		legend.Draw("same")
		hCanvas.SetLogy()
			
		line1 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line2 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line5 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line1.SetLineColor(ROOT.kBlack)
		line2.SetLineColor(ROOT.kBlack)
		line5.SetLineColor(ROOT.kBlack)
		line3.SetLineColor(ROOT.kRed+2)
		line4.SetLineColor(ROOT.kRed+2)
		line1.SetLineWidth(2)
		line2.SetLineWidth(2)
		line3.SetLineWidth(2)
		line4.SetLineWidth(2)
		line5.SetLineWidth(2)
		line1.Draw("same")
		line2.Draw("same")
		line3.Draw("same")
		line4.Draw("same")
		line5.Draw("same")
		Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"In")
		Labelout.DrawLatex(32.5,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Labelout.DrawLatex(150,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > 20 GeV}{ %d GeV < met < %d GeV, nJets ==%d}" %(metBinsDown[index],metBinsUp[index],nJets))
			#~ Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
			#~ Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
			#~ Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20(10) GeV}{MET < 100 GeV, nJets ==3}")
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True) 
			
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
		cmsExtra = "Preliminary"
		if Simulation:
			cmsExtra = "Simulation"
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 			
			
		if highMass:	
			hCanvas.Print("fig/Rinout_highMass_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		else:
			hCanvas.Print("fig/Rinout_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		
	hCanvas.Clear()			
	hCanvas.SetLogy(0)		
	
	
	
	arg6 = numpy.array([-5,105],"d")
	arg7 = numpy.array([Rinout,Rinout],"d")
	arg8 = numpy.array([0,0],"d")
	arg9 = numpy.array([Rinout*0.25,Rinout*0.25],"d")
	
	errorband = ROOT.TGraphErrors(2,arg6,arg7,arg8,arg9)
	errorband.GetYaxis().SetRangeUser(0.0,0.15)
	errorband.GetXaxis().SetRangeUser(-5,105)
	errorband.GetXaxis().SetTitle("E_{T}^{miss} [GeV]")
	errorband.GetYaxis().SetTitle("r_{out,in}")
	errorband.Draw("A3")
	errorband.SetFillColor(ROOT.kOrange-9)
	rinoutLine = ROOT.TLine(-5,Rinout,105,Rinout)
	rinoutLine.SetLineStyle(ROOT.kDashed)
	rinoutLine.SetLineWidth(2)
	rinoutLine.Draw("same")

	METvalues =[5,15,25,35,50,80]
	METErrors =[5,5,5,5,10,20]
	arg2 = numpy.array(METvalues,"d")
	arg3 = numpy.array(Rinout2Jets,"d")
	arg4 = numpy.array(METErrors,"d")
	arg5 = numpy.array(ErrRinout2Jets,"d")	
	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graph2jet = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graph2jet.Draw("Psame0")
	legend.Clear()
	#legend.AddEntry(graph1jet,"NJets==1","p")
	if argv[3] == "MC":
		legend.AddEntry(graph2jet,"r_{out,in} MC","p")
	else:
		legend.AddEntry(graph2jet,"r_{out,in} Data","p")
	#legend.AddEntry(graph3jet,"NJets==3","p")
	legend.AddEntry(rinoutLine, "Mean r_{out,in} = %.3f"%Rinout,"l")
	legend.AddEntry(errorband, "Mean r_{out,in} #pm 25%","f")
	legend.Draw("same")


	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if argv[3] == "MC":
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 		
		
	ROOT.gPad.RedrawAxis()
	if highMass:		
		hCanvas.Print("fig/RinoutSystMET_highMass_Full2012_%s.pdf"%suffix)
	else:
		hCanvas.Print("fig/RinoutSystMET_Full2012_%s.pdf"%suffix)

	RinoutMET100 = []
	ErrRinoutMET100 = []	
	
	for nJets in range (0,6):

		legend.Clear()
		addHist = None 
		for name, tree in EEtrees.iteritems():
			if name == sampleName:
				EEhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)	
		if addHist != None:
			EEhist.Add(addHist.Clone())
		addHist = None
		for name, tree in MuMutrees.iteritems():
			if name == sampleName:
				MuMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)				
		if addHist != None:
			MuMuhist.Add(addHist.Clone())
		addHist = None		
		for name, tree in EMutrees.iteritems():
			if name == sampleName:
				EMuhist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)
			if Simulation:
				if name == sampleName2:
					addHist = createHistoFromTree(tree,  variable, cuts %(ptCut,100,0,nJets,etaCut), nBins, firstBin, lastBin)				
		if addHist != None:
			EMuhist.Add(addHist.Clone())
						
		if argv[2] == "SF":		
			SFhist = EEhist.Clone()
			SFhist.Add(MuMuhist.Clone())
		elif argv[2] == "EE":
			SFhist = EEhist.Clone()
		else:
			SFhist = MuMuhist.Clone()
			
		peak = (SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))- EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))*nllPredictionScale) 
		peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101+0.01))*nllPredictionScale)**2)
		continuum = (SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)) - EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale )
		continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(maxMll)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll+0.01),EMuhist.FindBin(maxMll))*nllPredictionScale)**2) 
		localRinout =   continuum / peak			
			
			#localRinout = SFhist.Integral(SFhist.FindBin(15),SFhist.FindBin(70)) / SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101))
		localErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
		print localRinout
		print localErrRinout

		RinoutMET100.append(localRinout)
		ErrRinoutMET100.append(localErrRinout)	
		
		SFhist.Rebin(25)
		EMuhist.Rebin(25)
		SFhist.Draw("")
		SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
		SFhist.GetYaxis().SetTitle("Events / 5 GeV")
		EMuhist.Draw("samehist")
		#EMuhist.SetLineColor(ROOT.kRed)
		EMuhist.SetFillColor(855)
		legend.AddEntry(SFhist,"SF events","p")
		legend.AddEntry(EMuhist,"OF events","f")
		legend.Draw("same")
		hCanvas.SetLogy()
			
		line1 = ROOT.TLine(120,0,120,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line2 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line5 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))		
		line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
		line1.SetLineColor(ROOT.kBlack)
		line2.SetLineColor(ROOT.kBlack)
		line5.SetLineColor(ROOT.kBlack)
		line3.SetLineColor(ROOT.kRed+2)
		line4.SetLineColor(ROOT.kRed+2)
		line1.SetLineWidth(2)
		line2.SetLineWidth(2)
		line3.SetLineWidth(2)
		line4.SetLineWidth(2)
		line5.SetLineWidth(2)
		line1.Draw("same")
		line2.Draw("same")
		line3.Draw("same")
		line4.Draw("same")
		line5.Draw("same")
		Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"In")
		Labelout.DrawLatex(150,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
		Labelout.DrawLatex(32.5,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")		
		Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > 20 GeV}{ %d GeV < met < %d GeV, nJets ==%d}" %(0,100,nJets))
			#~ Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
			#~ Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
			#~ Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20(10) GeV}{MET < 100 GeV, nJets ==3}")
			
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.055)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.03)
		latexCMSExtra.SetNDC(True) 
			
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
		cmsExtra = "Preliminary"
		if Simulation:
			cmsExtra = "Simulation"
		latexCMS.DrawLatex(0.19,0.89,"CMS")
		latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 
			
		if highMass:	
			hCanvas.Print("fig/Rinout_highMass_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))		
		else:
			hCanvas.Print("fig/Rinout_Full2012_%dJets_MET%d_%s.pdf"%(nJets,metBinsUp[index],suffix))
		
	hCanvas.Clear()
	hCanvas.SetLogy(0)	
	arg6 = numpy.array([-0.5,6.5],"d")
	arg7 = numpy.array([Rinout,Rinout],"d")
	arg8 = numpy.array([0,0],"d")
	arg9 = numpy.array([Rinout*0.25,Rinout*0.25],"d")
	
	errorband = ROOT.TGraphErrors(2,arg6,arg7,arg8,arg9)
	errorband.GetYaxis().SetRangeUser(0.0,0.15)
	errorband.GetXaxis().SetRangeUser(-0.5,6.5)
	errorband.GetXaxis().SetTitle("N_{Jets}")
	errorband.GetYaxis().SetTitle("r_{out,in}")
	errorband.Draw("A3")
	errorband.SetFillColor(ROOT.kOrange-9)
	rinoutLine = ROOT.TLine(-0.5,Rinout,6.5,Rinout)
	rinoutLine.SetLineStyle(ROOT.kDashed)
	rinoutLine.SetLineWidth(2)
	rinoutLine.Draw("same")

	METvalues =[0.5,1.5,2.5,3.5,4.5,5.5]
	METErrors =[0.5,0.5,0.5,0.5,0.5,0.5]
	arg2 = numpy.array(METvalues,"d")
	arg3 = numpy.array(RinoutMET100,"d")
	arg4 = numpy.array(METErrors,"d")
	arg5 = numpy.array(ErrRinoutMET100,"d")	
	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graphMET100 = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graphMET100.Draw("Psame0")
	legend.Clear()
	#legend.AddEntry(graph1jet,"NJets==1","p")
	if argv[3] == "MC":
		legend.AddEntry(graphMET100,"r_{out,in} MC","p")
	else:
		legend.AddEntry(graphMET100,"r_{out,in} Data","p")
	#legend.AddEntry(graph3jet,"NJets==3","p")
	legend.AddEntry(rinoutLine, "Mean r_{out,in} = %.3f"%Rinout,"l")
	legend.AddEntry(errorband, "Mean r_{out,in} #pm 25%","f")
	legend.Draw("same")
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%(printLumi,))
	cmsExtra = "Preliminary"
	if argv[3] == "MC":
		cmsExtra = "Simulation"
	latexCMS.DrawLatex(0.19,0.89,"CMS")
	latexCMSExtra.DrawLatex(0.19,0.85,"%s"%(cmsExtra)) 
	ROOT.gPad.RedrawAxis()
	if highMass:		
		hCanvas.Print("fig/RinoutSystNJets_highMass_Full2012_%s.pdf"%suffix)
	else:		
		hCanvas.Print("fig/RinoutSystNJets_Full2012_%s.pdf"%suffix)
	
	
corrections = {"Barrel":{"EE":[0.45,0.03],"MM":[0.55,0.03],"SF":[1.00,0.04]},"Endcap":{"EE":[0.48,0.06],"MM":[0.63,0.07],"SF":[1.11,0.07]}}	
	
	
if (__name__ == "__main__"):
	setTDRStyle()
	path = "/user/jschulte/Trees/sw538v0476/"
	import pickle	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend
	from sys import argv
	import defs	
	from defs import Backgrounds
	from helpers import *	

		
	etaCut = etaCuts[argv[1]]
	suffix = argv[1] + "_" + argv[2]
	useMC = False
	if argv[3] == "MC":
		suffix = suffix + "_MC"
		useMC = True
	else:
		suffix = suffix + "_Data"
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	
	#~ cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCut
	cuts = "weight*(chargeProduct < 0 && %s && met < 50 && nJets >=2 && %s && deltaR > 0.3 )"%(ptCut,etaCut)
	cutsPeak = "weight*(chargeProduct < 0 && %s && met < 50 && nJets >=2 && %s && deltaR > 0.3 && p4.M() > 81 && p4.M() < 101 )"%(ptCut,etaCut)
	cutsLowMass = "weight*(chargeProduct < 0 && %s && met < 50 && nJets >=2 && %s && deltaR > 0.3 && p4.M() > 20 && p4.M() < 70 )"%(ptCut,etaCut)
	cutsHighMass = "weight*(chargeProduct < 0 && %s && met < 50 && nJets >=2 && %s && deltaR > 0.3 && p4.M() > 120  )"%(ptCut,etaCut)		
	nEvents=-1
	minMll = 20
	lumi = 19.4
	printLumi = lumi
	sampleName = "MergedData"
	
	if argv[3] == "MC":
		path = "/user/jschulte/Trees/sw538v0477/"

	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")
	
	nBins = 1500
	firstBin = 0
	lastBin = 300
	if useMC:
		counts = {}
		import pickle
		#~ counts[pickleName] = {}
		print path
		eventCounts = totalNumberOfGeneratedEvents(path)
			
		TTJets = Process(Backgrounds.TTJets.subprocesses,eventCounts,Backgrounds.TTJets.label,Backgrounds.TTJets.fillcolor,Backgrounds.TTJets.linecolor,Backgrounds.TTJets.uncertainty,1)	
		TT = Process(Backgrounds.TT.subprocesses,eventCounts,Backgrounds.TT.label,Backgrounds.TT.fillcolor,Backgrounds.TT.linecolor,Backgrounds.TT.uncertainty,1)	
		TTJets_SC = Process(Backgrounds.TTJets_SpinCorrelations.subprocesses,eventCounts,Backgrounds.TTJets_SpinCorrelations.label,Backgrounds.TTJets_SpinCorrelations.fillcolor,Backgrounds.TTJets_SpinCorrelations.linecolor,Backgrounds.TTJets_SpinCorrelations.uncertainty,1)	
		TT_MCatNLO = Process(Backgrounds.TT_MCatNLO.subprocesses,eventCounts,Backgrounds.TT_MCatNLO.label,Backgrounds.TT_MCatNLO.fillcolor,Backgrounds.TT_MCatNLO.linecolor,Backgrounds.TT_MCatNLO.uncertainty,1)	
		Diboson = Process(Backgrounds.Diboson.subprocesses,eventCounts,Backgrounds.Diboson.label,Backgrounds.Diboson.fillcolor,Backgrounds.Diboson.linecolor,Backgrounds.Diboson.uncertainty,1)	
		Rare = Process(Backgrounds.Rare.subprocesses,eventCounts,Backgrounds.Rare.label,Backgrounds.Rare.fillcolor,Backgrounds.Rare.linecolor,Backgrounds.Rare.uncertainty,1)	
		DY = Process(Backgrounds.DrellYan.subprocesses,eventCounts,Backgrounds.DrellYan.label,Backgrounds.DrellYan.fillcolor,Backgrounds.DrellYan.linecolor,Backgrounds.DrellYan.uncertainty,1,additionalSelection=Backgrounds.DrellYan.additionalSelection)	
		#~ DYTauTau = Process(Backgrounds.DrellYanTauTau.subprocesses,eventCounts,Backgrounds.DrellYanTauTau.label,Backgrounds.DrellYanTauTau.fillcolor,Backgrounds.DrellYanTauTau.linecolor,Backgrounds.DrellYanTauTau.uncertainty,1,additionalSelection=Backgrounds.DrellYanTauTau.additionalSelection)	
		SingleTop = Process(Backgrounds.SingleTop.subprocesses,eventCounts,Backgrounds.SingleTop.label,Backgrounds.SingleTop.fillcolor,Backgrounds.SingleTop.linecolor,Backgrounds.SingleTop.uncertainty,1)	
		processes = [Rare,SingleTop,TTJets_SC,Diboson,DY]
		

		plot = defs.thePlots.mllPlots.mllPlot
		
		plot.cuts = cuts
		plot.firstBin = firstBin
		plot.lastBin = lastBin
		plot.nBins = nBins
		
		lumi = lumi * 1000
		scaleTree1 = 1.0
		scaleTree2 = 1.0
		stackEE = TheStack(processes,lumi,plot,EEtrees,"None",1.0,scaleTree1,scaleTree2,saveIntegrals=False,counts=counts)	
		stackMM = TheStack(processes,lumi,plot,MuMutrees,"None",1.0,scaleTree1,scaleTree2,saveIntegrals=False,counts=counts)	
		stackEM = TheStack(processes,lumi,plot,EMutrees,"None",1.0,scaleTree1,scaleTree2,saveIntegrals=False,counts=counts)	
		EEhist = stackEE.theHistogram.Clone("eeHist")
		MuMuhist = stackMM.theHistogram.Clone("mmHist")
		EMuhist = stackEM.theHistogram.Clone("emuHist")
		lumi = lumi / 1000
	else:
			
		
		for name, tree in EEtrees.iteritems():
			
			if name == sampleName:
				EEhist=createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
				eeTree = tree.CopyTree(cuts)
				eeTreeLowMass = tree.CopyTree(cutsLowMass)
				eeTreeHighMass = tree.CopyTree(cutsHighMass)					
				eeTreePeak = tree.CopyTree(cutsPeak)
		for name, tree in MuMutrees.iteritems():
			if name == sampleName:
				MuMuhist=createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
				mmTree = tree.CopyTree(cuts)
				mmTreeLowMass = tree.CopyTree(cutsLowMass)
				mmTreeHighMass = tree.CopyTree(cutsHighMass)
				mmTreePeak = tree.CopyTree(cutsPeak)				
		for name, tree in EMutrees.iteritems():
			if name == sampleName:
				EMuhist=createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
				emTree = tree.CopyTree(cuts)
				emTreeLowMass = tree.CopyTree(cutsLowMass)
				emTreeHighMass = tree.CopyTree(cutsHighMass)
				emTreePeak = tree.CopyTree(cutsPeak)				
			
			
	if argv[2] == "SF":	
		SFhist = EEhist.Clone()
		SFhist.Add(MuMuhist.Clone())
			
			
	elif argv[2] == "EE":
		SFhist = EEhist.Clone()	
		
	else:
		SFhist = MuMuhist.Clone()	

	
	
	nllPredictionScale	= corrections[argv[1]][argv[2]][0]	
	nllPredictionScaleErr	= corrections[argv[1]][argv[2]][1]	
	
	
	result = {}
	if useMC:
		peak = (SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))- EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))*nllPredictionScale) 
		peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81),EMuhist.FindBin(101))*nllPredictionScale)**2)
		continuum = (SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(70-0.01)) - EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70-0.01))*nllPredictionScale )
		continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale)**2) 
		highMass = (SFhist.Integral(SFhist.FindBin(120+0.01),SFhist.FindBin(1000)) - EMuhist.Integral(EMuhist.FindBin(120+0.01),EMuhist.FindBin(1000))*nllPredictionScale )
		highMassError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(120+0.01),SFhist.FindBin(1000)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(120+0.01),EMuhist.FindBin(1000))*nllPredictionScale)**2) 		
		result["peakSF"] = SFhist.Integral(SFhist.FindBin(81+0.01),SFhist.FindBin(101-0.01))
		result["peakOF"] = EMuhist.Integral(EMuhist.FindBin(81+0.01),EMuhist.FindBin(101-0.01))
		result["continuumSF"] = SFhist.Integral(SFhist.FindBin(minMll+0.01),SFhist.FindBin(70-0.01))
		result["continuumOF"] = EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70-0.01))
		result["highMassSF"] = SFhist.Integral(SFhist.FindBin(120+0.01),SFhist.FindBin(1000))
		result["highMassOF"] = EMuhist.Integral(EMuhist.FindBin(120+0.01),EMuhist.FindBin(1000))
		
	else:
	
		if argv[2] == "SF":			
			result["peakSF"] = mmTreePeak.GetEntries() + eeTreePeak.GetEntries()
			result["peakOF"] = emTreePeak.GetEntries() 
			result["continuumSF"] = mmTreeLowMass.GetEntries() + eeTreeLowMass.GetEntries() 
			result["continuumOF"] = emTreeLowMass.GetEntries()
			result["highMassSF"] = mmTreeHighMass.GetEntries() + eeTreeHighMass.GetEntries() 
			result["highMassOF"] = emTreeHighMass.GetEntries() 			 	
		elif argv[2] == "EE":
			result["peakSF"] = eeTreePeak.GetEntries()
			result["peakOF"] = emTreePeak.GetEntries()
			result["continuumSF"] = eeTreeLowMass.GetEntries()
			result["continuumOF"] = emTreeLowMass.GetEntries()
			result["highMassSF"] = eeTreeHighMass.GetEntries() 
			result["highMassOF"] = emTreeHighMass.GetEntries() 					
		else:
			result["peakSF"] = mmTreePeak.GetEntries()
			result["peakOF"] = emTreePeak.GetEntries()
			result["continuumSF"] = mmTreeLowMass.GetEntries()
			result["continuumOF"] = emTreeLowMass.GetEntries()		
			result["highMassSF"] = mmTreeHighMass.GetEntries() 
			result["highMassOF"] = emTreeHighMass.GetEntries()
			 				
			peak = mmTreePeak.GetEntries() + eeTreePeak.GetEntries()  - emTreePeak.GetEntries()*nllPredictionScale 
			peakError = sqrt(sqrt(mmTreePeak.GetEntries())**2 +sqrt(eeTreePeak.GetEntries())**2 + sqrt((emTreePeak.GetEntries() )*nllPredictionScale)**2 + sqrt((emTreePeak.GetEntries())*nllPredictionScaleErr*nllPredictionScale)**2 )
			continuum =mmTreeLowMass.GetEntries() + eeTreeLowMass.GetEntries()  - (emTreeLowMass.GetEntries())*nllPredictionScale 
			continuumError =  sqrt(sqrt(mmTreeLowMass.GetEntries())**2 +sqrt(eeTreeLowMass.GetEntries())**2 + sqrt((emTreeLowMass.GetEntries())*nllPredictionScale)**2 + sqrt((emTreeLowMass.GetEntries())*nllPredictionScaleErr*nllPredictionScale)**2 )
			highMass =mmTreeHighMass.GetEntries() + eeTreeHighMass.GetEntries()  - (emTreeHighMass.GetEntries())*nllPredictionScale 
			highMassError =  sqrt(sqrt(mmTreeHighMass.GetEntries())**2 +sqrt(eeTreeHighMass.GetEntries())**2 + sqrt((emTreeHighMass.GetEntries())*nllPredictionScale)**2 + sqrt((emTreeHighMass.GetEntries())*nllPredictionScaleErr*nllPredictionScale)**2 )				
				
	peak = result["peakSF"] - result["peakOF"]*nllPredictionScale			
	peakError = sqrt(result["peakSF"] + (sqrt(result["peakOF"])*nllPredictionScale)**2 + (sqrt(result["peakOF"])*nllPredictionScale*nllPredictionScaleErr)**2)
	continuum = result["continuumSF"] - result["continuumOF"]*nllPredictionScale			
	continuumError = sqrt(result["continuumSF"] + (sqrt(result["continuumOF"])*nllPredictionScale)**2 + (sqrt(result["continuumOF"])*nllPredictionScale*nllPredictionScaleErr)**2)
	highMass = result["highMassSF"] - result["highMassOF"]*nllPredictionScale			
	highMassError = sqrt(result["highMassSF"] + (sqrt(result["highMassOF"])*nllPredictionScale)**2 + (sqrt(result["highMassOF"])*nllPredictionScale*nllPredictionScaleErr)**2)			
	result["peak"] = peak
	result["peakError"] = peakError
	result["continuum"] = continuum
	result["continuumError"] = continuumError
	result["highMass"] = highMass
	result["highMassError"] = highMassError
	result["correction"] = 	nllPredictionScale
	result["correctionErr"] = 	nllPredictionScaleErr
	
	Rinout =   continuum / peak
	RinoutHighMass = highMass / peak
	ErrRinoutSyst = Rinout*0.25
	ErrRinoutHighMassSyst = RinoutHighMass*0.25
	ErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
	ErrRinoutHighMass = sqrt((highMassError/peak)**2 + (highMass*peakError/peak**2)**2)

	result["rInOut"] = Rinout
	result["rInOutErr"] = ErrRinout
	result["rInOutSyst"] = ErrRinoutSyst
	result["rInOutHighMass"] = RinoutHighMass
	result["rInOutHighMassErr"] = ErrRinoutHighMass
	result["rInOutHighMassSyst"] = ErrRinoutHighMassSyst
	if not useMC:
		outFilePkl = open("shelves/rInOut_Data_%s.pkl"%suffix,"w")
	else:
		outFilePkl = open("shelves/rInOut_MC_%s.pkl"%suffix,"w")
	pickle.dump(result, outFilePkl)
	outFilePkl.close()





	plotMllSpectra(SFhist,EMuhist,suffix,Simulation=useMC)
	plotSystematics(EEtrees,MuMutrees,EMutrees,suffix,RinoutHighMass,highMass=True,Simulation=useMC)
	plotSystematics(EEtrees,MuMutrees,EMutrees,suffix,Rinout,highMass=False,Simulation=useMC)



