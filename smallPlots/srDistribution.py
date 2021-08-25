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
from helpers import readTrees, readSignalTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, getSignalScale, createHistoFromTree


from locations import locations
from plotTemplate import plotTemplate



def getHistogram(path,plot,runRange,background):
        treesEE = readTrees(path,"EE")
        treesMM = readTrees(path,"MuMu")
        
        if "NLL" in path:
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
        
        eventCounts = totalNumberOfGeneratedEvents(path)        
        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
        histSF = proc.createCombinedHistogram(runRange.lumi,plot,treesEE,treesMM)                  
        return histSF,proc
        

def createVariableDistributions(selection, plotName, useNLL = False):
        from centralConfig import runRanges
        
        first = False
        
        backgrounds = ["DrellYan","RareOnZ", "TT_Powheg", "SingleTop", "OtherSM"]
        backgrounds.reverse()
        
        hists = {}
        procs = {}
        
        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                if useNLL:
                        path = locations[runRange.era].dataSetPathNLL
                else:
                        path = locations[runRange.era].dataSetPath
                
                for background in backgrounds:  
                        plot = getPlot(plotName)
                        plot.addRegion(selection)
                        plot.addRunRange(runRange)   

                        hist,proc = getHistogram(path,plot,runRange,background)
                        
                        if first:
                                hists[background] = hist.Clone()
                                procs[background] = proc
                        else:
                                hists[background].Add(hist, 1.0)
                
                if first:
                        first = False
                
        
        stack = ROOT.THStack()
        for background in backgrounds:
                stack.Add(hists[background])
       
        plotDistribution(stack, backgrounds, procs, selection, plot)

                
                

             
                        
def plotDistribution(stack, backgrounds, procs, selection, plot):
        
        template = plotTemplate()
        
        
        template.setPrimaryPlot(stack, "hist")

        # template.redrawPrimary = False
        
        # template.hasLegend = True
        # template.legendPosX1 = 0.43
        # template.legendPosX2 = 0.93
        # template.legendPosY1 = 0.6
        # template.legendPosY2 = 0.9
        # template.legendTextSize = 0.027
        
        leg = ROOT.TLegend(0.63, 0.6, 0.93, 0.9)
        leg.SetTextSize(0.03)
        leg.SetTextFont(42)
        
        tmpHists = []
        for background in reversed(backgrounds):
                tmpHist = ROOT.TH1F()
                tmpHist.SetLineColor(procs[background].theLineColor)
                tmpHist.SetFillColor(procs[background].theColor)
                # tmpHist.SetFillStyle(1)
                tmpHists.append(tmpHist)
                leg.AddEntry(tmpHist, procs[background].label, "F")
        
        template.latexCMS.posX = 0.15+0.02
        template.latexCMS.posY = 0.95-0.02
        template.latexCMS.align = 13
        
        template.latexCMSExtra.posX = 0.15+0.02
        template.latexCMSExtra.posY = 0.85
        template.latexCMSExtra.simPosY = 0.82
        
        template.labelX = plot.xaxis
        template.labelY = plot.yaxis
        
        template.latexCuts.text = selection.labelSubRegion
        # template.latexCuts.font = 62
        # template.latexCuts.size = 0.04
        template.latexCuts.posX = 0.9
        template.latexCuts.posY = 0.55
        # template.latexCuts.align = 12
        
        template.logY = False
        template.minimumY = 0
        # template.maximumY = maximum * 1.3
        
        template.lumiInt = 137
        template.latexLumi.posY = 0.9575
        template.latexLumi.size = 0.045
        
        template.draw()
        template.axisField.GetYaxis().SetTitleOffset(1.1)
        
        leg.Draw("same")
        
        template.setFolderName("srPlots")

        template.saveAs("stacked_%s_%s"%(plot.variablePlotName,selection.name))
        
        


def main():
        
        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
      
        args = parser.parse_args()




        # createVariableDistributions(getRegion("Inclusive"), "mllPlot", False) 
        createVariableDistributions(getRegion("SignalInclusiveHighMT2"), "mllPlot", True) 
        createVariableDistributions(getRegion("SignalInclusiveHighMT2Met200"), "mllPlot", True) 

                        

                                    
main()
