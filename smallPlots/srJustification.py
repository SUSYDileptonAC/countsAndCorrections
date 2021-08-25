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




def getSignalHistogram(path,plot,runRange,sample, m1, m2):

              
        
        if "NLL" in path:
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
        
        
        year = runRange.era
        if year == "2017":
                yearAppend = "_Fall17"
        elif year == "2016":
                yearAppend = "_Summer16"
        elif year == "2018":
                yearAppend = "_Autumn18"
        
        if sample == "T6bbllslepton":
                sampleName = "T6bbllslepton_msbottom_%s_mneutralino_%s"%(m1,m2)
        elif sample == "T6qqllslepton":
                sampleName = "T6qqllslepton_msquark_%s_mneutralino_%s"%(m1,m2)
        
        sampleName += yearAppend
        
        treesEE = readSignalTrees(path,"EE",sampleName)
        treesMM = readSignalTrees(path,"MuMu",sampleName)
        
        
        scale = getSignalScale(sampleName, runRange)

        import numpy as np
        if (plot.binning == [] or plot.binning == None):
                binning = np.linspace(plot.firstBin, plot.lastBin, plot.nBins+1)
        else:
                binning = plot.binning

  
        histEE = createHistoFromTree(treesEE[sampleName], plot.variable, plot.cuts, plot.nBins, plot.firstBin, plot.lastBin, binning = binning)
        histMM = createHistoFromTree(treesMM[sampleName], plot.variable, plot.cuts, plot.nBins, plot.firstBin, plot.lastBin, binning = binning)
        histSF = histEE.Clone()
        
        histSF.Scale(scale)

        return histSF


def getHistogram(path,plot,runRange,background):
        treesEE = readTrees(path,"EE")
        treesMM = readTrees(path,"MuMu")
        
        if "NLL" in path:
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
        
        eventCounts = totalNumberOfGeneratedEvents(path)        
        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
        histSF = proc.createCombinedHistogram(runRange.lumi,plot,treesEE,treesMM)                  
        return histSF
        

def createVariableDistributions(selection, plotName, useNLL = False):
        from centralConfig import runRanges
        
        first = False
        histTT = None
        histDY = None
        
        sigHists = {}
        color = [1,2,3,ROOT.kOrange+7,7,ROOT.kGreen+2]
        sigPoints = [("T6bbllslepton", 1200, 150), ("T6bbllslepton", 1200, 1150), ("T6qqllslepton", 1400, 250), ("T6qqllslepton", 1400, 400), ("T6qqllslepton", 1400, 800)] # 
        
        for point in sigPoints:
                sigHists["%s_%s_%s"%(point[0], point[1], point[2])] = None
        
        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                if useNLL:
                        path = locations[runRange.era].dataSetPathNLL
                else:
                        path = locations[runRange.era].dataSetPath
                
                plot = getPlot(plotName)
                plot.addRegion(selection)
                plot.addRunRange(runRange)   

                histSF = getHistogram(path,plot,runRange,"TT_Powheg")
                if first:
                        histTT = histSF.Clone()
                else:
                        histTT.Add(histSF, 1.0)
                        
                plot = getPlot(plotName)
                plot.addRegion(selection)
                plot.addRunRange(runRange)  
                
                histSF = getHistogram(path,plot,runRange,"DrellYan")
                if first:
                        histDY = histSF.Clone()
                else:
                        histDY.Add(histSF, 1.0) 
                        
                plot = getPlot(plotName)
                plot.addRegion(selection)
                plot.addRunRange(runRange)  
                
                histSF = getHistogram(path,plot,runRange,"RareOnZ")
                if first:
                        histZNu = histSF.Clone()
                else:
                        histZNu.Add(histSF, 1.0) 
                
                i = 1
                for point in sigPoints:
                        if useNLL:
                                path = locations[runRange.era]["dataSetPathSignalNLL%s"%point[0]]
                        else:
                                path = locations[runRange.era]["dataSetPathSignal%s"%point[0]]
                
                        plot = getPlot(plotName)
                        plot.addRegion(selection)
                        plot.addRunRange(runRange) 
                        
                        
                        histSF = getSignalHistogram(path, plot, runRange, point[0], point[1], point[2])
                        
                        if "T6bbllslepton" in point[0]:
                                signame = "m_{#tilde{b}} = %s, m_{#tilde{#chi}_{2}^{0}} = %s GeV"%(point[1], point[2])
                        else:
                                signame = "m_{#tilde{q}} = %s, m_{#tilde{#chi}_{2}^{0}} = %s GeV"%(point[1], point[2])
                                
                        if first:
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])] = (histSF.Clone(), signame)
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].SetLineColor(color[i])
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].SetLineWidth(2)
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].SetMarkerSize(0)
                                i += 1
                        else:
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].Add(histSF, 1)
                
                if first:
                        first = False
                
        
        histTT.Scale(1. / histTT.Integral())
        histDY.Scale(1. / histDY.Integral())
        histZNu.Scale(1. / histZNu.Integral())
        
        # print histTT.Integral(1, histTT.FindBin(79.9))
        
        for point in sigPoints:
                sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].Scale(1.0 / sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].Integral())
                
        
        plotDistribution(histTT, histDY, histZNu, sigPoints, sigHists, selection, plot)

                
                

             
                        
