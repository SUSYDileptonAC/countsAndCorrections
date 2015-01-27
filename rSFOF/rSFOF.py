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


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process

from corrections import rSFOF, rEEOF, rMMOF, rMuE, rSFOFTrig
from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins
import corrections



from locations import locations


def illustration():
	from corrections import rSFOF
	hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
	plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
	style = setTDRStyle()
	plotPad.UseCurrentStyle()		
	plotPad.Draw()	
	plotPad.cd()	
	hCanvas.DrawFrame(0,0,2,2,"; %s ; %s" %("r_{#mu e}","R_{SF/OF}"))	

	legend = TLegend(0.15, 0.13, 0.5, 0.5)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)


	x= array("f",[rMuE.central.val-rMuE.central.err, rMuE.central.val+rMuE.central.err]) 
   	y= array("f",[1.,1.])
   	ey= array("f",[1, 1])
   	ex= array("f",[0,0])
   	ge= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge.SetFillColor(ROOT.kGreen-3)
   	ge.SetFillStyle(3008)
   	ge.SetLineColor(ROOT.kWhite)
   	ge.Draw("SAME 3")	
	x= array("f",[0, 2]) 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	#~ y= array([rMuEs[region], rMuEs[region]],"f") # 1.237
   	y= array("f",[rSFOF.central.val,rSFOF.central.val])
   	ey= array("f",[rSFOF.central.err, rSFOF.central.err])
   	ex= array("f",[0.0,0.0])
   	ge2= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge2.SetFillColor(ROOT.kBlue-3)
   	ge2.SetFillStyle(3002)
   	ge2.SetLineColor(ROOT.kWhite)
   	ge2.Draw("SAME 3")	
	
	rSFOFLine = TF1("rSFOF","0.5*(x+1./x)*%s"%rSFOFTrig.central.val,0.,2.)
	rSFOFLine.SetLineColor(ROOT.kRed)
	rSFOFLine.SetLineWidth(2)
	rSFOFTrigUp = TF1("rSFOF","0.5*(x+1./x)*%s"%(rSFOFTrig.central.val+rSFOFTrig.central.err),0.,2.)
	rSFOFTrigUp.SetLineColor(ROOT.kBlack)
	rSFOFTrigUp.SetLineWidth(2)
	rSFOFTrigUp.SetLineStyle(ROOT.kDashed)
	rSFOFTrigDown = TF1("rSFOF","0.5*(x+1./x)*%s"%(rSFOFTrig.central.val-rSFOFTrig.central.err),0.,2.)
	rSFOFTrigDown.SetLineColor(ROOT.kBlack)
	rSFOFTrigDown.SetLineWidth(2)
	rSFOFTrigDown.SetLineStyle(ROOT.kDashed)
	
	rmueline= ROOT.TF1("rmueline","%s"%rSFOF.central.val,0, 2)
	rmueline.SetLineColor(ROOT.kBlue)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME") 

	line1 = ROOT.TLine(rMuE.central.val,0,rMuE.central.val,2)
	line1.Draw("Same")
	line1.SetLineWidth(2)
	line1.SetLineColor(ROOT.kGreen)
	
	legend.AddEntry(rSFOFLine,"R_{SF/OF} from r_{#mu e} & trig. eff.","l")
	legend.AddEntry(rSFOFTrigDown,"R_{SF/OF} #pm 1 #sigma trig. eff. ","l")
	legend.AddEntry(ge,"r_{#mu e} #pm 1 #sigma","f")
	legend.AddEntry(ge2,"R_{SF/OF} #pm 1 #sigma","f")
	
	legend.Draw("SAME")
	
	rSFOFLine.Draw("SAME")
	rSFOFTrigUp.Draw("SAME")
	rSFOFTrigDown.Draw("SAME")
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "Central Dilepton Selection")	  	

	
	hCanvas.Print("rMuEPropaganda_Central.pdf")
	hCanvas.Clear()
	hCanvas.DrawFrame(0,0,2,2,"; %s ; %s" %("r_{#mu e}","R_{SF/OF}"))	

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
	hCanvas.DrawFrame(0,0,2,2,"; %s ; %s" %("r_{#mu e}","R_{SF/OF}"))	

	legend = TLegend(0.15, 0.13, 0.5, 0.5)
	legend.SetFillStyle(0)
	legend.SetBorderSize(0)
	ROOT.gStyle.SetOptStat(0)


	x= array("f",[rMuE.forward.val-rMuE.forward.err, rMuE.forward.val+rMuE.forward.err]) 
   	y= array("f",[1.,1.])
   	ey= array("f",[1, 1])
   	ex= array("f",[0,0])
   	ge= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge.SetFillColor(ROOT.kGreen-3)
   	ge.SetFillStyle(3008)
   	ge.SetLineColor(ROOT.kWhite)
   	ge.Draw("SAME 3")	
	x= array("f",[0, 2]) 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	#~ y= array([rMuEs[region], rMuEs[region]],"f") # 1.237
   	y= array("f",[rSFOF.forward.val,rSFOF.forward.val])
   	ey= array("f",[rSFOF.forward.err, rSFOF.forward.err])
   	ex= array("f",[0.0,0.0])
   	ge2= ROOT.TGraphErrors(2, x, y,ex,ey)
   	ge2.SetFillColor(ROOT.kBlue-3)
   	ge2.SetFillStyle(3002)
   	ge2.SetLineColor(ROOT.kWhite)
   	ge2.Draw("SAME 3")	
	
	rSFOFLine = TF1("rSFOF","0.5*(x+1./x)*%s"%rSFOFTrig.forward.val,0.,2.)
	rSFOFLine.SetLineColor(ROOT.kRed)
	rSFOFLine.SetLineWidth(2)
	rSFOFTrigUp = TF1("rSFOF","0.5*(x+1./x)*%s"%(rSFOFTrig.forward.val+rSFOFTrig.forward.err),0.,2.)
	rSFOFTrigUp.SetLineColor(ROOT.kBlack)
	rSFOFTrigUp.SetLineWidth(2)
	rSFOFTrigUp.SetLineStyle(ROOT.kDashed)
	rSFOFTrigDown = TF1("rSFOF","0.5*(x+1./x)*%s"%(rSFOFTrig.forward.val-rSFOFTrig.forward.err),0.,2.)
	rSFOFTrigDown.SetLineColor(ROOT.kBlack)
	rSFOFTrigDown.SetLineWidth(2)
	rSFOFTrigDown.SetLineStyle(ROOT.kDashed)
	
	rmueline= ROOT.TF1("rmueline","%s"%rSFOF.forward.val,0, 2)
	rmueline.SetLineColor(ROOT.kBlue)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME") 

	line1 = ROOT.TLine(rMuE.forward.val,0,rMuE.forward.val,2)
	line1.Draw("Same")
	line1.SetLineWidth(2)
	line1.SetLineColor(ROOT.kGreen)
	
	legend.AddEntry(rSFOFLine,"R_{SF/OF} from r_{#mu e} & trig. eff.","l")
	legend.AddEntry(rSFOFTrigDown,"R_{SF/OF} #pm 1 #sigma trig. eff. ","l")
	legend.AddEntry(ge,"r_{#mu e} #pm 1 #sigma","f")
	legend.AddEntry(ge2,"R_{SF/OF} #pm 1 #sigma","f")
	
	legend.Draw("SAME")
	
	rSFOFLine.Draw("SAME")
	rSFOFTrigUp.Draw("SAME")
	rSFOFTrigDown.Draw("SAME")
	
	latex = ROOT.TLatex()
	latex.SetTextSize(0.04)
	latex.SetNDC(True)
	latex.DrawLatex(0.15, 0.96, "Forward Dilepton Selection")	  	

	
	hCanvas.Print("rMuEPropaganda_Forward.pdf")	



