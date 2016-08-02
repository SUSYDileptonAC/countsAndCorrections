import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
from ROOT import gROOT, gStyle, TFile, TH1F, TCanvas, TPad, TDirectory, TMath, TLorentzVector, TGraphAsymmErrors, TFile, TH2F,TLegend
from setTDRStyle import setTDRStyle

from messageLogger import messageLogger as log
import argparse	

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts,defineMyColors, myColors
from corrections import rSFOF, triggerEffs

from helpers import getDataTrees, TheStack, totalNumberOfGeneratedEvents, Process, readTrees,createMyColors,createHistoFromTree 

from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, cutNCountXChecks

from locations import locations
import ratios

parametersToSave  = {}
rootContainer = []

plotNames = {"defaultMll":"mllPlot","defaultNLL":"nLLPlot","lowNLL":"mllPlotLowNLL","highNLL":"mllPlotHighNLL","lowMll":"nLLPlotLowMll","highMll":"nLLPlotHighMll"}

def getHistograms(path,baseTreePath,plot,runRange,backgrounds):

	treesEE = readTrees(path,"EE")
	treesEM = readTrees(path,"EMu")
	treesMM = readTrees(path,"MuMu")
		
		
	eventCounts = totalNumberOfGeneratedEvents(baseTreePath)	
	processes = []
	for background in backgrounds:
		processes.append(Process(getattr(Backgrounds,background),eventCounts))
	histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram		
	histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
	histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram		
		
	
	return histoEE , histoMM, histoEM
	
def getErrHist(plot,ofHist,rSFOFErr):
	
	hist = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histUp = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	histDown = TH1F("errHist","errHist",plot.nBins,plot.firstBin,plot.lastBin)
	graph = TGraphAsymmErrors()
	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinContent(i,1)
		hist.SetBinError(i,ofHist.GetBinContent(i)*rSFOFErr)
		
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

	
def makePlot(sfHist,ofHist,selection,plot,runRange,cmsExtra):

	colors = createMyColors()	

	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	
	plotPad = ROOT.TPad("plotPad","plotPad",0,0.3,1,1)
	ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.3)
	style = setTDRStyle()
	ROOT.gStyle.SetOptStat(0)
	style.SetPadTopMargin(0.07)
	plotPad.UseCurrentStyle()
	ratioPad.UseCurrentStyle()
	plotPad.Draw()	
	ratioPad.Draw()	
	plotPad.cd()

	yMax = sfHist.GetBinContent(sfHist.GetMaximumBin())
	
	if plot.yMax == 0:
		yMax = yMax*1.5 
						
	else: 
		yMax = plot.yMax
					
	
	plotPad.DrawFrame(plot.firstBin,0,plot.lastBin, yMax,"; %s ; %s" %(plot.xaxis,plot.yaxis))
	
	#set overflow bin
	print sfHist.GetBinContent(sfHist.GetNbinsX()), sfHist.GetBinContent(sfHist.GetNbinsX()+1)
	sfHist.SetBinContent(sfHist.GetNbinsX(),sfHist.GetBinContent(sfHist.GetNbinsX())+sfHist.GetBinContent(sfHist.GetNbinsX()+1))
	sfHist.SetBinError(sfHist.GetNbinsX(),(sfHist.GetBinContent(sfHist.GetNbinsX())+sfHist.GetBinContent(sfHist.GetNbinsX()+1))**0.5)
	ofHist.SetBinContent(ofHist.GetNbinsX(),ofHist.GetBinContent(ofHist.GetNbinsX())+ofHist.GetBinContent(ofHist.GetNbinsX()+1))
	ofHist.SetBinError(ofHist.GetNbinsX(),(ofHist.GetBinContent(ofHist.GetNbinsX())+ofHist.GetBinContent(ofHist.GetNbinsX()+1))**0.5)
	
	rSFOFErr = rSFOF.inclusive.err
	
	errGraph, histUp, histDown = getErrHist(plot,ofHist,rSFOFErr)
		
	
	sfHist.SetMarkerStyle(20)
	sfHist.SetLineColor(ROOT.kBlack)
	ofHist.SetLineColor(ROOT.kBlue+3)
	ofHist.SetLineWidth(2)
	
		
	latex = ROOT.TLatex()
	latex.SetTextFont(42)
	latex.SetTextAlign(31)
	latex.SetTextSize(0.055)
	latex.SetLineWidth(2)
	latex.SetNDC(True)
	latexCMS = ROOT.TLatex()
	latexCMS.SetTextFont(61)
	latexCMS.SetTextSize(0.055)
	latexCMS.SetNDC(True)
	latexCMSExtra = ROOT.TLatex()
	latexCMSExtra.SetTextFont(52)
	latexCMSExtra.SetTextSize(0.03)
	latexCMSExtra.SetNDC(True) 
		
	latex.DrawLatex(0.93, 0.942, "%s fb^{-1} (13 TeV)"%runRange.printval)
	

	latexCMS.DrawLatex(0.19,0.86,"CMS")
	if "Simulation" in cmsExtra:
		yLabelPos = 0.81	
	else:
		yLabelPos = 0.84	

	latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))

	

	leg = TLegend(0.55, 0.6, 0.95, 0.92,"","brNDC")
		
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if "default" in selection:
		leg.AddEntry(legendHistDing,"Baseline signal region","h")
	elif selection == "lowNLL":
		leg.AddEntry(legendHistDing,"ttbar like signal region","h")
	elif selection == "highNLL":
		leg.AddEntry(legendHistDing,"non-ttbar like signal region","h")
	elif selection == "lowMll":
		leg.AddEntry(legendHistDing,"Low mass signal region","h")
	elif selection == "highMll":
		leg.AddEntry(legendHistDing,"High mass signal region","h")
	leg.AddEntry(sfHist,"observed SF ttbar","pe1")
	leg.AddEntry(ofHist, "prediction from OF ttbar","l")
	
	leg.Draw("same")
	
	
	ofHist.Draw("samehist")	
	
	sfHist.Draw("samepe1")

		
	plotPad.RedrawAxis()	


	ratioPad.cd()
		
	ratioGraphs =  ratios.RatioGraph(sfHist,ofHist, xMin=plot.firstBin, xMax=plot.lastBin,title="#frac{Simul.}{Pred.}  ",yMin=0.75,yMax=1.25,ndivisions=10,color=ROOT.kBlack,adaptiveBinning=1000)
	ratioGraphs.addErrorByHistograms( "rSFOF", histUp, histDown,color= myColors["MyBlue"],fillStyle=3001)			

	ratioGraphs.draw(ROOT.gPad,True,False,True,chi2Pos=0.8)
	
	ROOT.gPad.RedrawAxis()
	plotPad.RedrawAxis()
	ratioPad.RedrawAxis()

	hCanvas.Print("fig/rSFOFClosure_%s_%s.pdf"%(selection,runRange.label))	
	
	
					

