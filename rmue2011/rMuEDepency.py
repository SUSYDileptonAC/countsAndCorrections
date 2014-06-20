#!/usr/bin/env python



			
cutStrings = {"SignalForward": "weight*(chargeProduct < 0 && ((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && runNr < 201678 && !(runNr >= 198049 && runNr <= 198522) )",
			"SignalCentral": "weight*(chargeProduct < 0 && ((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  abs(eta1) < 1.4 && abs(eta2) < 1.4 && pt1 > 20 && pt2 > 20 && p4.M() > 20 && deltaR > 0.3 && runNr < 201678 && !(runNr >= 198049 && runNr <= 198522) )",
			"ControlForward": "weight*(chargeProduct < 0 && nJets == 2 && met < 150 && met > 100 &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && runNr < 201678 && !(runNr >= 198049 && runNr <= 198522) )",
			"ControlCentral": "weight*(chargeProduct < 0 && nJets == 2 && met < 150 && met > 100 &&  abs(eta1) < 1.4 && abs(eta2) < 1.4 && pt1 > 20 && pt2 > 20 && p4.M() > 20 && deltaR > 0.3 && runNr < 201678 && !(runNr >= 198049 && runNr <= 198522) )",
			}

regionNames = {"SignalForward":"Signal Region Forward",
				"SignalCentral":"Signal Region Central",
				"ControlCentral":"Control Region Central",
				"ControlForward":"Control Region Forward",			
				}
				
rMuEs = {"SignalCentral":1.10,"SignalForward":1.20,"ControlCentral":1.10,"ControlForward":1.20}
rMuEErrs = {"SignalCentral":0.110,"SignalForward":0.18,"ControlCentral":0.110,"ControlForward":0.18}

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

		
def rMuEMeasure(eeHist,mumuHist):
	from math import sqrt
	result = {"vals":[],"errs":[]}
	for x in range(1,eeHist.GetNbinsX()+1):
		if mumuHist.GetBinContent(x) > 0 and eeHist.GetBinContent(x) > 0:
			val = sqrt(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x))	
			#~ err = 1./(0.5*val)*sqrt((sqrt(mumuHist.GetBinContent(x))/eeHist.GetBinContent(x))**2+(mumuHist.GetBinContent(x)/eeHist.GetBinContent(x)**2*sqrt(eeHist.GetBinContent(x)))**2)
			err = 0.5*val*sqrt(1./float(eeHist.GetBinContent(x)) + 1./float(mumuHist.GetBinContent(x)) )
			result["vals"].append(val)
			result["errs"].append(err)
		else:
			result["vals"].append(0)
			result["errs"].append(0)
	return result

