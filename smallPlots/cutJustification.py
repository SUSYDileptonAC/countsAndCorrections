import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import os
import pickle

from messageLogger import messageLogger as log

import math
from math import sqrt
from array import array

import argparse	


import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rSFOFFact, triggerEffs
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations










def getHistograms(path,plot,runRange,isMC,backgrounds):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
	
	
	if isMC:
		
		eventCounts = totalNumberOfGeneratedEvents(path)	
		processes = []
		for background in backgrounds:
			processes.append(Process(getattr(Backgrounds,background),eventCounts))
		histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
		histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
		histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		

			
	else:
		histoEE = getDataHist(plot,treesEE)
		histoMM = getDataHist(plot,treesMM)
		histoEM = getDataHist(plot,treesEM)
	
	return histoEE , histoMM, histoEM
	
def getTrees(path,plot,runRange,background):


	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
				
	
	for index, tree in treesEE.iteritems():
		if index == background:
			treeEE = tree	
	for index, tree in treesMM.iteritems():
		if index == background:
			treeMM = tree	
	for index, tree in treesEM.iteritems():
		if index == background:
			treeEM = tree	

	return treeEE.CopyTree(plot.cuts) , treeMM.CopyTree(plot.cuts), treeEM.CopyTree(plot.cuts)	

def plotIsolation(path,selection,runRange,cmsExtra,backgrounds):

		plot = getPlot("trailingIsoPlot")
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut		
		tmpCuts = plot.cuts

		fake = "!((pt1 < pt 2)*(abs(pdgIdETH1)==11 || abs(pdgIdETH1)==13 || (abs(pdgIdETH1) == 22 && (abs(motherPdgIdETH1) == 11 || abs(motherPdgIdETH1) == 13 )))   || (pt1 > pt 2)*(abs(pdgIdETH2)==11 || abs(pdgIdETH2)==13) || (abs(pdgIdETH2) == 22 && (abs(motherPdgIdETH2) == 11 || abs(motherPdgIdETH2) == 13 )))"

		dilep = "((pt1 < pt 2)*(abs(motherPdgIdETH1)== 24 || abs(motherPdgIdETH1)== 23 || abs(grandMotherPdgIdETH1)== 24 || abs(grandMotherPdgIdETH1)== 23) || (pt1 > pt 2)*(abs(motherPdgIdETH2)== 24 || abs(motherPdgIdETH2)== 23 || abs(grandMotherPdgIdETH2)== 24 || abs(grandMotherPdgIdETH2)== 23))"

		plot.cuts = plot.cuts+"*(%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999))"%(dilep,fake)

		histEEPrompt, histMMPrompt, histEMPrompt = getHistograms(path,plot,runRange,True,backgrounds)



		
		plot.cuts = tmpCuts+"*(!%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999))"%(dilep,fake)
	
		histEEHeavyFlavour, histMMHeavyFlavour, histEMHeavyFlavour = getHistograms(path,plot,runRange,True,backgrounds)

		#~ eventCounts = totalNumberOfGeneratedEvents(path)	
		#~ print eventCounts
		#~ for background in backgrounds:
			#~ process = Process(getattr(Backgrounds,background),eventCounts)
			#~ for subprocess in process.samples:
				#~ 
				#~ print subprocess
				#~ treeEE, treeMM, treeEM = getTrees(path,plot,runRange, subprocess)
				#~ for ev in treeEE:
					
					#~ print ev.pdgIdETH1, ev.motherPdgIdETH1, ev.grandMotherPdgIdETH1, "--", ev.pdgIdETH2, ev.motherPdgIdETH2, ev.grandMotherPdgIdETH2
	
				#~ print treeEE.GetEntries(), treeMM.GetEntries(), treeEM.GetEntries()

		
		plot.cuts = tmpCuts+"*(%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999))"%(fake)
	
		histEEFake, histMMFake, histEMFake = getHistograms(path,plot,runRange,True,backgrounds)