def main():
	
	
	

	parser = argparse.ArgumentParser(description='edge fitter reloaded.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-S", "--sample", action="store", dest="sample", default="all",
						  help="choose a sample to convert, default is all.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="store", default="SignalInclusive",
						  help="selection which to apply.")	
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
					
	args = parser.parse_args()	
	
	canv = TCanvas("canv", "canv",800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style=setTDRStyle()	
	plotPad.UseCurrentStyle()
	plotPad.Draw()	
	plotPad.cd()
	
	path = locations.dataSetPathNLL
	baseTreePath = locations.dataSetPath
	
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.signal.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)



	region = args.selection
	
	print region
	
	from defs import Regions
	if not region in dir(Regions):
		print "invalid region, exiting"
		sys.exit()
	else:	
		Selection = getattr(Regions,region)
		
	backgrounds = ["TT_Powheg"]
	
	cmsExtra = "Simulation"
	
	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selection in ["defaultMll","defaultNLL","lowNLL","highNLL","lowMll","highMll"]:
			
			Counts = {}
			
			selectedRegion = getRegion(region)
		
			plot = getPlot(plotNames[selection])
			plot.addRegion(selectedRegion)
			
			plot.cuts = plot.cuts % runRange.runCut
			plot.cleanCuts()
			
			plot.cuts = plot.cuts.replace("p4.M()","mll")		
			
			
			histEE, histMM, histEM = getHistograms(path,baseTreePath,plot,runRange,backgrounds)
			#~ histEE.Scale(triggerEffs.inclusive.effEE.val)
			#~ histMM.Scale(triggerEffs.inclusive.effMM.val)
			#~ histEM.Scale(triggerEffs.inclusive.effEM.val)
			histEM.Scale(rSFOF.inclusive.valMC)
			histSF = histEE.Clone("histSF")
			histSF.Add(histMM.Clone())
			
			makePlot(histSF,histEM,selection,plot,runRange,cmsExtra)
			
			histSFOF = histSF.Clone()
			histSFOF.Add(histEM,-1)
			
			#~ n_SF, SF_err = histSF.IntegralAndError()
			#~ n_OF, OF_err = histOF.IntegralAndError()
			#~ n_SFOF, SFOF_err = histSFOF.IntegralAndError()
			#~ 
			#~ counts["TTbar":
			#~ 
			#~ backgrounds = ["DrellYan"]
			#~ 
			#~ 
			#~ DrellYanTauTau
			#~ SingleTop
			#~ 
			#~ Diboson
			#~ 
			#~ Rare
								
			
	
			

main()
