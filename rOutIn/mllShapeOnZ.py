#!/usr/bin/env python

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
ROOT.gROOT.SetBatch(True)
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, ensurePathExists, getTriggerScaleFactor

#from corrections import rSFOF, rEEOF, rMMOF, triggerEffs
from centralConfig import regionsToUse,  backgroundLists, plotLists, systematics,  mllBins
from centralConfig import runRanges as RR
from corrections import corrections

from plotTemplate import plotTemplate

from locations import locations


def getHistogram(plot,runRange,backgrounds,region):
        path = locations[runRange.era].dataSetPath
        treesEE = readTrees(path,"EE")
        treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")
                        
                
        eventCounts = totalNumberOfGeneratedEvents(path)        
        processes = []
        for background in backgrounds:
                processes.append(Process(getattr(Backgrounds[runRange.era],background),eventCounts))
        
        triggerSF_EE,_ = getTriggerScaleFactor("EE",   region, runRange)
        triggerSF_MM,_ = getTriggerScaleFactor("MuMu", region, runRange)
        triggerSF_EM,_ = getTriggerScaleFactor("EMu", region, runRange)
        
        histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,triggerSF_EE,1.0,useTriggerEmulation=True).theHistogram               
        histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,triggerSF_MM,1.0,useTriggerEmulation=True).theHistogram
        histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,triggerSF_EM,1.0,useTriggerEmulation=True).theHistogram
        
        histSF = histoEE.Clone()
        histSF.Add(histoMM.Clone(), 1)
        histSF.Add(histoEM.Clone(), -1)

        return histSF


def main():



        parser = argparse.ArgumentParser(description='R(out/in) measurements.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
        parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
                                                  help="select dependencies to study, default is all.")
        parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
                                                  help="name of run range.")
        parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
                                                  help="backgrounds to plot.")      
        parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
                                                  help="plot is private work.")   
                                        
        args = parser.parse_args()


        
        if len(args.backgrounds) == 0:
                args.backgrounds = ["DrellYan", "RareTTZOnZ","RareZZLowMassOnZ","RareWZOnZ"]

        args.runRange = [RR["2016"].name, RR["2017"].name ,RR["2018"].name]
        
        args.selection = ["DrellYanControl", "SignalHighMT2DeltaPhiJetMetFit"]
        
        template = plotTemplate()
        
        histos = {}
        merged = {}
        runRanges = [getRunRange(runRangeName) for runRangeName in args.runRange]
        for selectionName in args.selection:
                histos[selectionName] = {}
                selection = getRegion(selectionName)
                for runRangeName in args.runRange:
                        runRange = getRunRange(runRangeName)
                        
                        plot = getPlot("mllPlot")
                        plot.addRegion(selection)
                        plot.cleanCuts()
                        plot.addRunRange(runRange)      
                        
                        histo = getHistogram(plot, runRange, args.backgrounds, "Inclusive")
                        histos[selectionName][runRangeName] = histo
                for i,runRangeName in enumerate(args.runRange):
                        if i == 0:
                                merged[selectionName] = histos[selectionName][runRangeName].Clone()
                        else:
                                merged[selectionName].Add(histos[selectionName][runRangeName], 1)
                merged[selectionName].Scale(1.0/merged[selectionName].Integral())
        
        #["DrellYanControl", "SignalInclusiveHighMT2"]
        merged["DrellYanControl"].SetLineColor(ROOT.kBlack)
        merged["DrellYanControl"].SetLineWidth(2)
        merged["DrellYanControl"].SetLineStyle(2)
        merged["DrellYanControl"].SetMarkerSize(0)
        merged["SignalHighMT2DeltaPhiJetMetFit"].SetLineColor(ROOT.kRed)
        merged["SignalHighMT2DeltaPhiJetMetFit"].SetLineWidth(2)
        merged["SignalHighMT2DeltaPhiJetMetFit"].SetMarkerSize(0)
        template.setPrimaryPlot(merged["DrellYanControl"], "histE", label="Z backgrounds in CR")
        template.addSecondaryPlot(merged["SignalHighMT2DeltaPhiJetMetFit"], "histE", label="Z backgrounds in fit SR")
        template.labelX = "mll [GeV]"
        template.labelY = "a.u."
        template.hasLegend = True
        template.logY = True
        template.maximumY = 3
        template.minimumY = 1e-5
        template.setFolderName("onZMllShapes")
        template.draw()
        template.saveAs("cr_fitsr")
        
main()
