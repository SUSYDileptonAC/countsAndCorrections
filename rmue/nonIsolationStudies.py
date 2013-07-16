#!/usr/bin/env python

import ROOT

originCuts = {"bothW": "&& abs(motherPdgId1) == 24 && abs(motherPdgId2) == 24 && abs(motherPdgId1) != 15 && abs(motherPdgId2) != 15","oneW": "&& ((abs(motherPdgId1) == 24 && abs(motherPdgId2) != 24) || (abs(motherPdgId1) != 24 && abs(motherPdgId2) == 24)) && abs(motherPdgId1) != 15 && abs(motherPdgId1) != 15","noneW":"&& abs(motherPdgId1) != 24 && abs(motherPdgId2) !=24 && abs(motherPdgId1) != 15 && abs(motherPdgId2) != 15"}
labels = {"bothW":"2 from W decay","oneW":"1 from W decay","noneW":"0 from W decay"}
colors = {"bothW":ROOT.kRed+3,"oneW":ROOT.kBlue+2,"noneW":ROOT.kGreen+2}

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

def printMllPlots(hists,canvas,label):
	from ROOT import TH1F, TCanvas, TPad,TLegend
	from setTDRStyle import setTDRStyle
	canvas.Clear()
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()		
	plotPad.cd()		

	canvas.SetLogy(1)
	plotPad.SetLogy(1)
	canvas.DrawFrame(20,1,250,5000,"; %s ; %s" %("m_{%s} [GeV]"%label,"Events / 10 GeV"))
	
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Simulation  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	
	legend = TLegend(0.6, 0.6, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	legend.AddEntry(entryHist,"Composition non-iso t#bar{t} MC","h")
	
	for key in hists:
		legend.AddEntry(hists[key],labels[key],"p")
		hists[key].Draw("samepe")
	
	legend.Draw("same")
	canvas.Print("mll_NonIso_%s.pdf"%label)


def printRMuEPlot(eeHists,mmHists,canvas):


	from ROOT import TH1F, TCanvas, TPad,TLegend
	from setTDRStyle import setTDRStyle
	canvas.Clear()
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()		
	plotPad.cd()		


	canvas.DrawFrame(20,0,250,1.2,"; %s ; %s" %("m_{ll} [GeV]","r_{#mu e}"))			
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Simulation  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	
	legend = TLegend(0.6, 0.6, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	legend.AddEntry(entryHist,"Composition non-iso t#bar{t} MC","h")
	ratios = {}
	for key in eeHists:
		legend.AddEntry(eeHists[key],labels[key],"p")
		ratios[key] = eeHists[key].Clone()
		ratios[key].Divide(mmHists[key])
		ratios[key].Draw("samepe")
		
	legend.Draw("same")
	
	canvas.Print("rMuE_NonIsoTTbar.pdf")	



def printIsoPlots(hists,canvas,label):
	from ROOT import TH1F, TCanvas, TPad,TLegend,THStack
	from setTDRStyle import setTDRStyle
	canvas.Clear()
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()		
	plotPad.cd()		

	canvas.SetLogy(1)
	plotPad.SetLogy(1)
	canvas.DrawFrame(0,1,5,500000,"; %s ; %s" %("rel. iso (trailing) %s"%label,"Events / 0.1"))
	
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "CMS Simulation  #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %s fb^{-1}"%9.2)
	
	legend = TLegend(0.6, 0.6, 0.95, 0.95)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	entryHist = TH1F()
	entryHist.SetFillColor(ROOT.kWhite)
	legend.AddEntry(entryHist,"Composition non-iso t#bar{t} MC","h")
	
	theStack = THStack()
	
	for key in hists:
		legend.AddEntry(hists[key],labels[key],"f")
		#~ hists[key].Draw("samepe")
		theStack.Add(hists[key])
	theStack.Draw("sameh")
	legend.Draw("same")
	plotPad.RedrawAxis()
	canvas.Print("RelIso_%s.pdf"%label)



def main():
	import ROOT
	from ROOT import TH1F, TCanvas, TPad, THStack, TChain
	
	from setTDRStyle import setTDRStyle

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = TPad("plotPad","plotPad",0,0,1,1)
	
	style=setTDRStyle()
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()			
	
	path = "/home/jan/Trees/nonIsolated/sw532v0473.processed.TTJets_madgraph_Summer12.root"
	
	variable = "p4.M()"

	treeMuMu = TChain()
	treeMuMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "MuMu"))
	treeEE = TChain()
	treeEE.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EE"))
	treeEMu = TChain()
	treeEMu.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, "EMu"))
	
	cutString = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522) && ((id1 > 0.15 && id1 < 1 && id2 < 1) || (id2 > 0.15 && id2 < 1 && id1 < 1)) %s)"
	cutStringNoIso = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && runNr < 201657 && !(runNr >= 198049 && runNr <= 198522)  %s)"
	

	
	preSelection = cutString%""
	preSelectionNoIso = cutStringNoIso%""
	
	treeMuMuNoIso = treeMuMu.CopyTree(preSelectionNoIso)
	treeEENoIso = treeEE.CopyTree(preSelectionNoIso)
	treeEMuNoIso = treeEMu.CopyTree(preSelectionNoIso)
	treeMuMu = treeMuMu.CopyTree(preSelection)
	treeEE = treeEE.CopyTree(preSelection)
	treeEMu = treeEMu.CopyTree(preSelection)
	
	eeHists = {}
	mmHists = {}
	emHists = {}
	
	for key in originCuts:
		
		cut = cutString%originCuts[key]
		eeHists[key] = createHistoFromTree(treeEE,variable,cut,50,0,500)
		emHists[key] = createHistoFromTree(treeMuMu,variable,cut,50,0,500)
		mmHists[key] = createHistoFromTree(treeEMu,variable,cut,50,0,500)
		eeHists[key].SetLineColor(colors[key])
		eeHists[key].SetFillColor(colors[key])
		eeHists[key].SetMarkerColor(colors[key])
		emHists[key].SetLineColor(colors[key])
		emHists[key].SetFillColor(colors[key])
		emHists[key].SetMarkerColor(colors[key])
		mmHists[key].SetLineColor(colors[key])
		mmHists[key].SetFillColor(colors[key])
		mmHists[key].SetMarkerColor(colors[key])
	
	
	printMllPlots(eeHists,hCanvas,"ee")	
	printMllPlots(mmHists,hCanvas,"#mu#mu")	
	printMllPlots(emHists,hCanvas,"e#mu")
	printRMuEPlot(eeHists,mmHists,hCanvas)	
	
	variable = "id1"
	
	eeHists = {}
	mmHists = {}
	emHists = {}
	
	for key in originCuts:
		
		cut = cutStringNoIso%originCuts[key]
		eeHists[key] = createHistoFromTree(treeEENoIso,variable,cut,50,0,5)
		emHists[key] = createHistoFromTree(treeMuMuNoIso,variable,cut,50,0,5)
		mmHists[key] = createHistoFromTree(treeEMuNoIso,variable,cut,50,0,5)
		eeHists[key].SetLineColor(colors[key])
		eeHists[key].SetFillColor(colors[key])
		eeHists[key].SetMarkerColor(colors[key])
		emHists[key].SetLineColor(colors[key])
		emHists[key].SetFillColor(colors[key])
		emHists[key].SetMarkerColor(colors[key])
		mmHists[key].SetLineColor(colors[key])
		mmHists[key].SetFillColor(colors[key])
		mmHists[key].SetMarkerColor(colors[key])
		
	printIsoPlots(eeHists,hCanvas,"ee")
	printIsoPlots(mmHists,hCanvas,"#mu#mu")
			
		
main()
