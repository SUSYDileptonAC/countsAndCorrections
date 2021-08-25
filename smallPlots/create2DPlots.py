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
from plotTemplate import plotTemplate2D







def getHistogram(path,plot,plot2,runRange,background):

        treesEE = readTrees(path,"EE")
        treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")
        
        eventCounts = totalNumberOfGeneratedEvents(path)        

        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
        histSF = proc.createCombined2DHistogram(runRange.lumi,plot,plot2,treesEE,treesMM)

        # histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0, useTriggerEmulation=True).theHistogram                
        # histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0, useTriggerEmulation=True).theHistogram            
                

        return histSF
        

def createDistributions(selection, background):
        from centralConfig import runRanges
        
        first = False

     
        histSFAll = None

        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                path = locations[runRange.era].dataSetPath
                
                plot = getPlot("metPlot2D")
                plot.addRegion(selection)
                plot.addRunRange(runRange)   
                
                plot2 = getPlot("nJetsPlot2D")
                plot2.addRegion(selection)
                plot2.addRunRange(runRange)   


                histSF = getHistogram(path,plot,plot2,runRange,background)
                
                if first:
                        histSFAll = histSF.Clone()
                else:
                        histSFAll.Add(histSF, 1.0)

                if first:
                        first = False
        
        plotDistribution(histSFAll, plot ,plot2, background)
        
                    
def plotDistribution(hist, plot, plot2, background):
        
        template = plotTemplate2D()

        
        template.setPrimaryPlot(hist, "COLZ")


        
        # template.hasLegend = True
        # template.legendPosX1 = 0.7
        # template.legendPosX2 = 0.9
        # template.legendPosY1 = 0.6
        # template.legendPosY2 = 0.8
        # template.legendTextSize = 0.04
        
        template.latexCMS.posX = 0.15+0.02
        template.latexCMS.posY = 0.95-0.02
        template.latexCMS.align = 13
        template.latexCMS.size = 0.06
        
        template.latexCMSExtra.posX = 0.15+0.02
        template.latexCMSExtra.posY = 0.86
        template.latexCMSExtra.simPosY = 0.84
        template.latexCMSExtra.size = 0.03
        
        template.labelX = plot.xaxis
        template.labelY = plot2.xaxis
        template.labelZ = "Events"
        
        template.latexCuts.text = "t#bar{t} simulation"
        if background == "DrellYan":
                template.latexCuts.text = "DY+jets simulation"
        
        template.latexCuts.font = 62
        template.latexCuts.size = 0.033
        template.latexCuts.posX = 0.4
        template.latexCuts.posY = 0.88
        template.latexCuts.align = 12
        
        template.logZ = True
        template.minimumZ = 1
        # template.maximumScale = 1.3
        
        template.lumiInt = 137
        template.latexLumi.posY = 0.9575
        template.latexLumi.size = 0.045
        
        template.draw()
        hist.GetZaxis().SetTitleOffset(1.1)
        
        
        
        
        line1 = ROOT.TLine()
        # line1.SetLineStyle(2)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(3)
        line1.SetNDC(False)
        line1.DrawLine(150, 1.5,500, 1.5)
        line1.DrawLine(150, 1.5,150, 14.5)

        line2 = ROOT.TLine()
        line2.SetLineStyle(2)
        line2.SetLineColor(ROOT.kBlue)
        line2.SetLineWidth(3)
        line2.SetNDC(False)
        line2.DrawLine(0, 1.5,50, 1.5)
        line2.DrawLine(50, 1.5,50, 14.5)
        
        line3 = ROOT.TLine()
        line3.SetLineStyle(2)
        line3.SetLineColor(ROOT.kRed)
        line3.SetLineWidth(3)
        line3.SetNDC(False)
        line3.DrawLine(100, 1.5,100, 2.5)
        line3.DrawLine(100, 2.5,150, 2.5)
        line3.DrawLine(150, 1.5,150, 2.5)
        line3.DrawLine(100, 1.5,150, 1.5)

        h1 = ROOT.TH1F()
        h1.SetLineColor(ROOT.kBlack)
        h1.SetLineWidth(3)
        h1.SetLineStyle(1)

        h2 = ROOT.TH1F()
        h2.SetLineColor(ROOT.kBlue)
        h2.SetLineWidth(3)
        h2.SetLineStyle(2)

        h3 = ROOT.TH1F()
        h3.SetLineColor(ROOT.kRed)
        h3.SetLineWidth(3)
        h3.SetLineStyle(2)
        
        leg = ROOT.TLegend(0.4, 0.75, 0.75, 0.85)
        leg.SetFillStyle(0)
        leg.SetBorderSize(0)
        leg.SetTextFont(42)
        leg.AddEntry(h1, "Signal region", "l")
        leg.AddEntry(h3, "t#bar{t} control region", "l")
        leg.AddEntry(h2, "DY+jets control region", "l")
        leg.Draw()
        
        # box = ROOT.TPave()
        # box.SetNDC(False)
        # box.SetBorderSize(0)
        # box.SetFillStyle(2)
        # box.SetFillColor(ROOT.kBlack)
        # box.DrawPave(12.5,12,137.5,14.1)
        gr = ROOT.TGraph()
        gr.SetPoint(0, 12, 12)
        gr.SetPoint(1, 137.5,12)
        gr.SetPoint(2, 137.5,14.1)
        gr.SetPoint(3, 12,14.1)
        gr.SetPoint(4, 12,12)
        # gr.SetLineWidth(0)
        # gr.SetFillStyle(1)
        gr.SetFillColor(0)
        gr.Draw("fsame")
        template.drawLatexLabels()
        
        
        template.setFolderName("2DPlots")
        template.saveAs("2D_%s"%background)
        
        
        

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
                # createDistributions(selection, "TT_Powheg") 
                createDistributions(selection, "DrellYan") 

                        

                                    
main()
