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
ROOT.PyConfig.IgnoreCommandLineOptions = True
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds, defineMyColors, myColors

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process,createMyColors 

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig, rOutIn, rOutInEE, rOutInMM
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, zPredictions
import corrections
import ratios
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

def getErrHist(plot,combination,region,ofHist,dyHist,rSFOFErr):
	
	if combination == "SF":
		localZPred = zPredictions.SF
		localROutIn = rOutIn
	elif combination == "EE":
		localZPred = zPredictions.EE
		localROutIn = rOutInEE
	elif combination == "MM":
		localZPred = zPredictions.MM
		localROutIn = rOutInMM
	
	hist = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histUp = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histDown = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	graph = TGraphAsymmErrors()
	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinContent(i,1)
		hist.SetBinError(i,ofHist.GetBinContent(i)*rSFOFErr)
	if dyHist is not None:	
		print "hier"
		for i in range(hist.FindBin(mllBins.lowMass.low+0.01),hist.FindBin(mllBins.lowMass.high-0.01)):
			
			if region == "inclusive":
				zErrCentral = (((localZPred.central.err*localROutIn.lowMass.central.val)**2 + (localZPred.central.val*localROutIn.lowMass.central.err)**2)**0.5) / (localZPred.central.val*localROutIn.lowMass.central.val) * dyHist.GetBinContent(i)
				zErrForward = (((localZPred.forward.err*localROutIn.lowMass.forward.val)**2 + (localZPred.forward.val*localROutIn.lowMass.forward.err)**2)**0.5) / (localZPred.forward.val*localROutIn.lowMass.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward
			else:
				zErr = (((getattr(localZPred,region).err*getattr(localROutIn.lowMass,region).val)**2 + (getattr(localZPred,region).val*getattr(localROutIn.lowMass,region).err)**2)**0.5) / ((getattr(localZPred,region).val*getattr(localROutIn.lowMass,region).val)) * dyHist.GetBinContent(i)
							
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 
			
		for i in range(hist.FindBin(mllBins.highMass.low+0.01),hist.FindBin(plot.lastBin-0.01)+1):
			if region == "inclusive":
				zErrCentral = (((localZPred.central.err*localROutIn.highMass.central.val)**2 + (localZPred.central.val*localROutIn.highMass.central.err)**2)**0.5) / (localZPred.central.val*localROutIn.highMass.central.val) * dyHist.GetBinContent(i)
				zErrForward = (((localZPred.forward.err*localROutIn.highMass.forward.val)**2 + (localZPred.forward.val*localROutIn.highMass.forward.err)**2)**0.5) / (localZPred.forward.val*localROutIn.highMass.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward		
			
			else:
				zErr = (((getattr(localZPred,region).err*getattr(localROutIn.highMass,region).val)**2 + (getattr(localZPred,region).val*getattr(localROutIn.highMass,region).err)**2)**0.5) / ((getattr(localZPred,region).val*getattr(localROutIn.highMass,region).val)) * dyHist.GetBinContent(i)
			
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 
			
		for i in range(hist.FindBin(mllBins.onZ.low+0.01),hist.FindBin(mllBins.onZ.high-0.01)):
			if region == "inclusive":
				zErrCentral = (localZPred.central.err / localZPred.central.val) * dyHist.GetBinContent(i)
				zErrForward = (localZPred.forward.err / localZPred.forward.val) * dyHist.GetBinContent(i)
				
				zErr = zErrCentral + zErrForward


			
			else:
				zErr = (getattr(localZPred,region).err / getattr(localZPred,region).val) * dyHist.GetBinContent(i) 
			hist.SetBinError(i,(hist.GetBinError(i)**2 + zErr**2)**0.5) 

		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),dyHist.GetBinContent(i) + ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + dyHist.GetBinContent(i) + ofHist.GetBinContent(i))**0.5)			
		for i in range(1,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,dyHist.GetBinContent(i) + ofHist.GetBinContent(i) - hist.GetBinError(i))			
			#~ hist.SetBinError(i,hist.GetBinError(i) / (dyHist.GetBinContent(i) + ofHist.GetBinContent(i)))
			hist.SetBinError(i,0)
	else:
		for i in range(0,hist.GetNbinsX()+1):
			graph.SetPoint(i,plot.firstBin - ((plot.lastBin-plot.firstBin)/plot.nBins)*0.5 +(i)*((plot.lastBin-plot.firstBin)/plot.nBins),ofHist.GetBinContent(i))
			graph.SetPointError(i,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,((plot.firstBin-plot.lastBin)/plot.nBins)*0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5,(hist.GetBinError(i)**2 + ofHist.GetBinContent(i))**0.5)	
		for i in range(1,hist.GetNbinsX()+1):
			histUp.SetBinContent(i,ofHist.GetBinContent(i) + hist.GetBinError(i))
			histDown.SetBinContent(i,ofHist.GetBinContent(i) - hist.GetBinError(i))			
			if ofHist.GetBinContent(i) > 0:
				hist.SetBinError(i,hist.GetBinError(i) / (ofHist.GetBinContent(i)))
			else:
				hist.SetBinError(i,0)
	return graph, histUp, histDown

