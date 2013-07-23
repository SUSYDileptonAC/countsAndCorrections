import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)


etaCuts = {
			"Barrel":"abs(eta1) < 1.4 && abs(eta2) < 1.4",
			"Endcap":"((abs(eta1) < 2.4 && abs(eta2) > 1.4) || (abs(eta1) > 1.4 && abs(eta2) < 2.4))",
			"BothEndcap":"abs(eta1) > 1.4 && abs(eta2) > 1.4",
			"Inclusive":"abs(eta1) < 2.4 && abs(eta2) < 2.4"
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
	path = "/user/schomakers/trees"
	from sys import argv	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	ptCut = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	etaCut = etaCuts[argv[1]]
	suffix = argv[1]
	#~ cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCut
	cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && %s && deltaR > 0.3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))"%(ptCut,etaCut)
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
	nBins = 200
	firstBin = 0
	lastBin = 200

	for name, tree in EEtrees.iteritems():
		if name == "MergedData":
			print name
			EEhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
	for name, tree in MuMutrees.iteritems():
		if name == "MergedData":

			MuMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
	for name, tree in EMutrees.iteritems():
		if name == "MergedData":

			EMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
		
	SFhist = EEhist.Clone()
	SFhist.Add(MuMuhist.Clone())
	
	
	rmue = 1.21
	trigger = {
		"EE":97.0,
		"EMu":94.2,
		"MuMu":96.4
		}
	#~ nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
	#~ snllPredictionScale = 0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(1.-1./(rmue)**2)*0.1*rmue
	nllPredictionScale =  1.02
	if "Endcap" in suffix:
		snllPredictionScale = 0.12
	else:
		snllPredictionScale = 0.07

	fitHist = SFhist.Clone()
	fitHist.Add(EMuhist,-1)
	
	expo = TF1("expo","exp([0]+[1]*x)",20,35)
	expo.SetParameter(0,0)
	expo.SetParameter(1,-0.2)
	fitHist.Fit("expo","R")
	fitHist.Draw("p")
	expo.Draw("same")
	hCanvas.SetLogy()
	hCanvas.Print("fit.pdf")
	hCanvas.SetLogy(0)
	print expo.GetParameter(0), expo.GetParameter(1)
	
	peak = (SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101))- EMuhist.Integral(EMuhist.FindBin(81),EMuhist.FindBin(101))*nllPredictionScale) 
	peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81),EMuhist.FindBin(101))*nllPredictionScale)**2)
	continuum = (SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)) - EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale )
	continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale)**2) 
	Rinout =   continuum / peak
	ErrRinoutSyst = (snllPredictionScale*EMuhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70))/peak) + (snllPredictionScale*(continuum*SFhist.Integral(EMuhist.FindBin(81),SFhist.FindBin(101)))/(peak**2))

	ErrRinoutSyst = Rinout*0.25

	ErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
	
	print "R_{in,out} = %f \pm %f (stat.) \pm \%f (syst) "%(Rinout,ErrRinout,ErrRinoutSyst) 	
	print sqrt(ErrRinout**2+ErrRinoutSyst**2)
	ErrRinoutTotal = sqrt(ErrRinoutSyst**2 + ErrRinout**2)
	inPeak = 34
	inPeakError = 4.4
	prediction = inPeak*Rinout
	predictionError = sqrt((inPeak*ErrRinoutTotal**2) + (Rinout*inPeakError)**2)
	
	print prediction
	print predictionError
	
	
	
	SFhist.Rebin(5)
	EMuhist.Rebin(5)
	SFhist.GetXaxis().SetRangeUser(15,200)
	SFhist.Draw("")
	SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
	SFhist.GetYaxis().SetTitle("Events / 5 GeV")
	EMuhist.Draw("samehist")
	#EMuhist.SetLineColor(855)
	EMuhist.SetFillColor(855)
	legend.AddEntry(SFhist,"SF events","p")
	legend.AddEntry(EMuhist,"OF events","f")
	legend.Draw("same")
	#hCanvas.SetLogy()
	
	line1 = ROOT.TLine(minMll,0,minMll,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line3 = ROOT.TLine(81,0,81,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line4 = ROOT.TLine(101,0,101,SFhist.GetBinContent(SFhist.GetMaximumBin()))
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")

	Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
	Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
	Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > %s GeV}{MET < 100 GeV, nJets ==2}"%ptCutLabel)
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.05, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%lumi)
	
	
	hCanvas.Print("Rinout_NoLog_%s.pdf"%suffix)
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
	line1.SetLineColor(ROOT.kBlack)
	line2.SetLineColor(ROOT.kBlack)
	line3.SetLineColor(ROOT.kRed+2)
	line4.SetLineColor(ROOT.kRed+2)
	line1.SetLineWidth(2)
	line2.SetLineWidth(2)
	line3.SetLineWidth(2)
	line4.SetLineWidth(2)
	line1.Draw("same")
	line2.Draw("same")
	line3.Draw("same")
	line4.Draw("same")
	Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/12,"In")
	Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/12,"Out")
	Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/10,"#splitline{p_{T}^{lepton} > %s GeV}{MET < 100 GeV, nJets ==2}"%ptCutLabel)
	latex.DrawLatex(0.05, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%lumi)
	hCanvas.Print("Rinout_%s.pdf"%suffix)	
	
	
	hCanvas.Clear()
	legend.Clear()
	cutsLowMET = "weight*(chargeProduct < 0 && %s && met < 50 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%ptCut
	cutsLowJets = "weight*(chargeProduct < 0 && %s && met > 50 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3)"%ptCut
	for name, tree in EEtrees.iteritems():
		if name == "MergedData":
			print name
			EEhistLowMET = createHistoFromTree(tree,  variable, cutsLowMET, nBins, firstBin, lastBin, nEvents)
			EEhistLowJets = createHistoFromTree(tree,  variable, cutsLowJets, nBins, firstBin, lastBin, nEvents)
	for name, tree in MuMutrees.iteritems():
		if name == "MergedData":

			MuMuhistLowMET = createHistoFromTree(tree,  variable, cutsLowMET, nBins, firstBin, lastBin, nEvents)
			MuMuhistLowJets = createHistoFromTree(tree,  variable, cutsLowJets, nBins, firstBin, lastBin, nEvents)
	for name, tree in EMutrees.iteritems():
		if name == "MergedData":

			EMuhistLowMET = createHistoFromTree(tree,  variable, cutsLowMET, nBins, firstBin, lastBin, nEvents)
			EMuhistLowJets = createHistoFromTree(tree,  variable, cutsLowJets, nBins, firstBin, lastBin, nEvents)
		
	SFhistLowMET = EEhistLowMET.Clone()
	SFhistLowMET.Add(MuMuhistLowMET.Clone())	
	SFhistLowJets = EEhistLowJets.Clone()
	SFhistLowJets.Add(MuMuhistLowJets.Clone())	


	peakLowMET = (SFhistLowMET.Integral(SFhistLowMET.FindBin(81),SFhistLowMET.FindBin(101))- EMuhistLowMET.Integral(EMuhistLowMET.FindBin(81),EMuhistLowMET.FindBin(101))*nllPredictionScale) 
	peakErrorLowMET = sqrt(sqrt(SFhistLowMET.Integral(SFhistLowMET.FindBin(81),SFhistLowMET.FindBin(101)))**2 + sqrt(EMuhistLowMET.Integral(EMuhistLowMET.FindBin(81),EMuhistLowMET.FindBin(101))*nllPredictionScale)**2)
	continuumLowMET = (SFhistLowMET.Integral(SFhistLowMET.FindBin(minMll),SFhistLowMET.FindBin(70)) - EMuhistLowMET.Integral(EMuhistLowMET.FindBin(minMll),EMuhistLowMET.FindBin(70))*nllPredictionScale )
	continuumErrorLowMET = sqrt(sqrt(SFhistLowMET.Integral(SFhistLowMET.FindBin(minMll),SFhistLowMET.FindBin(70)))**2 + sqrt(EMuhistLowMET.Integral(EMuhistLowMET.FindBin(minMll),EMuhistLowMET.FindBin(70))*nllPredictionScale)**2) 
	RinoutLowMET =   continuumLowMET / peakLowMET
	ErrRinoutSystLowMET = (snllPredictionScale*EMuhistLowMET.Integral(SFhistLowMET.FindBin(minMll),SFhistLowMET.FindBin(70))/peak) + (snllPredictionScale*(continuumLowMET*SFhistLowMET.Integral(EMuhistLowMET.FindBin(81),SFhistLowMET.FindBin(101)))/(peak**2))
	ErrRinoutSystLowMET = sqrt(ErrRinoutSystLowMET**2 + (RinoutLowMET*0.1)**2)
	ErrRinoutLowMET = sqrt((continuumErrorLowMET/peakLowMET)**2 + (continuumLowMET*peakErrorLowMET/peak**2)**2)
	
	#~ print "R_{in,out} = %f \pm %f (stat.) \pm \%f (syst) "%(RinoutLowMET,ErrRinoutLowMET,ErrRinoutSystLowMET) 	
	
	
	
	peakLowJets = (SFhistLowJets.Integral(SFhistLowJets.FindBin(81),SFhistLowJets.FindBin(101))- EMuhistLowJets.Integral(EMuhistLowJets.FindBin(81),EMuhistLowJets.FindBin(101))*nllPredictionScale) 
	peakErrorLowJets = sqrt(sqrt(SFhistLowJets.Integral(SFhistLowJets.FindBin(81),SFhistLowJets.FindBin(101)))**2 + sqrt(EMuhistLowJets.Integral(EMuhistLowJets.FindBin(81),EMuhistLowJets.FindBin(101))*nllPredictionScale)**2)
	continuumLowJets = (SFhistLowJets.Integral(SFhistLowJets.FindBin(minMll),SFhistLowJets.FindBin(70)) - EMuhistLowJets.Integral(EMuhistLowJets.FindBin(minMll),EMuhistLowJets.FindBin(70))*nllPredictionScale )
	continuumErrorLowJets = sqrt(sqrt(SFhistLowJets.Integral(SFhistLowJets.FindBin(minMll),SFhistLowJets.FindBin(70)))**2 + sqrt(EMuhistLowJets.Integral(EMuhistLowJets.FindBin(minMll),EMuhistLowJets.FindBin(70))*nllPredictionScale)**2) 
	RinoutLowJets =   continuumLowJets / peakLowJets
	ErrRinoutSystLowJets = (snllPredictionScale*EMuhistLowJets.Integral(SFhistLowJets.FindBin(minMll),SFhistLowJets.FindBin(70))/peak) + (snllPredictionScale*(continuumLowJets*SFhistLowJets.Integral(EMuhistLowJets.FindBin(81),SFhistLowJets.FindBin(101)))/(peak**2))
	ErrRinoutSystLowJets = sqrt(ErrRinoutSystLowJets**2 + (RinoutLowJets*0.1)**2)
	ErrRinoutLowJets = sqrt((continuumErrorLowJets/peakLowJets)**2 + (continuumLowJets*peakErrorLowJets/peak**2)**2)
	
	#~ print "R_{in,out} = %f \pm %f (stat.) \pm \%f (syst) "%(RinoutLowJets,ErrRinoutLowJets,ErrRinoutSystLowJets) 	

	#hCanvas.SetLogy()
	
	SFhistLowMET.Add(EMuhistLowMET,-1)
	SFhistLowJets.Add(EMuhistLowJets,-1)
	SFhistLowJets.Rebin(10)
	SFhistLowMET.Rebin(10)
	
	SFhistLowMET.Draw()
	SFhistLowMET.GetYaxis().SetRangeUser(8,160000)
	SFhistLowMET.GetXaxis().SetTitle("m(ll) [GeV]")
	SFhistLowMET.GetYaxis().SetTitle("Events / 10 GeV")
	SFhistLowJets.SetMarkerColor(ROOT.kBlue)
	SFhistLowJets.Draw("same")
	
	Cutlabel.DrawLatex(105,SFhistLowMET.GetBinContent(SFhistLowMET.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > %s GeV}{SF events after OF subtraction}"%ptCutLabel)
	
	legend.AddEntry(SFhistLowMET, "nJets >= 2, MET < 50 GeV","p")
	legend.AddEntry(SFhistLowJets, "nJets >= 2, MET > 50 GeV","p")
	legend.Draw("same")
	latex.DrawLatex(0.05, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%lumi)
	hCanvas.Print("Lineshape_MET50_%s.pdf"%suffix)


	
