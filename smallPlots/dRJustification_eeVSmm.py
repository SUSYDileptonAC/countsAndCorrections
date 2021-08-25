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







def getHistograms(path,plot,runRange,backgrounds):

        treesEE = readTrees(path,"EE")
        treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")

        eventCounts = totalNumberOfGeneratedEvents(path)        
        processes = []
        for background in backgrounds:
                processes.append(Process(getattr(Backgrounds[runRange.era],background),eventCounts))
        histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram                
        histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram            


        return histoEE , histoMM
        

def createDRDistributions(selection, mllCut=True):
        from centralConfig import runRanges
        
        first = False
        histEEAll = None
        histMMAll = None
        
        
        
        backgrounds = ["TT_Powheg"]
        
        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                path = locations[runRange.era].dataSetPath
                
                plot = getPlot("deltaRPlot")
                plot.addRegion(selection)
                plot.addRunRange(runRange)   
                
                plot.cuts = plot.cuts.replace("deltaR > 0.1 &&", "")
                if not mllCut:
                        plot.cuts = plot.cuts.replace("mll > 20 &&", "")
                print plot.cuts
                
                histEE, histMM = getHistograms(path,plot,runRange,backgrounds)
                if first:
                        histEEAll = histEE.Clone()
                        histMMAll = histMM.Clone()
                else:
                        histEEAll.Add(histEE, 1.0)
                        histMMAll.Add(histMM, 1.0)
                
                if first:
                        first = False
                

        
        plotDistribution(histEEAll, histMMAll, plot, mllCut)

                
                

             
                        
def plotDistribution(histEE, histMM, plot, mllCut):
        
        template = plotTemplate()
        
        histEE.SetLineColor(ROOT.kBlack)
        histEE.SetMarkerColor(ROOT.kBlack)
        histEE.SetMarkerSize(0)

        histMM.SetLineColor(ROOT.kRed)
        histMM.SetMarkerColor(ROOT.kRed)
        histMM.SetMarkerSize(0)
        
        histEE.Scale(1. / histEE.Integral())
        histMM.Scale(1. / histMM.Integral())
        
        
        template.setPrimaryPlot(histEE, "hist", label="e^{#pm} e^{#mp}")
        template.addSecondaryPlot(histMM, "hist", label="#mu^{#pm} #mu^{#mp}")
        
        template.hasRatio = True
        template.addRatioPair(histEE, histMM)
        template.ratioLabel = "e^{#pm} e^{#mp} / #mu^{#pm} #mu^{#mp}"
        
        template.hasLegend = True
        template.legendPosX1 = 0.7
        template.legendPosX2 = 0.9
        template.legendPosY1 = 0.6
        template.legendPosY2 = 0.8
        template.legendTextSize = 0.04
        
        template.latexCMS.posX = 0.15+0.02
        template.latexCMS.posY = 0.95-0.02
        template.latexCMS.align = 13
        
        template.latexCMSExtra.posX = 0.15+0.02
        template.latexCMSExtra.posY = 0.85
        template.latexCMSExtra.simPosY = 0.82
        
        template.labelX = plot.xaxis
        template.labelY = "fraction"
        
        template.latexCuts.text = "t#bar{t} simulation"
        template.latexCuts.font = 62
        template.latexCuts.size = 0.04
        template.latexCuts.posX = 0.9
        
        template.logY = False
        template.minimumY = 0
        template.maximumScale = 1.3
        
        # template.lumiInt = 137
        template.latexLumi.posY = 0.9575
        template.latexLumi.size = 0.045
        
        template.draw()
        template.axisField.GetYaxis().SetTitleOffset(1.1)
        
        line1 = ROOT.TLine()
        line1.SetLineStyle(2)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.SetNDC(False)

        
        line1.DrawLine(1.4, 0, 1.4, histEE.GetMaximum()/1.6)
        line1.DrawLine(1.6, 0, 1.6, histEE.GetMaximum()/1.6)
        
        template.setFolderName("dRPlots")
        if mllCut:
                mllC = "mllCut"
        else:
                mllC = "nomllCut"
        template.saveAs("dR_%s"%mllC)
        
        


def main():
        
        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
      
        args = parser.parse_args()



        if len(args.selection) == 0:
                args.selection.append("Inclusive") 
        
        for selectionName in args.selection:
                selection = getRegion(selectionName)
                createDRDistributions(selection,True) 
                createDRDistributions(selection,False) 

                        

                                    
main()