def dependencies(path,selection,plots,runRange,isMC,backgrounds,cmsExtra,fit):
	for name in plots:
		plot = getPlot(name)
		plot.addRegion(selection)
		plot.cleanCuts()	
		plot.cuts = plot.cuts % runRange.runCut	


		histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC, backgrounds)
		
		histRSFOF = histEE.Clone("histRSFOF")
		histRSFOF.Add(histMM.Clone())
		histRSFOF.Divide(histEM)				
		
		hCanvas = TCanvas("hCanvas", "Distribution", 800,300)
		
		plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
		style = setTDRStyle()
		#~ style.SetTitleYOffset(0.70)
		style.SetTitleSize(0.1, "XYZ")
		style.SetTitleYOffset(0.35)
		style.SetTitleXOffset(0.7)
		style.SetPadLeftMargin(0.1)
		style.SetPadTopMargin(0.12)
		style.SetPadBottomMargin(0.17)
		plotPad.UseCurrentStyle()		
		plotPad.Draw()	
		plotPad.cd()	
					
	
		plotPad.DrawFrame(plot.firstBin,0,plot.lastBin,3,"; %s ; %s" %(plot.xaxis,"SF/OF"))
		
		
		from ROOT import TH1F,kWhite
		legendHistDing = TH1F()
		legendHistDing.SetFillColor(kWhite)
		legend = ROOT.TLegend(0.65,0.7,1,0.9)
		legend.SetFillStyle(0)
		legend.SetBorderSize(0)			
		legend.AddEntry(legendHistDing,"%s"%selection.latex,"h")	
		legend.Draw("same")

		zeroLine = ROOT.TLine(plot.firstBin, 1., plot.lastBin , 1.)
		zeroLine.SetLineWidth(1)
		zeroLine.SetLineColor(ROOT.kBlue)
		zeroLine.SetLineStyle(2)
		zeroLine.Draw("same")
		histRSFOF.SetLineColor(ROOT.kBlack)
		histRSFOF.SetMarkerColor(ROOT.kBlack)
		histRSFOF.SetMarkerStyle(20)
		histRSFOF.Draw("sameE0")
		
		latex = ROOT.TLatex()
		latex.SetTextFont(42)
		latex.SetTextAlign(31)
		latex.SetTextSize(0.1)
		latex.SetNDC(True)
		latexCMS = ROOT.TLatex()
		latexCMS.SetTextFont(61)
		#latexCMS.SetTextAlign(31)
		latexCMS.SetTextSize(0.12)
		latexCMS.SetNDC(True)
		latexCMSExtra = ROOT.TLatex()
		latexCMSExtra.SetTextFont(52)
		#latexCMSExtra.SetTextAlign(31)
		latexCMSExtra.SetTextSize(0.1)
		latexCMSExtra.SetNDC(True)	
		latex.DrawLatex(0.95, 0.91, "%s fb^{-1} (8 TeV)"%runRange.printval)
		

		latexCMS.DrawLatex(0.12,0.76,"CMS")
		if "Simulation" in cmsExtra and "Private Work" in cmsExtra:
			yLabelPos = 0.635	
		else:
			yLabelPos = 0.68	

		latexCMSExtra.DrawLatex(0.12,yLabelPos,"%s"%(cmsExtra))	


		if fit:
			fit = TF1("dataFit","pol1",0,300)
			fit.SetLineColor(ROOT.kBlack)
			histRSFOF.Fit("dataFit")		
			
			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)	
			latex.SetNDC()	
			latex.DrawLatex(0.2, 0.25, "Fit: %.2f #pm %.2f %.5f #pm %.5f * m_{ll}"%(fit.GetParameter(0),fit.GetParError(0),fit.GetParameter(1),fit.GetParError(1)))


		
		if isMC:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s_MC.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	
		else:
			hCanvas.Print("fig/rSFOF_%s_%s_%s_%s.pdf"%(selection.name,runRange.label,plot.variablePlotName,plot.additionalName))	




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
	
	

	

