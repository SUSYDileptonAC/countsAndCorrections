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
from helpers import readTrees, readSignalTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, getSignalScale, createHistoFromTree,getTriggerScaleFactor,getDataTriggerEfficiency


from locations import locations
from plotTemplate import plotTemplate

import ctypes
sigPoints = [("T6bbllslepton", 1200, 150), ("T6bbllslepton", 1200, 1150), ("T6qqllslepton", 1400, 250), ("T6qqllslepton", 1400, 400), ("T6qqllslepton", 1400, 800)] 
# sigPoints = [] 


mllCuts = {
                        "20To60":"mll < 60 && mll > 20",
                        "60To86":"mll < 86 && mll > 60",
                        "86To96":"mll < 96 && mll > 86",
                        "96To150":"mll < 150 && mll > 96",
                        "150To200":"mll < 200 && mll > 150",
                        "200To300":"mll > 200 && mll < 300",
                        "300To400":"mll > 300 && mll < 400",
                        "Above400":"mll > 400 ",
                        }

NllCuts = {
                        "lowNll":"nLL < 24",
                        "highNll":"nLL > 24",
                        }

NBCuts = {
                        "zeroBJets":"nBJets == 0",
                        "oneOrMoreBJets":"nBJets >= 1",
}

signalRegionCuts = {
                        "basicCut":"1>0",
                        "nJets2Cut":"nJets >= 2",
                        "met150Cut":"met > 150 && nJets >= 2",
                        "deltaPhiCut":"abs(deltaPhiJetMet1) > 0.4  && abs(deltaPhiJetMet2) > 0.4 && met > 150 && nJets >= 2",
                        "signalRegionCut":"met > 150 && MT2 > 80 && abs(deltaPhiJetMet1) > 0.4  && abs(deltaPhiJetMet2) > 0.4",
                        }



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
        
        eeEff = getDataTriggerEfficiency("EE", "Inclusive", runRange)
        mmEff = getDataTriggerEfficiency("MM", "Inclusive", runRange)
        
        scale = getSignalScale(sampleName, runRange)

        import numpy as np
        if (plot.binning == [] or plot.binning == None):
                binning = np.linspace(plot.firstBin, plot.lastBin, plot.nBins+1)
        else:
                binning = plot.binning

  
        histEE = createHistoFromTree(treesEE[sampleName], plot.variable, plot.cuts, plot.nBins, plot.firstBin, plot.lastBin, binning = binning)
        histEE.Scale(eeEff)
        histMM = createHistoFromTree(treesMM[sampleName], plot.variable, plot.cuts, plot.nBins, plot.firstBin, plot.lastBin, binning = binning)
        histMM.Scale(mmEff)
        histSF = histEE.Clone()
        
        histSF.Scale(scale)

        return histSF


def getHistogram(path,plot,runRange,background):
        treesEE = readTrees(path,"EE")
        treesMM = readTrees(path,"MuMu")
        
        if "NLL" in path:
                plot.cuts = plot.cuts.replace(" && metFilterSummary > 0", "")
        
        eeSF = getTriggerScaleFactor("EE", "Inclusive", runRange)[0]
        mmSF = getTriggerScaleFactor("EE", "Inclusive", runRange)[0]
        
        eventCounts = totalNumberOfGeneratedEvents(path)        
        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
        histSF = proc.createCombinedHistogram(runRange.lumi,plot,treesEE,treesMM, 1.0, eeSF, mmSF)                  
        return histSF
        

def getEventCount(selection, addCut, plotName, useNLL = False):
        from centralConfig import runRanges
        
        histTT = None
        histDY = None
        
        
        sigHists = {}
        
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
                plot.cuts = plot.cuts.replace("deltaR > 0.1 &&", "deltaR > 0.1 && (%s) &&"%(addCut))
                 

                histSF = getHistogram(path,plot,runRange,"TT_Powheg")
                if first:
                        histTT = histSF.Clone()
                else:
                        histTT.Add(histSF, 1.0)
                        

                
                for point in sigPoints:
                        if useNLL:
                                path = locations[runRange.era]["dataSetPathSignalNLL%s"%point[0]]
                        else:
                                path = locations[runRange.era]["dataSetPathSignal%s"%point[0]]
                
                        plot = getPlot(plotName)
                        plot.addRegion(selection)
                        plot.addRunRange(runRange) 
                        plot.cuts = plot.cuts.replace("deltaR > 0.1 &&", "deltaR > 0.1 && (%s) &&"%(addCut))
                        
                        
                        histSF = getSignalHistogram(path, plot, runRange, point[0], point[1], point[2])
                        
                        if first:
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])] = histSF.Clone()
                        else:
                                sigHists["%s_%s_%s"%(point[0], point[1], point[2])].Add(histSF, 1)
                
                if first:
                        first = False
        
        sf_yield = ctypes.c_double(1.0)
                
        counts = {}
        count = histTT.IntegralAndError(1, histTT.GetNbinsX()+1, sf_yield)
        err = sf_yield.value
        counts["TT_Powheg"] = (count, err)

        for point in sigPoints:
                count = sigHists["%s_%s_%s"%(point[0], point[1], point[2])].IntegralAndError(1, histTT.GetNbinsX()+1, sf_yield)
                err = sf_yield.value
                counts["%s_%s_%s"%(point[0], point[1], point[2])] = (count, err)
        return counts
        # print counts["TT_Powheg"]
        # print counts["T6bbllslepton_1200_150"]
  
