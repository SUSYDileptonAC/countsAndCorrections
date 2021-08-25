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
        

def plotIsolation(selection):
        from centralConfig import runRanges
        
        first = False
        histEEPromptAll = None
        histMMPromptAll = None
        histEEHeavyFlavourAll = None
        histMMHeavyFlavourAll = None
        histEEFakeAll = None
        histMMFakeAll = None
        
        fake = "!((pt1 < pt 2)*(abs(pdgId1)==11 || abs(pdgId1)==13 || (abs(pdgId1) == 22 && (abs(motherPdgId1) == 11 || abs(motherPdgId1) == 13 )))   || (pt1 > pt 2)*(abs(pdgId2)==11 || abs(pdgId2)==13) || (abs(pdgId2) == 22 && (abs(motherPdgId2) == 11 || abs(motherPdgId2) == 13 )))"
        dilep = "((pt1 < pt 2)*(abs(motherPdgId1)== 24 || abs(motherPdgId1)== 23 || abs(grandMotherPdgId1)== 24 || abs(grandMotherPdgId1)== 23) || (pt1 > pt 2)*(abs(motherPdgId2)== 24 || abs(motherPdgId2)== 23 || abs(grandMotherPdgId2)== 24 || abs(grandMotherPdgId2)== 23))"

        backgrounds = ["TT_Powheg"]
        
        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                path = locations[runRange.era].dataSetPathNonIso
                
                plot = getPlot("trailingIsoPlot")
                plot.addRegion(selection)
                plot.addRunRange(runRange)   
                    
                tmpCuts = plot.cuts
                
                plot.cuts = plot.cuts+"*(%s && !%s && !(pdgId1 == -9999 || pdgId2 == -9999))"%(dilep,fake)

                histEEPrompt, histMMPrompt = getHistograms(path,plot,runRange,backgrounds)
                if first:
                        histEEPromptAll = histEEPrompt.Clone()
                        histMMPromptAll = histMMPrompt.Clone()
                else:
                        histEEPromptAll.Add(histEEPrompt, 1.0)
                        histMMPromptAll.Add(histMMPrompt, 1.0)

        
                plot.cuts = tmpCuts+"*(!%s && !%s && !(pdgId1 == -9999 || pdgId2 == -9999))"%(dilep,fake)

                histEEHeavyFlavour, histMMHeavyFlavour = getHistograms(path,plot,runRange,backgrounds)
                
                if first:
                        histEEHeavyFlavourAll = histEEHeavyFlavour.Clone()
                        histMMHeavyFlavourAll = histMMHeavyFlavour.Clone()
                else:
                        histEEHeavyFlavourAll.Add(histEEHeavyFlavour, 1.0)
                        histMMHeavyFlavourAll.Add(histMMHeavyFlavour, 1.0)
                

        
                plot.cuts = tmpCuts+"*(%s && !(pdgId1 == -9999 || pdgId2 == -9999))"%(fake)

                histEEFake, histMMFake = getHistograms(path,plot,runRange,backgrounds)
#~ 
                if first:
                        histEEFakeAll = histEEFake.Clone()
                        histMMFakeAll = histMMFake.Clone()
                else:
                        histEEFakeAll.Add(histEEFake, 1.0)
                        histMMFakeAll.Add(histMMFake, 1.0)
                
                
                if first:
                        first = False
                

        
        plotDistribution(histEEPromptAll, histEEHeavyFlavourAll, histEEFakeAll, "electrons")
        plotDistribution(histMMPromptAll, histMMHeavyFlavourAll, histMMFakeAll, "muons")
                
                

             
                        
def plotDistribution(histPrompt, histHeavyFlavour, histFake, lepton):
        
        template = plotTemplate()
        
        histPrompt.SetLineColor(ROOT.kBlack)
        histPrompt.SetMarkerColor(ROOT.kBlack)
        histPrompt.SetMarkerSize(0)

        histHeavyFlavour.SetLineColor(ROOT.kBlue)
        histHeavyFlavour.SetMarkerColor(ROOT.kBlue)
        histHeavyFlavour.SetMarkerSize(0)
        
        histFake.SetLineColor(ROOT.kRed)
        histFake.SetMarkerColor(ROOT.kRed)
        histFake.SetMarkerSize(0)
        
        template.setPrimaryPlot(histPrompt, "histe", label="prompt %s"%lepton)
        template.addSecondaryPlot(histHeavyFlavour, "histe", label="%s from heavy flavour hadrons"%lepton)
        template.addSecondaryPlot(histFake, "histe", label="%s from misidentified jets"%lepton)
        
        template.hasLegend = True
        template.legendPosX1 = 0.4
        template.legendPosX2 = 0.9
        template.legendTextSize = 0.025
        
        template.latexCMS.posX = 0.15+0.02
        template.latexCMS.posY = 0.95-0.02
        template.latexCMS.align = 13
        
        template.latexCMSExtra.posX = 0.15+0.02
        template.latexCMSExtra.posY = 0.85
        template.latexCMSExtra.simPosY = 0.82
        
        template.labelX = "Iso_{rel}^{trailing %s}"%lepton
        template.labelY = "Events / 0.025"
        
        template.latexCuts.text = "t#bar{t} simulation"
        template.latexCuts.font = 62
        template.latexCuts.posX = 0.9
        
        template.logY = True
        template.minimumY = 0.1
        template.maximumScale = 1000
        
        template.lumiInt = 137
        template.latexLumi.posY = 0.9575
        template.latexLumi.size = 0.045
        
        template.draw()
        template.axisField.GetYaxis().SetTitleOffset(1.1)
        
        line1 = ROOT.TLine()
        line1.SetLineStyle(2)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.SetNDC(False)
        
        if lepton == "muons":
                posX = 0.2
        else:
                posX = 0.1
        
        line1.DrawLine(posX, 0.1, posX, histPrompt.GetMaximum()/100)
        
        template.setFolderName("isoPlots")
        template.saveAs("iso_%s"%lepton)
        
        


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
                plotIsolation(selection) 

                        

                                    
main()
