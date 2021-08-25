#!/usr/bin/env python

import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import os
import pickle

from messageLogger import messageLogger as log

import math

from array import array

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse 

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

from setTDRStyle import setTDRStyle
from helpers import getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, readTrees, createHistoFromTree, getTriggerScaleFactor, ensurePathExists


from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, cutNCountXChecks

from locations import locations
from plotTemplate import plotTemplate, LatexLabel

def readScaleFactor(runRange, sample,noJetCuts=False):
        ensurePathExists("shelves/")
        jetsString = ""
        if noJetCuts:
                jetsString = "_zeroJets"
        with open("shelves/scaleFactor_%s_%s%s.pkl"%(runRange.label, sample, jetsString), "r") as fi:
                factor = pickle.load(fi)
        return factor
        
        
        
def main():
    pass
    WZCounts = {}
    ZZCounts = {}
    TTCounts = {}
    
    ZZCounts["2016"] = readScaleFactor(getRunRange("Run2016_36fb"), "ZZTo4L")
    ZZCounts["2017"] = readScaleFactor(getRunRange("Run2017_42fb"), "ZZTo4L")
    ZZCounts["2018"] = readScaleFactor(getRunRange("Run2018_60fb"), "ZZTo4L")
    WZCounts["2016"] = readScaleFactor(getRunRange("Run2016_36fb"), "WZTo3LNu")
    WZCounts["2017"] = readScaleFactor(getRunRange("Run2017_42fb"), "WZTo3LNu")
    WZCounts["2018"] = readScaleFactor(getRunRange("Run2018_60fb"), "WZTo3LNu")
    TTCounts["2016"] = readScaleFactor(getRunRange("Run2016_36fb"), "ttZToLL")
    TTCounts["2017"] = readScaleFactor(getRunRange("Run2017_42fb"), "ttZToLL")
    TTCounts["2018"] = readScaleFactor(getRunRange("Run2018_60fb"), "ttZToLL")
    backgrounds = ["WZTo3LNu", "ZZTo4L", "ttZToLL", "DrellYan", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
    
    template = plotTemplate()
    
    scaleFacs = {}
    scaleFacs[1] = ZZCounts["2016"]["scaleFac"]
    scaleFacs[2] = ZZCounts["2017"]["scaleFac"]
    scaleFacs[2] = ZZCounts["2018"]["scaleFac"]
    scaleFacs[3] = WZCounts["2016"]["scaleFac"]
    scaleFacs[4] = WZCounts["2017"]["scaleFac"]
    scaleFacs[5] = WZCounts["2018"]["scaleFac"]
    scaleFacs[6] = TTCounts["2016"]["scaleFac"]
    scaleFacs[7] = TTCounts["2017"]["scaleFac"]
    scaleFacs[8] = TTCounts["2018"]["scaleFac"]
    scaleFacErrs = {}
    scaleFacErrs[1] = ZZCounts["2016"]["scaleFacStatErr"]
    scaleFacErrs[2] = ZZCounts["2017"]["scaleFacStatErr"]
    scaleFacErrs[2] = ZZCounts["2018"]["scaleFacStatErr"]
    scaleFacErrs[3] = WZCounts["2016"]["scaleFacStatErr"]
    scaleFacErrs[4] = WZCounts["2017"]["scaleFacStatErr"]
    scaleFacErrs[5] = WZCounts["2018"]["scaleFacStatErr"]
    scaleFacErrs[6] = TTCounts["2016"]["scaleFacStatErr"]
    scaleFacErrs[7] = TTCounts["2017"]["scaleFacStatErr"]
    scaleFacErrs[8] = TTCounts["2018"]["scaleFacStatErr"]
    
    
    hists = {}
    
    hists["Data"] = ROOT.TH1F("", "", 9, 0, 9)
    hists["Data"].SetBinContent(1, ZZCounts["2016"]["Data"])
    hists["Data"].SetBinContent(2, ZZCounts["2017"]["Data"])
    hists["Data"].SetBinContent(3, ZZCounts["2018"]["Data"])
    hists["Data"].SetBinContent(4, WZCounts["2016"]["Data"])
    hists["Data"].SetBinContent(5, WZCounts["2017"]["Data"])
    hists["Data"].SetBinContent(6, WZCounts["2018"]["Data"])
    hists["Data"].SetBinContent(7, TTCounts["2016"]["Data"])
    hists["Data"].SetBinContent(8, TTCounts["2017"]["Data"])
    hists["Data"].SetBinContent(9, TTCounts["2018"]["Data"])
    hists["Data"].GetXaxis().SetBinLabel(1, "2016")
    hists["Data"].GetXaxis().SetBinLabel(2, "2017")
    hists["Data"].GetXaxis().SetBinLabel(3, "2018")
    hists["Data"].GetXaxis().SetBinLabel(4, "2016")
    hists["Data"].GetXaxis().SetBinLabel(5, "2017")
    hists["Data"].GetXaxis().SetBinLabel(6, "2018")
    hists["Data"].GetXaxis().SetBinLabel(7, "2016")
    hists["Data"].GetXaxis().SetBinLabel(8, "2017")
    hists["Data"].GetXaxis().SetBinLabel(9, "2018")
    hists["Data"].SetBinError(1, ZZCounts["2016"]["DataErr"])
    hists["Data"].SetBinError(2, ZZCounts["2017"]["DataErr"])
    hists["Data"].SetBinError(3, ZZCounts["2018"]["DataErr"])
    hists["Data"].SetBinError(4, WZCounts["2016"]["DataErr"])
    hists["Data"].SetBinError(5, WZCounts["2017"]["DataErr"])
    hists["Data"].SetBinError(6, WZCounts["2018"]["DataErr"])
    hists["Data"].SetBinError(7, TTCounts["2016"]["DataErr"])
    hists["Data"].SetBinError(8, TTCounts["2017"]["DataErr"])
    hists["Data"].SetBinError(9, TTCounts["2018"]["DataErr"])
    
    hists["signalYield"] = ROOT.TH1F("", "", 9, 0, 9)
    hists["signalYield"].SetBinContent(1, ZZCounts["2016"]["signalYield"])
    hists["signalYield"].SetBinContent(2, ZZCounts["2017"]["signalYield"])
    hists["signalYield"].SetBinContent(3, ZZCounts["2018"]["signalYield"])
    hists["signalYield"].SetBinContent(4, WZCounts["2016"]["signalYield"])
    hists["signalYield"].SetBinContent(5, WZCounts["2017"]["signalYield"])
    hists["signalYield"].SetBinContent(6, WZCounts["2018"]["signalYield"])
    hists["signalYield"].SetBinContent(7, TTCounts["2016"]["signalYield"])
    hists["signalYield"].SetBinContent(8, TTCounts["2017"]["signalYield"])
    hists["signalYield"].SetBinContent(9, TTCounts["2018"]["signalYield"])
    hists["signalYield"].SetBinError(1, ZZCounts["2016"]["signalYieldErr"])
    hists["signalYield"].SetBinError(2, ZZCounts["2017"]["signalYieldErr"])
    hists["signalYield"].SetBinError(3, ZZCounts["2018"]["signalYieldErr"])
    hists["signalYield"].SetBinError(4, WZCounts["2016"]["signalYieldErr"])
    hists["signalYield"].SetBinError(5, WZCounts["2017"]["signalYieldErr"])
    hists["signalYield"].SetBinError(6, WZCounts["2018"]["signalYieldErr"])
    hists["signalYield"].SetBinError(7, TTCounts["2016"]["signalYieldErr"])
    hists["signalYield"].SetBinError(8, TTCounts["2017"]["signalYieldErr"])
    hists["signalYield"].SetBinError(9, TTCounts["2018"]["signalYieldErr"])
    
    hists["proc"] = ROOT.TH1F("", "", 9, 0, 9)
    hists["proc"].SetBinContent(1, ZZCounts["2016"]["ZZTo4L"])
    hists["proc"].SetBinContent(2, ZZCounts["2017"]["ZZTo4L"])
    hists["proc"].SetBinContent(3, ZZCounts["2018"]["ZZTo4L"])
    hists["proc"].SetBinContent(4, WZCounts["2016"]["WZTo3LNu"])
    hists["proc"].SetBinContent(5, WZCounts["2017"]["WZTo3LNu"])
    hists["proc"].SetBinContent(6, WZCounts["2018"]["WZTo3LNu"])
    hists["proc"].SetBinContent(7, TTCounts["2016"]["ttZToLL"])
    hists["proc"].SetBinContent(8, TTCounts["2017"]["ttZToLL"])
    hists["proc"].SetBinContent(9, TTCounts["2018"]["ttZToLL"])
    hists["proc"].SetBinError(1, ZZCounts["2016"]["ZZTo4LErr"])
    hists["proc"].SetBinError(2, ZZCounts["2017"]["ZZTo4LErr"])
    hists["proc"].SetBinError(3, ZZCounts["2018"]["ZZTo4LErr"])
    hists["proc"].SetBinError(4, WZCounts["2016"]["WZTo3LNuErr"])
    hists["proc"].SetBinError(5, WZCounts["2017"]["WZTo3LNuErr"])
    hists["proc"].SetBinError(6, WZCounts["2018"]["WZTo3LNuErr"])
    hists["proc"].SetBinError(7, TTCounts["2016"]["ttZToLLErr"])
    hists["proc"].SetBinError(8, TTCounts["2017"]["ttZToLLErr"])
    hists["proc"].SetBinError(9, TTCounts["2018"]["ttZToLLErr"])
    
    stack = ROOT.THStack()
    leg = ROOT.TLegend(0.2, 0.7, 0.93, 0.9)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.07)
    leg.SetBorderSize(0)
    leg.SetNColumns(5)
    
    for background in reversed(backgrounds):
        hists[background] = ROOT.TH1F("", "", 9, 0, 9)
        bkg = getattr(Backgrounds["2016"],background)
        hists[background].SetFillColor(bkg.fillcolor)
        hists[background].SetLineColor(bkg.linecolor)
        hists[background].SetBinContent(1, ZZCounts["2016"][background])
        hists[background].SetBinContent(2, ZZCounts["2017"][background])
        hists[background].SetBinContent(3, ZZCounts["2018"][background])
        hists[background].SetBinContent(4, WZCounts["2016"][background])
        hists[background].SetBinContent(5, WZCounts["2017"][background])
        hists[background].SetBinContent(6, WZCounts["2018"][background])
        hists[background].SetBinContent(7, TTCounts["2016"][background])
        hists[background].SetBinContent(8, TTCounts["2017"][background])
        hists[background].SetBinContent(9, TTCounts["2018"][background])
        hists[background].SetBinContent(1, ZZCounts["2016"][background])
        hists[background].SetBinContent(2, ZZCounts["2017"][background])
        hists[background].SetBinContent(3, ZZCounts["2018"][background])
        hists[background].SetBinContent(4, WZCounts["2016"][background])
        hists[background].SetBinContent(5, WZCounts["2017"][background])
        hists[background].SetBinContent(6, WZCounts["2018"][background])
        hists[background].SetBinContent(7, TTCounts["2016"][background])
        hists[background].SetBinContent(8, TTCounts["2017"][background])
        hists[background].SetBinContent(9, TTCounts["2018"][background])
        stack.Add(hists[background])
        leg.AddEntry(hists[background], bkg.label, "F")
    
    leg.AddEntry(hists["Data"], "Data", "pe")
    
    # hists["Data"].Draw("PE")
    # stack.Draw("hist same")
    # hists["Data"].Draw("PE same")
    template.plotData = True
    template.setPrimaryPlot(hists["Data"], "PE")
    template.addSecondaryPlot(stack, "hist")
    template.canvasSizeX = 1600
    template.maximumScale = 1.8
    template.minimumY = 0
    
    template.labelY = "Events"
    template.ratioLabel = "scale factor"
    template.hasRatio = True
    template.addRatioPair(hists["signalYield"], hists["proc"])
    template.labeledAxisX = True
    
    template.marginLeft = 0.08
    
    template.latexCMS.posX = 0.1
    template.latexCMS.posY = 0.93
    template.latexCMSExtra.posX = 0.1
    template.latexCMSExtra.posY = 0.835
    
    template.lumiInt = 137
    template.latexLumi.size = 0.04
    template.latexLumi.posY = 0.96
    
    template.ratioTitleOffset = 0.2
    template.draw()
    template.axisField.GetXaxis().SetLabelSize(0.1)
    template.axisField.GetYaxis().SetTitleOffset(0.5)
    
    
    line =ROOT.TLine()
    line.SetLineStyle(2)
    line.SetLineWidth(3)
    line.SetLineColor(ROOT.kGray+3)
    
    template.plotPad.cd()
    line.DrawLine(3,0,3,100)
    line.DrawLine(6,0,6,100)
    
    text = ROOT.TLatex()
    text.SetTextSize(0.08)
    text.SetTextFont(62)
    text.SetTextAlign(22)
    text.SetNDC(False)
    text.DrawLatex(1.5, 90, "ZZ CR")
    text.DrawLatex(4.5, 90, "WZ CR")
    text.DrawLatex(7.5, 90, "t#bar{t}Z CR")
    
    
    leg.Draw("same")
    
    template.ratioPad.cd()
    line.DrawLine(3,0,3,2)
    line.DrawLine(6,0,6,2)
    
    
    
    template.setFolderName("multiYearPlots")
    template.saveAs("scaleFacs")
    
if __name__ == "__main__":
    main()