def getLines(yMin,yMax, xPos = [70.,81., 101]):
	from ROOT import TLine, kGray
	result = []
	for x in xPos:
		result.append(TLine(x, yMin, x,yMax))
		result[-1].SetLineWidth(1)
		result[-1].SetLineColor(kGray+2)
		result[-1].SetLineStyle(2)
	return result

	
def makePlot(sfHist,ofHist,selection,plot,runRange,region,cmsExtra,combination,dyHist=None):

	colors = createMyColors()	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()		
	ROOT.gStyle.SetOptStat(0)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()

	yMax = sfHist.GetBinContent(sfHist.GetMaximumBin())
	
	if plot.yMax == 0:
		yMax = yMax*1.35
						
	else: 
		yMax = plot.yMax
					
	yMax = 15
	plotPad.DrawFrame(plot.firstBin,0,plot.lastBin, yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	
	bkgHist = ofHist.Clone("bkgHist")
	if dyHist is not None:
		bkgHist.Add(dyHist)
		
	
	sfHist.SetMarkerStyle(20)
	bkgHist.SetLineColor(ROOT.kBlue+3)
	bkgHist.SetLineWidth(2)
	
	dyHist.SetLineColor(ROOT.kGreen+3)
	dyHist.SetFillColor(ROOT.kGreen+3)
	dyHist.SetFillStyle(3002)
	


	
	
		
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
		
	latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%"19.4")
	

	latexCMS.DrawLatex(0.21,0.88,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.21,yLabelPos,"%s"%(cmsExtra))
	




	
	if combination == "SF":
		rSFOFErr = getattr(rSFOF,region).err
	elif combination == "EE":
		rSFOFErr = getattr(rEEOF,region).err
	elif combination == "MM":
		rSFOFErr = getattr(rMMOF,region).err
	
	errGraph, histUp, histDown = getErrHist(plot,combination,region,ofHist,dyHist,rSFOFErr)
	errGraph.SetFillColor(myColors["MyBlue"])
	errGraph.SetFillStyle(3001)
	#~ errGraph.SetLineColor(myColors["MyDarkBlue"])
	#~ errGraph.SetMarkerColor(myColors["MyDarkBlue"])
	
	errGraph.Draw("SAME02")
	bkgHist.Draw("samehist")	
	dyHist.Draw("samehist")	
	sfHist.Draw("samepe")	


	lines = getLines(0, sfHist.GetBinContent(sfHist.GetMaximumBin())+10,xPos=[mllBins.lowMass.high,mllBins.onZ.low,mllBins.onZ.high, mllBins.highMass.low ])
	for line in lines:
		line.Draw()

	leg = TLegend(0.62, 0.51, 0.89, 0.92,"","brNDC")
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if region == "inclusive":
		leg.AddEntry(legendHistDing,"ATLAS signal region","h")
	elif region == "central":
		leg.AddEntry(legendHistDing,"Central signal region","h")
	elif region == "forward":
		leg.AddEntry(legendHistDing,"Forward signal region","h")
	leg.AddEntry(sfHist,"Data","PL")
	leg.AddEntry(bkgHist, "Total backgrounds","l")
	leg.AddEntry(dyHist,"Drell--Yan", "f")
	leg.AddEntry(errGraph,"Total uncert.", "f")	
	
	leg.Draw("same")






		
	plotPad.RedrawAxis()	


	ratioPad.cd()
		
	ratioGraphs =  ratios.RatioGraph(sfHist,bkgHist, xMin=plot.firstBin, xMax=plot.lastBin,title="Data / Bgnd",yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=1000)
	ratioGraphs.addErrorByHistograms( "rSFOF", histUp, histDown,color= myColors["MyBlue"],fillStyle=3001)			

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)

	leg2 = TLegend(0.175, 0.78, 0.475, 0.9,"","brNDC")
	leg2.SetFillColor(10)
	leg2.SetLineColor(10)
	leg2.SetShadowColor(0)
	leg2.SetBorderSize(1)
	leg2.AddEntry(errGraph,"Systematic uncert.", "f")	
	leg2.Draw("same")
	
	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	ratioPad.RedrawAxis()

	
	hCanvas.Print("fig/mllResult_%s_%s_%s.pdf"%(selection.name,runRange.label,combination))	
	
	
		