def finishLineSignals(counts, selection):
        c = counts[selection]
        line = ""
        for sig in sigPoints:
                name = "%s_%s_%s"%(sig[0],sig[1],sig[2])
                val = c[name][0]
                err = c[name][1]
                if val > 0.1:
                        if err > 0.1:
                                line += r" & $%.1f \pm %.1f$ "%(val, err)
                        else:
                                line += r" & $%.2f \pm %.2f$ "%(val, err)
                else:
                        line += r" & $ < 0.1$ "
        return line
                
def makeCutflowTable(counts):
        #("T6bbllslepton", 1200, 150), ("T6bbllslepton", 1200, 1150), ("T6qqllslepton", 1400, 250), ("T6qqllslepton", 1400, 400), ("T6qqllslepton", 1400, 800)
        table = ""
        table += r"\begin{tabular}{crcccccc}\hline" + "\n"
        table += r"  &  &\multicolumn{6}{c}{SF events}\\\hline" + "\n"
        table += r"  &  & & \multicolumn{2}{c}{$m_{\sbottom}, m_{\chitwo}$[GeV]} & \multicolumn{3}{c}{$m_{\squark}, m_{\chitwo}$[GeV]} \\" + "\n"
        table += r" \multicolumn{2}{c}{Selection} & \ttbar production & $1200,150$ & $1200,1150$ & $1400,250$ & $1400,400$ & $1400,800$ \\\hline" + "\n"
        table += r" \multicolumn{2}{c}{Inclusive} & $%.1f \pm %.1f$ %s\\"%(counts["basicCut"]["TT_Powheg"][0],counts["basicCut"]["TT_Powheg"][1], finishLineSignals(counts, "basicCut")) + "\n"
        table += r" \multicolumn{2}{c}{$\nj \geq 2$} & $%.1f \pm %.1f$ %s\\"%(counts["nJets2Cut"]["TT_Powheg"][0],counts["nJets2Cut"]["TT_Powheg"][1], finishLineSignals(counts, "nJets2Cut")) + "\n"
        table += r" \multicolumn{2}{c}{$\met > 150\GeV$} & $%.1f \pm %.1f$ %s\\"%(counts["met150Cut"]["TT_Powheg"][0],counts["met150Cut"]["TT_Powheg"][1], finishLineSignals(counts, "met150Cut")) + "\n"
        table += r" \multicolumn{2}{c}{$\Delta\phi(\vecptjet, \vecmet)> 0.4$ } & $%.1f \pm %.1f$ %s\\"%(counts["deltaPhiCut"]["TT_Powheg"][0],counts["deltaPhiCut"]["TT_Powheg"][1], finishLineSignals(counts, "deltaPhiCut")) + "\n"
        table += r" \multicolumn{2}{c}{$\mttwo > 80\GeV$} & $%.1f \pm %.1f$ %s\\\hline"%(counts["signalRegionCut"]["TT_Powheg"][0],counts["signalRegionCut"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut")) + "\n"
        
        table += r" &\multicolumn{7}{c}{\ttbar-like}\\"+ "\n"
        table += r" & $20 < \mll < 60\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_lowNll_zeroBJets_20To60"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_20To60"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_20To60")) + "\n"
        table += r" & $60 < \mll < 86\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_lowNll_zeroBJets_60To86"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_60To86"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_60To86")) + "\n"
        table += r" & $96 < \mll < 150\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_zeroBJets_96To150"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_96To150"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_96To150")) + "\n"
        table += r" & $150 < \mll < 200\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_zeroBJets_150To200"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_150To200"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_150To200")) + "\n"
        table += r" & $200 < \mll < 300\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_zeroBJets_200To300"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_200To300"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_200To300")) + "\n"
        table += r" & $300 < \mll < 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_zeroBJets_300To400"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_300To400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_300To400")) + "\n"
        table += r" & $\mll > 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_zeroBJets_Above400"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_zeroBJets_Above400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_zeroBJets_Above400")) + "\n"
        
        table += r" $\nb=0$ &\multicolumn{7}{c}{non-\ttbar-like}\\"+ "\n"
        table += r" & $20 < \mll < 60\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_highNll_zeroBJets_20To60"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_20To60"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_20To60")) + "\n"
        table += r" & $60 < \mll < 86\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_highNll_zeroBJets_60To86"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_60To86"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_60To86")) + "\n"
        table += r" & $96 < \mll < 150\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_zeroBJets_96To150"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_96To150"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_96To150")) + "\n"
        table += r" & $150 < \mll < 200\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_zeroBJets_150To200"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_150To200"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_150To200")) + "\n"
        table += r" & $200 < \mll < 300\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_zeroBJets_200To300"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_200To300"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_200To300")) + "\n"
        table += r" & $300 < \mll < 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_zeroBJets_300To400"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_300To400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_300To400")) + "\n"
        table += r" & $\mll > 400\GeV$ & $%.1f \pm %.1f$ %s\\\hline"%(counts["signalRegionCut_highNll_zeroBJets_Above400"]["TT_Powheg"][0],counts["signalRegionCut_highNll_zeroBJets_Above400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_zeroBJets_Above400")) + "\n"        
        
        table += r" &\multicolumn{7}{c}{\ttbar-like}\\"+ "\n"
        table += r" & $20 < \mll < 60\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_lowNll_oneOrMoreBJets_20To60"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_20To60"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_20To60")) + "\n"
        table += r" & $60 < \mll < 86\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_lowNll_oneOrMoreBJets_60To86"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_60To86"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_60To86")) + "\n"
        table += r" & $96 < \mll < 150\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_oneOrMoreBJets_96To150"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_96To150"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_96To150")) + "\n"
        table += r" & $150 < \mll < 200\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_oneOrMoreBJets_150To200"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_150To200"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_150To200")) + "\n"
        table += r" & $200 < \mll < 300\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_oneOrMoreBJets_200To300"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_200To300"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_200To300")) + "\n"
        table += r" & $300 < \mll < 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_oneOrMoreBJets_300To400"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_300To400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_300To400")) + "\n"
        table += r" & $\mll > 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_lowNll_oneOrMoreBJets_Above400"]["TT_Powheg"][0],counts["signalRegionCut_lowNll_oneOrMoreBJets_Above400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_lowNll_oneOrMoreBJets_Above400")) + "\n"        
        
        table += r" $\nb\geq1$ &\multicolumn{7}{c}{non-\ttbar-like}\\"+ "\n"
        table += r" & $20 < \mll < 60\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_highNll_oneOrMoreBJets_20To60"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_20To60"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_20To60")) + "\n"
        table += r" & $60 < \mll < 86\GeV$ & $%.1f \pm %.1f$ %s\\"%( counts["signalRegionCut_highNll_oneOrMoreBJets_60To86"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_60To86"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_60To86")) + "\n"
        table += r" & $96 < \mll < 150\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_oneOrMoreBJets_96To150"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_96To150"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_96To150")) + "\n"
        table += r" & $150 < \mll < 200\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_oneOrMoreBJets_150To200"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_150To200"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_150To200")) + "\n"
        table += r" & $200 < \mll < 300\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_oneOrMoreBJets_200To300"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_200To300"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_200To300")) + "\n"
        table += r" & $300 < \mll < 400\GeV$ & $%.1f \pm %.1f$ %s\\"%(counts["signalRegionCut_highNll_oneOrMoreBJets_300To400"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_300To400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_300To400")) + "\n"
        table += r" & $\mll > 400\GeV$ & $%.1f \pm %.1f$ %s\\\hline"%(counts["signalRegionCut_highNll_oneOrMoreBJets_Above400"]["TT_Powheg"][0],counts["signalRegionCut_highNll_oneOrMoreBJets_Above400"]["TT_Powheg"][1], finishLineSignals(counts, "signalRegionCut_highNll_oneOrMoreBJets_Above400")) + "\n"        

        
        table += r"\end{tabular}"
        print table
def main():
        
        

        parser = argparse.ArgumentParser(description='create cut justification plots.')
        
        parser.add_argument("-u", "--use", action="store_true", dest="use", default=False,
                                                  help="Use existing.")

        args = parser.parse_args()


        cutRegions = ["basicCut","nJets2Cut","met150Cut","deltaPhiCut","signalRegionCut"]
        NllCutRegions = ["lowNll","highNll"]
        nBCutRegions = NBCuts.keys()
        mllCutRegions = ["20To60","60To86","86To96","96To150","150To200","200To300","300To400","Above400"]
        
        
        
        
        if not args.use:
                counts = {}
                
                for cutRegion in cutRegions:
                        addCut = signalRegionCuts[cutRegion]
                        useNLL = False
                        if "met > 150" in addCut:
                                useNLL = True
                        counts[cutRegion] = getEventCount(getRegion("Inclusive"), addCut, "mllPlot", useNLL) 
                        print cutRegion
                        
                cutRegion = "signalRegionCut"
                for nBCut in nBCutRegions:
                        for nllCut in NllCutRegions:
                                for mllCut in mllCutRegions:
                                        addCut = "%s && %s && %s && %s"%(signalRegionCuts[cutRegion], NllCuts[nllCut], NBCuts[nBCut], mllCuts[mllCut])
                                        cutName = "%s_%s_%s_%s"%(cutRegion, nllCut, nBCut, mllCut)
                                        useNLL = True
                                        counts[cutName] = getEventCount(getRegion("Inclusive"), addCut, "mllPlot", useNLL) 
                                        print cutName
                                        
                with open("shelves/cutFlowMC.pkl", "w") as fi:
                        pickle.dump(counts, fi)
        else:
                with open("shelves/cutFlowMC.pkl", "r") as fi:
                        counts = pickle.load(fi)                           
         
        makeCutflowTable(counts)
        # import pprint
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(counts)
                        
main()
