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
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle
ROOT.gROOT.SetBatch(True)

from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process


from locations import locations
from plotTemplate import plotTemplate







def getHistograms(path,plot,runRange,isMC,backgrounds):

        treesEE = readTrees(path,"EE")
        treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")
        
        if "NLL" in path:
                isNLL = True
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
        
        if isMC:
                eventCounts = totalNumberOfGeneratedEvents(path)        
                processes = []
                for background in backgrounds:
                        processes.append(Process(getattr(Backgrounds[runRange.era],background),eventCounts))
                histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0, useTriggerEmulation=(not isNLL)).theHistogram                
                histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0, useTriggerEmulation=(not isNLL)).theHistogram            
        else:
                histoEE = getDataHist(plot, treesEE)
                histoMM = getDataHist(plot, treesMM)
                

        return histoEE , histoMM
        

def countEvents(selection):
        from centralConfig import runRanges
        
        first = False

        
        dataEEAll = None
        dataMMAll = None
        dataSFAll = None
        
        backgrounds = ["Rare","SingleTop","TT_Powheg","Diboson","DrellYanTauTau","DrellYan"]
        
        histEEAll = {}
        histMMAll = {}
        histSFAll = {}
        for backgroundName in backgrounds:
                histEEAll[backgroundName] = None
                histMMAll[backgroundName] = None
                histSFAll[backgroundName] = None
        
        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                plot = getPlot("mllPlot")
                plot.addRegion(selection)
                plot.addRunRange(runRange)   
                
                if "met > 150" in plot.cuts or "met > 100" in plot.cuts:
                        path = locations[runRange.era].dataSetPathNLL
                else:
                        path = locations[runRange.era].dataSetPath
                
                dataEE, dataMM = getHistograms(path,plot,runRange,False,backgrounds)
                if first:
                        dataEEAll = dataEE.Clone()
                        dataMMAll = dataMM.Clone()
                else:
                        dataEEAll.Add(dataEE, 1.0)
                        dataMMAll.Add(dataMM, 1.0)
                
                for backgroundName in backgrounds:
                        histEE, histMM = getHistograms(path,plot,runRange,True,[backgroundName,])
                        
                        if first:
                                histEEAll[backgroundName] = histEE.Clone()
                                histMMAll[backgroundName] = histMM.Clone()
                        else:
                                histEEAll[backgroundName].Add(histEE, 1.0)
                                histMMAll[backgroundName].Add(histMM, 1.0)
                if first:
                        first = False
        
        dataSFAll = dataEEAll.Clone()
        dataSFAll.Add(dataMMAll, 1.0)
        
        firstProc = True
        histMCSFAll = None
        histMCEEAll = None
        histMCMMAll = None
        
        for backgroundName in backgrounds:
                histSFAll[backgroundName] = histEEAll[backgroundName].Clone()
                histSFAll[backgroundName].Add(histMMAll[backgroundName], 1.0)
                
                if firstProc:
                        histMCSFAll = histSFAll[backgroundName].Clone()
                        histMCEEAll = histEEAll[backgroundName].Clone()
                        histMCMMAll = histMMAll[backgroundName].Clone()
                        firstProc = False
                else:
                        histMCSFAll.Add(histSFAll[backgroundName].Clone(), 1)
                        histMCEEAll.Add(histEEAll[backgroundName].Clone(), 1)
                        histMCMMAll.Add(histMMAll[backgroundName].Clone(), 1)
                        
        
        print "Data: "
        print "EE: ",dataEEAll.Integral()
        print "MM: ",dataMMAll.Integral()
        print "SF: ",dataSFAll.Integral()
        print ""
        print "MC: "
        print "EE: ",histMCEEAll.Integral()
        print "MM: ",histMCMMAll.Integral()
        print "SF: ",histMCSFAll.Integral()
        for backgroundName in backgrounds:
                print ""
                print backgroundName
                print "EE: ",histEEAll[backgroundName].Integral(), histEEAll[backgroundName].Integral()/histMCEEAll.Integral()
                print "MM: ",histMMAll[backgroundName].Integral(), histMMAll[backgroundName].Integral()/histMCMMAll.Integral()
                print "SF: ",histSFAll[backgroundName].Integral(), histSFAll[backgroundName].Integral()/histMCSFAll.Integral() 
        

def main():        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
      
        args = parser.parse_args()



        if len(args.selection) == 0:
                args.selection.append("SignalInclusiveVetoZ") 
        
        for selectionName in args.selection:
                selection = getRegion(selectionName)
                countEvents(selection) 

                        

                                    
main()
