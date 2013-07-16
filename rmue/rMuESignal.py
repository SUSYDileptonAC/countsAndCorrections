#!/usr/bin/env python


cutStrings = {"SignalHighMET":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 150 && ht > 100 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",
				"BarrelHighMET":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 150 && ht > 100 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",
				"SignalLowMET":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && nJets >=3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",
				"SignalLowMETFullEta":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 100  && nJets >=3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",
				"ControlBarrel":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && met < 150  && nJets ==2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",	
				"ControlInclusive":"weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && met < 150 && nJets ==2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522))",						
			}

regionNames = {"SignalHighMET":"High E_{T}^{miss} inclusive",
				"BarrelHighMET":"High E_{T}^{miss} central",
				"SignalLowMET":"Low E_{T}^{miss} central",
				"SignalLowMETFullEta":"Low E_{T}^{miss} inclusive",
				"ControlBarrel":"Control region central",
				"ControlInclusive":"Control region inclusive",				
				}
				
rMuEs = {"SignalHighMET":1.21,"BarrelHighMET":1.10,"SignalLowMET":1.10,"SignalLowMETFullEta":1.21,"ControlBarrel":1.10,"ControlInclusive":1.21,}

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

def rMuEFromSFOF(eeHist,mumuHist,emuHist):
	from math import sqrt
	result = {"up":[],"down":[]}
	resultErr = {"up":[],"down":[]}
	
	for x in range(1,eeHist.GetNbinsX()+1):
		print eeHist.GetBinContent(x), mumuHist.GetBinContent(x), emuHist.GetBinContent(x)
		sf = float(eeHist.GetBinContent(x) + mumuHist.GetBinContent(x))
		of = emuHist.GetBinContent(x)*1.02
		if of > 0:
			rSFOF = sf/of
			if eeHist.GetBinContent(x) >0 and mumuHist.GetBinContent(x) >0:
				eemmPart = 1./(eeHist.GetBinContent(x)+mumuHist.GetBinContent(x))
			else: 
				eemmPart = 0.
			if emuHist.GetBinContent(x) >0:
				emPart = 1./emuHist.GetBinContent(x)
			else: 
				emPart = 0.
				
			relErrRSFOF = sqrt(eemmPart + emPart)
			print rSFOF, relErrRSFOF
			if rSFOF >1.05:
				result["up"].append(rSFOF + sqrt(rSFOF**2-1) )
				result["down"].append(rSFOF - sqrt(rSFOF**2-1) )
				
				resultErr["up"].append(rSFOF*relErrRSFOF*(1+rSFOF/sqrt(rSFOF**2-1)))
				resultErr["down"].append(rSFOF*relErrRSFOF*(1-rSFOF/sqrt(rSFOF**2-1)))
			else:
				result["up"].append(1)
				result["down"].append(1)
				
				resultErr["up"].append(rSFOF*relErrRSFOF)
				resultErr["down"].append(rSFOF*relErrRSFOF)				
		else:
			result["up"].append(0)
			result["down"].append(0)
			
			resultErr["up"].append(0)
			resultErr["down"].append(0)			
		
	return result, resultErr
		
def rMuEMeasure(eeHist,mumuHist):
	from math import sqrt
	result = {"vals":[],"errs":[]}
	for x in range(1,eeHist.GetNbinsX()+1):
		if mumuHist.GetBinContent(x) > 0 and eeHist.GetBinContent(x) > 0:
			val = sqrt(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x))	
			#~ err = 1./(0.5*val)*sqrt((sqrt(mumuHist.GetBinContent(x))/eeHist.GetBinContent(x))**2+(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x)**2*sqrt(eeHist.GetBinContent(x)))**2)
			err = sqrt(0.5*val*((float(eeHist.GetBinContent(x)+mumuHist.GetBinContent(x)))/eeHist.GetBinContent(x)**2))
			result["vals"].append(val)
			result["errs"].append(err)
		else:
			result["vals"].append(0)
			result["errs"].append(0)
	return result