def plotDistribution(histTT, histDY, histZNu, sigPoints, sigHists, selection, plot):
        
        template = plotTemplate()
        
        # histTT.SetLineColor(855)
        # histTT.SetFillStyle(0)
        # histTT.SetLineWidth(3)
        histTT.SetMarkerSize(0)

        histDY.SetLineColor(401)
        histDY.SetFillStyle(0)
        histDY.SetLineWidth(3)
        
        histZNu.SetLineColor(920)
        histZNu.SetFillStyle(0)
        histZNu.SetLineWidth(3)
        # histDY.SetMarkerSize(0)
        
        maximum = histTT.GetMaximum()
        if histDY.GetMaximum() > maximum:
                maximum = histDY.GetMaximum()
        if histZNu.GetMaximum() > maximum:
                maximum = histZNu.GetMaximum()
        
        template.setPrimaryPlot(histTT, "hist", label="t#bar{t}", legOption="F")
        template.addSecondaryPlot(histDY, "hist", label="DY+jets")
        template.addSecondaryPlot(histZNu, "hist", label="Z+#nu")
        template.redrawPrimary = False
        for point in sigPoints:
                if sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].GetMaximum() > maximum:
                        maximum = sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0].GetMaximum()
                
                template.addSecondaryPlot(sigHists["%s_%s_%s"%(point[0], point[1], point[2])][0], "hist", label=sigHists["%s_%s_%s"%(point[0], point[1], point[2])][1])
        
        template.hasLegend = True
        template.legendPosX1 = 0.43
        template.legendPosX2 = 0.93
        template.legendPosY1 = 0.6
        template.legendPosY2 = 0.9
        template.legendTextSize = 0.027
        
        template.latexCMS.posX = 0.15+0.02
        template.latexCMS.posY = 0.95-0.02
        template.latexCMS.align = 13
        
        template.latexCMSExtra.posX = 0.15+0.02
        template.latexCMSExtra.posY = 0.85
        template.latexCMSExtra.simPosY = 0.82
        
        template.labelX = plot.xaxis
        template.labelY = "fraction"
        
        template.latexCuts.text = selection.labelSubRegion
        # template.latexCuts.font = 62
        # template.latexCuts.size = 0.04
        template.latexCuts.posX = 0.5
        template.latexCuts.posY = 0.55
        template.latexCuts.align = 12
        
        template.logY = False
        template.minimumY = 0
        template.maximumY = maximum * 1.3
        
        # template.lumiInt = 137
        template.latexLumi.posY = 0.9575
        template.latexLumi.size = 0.045
        
        template.draw()
        template.axisField.GetYaxis().SetTitleOffset(1.2)
        
        # line1 = ROOT.TLine()
        # line1.SetLineStyle(2)
        # line1.SetLineColor(ROOT.kBlack)
        # line1.SetLineWidth(2)
        # line1.SetNDC(False)

        
        # line1.DrawLine(1.4, 0, 1.4, histEE.GetMaximum()/1.6)
        # line1.DrawLine(1.6, 0, 1.6, histEE.GetMaximum()/1.6)
        
        template.setFolderName("srPlots")

        template.saveAs("%s_%s"%(plot.variablePlotName,selection.name))
        
        


def main():
        
        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
      
        args = parser.parse_args()




        # createVariableDistributions(getRegion("Inclusive"), "mllPlot", False) 
        # createVariableDistributions(getRegion("SignalInclusive"), "mt2Plot", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "mllPlot", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "metPlot150", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "nJetsPlotC", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "htPlotC", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "nBJetsPlot", True) 
        # createVariableDistributions(getRegion("SignalInclusive"), "ptllPlot", True) 
        createVariableDistributions(getRegion("SignalInclusive"), "deltaPhiPlot", True) 
        createVariableDistributions(getRegion("SignalInclusive"), "sumMlbPlot", True) 

                        

                                    
main()