def makeResultPlot(path,selection,runRange,cmsExtra):
	
	plot = getPlot("mllPlot")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut			
	print plot.cuts
	plotDY = getPlot("mllPlot")
	
	if "Forward" in selection.name:
		plotDY.addRegion(getRegion("DrellYanControlForward"))
		region = "forward"
	elif "Central" in selection.name:
		plotDY.addRegion(getRegion("DrellYanControlCentral"))
		region = "central"
	else:		
		plotDY.addRegion(getRegion("DrellYanControl"))
		region = "inclusive"
	plotDY.cleanCuts()
	plotDY.cuts = plotDY.cuts % runRange.runCut		

	plotDYScale = getPlot("mllPlotROutIn")
	
	if "Forward" in selection.name:
		plotDYScale.addRegion(getRegion("DrellYanControlForward"))
	elif "Central" in selection.name:
		plotDYScale.addRegion(getRegion("DrellYanControlCentral"))
	else:		
		plotDYScale.addRegion(getRegion("DrellYanControl"))
	plotDYScale.cleanCuts()
	plotDYScale.cuts = plotDYScale.cuts % runRange.runCut		
	
	
	
	histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[])
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())

	histEEDY, histMMDY, histEMDY = getHistograms(path,plotDY,runRange,False,[])
	histSFDY = histEEDY.Clone("histSFDY")
	histSFDY.Add(histMMDY.Clone())	

	histEEDYScale, histMMDYScale, histEMDYScale = getHistograms(path,plotDY,runRange,False,[])
	histSFDYScale = histEEDYScale.Clone("histSFDYScale")
	histSFDYScale.Add(histMMDYScale.Clone())	
	
	
	histOFSF = histEM.Clone("histOFSF")
	histOFEE = histEM.Clone("histOFEE")
	histOFMM = histEM.Clone("histOFMM")
	histOFSF.Scale(getattr(rSFOF,region).val)
	histOFEE.Scale(getattr(rEEOF,region).val)
	histOFMM.Scale(getattr(rMMOF,region).val)

	if region == "inclusive":
		histSFDY.Scale((zPredictions.SF.central.val + zPredictions.SF.forward.val) / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
		histEEDY.Scale((zPredictions.EE.central.val + zPredictions.EE.forward.val) / histEEDYScale.Integral(histEEDYScale.FindBin(81),histEEDYScale.FindBin(101)))
		histMMDY.Scale((zPredictions.MM.central.val + zPredictions.MM.forward.val) / histMMDYScale.Integral(histMMDYScale.FindBin(81),histMMDYScale.FindBin(101)))
	else:
		histSFDY.Scale(getattr(zPredictions.SF,region).val / histSFDYScale.Integral(histSFDYScale.FindBin(81),histSFDYScale.FindBin(101)))
		histEEDY.Scale(getattr(zPredictions.EE,region).val / histEEDYScale.Integral(histEEDYScale.FindBin(81),histEEDYScale.FindBin(101)))
		histMMDY.Scale(getattr(zPredictions.MM,region).val / histMMDYScale.Integral(histMMDYScale.FindBin(81),histMMDYScale.FindBin(101)))
	histSFDY.Scale(0)
	histEEDY.Scale(0)
	histMMDY.Scale(0)
	
	makePlot(histSF,histOFSF,selection,plot,runRange,region,cmsExtra,"SF",histSFDY)
	makePlot(histEE,histOFEE,selection,plot,runRange,region,cmsExtra,"EE",histEEDY)
	makePlot(histMM,histOFMM,selection,plot,runRange,region,cmsExtra,"MM",histMMDY)


def makeDependencyPlot(path,selection,plots,useMC,backgrounds,runRange,cmsExtra):
	colors = createMyColors()
	for plotName in plots:
		plot = getPlot(plotName)
		plot.addRegion(selection)
		plot.cuts = plot.cuts % runRange.runCut			
		
		if "Forward" in selection.name:
			region = "forward"
		elif "Central" in selection.name:
			region = "central"
		else:		
			region = "inclusive"	
		tmpCuts = plot.cuts
		for binName in ["lowMass","highMass"]: 

				
			plot.cuts = tmpCuts
			plot.cuts += "*(p4.M() > %f && p4.M() < %f)"%(getattr(mllBins,binName).low,getattr(mllBins,binName).high)

			histEE, histMM, histEM = getHistograms(path,plot,runRange,False,[])
			histSF = histEE.Clone("histSF")
			histSF.Add(histMM.Clone())
					
			histOFSF = histEM.Clone("histOFSF")
			histOFEE = histEM.Clone("histOFEE")
			histOFMM = histEM.Clone("histOFMM")
			histOFSF.Scale(getattr(rSFOF,region).val)
			histOFEE.Scale(getattr(rEEOF,region).val)
			histOFMM.Scale(getattr(rMMOF,region).val)


			
			if useMC:
				histEEMC, histMMMC, histEMMC = getHistograms(path,plot,runRange,True,backgrounds)
				histSFMC = histEEMC.Clone("histSFMC")
				histSFMC.Add(histMMMC.Clone())		
				histOFSFMC = histEMMC.Clone("histOFSFMC")
				histOFEEMC = histEMMC.Clone("histOFEEMC")
				histOFMMMC = histEMMC.Clone("histOFMMMC")
				histOFSFMC.Scale(getattr(rSFOF,region).valMC)
				histOFEEMC.Scale(getattr(rEEOF,region).valMC)
				histOFMMMC.Scale(getattr(rMMOF,region).valMC)		
				histsSFMC = {}
				histsOFMC = {}
				histsSFMC["SF"] = histSFMC
				histsSFMC["EE"] = histEEMC
				histsSFMC["MM"] = histMMMC
				histsOFMC["SF"] = histOFSFMC
				histsOFMC["EE"] = histOFEEMC
				histsOFMC["MM"] = histOFMMMC

			histsSF = {}
			histsOF = {}
			histsSF["SF"] = histSF
			histsSF["EE"] = histEE
			histsSF["MM"] = histMM
			histsOF["SF"] = histOFSF
			histsOF["EE"] = histOFEE
			histsOF["MM"] = histOFMM
			

			for combination in ["SF","EE","MM"]: 

				
				hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
				
				plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
				ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
				style = setTDRStyle()		
				ROOT.gStyle.SetOptStat(0)
				plotPad.UseCurrentStyle()
				ratioPad.UseCurrentStyle()
				plotPad.Draw()	
				ratioPad.Draw()	
				plotPad.cd()

				sfHist = histsSF[combination]
				bkgHist = histsOF[combination]	
				
				sfHist.SetMarkerStyle(20)
				bkgHist.SetLineColor(ROOT.kBlue+3)
				bkgHist.SetLineWidth(2)			
						
				yMax = sfHist.GetBinContent(sfHist.GetMaximumBin())
				
				if plot.yMax == 0:
					yMax = yMax*1.35
									
				else: 
					yMax = plot.yMax
								
				
				plotPad.DrawFrame(plot.firstBin,0,plot.lastBin, yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
				
							
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
					
				latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (8 TeV)"%runRange.printval)
				

				latexCMS.DrawLatex(0.21,0.88,"CMS")
				if "Simulation" in cmsExtra:
					yLabelPos = 0.81	
				else:
					yLabelPos = 0.84	

				latexCMSExtra.DrawLatex(0.21,yLabelPos,"%s"%(cmsExtra))
				
				
				if combination == "SF":
					rSFOFErr = getattr(rSFOF,region).err
				elif combination == "EE":
					rSFOFErr = getattr(rEEOF,region).err
				elif combination == "MM":
					rSFOFErr = getattr(rMMOF,region).err
				
				errGraph, histUp, histDown = getErrHist(plot,combination,region,bkgHist,None,rSFOFErr)
				errGraph.SetFillColor(myColors["MyBlue"])
				errGraph.SetFillStyle(3001)
				#~ errGraph.SetLineColor(myColors["MyDarkBlue"])
				#~ errGraph.SetMarkerColor(myColors["MyDarkBlue"])
				
				errGraph.Draw("SAME02")
				bkgHist.Draw("samehist")	
				sfHist.Draw("samepe")	



				leg = TLegend(0.62, 0.51, 0.89, 0.92,"","brNDC")
				leg.SetFillColor(10)
				leg.SetLineColor(10)
				leg.SetShadowColor(0)
				leg.SetBorderSize(1)
				from ROOT import TH1F,kWhite
				legendHistDing = TH1F()
				legendHistDing.SetFillColor(kWhite)
				if region == "inclusive":
					leg.AddEntry(legendHistDing,"Inclusive signal region","h")
				elif region == "central":
					leg.AddEntry(legendHistDing,"Central signal region","h")
				elif region == "forward":
					leg.AddEntry(legendHistDing,"Forward signal region","h")
				leg.AddEntry(sfHist,"Data","PL")
				leg.AddEntry(bkgHist, "Flav. Sym. backgrounds","l")
				leg.AddEntry(errGraph,"Background uncert.", "f")	
				
				leg.Draw("same")
					
				plotPad.RedrawAxis()	


				ratioPad.cd()
					
				ratioGraphs =  ratios.RatioGraph(sfHist,bkgHist, xMin=plot.firstBin, xMax=plot.lastBin,title="%s / OF"%combination,yMin=0.0,yMax=2,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=1000)
				ratioGraphs.addErrorByHistograms( "rSFOF", histUp, histDown,color= myColors["MyBlue"],fillStyle=3001)			

				ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)

				leg2 = TLegend(0.175, 0.78, 0.475, 0.9,"","brNDC")
				leg2.SetFillColor(10)
				leg2.SetLineColor(10)
				leg2.SetShadowColor(0)
				leg2.SetBorderSize(1)
				leg2.AddEntry(errGraph,"Systematic uncert.", "f")	
				leg2.Draw("same")
				
				ROOT.gPad.RedrawAxis()
				plotPad.RedrawAxis()
				ratioPad.RedrawAxis()

				
				hCanvas.Print("fig/rSFOFDependency_%s_%s_%s_%s_%s.pdf"%(selection.name,plot.variablePlotName,runRange.label,combination,binName))	



def main():
	
	

	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")		
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default=False,
						  help="SF/OF dependency crosschecks.")								  			  	
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="add MC.")								  			  	
	parser.add_argument("-c", "--control", action="store_true", dest="control", default=False,
						  help="use control region.")								  			  	
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
						  					
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.rSFOF
	if len(args.plots) == 0:
		args.plots = plotLists.default


	selections = []
	
	if args.control:
		
		selections.append(regionsToUse.rSFOF.central.name)	
		selections.append(regionsToUse.rSFOF.forward.name)	
		selections.append(regionsToUse.rSFOF.inclusive.name)	
	else:	
		selections.append("SignalATLAS")	
		#~ selections.append(regionsToUse.signal.central.name)	
		#~ selections.append(regionsToUse.signal.forward.name)	
		#~ selections.append(regionsToUse.signal.inclusive.name)	
	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPath	
	path = "/home/jan/Trees/sw538v0477/"	


	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
	else:
		cmsExtra = "Preliminary"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in selections:
			
			selection = getRegion(selectionName)
			if args.dependencies:
				makeDependencyPlot(path,selection,args.plots,args.mc,args.backgrounds,runRange,cmsExtra)
			else:	
				makeResultPlot(path,selection,runRange,cmsExtra)

main()



