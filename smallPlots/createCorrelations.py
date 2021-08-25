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
        # treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")
        
        eventCounts = totalNumberOfGeneratedEvents(path)        

        if "NLL" in path:
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
                plot2.cuts = plot2.cuts.replace(" && metFilterSummary > 0", "")
        

        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
        histSF = proc.createCombined2DHistogram(runRange.lumi,plot,plot2,treesEE,treesMM)

        # histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0, useTriggerEmulation=True).theHistogram                
        # histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0, useTriggerEmulation=True).theHistogram            
                

        return histSF
        

def getCorrelation(selection, background, var1, var2):
        from centralConfig import runRanges
        
        first = False

     
        histSFAll = None

        first = True
        for runRangeName in runRanges.allNames:
                runRange = getRunRange(runRangeName)
                path = locations[runRange.era].dataSetPathNLL
                
                plot = getPlot(var1)
                plot.addRegion(selection)
                plot.addRunRange(runRange)   
                
                plot2 = getPlot(var2)
                plot2.addRegion(selection)
                plot2.addRunRange(runRange)   


                histSF = getHistogram(path,plot,plot2,runRange,background)
                
                if first:
                        histSFAll = histSF.Clone()
                else:
                        histSFAll.Add(histSF, 1.0)

                if first:
                        first = False

        return histSFAll.GetCorrelationFactor()
        

def main():        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
      
        args = parser.parse_args()



        if len(args.selection) == 0:
                args.selection.append("SignalDeltaPhi") 
        
        variables = ["nJetsPlotC","htPlotC","sumMlbPlot","metPlot150","ptllPlot","deltaPhiPlot","mt2Plot"] #
        axes = []
        for var in variables:
                axis = getPlot(var).xaxis
                axis = axis.split(" [")[0]
                axes.append(axis)
        
        sample = "TT_Powheg"
        
        for selectionName in args.selection:
                selection = getRegion(selectionName)
                template = plotTemplate2D()
                
                corrHist = ROOT.TH2F("", "", len(variables), 0, len(variables)+1, len(variables), 0, len(variables)+1) 
                
                for i, var in enumerate(variables):
                        corrHist.GetXaxis().SetBinLabel(i+1, axes[i])
                        corrHist.GetXaxis().ChangeLabel(i+1, 90)
                        corrHist.GetYaxis().SetBinLabel(i+1, axes[i])
                
                for i,var1 in enumerate(variables):
                        for j, var2 in enumerate(variables):
                                if j <= i:
                                        corr = getCorrelation (selection, sample, var1, var2) 
                                        corrHist.SetBinContent(i+1, j+1, corr)
                                else:
                                        corrHist.SetBinContent(i+1, j+1, -5)
                                
                
                corrHist.GetZaxis().SetRangeUser(-1, 1)
                corrHist.GetZaxis().SetTitleOffset(1.1)
                
                template.setPrimaryPlot(corrHist, "COLZ TEXT")
                template.labelZ = "Correlation (#rho_{xy})"
                
                template.latexCMS.posX = 0.15+0.02
                
                template.latexCMS.posY = 0.95-0.02
                template.latexCMS.align = 13
                template.latexCMS.size = 0.06
                
                template.latexCMSExtra.posX = 0.15+0.02
                template.latexCMSExtra.posY = 0.86
                template.latexCMSExtra.simPosY = 0.84
                template.latexCMSExtra.size = 0.03
                
                template.lumiInt = 137
                template.latexLumi.posY = 0.9575
                template.latexLumi.size = 0.045
                
                template.latexRegion.text = selection.labelSubRegion
                template.latexRegion.size = 0.03
                template.latexRegion.posX = 0.15+0.02
                template.latexRegion.posY = 0.81
                template.latexRegion.align = 13
                
                template.labeledAxisX = True
                template.labeledAxisY = True
                
                ROOT.gStyle.SetPaintTextFormat("4.2f")
                
                ndiv = len(axes)-1
                template.nDivX = -8
                template.nDivY = -8
                
                template.draw()
                template.setFolderName("correlation")
                template.saveAs("corrs_%s_%s"%(selection.name, sample))
                # corrHist.Draw("COLZ TEXT")
                # raw_input("...")
                        

                                    
main()