def centralValues(path,selection,runRange,isMC,backgrounds,cmsExtra):


	plot = getPlot("mllPlotROutIn")
	plot.addRegion(selection)
	plot.cleanCuts()
	plot.cuts = plot.cuts % runRange.runCut		

	plotSignal = getPlot("mllPlot")
	
	if "Forward" in selection.name:
		plotSignal.addRegion(getRegion("SignalForward"))
	elif "Central" in selection.name:
		plotSignal.addRegion(getRegion("SignalBarrel"))
	else:		
		plotSignal.addRegion(getRegion("SignalInclusive"))

	plotSignal.cleanCuts()
	plotSignal.cuts = plotSignal.cuts % runRange.runCut	


	histEE, histMM, histEM = getHistograms(path,plot,runRange,isMC,backgrounds)
	histSF = histEE.Clone("histSF")
	histSF.Add(histMM.Clone())

	histEESignal, histMMSignal, histEMSignal = getHistograms(path,plotSignal,runRange,isMC,backgrounds)
	histSFSignal = histEESignal.Clone("histSFSignal")
	histSFSignal.Add(histMMSignal.Clone())
	result = {}
	

	lowMassLow = mllBins.lowMass.low
	lowMassHigh = mllBins.lowMass.high
	peakLow = mllBins.onZ.low
	peakHigh = mllBins.onZ.high
	highMassLow = mllBins.highMass.low
	highMassHigh = mllBins.highMass.high
		

	eeLowMassErr = ROOT.Double()
	eeLowMass = histEE.IntegralAndError(histEE.FindBin(lowMassLow+0.01),histEE.FindBin(lowMassHigh-0.01),eeLowMassErr)
	eeHighMassErr = ROOT.Double()
	eeHighMass = histEE.IntegralAndError(histEE.FindBin(highMassLow+0.01),histEE.FindBin(highMassHigh-0.01),eeHighMassErr)
	
	ee = eeLowMass + eeHighMass
	eeErr = (eeLowMassErr**2 + eeHighMassErr**2)**0.5
	
	mmLowMassErr = ROOT.Double()
	mmLowMass = histMM.IntegralAndError(histMM.FindBin(lowMassLow+0.01),histMM.FindBin(lowMassHigh-0.01),mmLowMassErr)
	mmHighMassErr = ROOT.Double()
	mmHighMass = histMM.IntegralAndError(histMM.FindBin(highMassLow+0.01),histMM.FindBin(highMassHigh-0.01),mmHighMassErr)
	
	mm = mmLowMass + mmHighMass
	mmErr = (mmLowMassErr**2 + mmHighMassErr**2)**0.5
	
	ofLowMassErr = ROOT.Double()
	ofLowMass = histEM.IntegralAndError(histEM.FindBin(lowMassLow+0.01),histEM.FindBin(lowMassHigh-0.01),ofLowMassErr)
	ofHighMassErr = ROOT.Double()
	ofHighMass = histEM.IntegralAndError(histEM.FindBin(highMassLow+0.01),histEM.FindBin(highMassHigh-0.01),ofHighMassErr)
	
	of = ofLowMass + ofHighMass
	ofErr = (ofLowMassErr**2 + ofHighMassErr**2)**0.5

	
	sf = ee + mm 
	sfErr = (eeErr**2 + mmErr**2)**0.5

	eeLowMassErrSignal = ROOT.Double()
	eeLowMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(lowMassLow+0.01),histEESignal.FindBin(lowMassHigh-0.01),eeLowMassErrSignal)
	eeHighMassErrSignal = ROOT.Double()
	eeHighMassSignal = histEESignal.IntegralAndError(histEESignal.FindBin(highMassLow+0.01),histEESignal.FindBin(highMassHigh-0.01),eeHighMassErrSignal)
	
	eeSignal = eeLowMassSignal + eeHighMassSignal
	eeErrSignal = (eeLowMassErrSignal**2 + eeHighMassErrSignal**2)**0.5
	
	mmLowMassErrSignal = ROOT.Double()
	mmLowMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(lowMassLow+0.01),histMMSignal.FindBin(lowMassHigh-0.01),mmLowMassErrSignal)
	mmHighMassErrSignal = ROOT.Double()
	mmHighMassSignal = histMMSignal.IntegralAndError(histMMSignal.FindBin(highMassLow+0.01),histMMSignal.FindBin(highMassHigh-0.01),mmHighMassErrSignal)
	
	mmSignal = mmLowMassSignal + mmHighMassSignal
	mmErrSignal = (mmLowMassErrSignal**2 + mmHighMassErrSignal**2)**0.5
	
	ofLowMassErrSignal = ROOT.Double()
	ofLowMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(lowMassLow+0.01),histEMSignal.FindBin(lowMassHigh-0.01),ofLowMassErrSignal)
	ofHighMassErrSignal = ROOT.Double()
	ofHighMassSignal = histEMSignal.IntegralAndError(histEMSignal.FindBin(highMassLow+0.01),histEMSignal.FindBin(highMassHigh-0.01),ofHighMassErrSignal)
	
	ofSignal = ofLowMassSignal + ofHighMassSignal
	ofErrSignal = (ofLowMassErrSignal**2 + ofHighMassErrSignal**2)**0.5

	
	sfSignal = eeSignal + mmSignal 
	sfErrSignal = (eeErrSignal**2 + mmErrSignal**2)**0.5
	
	
	rsfof = float(sf)/float(of)
	rsfofErr = rsfof*(sfErr**2/sf**2+ofErr**2/of**2)**0.5
	rsfofSignal = float(sfSignal)/float(ofSignal)
	rsfofErrSignal = rsfofSignal*(sfErrSignal**2/sfSignal**2+ofErrSignal**2/ofSignal**2)**0.5
	rEEOF = float(ee)/float(of)
	rEEOFErr = rEEOF * (eeErr**2/ee**2 + ofErr**2/of**2)**0.5
	rEEOFSignal = float(eeSignal)/float(ofSignal)
	rEEOFErrSignal = rEEOFSignal * (eeErrSignal**2/eeSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
	rMMOF = float(mm)/float(of)
	rMMOFErr = rMMOF * (mmErr**2/mm**2 + ofErr**2/of**2)**0.5
	rMMOFSignal = float(mmSignal)/float(ofSignal)
	rMMOFErrSignal = rMMOFSignal * (mmErrSignal**2/mmSignal**2 + ofErrSignal**2/ofSignal**2)**0.5
	
	transferFaktor = rsfofSignal/rsfof
	transferFaktorErr = transferFaktor*((rsfofErr/rsfof)**2+(rsfofErrSignal/rsfofSignal)**2)**0.5
	transferFaktorEE = rEEOFSignal/rEEOF
	transferFaktorEEErr = transferFaktorEE*((rEEOFErr/rEEOF)**2+(rEEOFErrSignal/rEEOFSignal)**2)**0.5
	transferFaktorMM = rMMOFSignal/rMMOF
	transferFaktorMMErr = transferFaktorMM*((rMMOFErr/rMMOF)**2+(rMMOFErrSignal/rMMOFSignal)**2)**0.5
	result = {}
	result["EE"] = ee
	result["MM"] = mm
	result["SF"] = sf
	result["OF"] = of
	result["EESignal"] = eeSignal
	result["MMSignal"] = mmSignal
	result["SFSignal"] = sfSignal
	result["OFSignal"] = ofSignal
	result["rSFOF"] = rsfof
	result["rSFOFErr"] = rsfofErr
	result["rEEOF"] = rEEOF
	result["rEEOFErr"] = rEEOFErr
	result["rMMOF"] = rMMOF
	result["rMMOFErr"] = rMMOFErr
	result["rSFOFSignal"] = rsfofSignal
	result["rSFOFErrSignal"] = rsfofErrSignal
	result["rEEOFSignal"] = rEEOFSignal
	result["rEEOFErrSignal"] = rEEOFErrSignal
	result["rMMOFSignal"] = rMMOFSignal
	result["rMMOFErrSignal"] = rMMOFErrSignal
	result["transfer"] = transferFaktor
	result["transferErr"] = transferFaktorErr
	result["transferEE"] = transferFaktorEE
	result["transferEEErr"] = transferFaktorEEErr
	result["transferMM"] = transferFaktorMM
	result["transferMMErr"] = transferFaktorMMErr
	
	return result
	
	
def main():
	
	

	parser = argparse.ArgumentParser(description='rSFOF from control region.')
	
	parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
						  help="Verbose mode.")
	parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
						  help="use MC, default is to use data.")
	parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
						  help="selection which to apply.")
	parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
						  help="select dependencies to study, default is all.")
	parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
						  help="name of run range.")
	parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
						  help="calculate effinciecy central values")
	parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
						  help="backgrounds to plot.")
	parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
						  help="make dependency plots")	
	parser.add_argument("-f", "--fit", action="store_true", dest="fit", default= False,
						  help="do dependecy fit")	
	parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
						  help="plot is private work.")	
	parser.add_argument("-i", "--illustrate", action="store_true", dest="illustrate", default=False,
						  help="plot dependency illustrations.")	
	parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
						  help="write results to central repository")	
					
	args = parser.parse_args()


	if len(args.backgrounds) == 0:
		args.backgrounds = backgroundLists.default
	if len(args.plots) == 0:
		args.plots = plotLists.rSFOF
	if len(args.selection) == 0:
		args.selection.append(regionsToUse.rSFOF.central.name)	
		args.selection.append(regionsToUse.rSFOF.forward.name)	
		args.selection.append(regionsToUse.rSFOF.inclusive.name)	
	if len(args.runRange) == 0:
		args.runRange.append(runRanges.name)	
			

	path = locations.dataSetPath	


	cmsExtra = ""
	if args.private:
		cmsExtra = "Private Work"
		if args.mc:
			cmsExtra = "#splitline{Private Work}{Simulation}"
	elif args.mc:
		cmsExtra = "Simulation"	
	else:
		cmsExtra = "Preliminary"

	for runRangeName in args.runRange:
		runRange = getRunRange(runRangeName)
	
		for selectionName in args.selection:
			
			selection = getRegion(selectionName)

			if args.central:
				
				centralVal = centralValues(path,selection,runRange,args.mc,args.backgrounds,cmsExtra)
				if args.mc:
					outFilePkl = open("shelves/rSFOF_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
				else:
					outFilePkl = open("shelves/rSFOF_%s_%s.pkl"%(selection.name,runRange.label),"w")
				pickle.dump(centralVal, outFilePkl)
				outFilePkl.close()
				
			if args.dependencies:
				 dependencies(path,selection,args.plots,runRange,args.mc,args.backgrounds,cmsExtra,args.fit)		
				
			if args.illustrate:
				illustration()
				
			if args.write:
				import subprocess
				if args.mc:
					bashCommand = "cp shelves/rSFOF_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)		
				else:	
					bashCommand = "cp shelves//rSFOF_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
				process = subprocess.Popen(bashCommand.split())					
main()