#~ 


		
		histEEPrompt.Add(histMMPrompt)
		histEEPrompt.Add(histEMPrompt)
		
		histEEHeavyFlavour.Add(histMMHeavyFlavour)
		histEEHeavyFlavour.Add(histEMHeavyFlavour)
		
		histEEFake.Add(histMMFake)
		histEEFake.Add(histEMFake)
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		#~ style.SetTitleYOffset(0.70)
		#~ style.SetTitleSize(0.1, "XYZ")
		#~ style.SetTitleYOffset(0.35)
		#~ style.SetTitleXOffset(0.7)
		#~ style.SetPadLeftMargin(0.1)
		#~ style.SetPadTopMargin(0.12)
		#~ style.SetPadBottomMargin(0.17)
		plotPad.UseCurrentStyle()		
		plotPad.Draw()	
		plotPad.cd()	
					
		plotPad.SetLogy()
		plotPad.DrawFrame(plot.firstBin,0.1,plot.lastBin,histEEPrompt.GetBinContent(histEEPrompt.GetMaximumBin())*1000,"; %s ; %s" %(plot.xaxis,plot.yaxis))
		
		
		from ROOT import TH1F,kWhite
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.55,0.65,0.9,0.95)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")	



		histEEPrompt.SetLineColor(ROOT.kBlack)
		histEEPrompt.SetMarkerColor(ROOT.kBlack)
		histEEPrompt.SetMarkerSize(0)
		histEEPrompt.Draw("samehiste")
		histEEHeavyFlavour.SetLineColor(ROOT.kBlue)
		histEEHeavyFlavour.SetMarkerColor(ROOT.kBlue)
		histEEHeavyFlavour.SetMarkerSize(0)
		histEEHeavyFlavour.Draw("samehiste")
		histEEFake.SetLineColor(ROOT.kRed)
		histEEFake.SetMarkerColor(ROOT.kRed)
		histEEFake.SetMarkerSize(0)
		histEEFake.Draw("samehiste")


		legend.AddEntry(histEEPrompt,"prompt leptons","le")	
		legend.AddEntry(histEEHeavyFlavour,"leptons from heavy flavour hadrons","le")	
		legend.AddEntry(histEEFake,"leptons from misidentified jets","le")	


		legend.Draw("same")

		line1 = ROOT.TLine(0.15,0,0.15,histEEPrompt.GetBinContent(histEEPrompt.GetMaximumBin())*10)
		line1.SetLineColor(ROOT.kBlue+3)

		line1.SetLineWidth(2)
		line1.SetLineStyle(2)

		line1.Draw("same")



		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetNDC(True)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)

		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)				

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	



		
		hCanvas.Print("fig/iso_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
			

def plotIsolationEff(path,selection,runRange,cmsExtra,backgrounds):

		plot = getPlot("nVtxPlot")
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut		
		tmpCuts = plot.cuts
		
		backgrounds = ["TTJets_SpinCorrelations"]
		
		fake = "!((pt1 < pt 2)*(abs(pdgIdETH1)==11 || abs(pdgIdETH1)==13 || (abs(pdgIdETH1) == 22 && (abs(motherPdgIdETH1) == 11 || abs(motherPdgIdETH1) == 13 )))   || (pt1 > pt 2)*(abs(pdgIdETH2)==11 || abs(pdgIdETH2)==13) || (abs(pdgIdETH2) == 22 && (abs(motherPdgIdETH2) == 11 || abs(motherPdgIdETH2) == 13 )))"

		dilep = "((pt1 < pt 2)*(abs(motherPdgIdETH1)== 24 || abs(motherPdgIdETH1)== 23 || abs(grandMotherPdgIdETH1)== 24 || abs(grandMotherPdgIdETH1)== 23) || (pt1 > pt 2)*(abs(motherPdgIdETH2)== 24 || abs(motherPdgIdETH2)== 23 || abs(grandMotherPdgIdETH2)== 24 || abs(grandMotherPdgIdETH2)== 23))"

		plot.cuts = plot.cuts+"*(%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999) && (pt1 < pt2)*id2 < 0.15 && (pt2 < pt1)*id1 < 0.15)"%(dilep,fake)

		histEELoose, histMMLoose, histEMLoose = getHistograms(path,plot,runRange,True,backgrounds)

		plot.cuts = tmpCuts+"*(%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999) && id1 < 0.15 && id2 < 0.15)"%(dilep,fake)

		histEETight, histMMTight, histEMTight = getHistograms(path,plot,runRange,True,backgrounds)

		
		#~ histEELoose.Add(histMMLoose)
		#~ histEELoose.Add(histEMLoose)
		#~ 
		#~ histEETight.Add(histMMTight)
		#~ histEETight.Add(histEMTight)

		backgrounds = ["DrellYan"]

		plot.cuts = tmpCuts+"*(%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999) && (pt1 < pt2)*id2 < 0.15 && (pt2 < pt1)*id1 < 0.15)"%(dilep,fake)

		histEELooseDY, histMMLooseDY, histEMLooseDY = getHistograms(path,plot,runRange,True,backgrounds)

		plot.cuts = tmpCuts+"*(%s && !%s && !(pdgIdETH1 == -9999 || pdgIdETH2 == -9999) && id1 < 0.15 && id2 < 0.15)"%(dilep,fake)

		histEETightDY, histMMTightDY, histEMTightDY = getHistograms(path,plot,runRange,True,backgrounds)

		
		effEE = ROOT.TGraphAsymmErrors(histEETight,histEELoose)
		effMM = ROOT.TGraphAsymmErrors(histMMTight,histMMLoose)
		
		effEEDY = ROOT.TGraphAsymmErrors(histEETightDY,histEELooseDY)
		effMMDY = ROOT.TGraphAsymmErrors(histMMTightDY,histMMLooseDY)
		
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		#~ style.SetTitleYOffset(0.70)
		#~ style.SetTitleSize(0.1, "XYZ")
		#~ style.SetTitleYOffset(0.35)
		#~ style.SetTitleXOffset(0.7)
		#~ style.SetPadLeftMargin(0.1)
		#~ style.SetPadTopMargin(0.12)
		#~ style.SetPadBottomMargin(0.17)
		plotPad.UseCurrentStyle()		
		plotPad.Draw()	
		plotPad.cd()	
					

		plotPad.DrawFrame(plot.firstBin,0.8,plot.lastBin,1.1,"; %s ; %s" %(plot.xaxis,"Isolation efficiency"))
		
		
		from ROOT import TH1F,kWhite
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.55,0.7,0.9,0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")	



		effEE.SetLineColor(ROOT.kRed)
		effEE.SetMarkerColor(ROOT.kRed)
		effEE.SetMarkerStyle(20)
		effEE.Draw("samepe")
		effMM.SetLineColor(ROOT.kBlue)
		effMM.SetMarkerColor(ROOT.kBlue)
		effMM.SetMarkerStyle(20)
		effMM.Draw("samepe")

		effEEDY.SetLineColor(ROOT.kRed+2)
		effEEDY.SetMarkerColor(ROOT.kRed+2)
		effEEDY.SetMarkerStyle(20)
		effEEDY.Draw("samepe")
		effMMDY.SetLineColor(ROOT.kBlue+2)
		effMMDY.SetMarkerColor(ROOT.kBlue+2)
		effMMDY.SetMarkerStyle(20)
		effMMDY.Draw("samepe")




		legend.AddEntry(effEE,"electrons t#bar{t}","pe")	
		legend.AddEntry(effMM,"muons t#bar{t}","pe")	
		legend.AddEntry(effEEDY,"electrons Drell-Yan","pe")	
		legend.AddEntry(effMMDY,"muons Drell-Yan","pe")	


		legend.Draw("same")

		line1 = ROOT.TLine(plot.firstBin,1,plot.lastBin,1)
		line1.SetLineColor(ROOT.kBlack)

		line1.SetLineWidth(1)
		line1.SetLineStyle(2)

		line1.Draw("same")

		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetNDC(True)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.04)		
		latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)

		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		latexCMS.SetTextSize(0.06)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		latexCMSExtra.SetTextSize(0.045)
		latexCMSExtra.SetNDC(True)				

		latexCMS.DrawLatex(0.19,0.88,"CMS")
		if "Simulation" in cmsExtra:
			yLabelPos = 0.81	
		else:
			yLabelPos = 0.84	

		latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))	



		
		hCanvas.Print("fig/isoEff_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	

	
def main():
	
	

	parser = argparse.ArgumentParser(description='create cut justification plots.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")		
					
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.Loose
	if len(args.selection) == 0:
		args.selection.append("Region")	

	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPathLoose	


	cmsExtra = ""
	if args.private:
		cmsExtra = "#splitline{Private Work}{Simulation}"
	else:
		cmsExtra = "Simulation"	


	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)

			plotIsolationEff(path,selection,runRange,cmsExtra,args.backgrounds)		
main()
