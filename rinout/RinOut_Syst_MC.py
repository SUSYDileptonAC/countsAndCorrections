import ROOT
import numpy 
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
	path = "/user/schomakers/Trees"
	
	from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	ptCuts = "pt1 > 20 && pt2 > 20"#(pt1 > 10 && pt2 > 20 || pt1 > 20 && pt2 > 10)
	ptCutLabel = "20"#"20(10)"
	variable = "p4.M()"
	cuts = "weight*(chargeProduct < 0 && %s && met < 100 && nJets ==2 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && deltaR > 0.3 && runNr < 201657 && (runNr < 198049 || runNr > 198522))"%ptCuts
	nEvents=-1
	minMll = 15
	lumi = 9.2	
	Lumi = 9200
	
	xSecAStar = 877.
	xSecZJets = 3503.71
	xSecTTJets = 225.2
	
	nEventsAStar = 7132199
	nEventsZJets = 30219425
	nEventsTTJets = 6883750
		
	scaleFactorAstar = Lumi*xSecAStar/nEventsAStar
	scaleFactorZJets = Lumi*xSecZJets/nEventsZJets
	scaleFactorTTJets = Lumi*xSecTTJets/nEventsTTJets
	
	
	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")


	nBins = 200
	firstBin = 0
	lastBin = 200
	for name, tree in EEtrees.iteritems():
		if name[0:10] == "MergedData":
			print name
			EEhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
	for name, tree in MuMutrees.iteritems():
		if name[0:10] == "MergedData":

			MuMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
	for name, tree in EMutrees.iteritems():
		if name[0:10] == "MergedData":

			EMuhist = createHistoFromTree(tree,  variable, cuts, nBins, firstBin, lastBin, nEvents)
		
	SFhist = EEhist.Clone()
	SFhist.Add(MuMuhist.Clone())
	
	
	rmue = 1.20
	trigger = {
		"EE":93.0,
		"EMu":92.5,
		"MuMu":94.4
		}
	nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
	snllPredictionScale = 0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(1.-1./(rmue)**2)*0.1*rmue

	
	peak = (SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101))- EMuhist.Integral(EMuhist.FindBin(81),EMuhist.FindBin(101))*nllPredictionScale) 
	peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(81),SFhist.FindBin(101)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(81),EMuhist.FindBin(101))*nllPredictionScale)**2)
	continuum = (SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)) - EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale )
	continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale)**2) 
	Rinout =   continuum / peak
	ErrRinoutSyst = (snllPredictionScale*EMuhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70))/peak) + (snllPredictionScale*(continuum*SFhist.Integral(EMuhist.FindBin(81),SFhist.FindBin(101)))/(peak**2))

	ErrRinoutSyst = Rinout*0.25

	ErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)

	cuts =  "weight*(chargeProduct < 0 && %s && met < %d && met > %d && nJets == %d && runNr <= 196531 && deltaR > 0.3 && abs(eta1)<2.4 && abs(eta2)<2.4)"
	
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(1)
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
	nBins = 200
	firstBin = 0
	lastBin = 200
	metRange = 7
	metBinsUp=[10,20,40,60,100,150,300]
	metBinsDown=[0,10,20,40,60,100,150]
	Rinout1Jets = []
	ErrRinout1Jets = []	
	Rinout2Jets = []
	ErrRinout2Jets = []	
	Rinout3Jets = []
	ErrRinout3Jets = []	
	for nJets in range (1,4):
		for index in range (0,metRange):
			
			legend.Clear()
			print nJets  
			for name, tree in EEtrees.iteritems():
				if name[0:5] == "AStar":
					print name
					EEhistAStar = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EEhistAStar.Scale(scaleFactorAstar)

				if name[0:5] == "ZJets":
					print name
					EEhistZJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EEhistZJets.Scale(scaleFactorZJets)
				if name[0:6] == "TTJets":
					print name
					EEhistTTJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EEhistTTJets.Scale(scaleFactorTTJets)
			for name, tree in MuMutrees.iteritems():
				if name[0:5] == "AStar":

					MuMuhistAStar = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					MuMuhistAStar.Scale(scaleFactorAstar)
				if name[0:5] == "ZJets":

					MuMuhistZJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					MuMuhistZJets.Scale(scaleFactorZJets)
				if name[0:6] == "TTJets":

					MuMuhistTTJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					MuMuhistTTJets.Scale(scaleFactorTTJets)
			for name, tree in EMutrees.iteritems():
				if name[0:5] == "AStar":

					EMuhistAStar = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EMuhistAStar.Scale(scaleFactorAstar)
				if name[0:5] == "ZJets":

					EMuhistZJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EMuhistZJets.Scale(scaleFactorZJets)
				if name[0:6] == "TTJets":

					EMuhistTTJets = createHistoFromTree(tree,  variable, cuts %(ptCuts,metBinsUp[index],metBinsDown[index],nJets), nBins, firstBin, lastBin, nEvents)
					EMuhistTTJets.Scale(scaleFactorTTJets)
			SFhist = EEhistAStar.Clone()
			SFhist.Add(MuMuhistAStar.Clone())
			SFhist.Add(MuMuhistZJets.Clone())
			SFhist.Add(EEhistZJets.Clone())
			SFhist.Add(MuMuhistTTJets.Clone())
			SFhist.Add(EEhistTTJets.Clone())
			SFhist.Draw("")
			SFhist.GetXaxis().SetTitle("m(ll) [GeV]")
			SFhist.GetYaxis().SetTitle("Events / 2 GeV")
			EMuhist = EMuhistAStar.Clone()
			EMuhist.Add(EMuhistZJets.Clone())
			EMuhist.Add(EMuhistTTJets.Clone())
			EMuhist.Draw("samehist")
			#EMuhist.SetLineColor(855)
			EMuhist.SetFillColor(855)
			legend.AddEntry(SFhist,"SF events","p")
			legend.AddEntry(EMuhist,"OF events","f")
			legend.Draw("same")
			hCanvas.SetLogy()
			
			line1 = ROOT.TLine(20,0,20,SFhist.GetBinContent(SFhist.GetMaximumBin()))
			line2 = ROOT.TLine(70,0,70,SFhist.GetBinContent(SFhist.GetMaximumBin()))
			line3 = ROOT.TLine(71,0,71,SFhist.GetBinContent(SFhist.GetMaximumBin()))
			line4 = ROOT.TLine(111,0,111,SFhist.GetBinContent(SFhist.GetMaximumBin()))
			line1.SetLineColor(ROOT.kBlue)
			line2.SetLineColor(ROOT.kBlue)
			line3.SetLineColor(ROOT.kRed+3)
			line4.SetLineColor(ROOT.kRed+3)
			line1.SetLineWidth(2)
			line2.SetLineWidth(2)
			line3.SetLineWidth(2)
			line4.SetLineWidth(2)
			line1.Draw("same")
			line2.Draw("same")
			line3.Draw("same")
			line4.Draw("same")
			Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"In")
			Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"Out")
			Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin()/10),"#splitline{p_{T}^{lepton} > 20(10) GeV}{%d GeV < met < %d GeV, nJets ==%d}" %(metBinsDown[index],metBinsUp[index],nJets))
			#~ Labelin.DrawLatex(82.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"In")
			#~ Labelout.DrawLatex(37.25,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"Out")
			#~ Cutlabel.DrawLatex(120,SFhist.GetBinContent(SFhist.GetMaximumBin())/2,"#splitline{p_{T}^{lepton} > 20(10) GeV}{MET < 100 GeV, nJets ==3}")
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.04)
			latex.SetNDC(True)
			latex.DrawLatex(0.05, 0.96, "CMS Simulation  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 5.1fb^{-1}")
			
			
			hCanvas.Print("Rinout_%dJets_MET%d_MC.pdf"%(nJets,metBinsUp[index]))

			peak = (SFhist.Integral(SFhist.FindBin(71),SFhist.FindBin(111))- EMuhist.Integral(EMuhist.FindBin(71),EMuhist.FindBin(111))*nllPredictionScale) 
			peakError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(71),SFhist.FindBin(111)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(71),EMuhist.FindBin(111))*nllPredictionScale)**2)
			continuum = (SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)) - EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale )
			continuumError = sqrt(sqrt(SFhist.Integral(SFhist.FindBin(minMll),SFhist.FindBin(70)))**2 + sqrt(EMuhist.Integral(EMuhist.FindBin(minMll),EMuhist.FindBin(70))*nllPredictionScale)**2) 
			localRinout =   continuum / peak			
			
			#localRinout = SFhist.Integral(SFhist.FindBin(15),SFhist.FindBin(70)) / SFhist.Integral(SFhist.FindBin(71),SFhist.FindBin(111))
			localErrRinout = sqrt((continuumError/peak)**2 + (continuum*peakError/peak**2)**2)
			print localRinout
			print localErrRinout
			if nJets==1:
				Rinout1Jets.append(localRinout)
				ErrRinout1Jets.append(localErrRinout)
			if nJets==2:
				Rinout2Jets.append(localRinout)
				ErrRinout2Jets.append(localErrRinout)
			if nJets==3:
				Rinout3Jets.append(localRinout)
				ErrRinout3Jets.append(localErrRinout)
				
	hCanvas.Clear()			
	hCanvas.SetLogy(0)	
	
	arg6 = numpy.array([0,305],"d")
	arg7 = numpy.array([Rinout,Rinout],"d")
	arg8 = numpy.array([0,0],"d")
	arg9 = numpy.array([Rinout*0.1,Rinout*0.1],"d")
	
	errorband = ROOT.TGraphErrors(2,arg6,arg7,arg8,arg9)
	errorband.GetYaxis().SetRangeUser(0.05,0.25)
	errorband.GetXaxis().SetRangeUser(0,305)
	errorband.GetXaxis().SetTitle("MET [GeV]")
	errorband.GetYaxis().SetTitle("R_{out,in}")
	errorband.Draw("A3")
	errorband.SetFillColor(ROOT.kOrange-9)
	rinoutLine = ROOT.TLine(0,0.1288,305,0.1288)
	rinoutLine.SetLineStyle(ROOT.kDashed)
	rinoutLine.SetLineWidth(2)
	rinoutLine.Draw("same")

	METvalues =[5,15,30,50,80,125,225]
	METErrors =[5,5,10,10,20,25,75]
	arg2 = numpy.array(METvalues,"d")
	arg3 = numpy.array(Rinout1Jets,"d")
	arg4 = numpy.array(METErrors,"d")
	arg5 = numpy.array(ErrRinout1Jets,"d")	
	#~ graph1jet = ROOT.TGraphErrors(6,METvalues,Rinout1Jets,METErrors,ErrRinout1Jets)
	graph1jet = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graph1jet.Draw("Psame")
	graph1jet.GetYaxis().SetTitle("R_{in,out}")
	graph1jet.GetYaxis().SetRangeUser(0.,0.3)
	graph1jet.GetXaxis().SetTitle("MET < x [GeV]")
	arg3 = numpy.array(Rinout2Jets,"d")
	arg5 = numpy.array(ErrRinout2Jets,"d")
	graph2jet = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graph2jet.Draw("Psame")
	graph2jet.SetMarkerColor(ROOT.kGreen+3)
	graph2jet.SetLineColor(ROOT.kGreen+3)
	arg3 = numpy.array(Rinout3Jets,"d")
	arg5 = numpy.array(ErrRinout3Jets,"d")
	graph3jet = ROOT.TGraphErrors(metRange,arg2,arg3,arg4,arg5)
	graph3jet.Draw("Psame")
	graph3jet.SetMarkerColor(ROOT.kBlue)
	graph3jet.SetLineColor(ROOT.kBlue)
	legend.Clear()
	legend.AddEntry(graph1jet,"NJets==1","p")
	legend.AddEntry(graph2jet,"NJets==2","p")
	legend.AddEntry(graph3jet,"NJets==3","p")
	legend.AddEntry(errorband, "R_{out,in} #pm 10%","f")
	legend.Draw("same")
	latex2 = ROOT.TLatex()
	latex2.SetTextSize(0.04)
	latex2.SetNDC(True)
	latex2.DrawLatex(0.2, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = 5.1fb^{-1}")
	hCanvas.Print("RinoutSyst_MC.pdf")
	
