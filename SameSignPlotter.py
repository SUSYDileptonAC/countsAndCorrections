#!/usr/bin/env python


cutStrings = {"SignalHighMET":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 150 && ht > 100 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15  && id2 < 0.15)",
				"BarrelHighMET":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 150 && ht > 100 && nJets >=2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)&& id1 < 0.15  && id2 < 0.15)",
				"SignalLowMET":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && nJets >=3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)&& id1 < 0.15  && id2 < 0.15)",
				"SignalLowMETFullEta":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 100  && nJets >=3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)&& id1 < 0.15  && id2 < 0.15)",	
				"ControlBarrel":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<1.4  && abs(eta2) < 1.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && met < 150  && nJets ==2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)&& id1 < 0.15  && id2 < 0.15)",	
				"ControlInclusive":"weight*(chargeProduct > 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && met > 100 && met < 150 && nJets ==2 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)&& id1 < 0.15  && id2 < 0.15)",	
			}

regionNames = {"SignalHighMET":"High E_{T}^{miss} inclusive",
				"BarrelHighMET":"High E_{T}^{miss} central",
				"SignalLowMET":"Low E_{T}^{miss} central",
				"SignalLowMETFullEta":"Low E_{T}^{miss} inclusive",
				"ControlBarrel":"Control region central",
				"ControlInclusive":"Control region inclusive",
				}
				
				
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
				

def main():
	
	from sys import argv
	import ROOT
	from ROOT import TCanvas, TGraphErrors, TPad, TChain, TH1F, TLegend
	from numpy import array
	from setTDRStyle import setTDRStyle
	

	region = argv[1]
	relaxedIso = False
	if len(argv) > 2:
		relaxedIso = argv[2]
	
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()		
	
	path = "/home/jan/Trees/sw532v0470/sw532v0470.processed.MergedData.root"
	if relaxedIso:
			path = "/home/jan/Trees/nonIsolated/sw532v0473.processed.MergedData.root"
	
	
	treeEMu = TChain()
	treeEMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EMu"))
	treeMuMu = TChain()
	treeMuMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "MuMu"))
	treeEE = TChain()
	treeEE.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EE"))	

	cutString = cutStrings[region]
	if relaxedIso:
		cutString = cutString.replace("id1 < 0.15","((id1 > 0.15 && id1 < 1 && id2 < 1) || ")
		cutString = cutString.replace("&& id2 < 0.15","(id2 > 0.15 && id2 < 1 && id1 < 1))")
	variable = "p4.M()"
	eeHist = createHistoFromTree(treeEE,variable,cutString,100,0,500)
	mumuHist = createHistoFromTree(treeMuMu,variable,cutString,100,0,500)
	emuHist = createHistoFromTree(treeEMu,variable,cutString,100,0,500)		
	
	eeHist.SetMarkerColor(ROOT.kGreen+2)
	eeHist.SetLineColor(ROOT.kGreen+2)
	mumuHist.SetMarkerColor(ROOT.kBlue+2)
	mumuHist.SetLineColor(ROOT.kBlue+2)
	emuHist.SetMarkerColor(ROOT.kBlack)
	emuHist.SetLineColor(ROOT.kBlack)
	if relaxedIso:
		hCanvas.DrawFrame(20,0,250,25,"; %s ; %s" %("m_{ll} [GeV]","Events / GeV"))	
	else:
		hCanvas.DrawFrame(20,0,250,10,"; %s ; %s" %("m_{ll} [GeV]","Events / GeV"))					
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	

	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.17, 0.8, "#splitline{ee: %d low mass %d full range}{#splitline{#mu#mu: %d low mass %d full range}{e#mu: %d low mass %d full range}}"%(eeHist.Integral(eeHist.FindBin(20),eeHist.FindBin(70)),eeHist.Integral(eeHist.FindBin(20),eeHist.FindBin(250)),mumuHist.Integral(mumuHist.FindBin(20),mumuHist.FindBin(70)),mumuHist.Integral(mumuHist.FindBin(20),mumuHist.FindBin(250)),emuHist.Integral(emuHist.FindBin(20),emuHist.FindBin(70)),emuHist.Integral(emuHist.FindBin(20),emuHist.FindBin(250))))

	
	legend = TLegend(0.6, 0.6, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	if relaxedIso:
		legend.AddEntry(entryHist,regionNames[region]+" relaxed Iso","h")
	else:
		legend.AddEntry(entryHist,regionNames[region],"h")
	legend.AddEntry(eeHist,"Same Sign ee","p")
	legend.AddEntry(mumuHist,"Same Sign #mu#mu","p")
	legend.AddEntry(emuHist,"Same Sign e#mu","p")

	eeHist.Draw("samepe")
	mumuHist.Draw("samepe")
	emuHist.Draw("samepe")
	
	legend.Draw("same")
	if relaxedIso:
		hCanvas.Print("SSPlot_RelaxedIso_%s.pdf"%region)	
	else:
		hCanvas.Print("SSPlot_%s.pdf"%region)
	
	
main()