def main():
	from sys import argv
	import ROOT
	from ROOT import TCanvas, TGraphErrors, TPad, TChain, TH1F, TLegend, TF1
	from numpy import array
	from setTDRStyle import setTDRStyle
	
	region = argv[1]
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()		

	path = "/home/jan/Trees/sw532v0474/sw532v0474.processed.MergedData.root"
	pathMC = "/home/jan/Trees/sw532v0474/sw532v0474.processed.TTJets_MGDecays_madgraph_Summer12.root"
	
	
	treeEMu = TChain()
	treeEMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EMu"))
	treeMuMu = TChain()
	treeMuMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "MuMu"))
	treeEE = TChain()
	treeEE.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EE"))	
	
	treeEMuMC = TChain()
	treeEMuMC.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(pathMC, "EMu"))
	treeMuMuMC = TChain()
	treeMuMuMC.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(pathMC, "MuMu"))
	treeEEMC = TChain()
	treeEEMC.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(pathMC, "EE"))	

	cutString = cutStrings[region]
	variable = "p4.M()"
	eeHist = createHistoFromTree(treeEE,variable,cutString,15,0,300)
	mumuHist = createHistoFromTree(treeMuMu,variable,cutString,15,0,300)
	emuHist = createHistoFromTree(treeEMu,variable,cutString,15,0,300)
	
	eeHistMC = createHistoFromTree(treeEEMC,variable,cutString,60,0,300)
	mumuHistMC = createHistoFromTree(treeMuMuMC,variable,cutString,60,0,300)
	emuHistMC = createHistoFromTree(treeEMuMC,variable,cutString,60,0,300)

	rMuEMeasured = rMuEMeasure(eeHist,mumuHist)	
	rMuEMeasuredMC = rMuEMeasure(eeHistMC,mumuHistMC)	
	
	hCanvas.DrawFrame(20,0,300,2.5,"; %s ; %s" %("m_{ll} [GeV]","r_{#mu e}"))			
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	x= array([20, 300],"f") 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	y= array([rMuEs[region], rMuEs[region]],"f") # 1.237
   	ex= array([0.,0.],"f")
   	ey= array([rMuEErrs[region], rMuEErrs[region]],"f")
   	ge= ROOT.TGraphErrors(2, x, y, ex, ey)
   	ge.SetFillColor(ROOT.kOrange-9)
   	ge.SetFillStyle(1001)
   	ge.SetLineColor(ROOT.kWhite)
   	ge.Draw("SAME 3")
   	
	rmueline= ROOT.TF1("rmueline","%s"%rMuEs[region],20, 300)
	rmueline.SetLineColor(ROOT.kOrange+3)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME")   		
	
	#~ rMuEHigh = [2.45,1,1.28]
	#~ rMuELow = [0.41,1,0.78]		
	
	

	arrayRMuEMeasured = array(rMuEMeasured["vals"],"d")
	arrayRMuEMeasuredUncert = array(rMuEMeasured["errs"],"d")

	arrayRMuEMeasuredMC = array(rMuEMeasuredMC["vals"],"d")
	arrayRMuEMeasuredUncertMC = array(rMuEMeasuredMC["errs"],"d")
	xValues = []
	xValuesUncert = []
	xValuesMC = []
	xValuesUncertMC = []
	for x in range(0,eeHist.GetNbinsX()):	
		xValues.append(10+x*20)
		xValuesUncert.append(0)
	for x in range(0,eeHistMC.GetNbinsX()):	
		xValuesMC.append(2.5+x*5)
		xValuesUncertMC.append(0)
	
	arrayXValues = array(xValues,"d")
	arrayXValuesUncert = array(xValuesUncert,"d")
	arrayXValuesMC = array(xValuesMC,"d")
	arrayXValuesUncertMC = array(xValuesUncertMC,"d")
	

	graphMeasured = TGraphErrors(eeHist.GetNbinsX(),arrayXValues,arrayRMuEMeasured,arrayXValuesUncert,arrayRMuEMeasuredUncert)
	graphMeasuredMC = TGraphErrors(eeHistMC.GetNbinsX(),arrayXValuesMC,arrayRMuEMeasuredMC,arrayXValuesUncertMC,arrayRMuEMeasuredUncertMC)
	
	

	graphMeasured.SetMarkerStyle(23)
	graphMeasuredMC.SetMarkerStyle(22)
	graphMeasured.SetMarkerColor(ROOT.kGreen+3)
	graphMeasuredMC.SetMarkerColor(ROOT.kBlue+3)
	graphMeasured.SetLineColor(ROOT.kGreen+3)
	graphMeasuredMC.SetLineColor(ROOT.kBlue+3)

	fit = TF1("dataFit","pol1",0,300)
	fit.SetLineColor(ROOT.kGreen+3)
	fitMC = TF1("mcFit","pol1",0,300)
	fitMC.SetLineColor(ROOT.kBlue+3)
	graphMeasured.Fit("dataFit")
	graphMeasuredMC.Fit("mcFit")

	graphMeasured.Draw("sameEP0")
	graphMeasuredMC.Draw("sameEP0")
	
	
	ROOT.gStyle.SetOptFit(0)
	
	legend = TLegend(0.6, 0.7, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	legend.AddEntry(entryHist,regionNames[region],"h")
	legend.AddEntry(rmueline,"r_{#mu e} from Z peak","l")
	legend.AddEntry(ge,"Syst. Uncert. of r_{#mu e}","f")
	legend.AddEntry(graphMeasured,"r_{#mu e} = #sqrt{N_{#mu#mu}/N_{ee}} Data","p")
	legend.AddEntry(graphMeasuredMC,"r_{#mu e} = #sqrt{N_{#mu#mu}/N_{ee}} MC","p")

	latex = ROOT.TLatex()
	latex.SetTextSize(0.035)	
	latex.SetNDC()	
	latex.DrawLatex(0.2, 0.25, "Fit on data: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))
	latex.DrawLatex(0.2, 0.20, "Fit on MC:   %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fitMC.GetParameter(0),fitMC.GetParError(0),fitMC.GetParameter(1),fitMC.GetParError(1)))
	
	
	legend.Draw("same")
	plotPad.RedrawAxis()
	hCanvas.Print("rMuMllDepedency_%s.pdf"%region)
	
	
	
	
	
	
	
main()