def main():
	from sys import argv
	import ROOT
	from ROOT import TCanvas, TGraphErrors, TPad, TChain, TH1F, TLegend,
	from numpy import array
	from setTDRStyle import setTDRStyle
	
	region = argv[1]
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()		

	path = "/home/jan/Trees/sw532v0470/sw532v0470.processed.MergedData.root"
	
	
	treeEMu = TChain()
	treeEMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EMu"))
	treeMuMu = TChain()
	treeMuMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "MuMu"))
	treeEE = TChain()
	treeEE.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EE"))	

	cutString = cutStrings[region]
	variable = "p4.M()"
	eeHist = createHistoFromTree(treeEE,variable,cutString,10,0,200)
	mumuHist = createHistoFromTree(treeMuMu,variable,cutString,10,0,200)
	emuHist = createHistoFromTree(treeEMu,variable,cutString,10,0,200)

	rMuE, rMuEUncert = rMuEFromSFOF(eeHist,mumuHist,emuHist)
	rMuEMeasured = rMuEMeasure(eeHist,mumuHist)	
	
	hCanvas.DrawFrame(20,0,200,5,"; %s ; %s" %("m_{ll} [GeV]","r_{#mu e}"))			
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	x= array([20, 200],"f") 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	y= array([rMuEs[region], rMuEs[region]],"f") # 1.237
   	ex= array([0.,0.],"f")
   	ey= array([rMuEs[region]*0.10, rMuEs[region]*0.10],"f")
   	ge= ROOT.TGraphErrors(2, x, y, ex, ey)
   	ge.SetFillColor(ROOT.kOrange-9)
   	ge.SetFillStyle(1001)
   	ge.SetLineColor(ROOT.kWhite)
   	ge.Draw("SAME 3")
   	
	rmueline= ROOT.TF1("rmueline","%s"%rMuEs[region],20, 200)
	rmueline.SetLineColor(ROOT.kOrange+3)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME")   		
	
	#~ rMuEHigh = [2.45,1,1.28]
	#~ rMuELow = [0.41,1,0.78]		
	
	
	arrayRMuEHigh = array(rMuE["up"],"d")
	arrayRMuELow = array(rMuE["down"],"d")
	arrayRMuEMeasured = array(rMuEMeasured["vals"],"d")
	arrayRMuEHighUncert = array(rMuEUncert["up"],"d")
	arrayRMuELowUncert = array(rMuEUncert["down"],"d")
	arrayRMuEMeasuredUncert = array(rMuEMeasured["errs"],"d")
	xValues = []
	xValuesUncert = []
	for x in range(0,eeHist.GetNbinsX()):	
		xValues.append(10+x*20)
		xValuesUncert.append(0)
	
	arrayXValues = array(xValues,"d")
	arrayXValuesUncert = array(xValuesUncert,"d")
	
	graphHigh = TGraphErrors(eeHist.GetNbinsX(),arrayXValues,arrayRMuEHigh,arrayXValuesUncert,arrayRMuEHighUncert)
	graphLow = TGraphErrors(eeHist.GetNbinsX(),arrayXValues,arrayRMuELow,arrayXValuesUncert,arrayRMuEHighUncert)
	graphMeasured = TGraphErrors(eeHist.GetNbinsX(),arrayXValues,arrayRMuEMeasured,arrayXValuesUncert,arrayRMuEMeasuredUncert)
	
	
	graphHigh.SetMarkerStyle(21)
	graphLow.SetMarkerStyle(22)
	graphMeasured.SetMarkerStyle(23)
	graphHigh.SetMarkerColor(ROOT.kRed)
	graphLow.SetMarkerColor(ROOT.kBlue)
	graphHigh.SetLineColor(ROOT.kRed)
	graphLow.SetLineColor(ROOT.kBlue)
	
	graphHigh.Draw("sameEP0")
	graphLow.Draw("sameEP0")
	graphMeasured.Draw("sameEP0")
	
	
	
	
	legend = TLegend(0.5, 0.6, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	legend.AddEntry(entryHist,regionNames[region],"h")
	legend.AddEntry(graphHigh,"r_{#mu e} = N_{SF}/N_{OF} + #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
	legend.AddEntry(graphLow,"r_{#mu e} = N_{SF}/N_{OF} - #sqrt{(N_{SF}/N_{OF})^{2} -1}","p")
	legend.AddEntry(rmueline,"r_{#mu e} from Z peak","l")
	legend.AddEntry(ge,"Syst. Uncert. of r_{#mu e}","f")
	legend.AddEntry(graphMeasured,"r_{#mu e} = #sqrt{N_{#mu#mu}/N_{ee}} in SF signal region","p")
	
	legend.Draw("same")
	
	hCanvas.Print("rMuESignal_%s.pdf"%region)
	
	
	
	
	
	
	
main()
