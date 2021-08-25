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

# WZ, ZZ, TTZ scaling

def existsScaleFactor(runRange, sample,noJetCuts=False):
        jetsString = ""
        if noJetCuts:
                jetsString = "_zeroJets"
        return os.path.isfile("shelves/scaleFactor_%s_%s%s.pkl"%(runRange.label, sample, jetsString))

def initializeScaleFactor(runRange, sample,noJetCuts=False):
        ensurePathExists("shelves/")
        factor = {}
        factor["scaleFac"] = 1.0
        factor["scaleFacErr"] = 0.0
        jetsString = ""
        if noJetCuts:
                jetsString = "_zeroJets"
                
        with open("shelves/scaleFactor_%s_%s%s.pkl"%(runRange.label, sample, jetsString), "w") as fi:
                pickle.dump(factor, fi)

def writeScaleFactor(runRange, sample, factor, noJetCuts=False):
        ensurePathExists("shelves/")
        jetsString = ""
        if noJetCuts:
                jetsString = "_zeroJets"
        with open("shelves/scaleFactor_%s_%s%s.pkl"%(runRange.label, sample, jetsString), "w") as fi:
                pickle.dump(factor, fi)
                
def readScaleFactor(runRange, sample,noJetCuts=False):
        ensurePathExists("shelves/")
        jetsString = ""
        if noJetCuts:
                jetsString = "_zeroJets"
        with open("shelves/scaleFactor_%s_%s%s.pkl"%(runRange.label, sample, jetsString), "r") as fi:
                factor = pickle.load(fi)
        return factor
        

def getHistograms(plot, runRange, backgrounds, scaling):
        era = runRange.era
        path = locations[era].dataSetPath
        
        treesEE = readTrees(path, "EE")
        treesEM = readTrees(path, "EMu")
        treesMM = readTrees(path, "MuMu")  
        

        cuts = plot.cuts
        plot.cuts = plot.cuts.replace("bTagWeightLoose*", "")
        plot.cuts = plot.cuts.replace("weight*", "")
        plot.cuts = plot.cuts.replace("genWeight*", "")
        
        dataEE = getDataHist(plot,treesEE)
        dataEM = getDataHist(plot,treesEM)
        dataMM = getDataHist(plot,treesMM)
        
        plot.cuts = cuts
        
        dataSF = dataEE.Clone()
        dataSF.Add(dataEM, 1)
        dataSF.Add(dataMM, 1)
        dataSF.SetBinErrorOption(ROOT.TH1.kPoisson)
        
        eventCounts = totalNumberOfGeneratedEvents(path)        
        processes = {}
        for background in backgrounds:
                processes[background]  = Process(getattr(Backgrounds[era],background),eventCounts)
        
        triggerSF_EE,_ = getTriggerScaleFactor("EE",   "inclusive", runRange)
        triggerSF_EM,_ = getTriggerScaleFactor("EMu", "inclusive", runRange)
        triggerSF_MM,_ = getTriggerScaleFactor("MuMu", "inclusive", runRange)
        
        histos = {}
        for background, process in processes.iteritems():
                histos[background] = {}
                
                sf = 1.0
                if scaling.has_key(background):
                        sf = scaling[background]["scaleFac"]
                        
                histoEE = process.createCombinedHistogram(runRange.lumi,plot,treesEE,tree2 = "None",shift = 1.,scalefacTree1=triggerSF_EE*sf,scalefacTree2=1.,useTriggerEmulation=True)
                histoEM = process.createCombinedHistogram(runRange.lumi,plot,treesEM,tree2 = "None",shift = 1.,scalefacTree1=triggerSF_EM*sf,scalefacTree2=1.,useTriggerEmulation=True)
                histoMM = process.createCombinedHistogram(runRange.lumi,plot,treesMM,tree2 = "None",shift = 1.,scalefacTree1=triggerSF_MM*sf,scalefacTree2=1.,useTriggerEmulation=True)
                histoSF = histoEE.Clone()
                histoSF.Add(histoEM, 1)
                histoSF.Add(histoMM, 1)
                
                histos[background]["EE"] = histoEE
                histos[background]["EM"] = histoEM
                histos[background]["MM"] = histoMM
                histos[background]["SF"] = histoSF
        
        histos["data"] = {}
        histos["data"]["EE"] = dataEE
        histos["data"]["EM"] = dataEM
        histos["data"]["MM"] = dataMM
        histos["data"]["SF"] = dataSF
        
        return histos, processes
        

def doPlots(sample, runRanges, plots, onZ=False, scaled=False, noJetCuts=False):
        backgrounds = ["ZZTo4L", "ttZToLL", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
        
        srVeto = "!(nJets >= 2 && met > 150 && MT2 > 80)"
        
        toScale =  ["ZZTo4L", "ttZToLL", "WZTo3LNu"]
        if noJetCuts:
                toScale = ["ZZTo4L", "WZTo3LNu"]
        
        if sample == "ZZTo4L":
                backgrounds = ["ZZTo4L", "ttZToLL", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleZZTo4L"),] # [getRegion("ControlScaleZZTo4LTwoJets"),
                if noJetCuts:
                         selections = [getRegion("ControlScaleZZTo4L"),] # 
                plotNames = ["nJetsPlot", ] # "mllPlotZCand4LScaleFactors","mt2Plot"
                zMassVar = "((abs(zcand.M() - 91) < abs(zcand2.M() - 91))*zcand.M() + (abs(zcand.M() - 91) > abs(zcand2.M() - 91))*zcand2.M())"
                additionalWeight = "bTagWeightLoose"
        elif sample == "ttZToLL":
                backgrounds = ["ttZToLL", "ZZTo4L", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleTTZToLLTwoJets"),] # getRegion("ControlScaleTTZToLL")
                # selections = [getRegion("ControlScaleTTZToLLTwoJetsOneB"),] # getRegion("ControlScaleTTZToLL")
                plotNames = ["nJetsPlot", "metPlot"] # , "mllPlotZCand3LScaleFactors","mt2Plot"
                zMassVar = "zcand.M()"
                additionalWeight = "bTagWeight"
        elif sample == "WZTo3LNu": 
                backgrounds = ["WZTo3LNu", "ZZTo4L", "ttZToLL", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleWZTo3LNu")] # 
                # selections = [getRegion("ControlScaleWZTo3LNuTwoJets"),getRegion("ControlScaleWZTo3LNu")] # 
                if noJetCuts:
                         selections = [getRegion("ControlScaleWZTo3LNu"),]
                plotNames = ["nJetsPlot", "metPlot"] # , "mt2Plot" "mllPlotZCand3LScaleFactors",
                zMassVar = "zcand.M()"
                additionalWeight = "bTagWeightLoose"
        
        
        vetoOffZ = "({zMass} > 86 && {zMass} < 96)".format(zMass=zMassVar)
        
        
        plotNames.extend(plots)
        
        template = plotTemplate()
        for runRange in runRanges:
                for selection in selections:
                        era = runRange.era
                        for plotName in plotNames:
                                plot = getPlot(plotName)
                                plot.addRegion(selection)
                                plot.addRunRange(runRange)
                                
                                plot.cuts = plot.cuts[:-1] + " && " + srVeto + ")"
                                if onZ:
                                        plot.cuts = plot.cuts[:-1] + " && " + vetoOffZ + ")"
                                plot.cuts = additionalWeight+"*"+plot.cuts
                                
                                if plot.variable == "met":
                                        if "met > " in selection.cut:
                                                metcut = 0.0
                                                parts = selection.cut.split("&&")
                                                for part in parts:
                                                        if "met > " in part: 
                                                                metcut = max(metcut, float(part.split("met > ")[1]))
                                                #print "met cut:",metcut
                                                #print plot.cuts
                                                plot.binning = [0, metcut]+ [r for r in range(0,201,50) if r > metcut]
                                                plot.yaxis = "Events / Bin"
                                                
                                
                                scaling = {}
                                if scaled:
                                        for s in toScale:
                                                scaling[s] = readScaleFactor(runRange, s,noJetCuts)
                                                                
                                histos, processes = getHistograms(plot, runRange, backgrounds, scaling)
                                
                                legend = ROOT.TLegend(0.7, 0.4, 0.93, 0.85)
                                legend.AddEntry(histos["data"]["SF"], "Data", "PE")
                                    
                                for background in backgrounds:
                                        process = processes[background]
                                        legend.AddEntry(histos[background]["SF"], process.label, "F")
                                
                                for combination in ["SF",]:
                                        template.maximumScale = 1.8
                                        template.plotData = True
                                        template.labelX = plot.xaxis
                                        template.labelY = plot.yaxis
                                        template.marginTop = 0.065
                                        template.marginLeft = 0.13
                                        
                                        template.minimumY = 0.0
                                        
                                        template.latexCuts.text = plot.label2
                                        if onZ:
                                                template.latexCuts.text += ", 86 < m_{ll}^{Z Cand} < 96 GeV"
                                        template.latexCuts.posY = 0.90
                                        
                                        template.lumiInt = runRange.printval
                                        
                                        template.hasRatio = True
                                        stack = ROOT.THStack()
                                        
                                        first = True
                                        for background in reversed(backgrounds):
                                                if first:
                                                        denom = histos[background][combination].Clone()
                                                        
                                                        denomUp = histos[background][combination].Clone()
                                                        denomDn = histos[background][combination].Clone()
                                                        
                                                        denomUpFull = histos[background][combination].Clone()
                                                        denomDnFull = histos[background][combination].Clone()
                                                        first = False
                                                else:
                                                        if scaled and background in toScale:
                                                                        denomUp.Add(histos[background][combination], 1.00+scaling[background]["scaleFacStatErr"]/scaling[background]["scaleFac"])
                                                                        denomDn.Add(histos[background][combination], 1.00-scaling[background]["scaleFacStatErr"]/scaling[background]["scaleFac"])
                                                                        
                                                                        denomUpFull.Add(histos[background][combination], 1.00+scaling[background]["scaleFacSystErr"]/scaling[background]["scaleFac"])
                                                                        denomDnFull.Add(histos[background][combination], 1.00-scaling[background]["scaleFacSystErr"]/scaling[background]["scaleFac"])
                                                        else:
                                                                        denomUp.Add(histos[background][combination], 1)
                                                                        denomDn.Add(histos[background][combination], 1)
                                                                        
                                                                        denomUpFull.Add(histos[background][combination], 1)
                                                                        denomDnFull.Add(histos[background][combination], 1)
                                                        denom.Add(histos[background][combination], 1)

                                                stack.Add(histos[background][combination])
        
                                        
                                        template.setPrimaryPlot(histos["data"][combination], "P")
                                        template.addSecondaryPlot(stack, "hist")
                                        
                                        if scaled:                                                
                                                #template.addRatioErrorBySize( "", scaling[sample]["scaleFacErr"], ROOT.kGreen+2, 1001, False,0)
                                                #template.addRatioErrorByHist("", denomUp, denomDn, ROOT.kGreen+2, 1001,number=0)
                                                template.addRatioErrorByHist("", denomUpFull, denomDnFull, ROOT.kBlue+2, 1001,number=0)
                                                
                                        
                                        stack.Draw("hist")
                                        template.addRatioPair(histos["data"][combination], denom)
                                        template.ratioLabel = "Data / MC"
                                        
                                        template.setFolderName(runRange.label)
                                        template.draw()
                                        template.plotPad.cd()
                                        legend.Draw("same")
                                        if scaled:
                                                scaleOrNot = "scaled"
                                        else:
                                                scaleOrNot = "unscaled"
                                        if onZ:
                                                onZOrNot = "onZ"
                                        else:
                                                onZOrNot = "allMasses"
                                        
                                        jetstring = ""
                                        if noJetCuts:
                                                template.setFolderName(runRange.label+"_noJetCut")
                                                jetstring = "_noJetsScaleFactor"
                                        template.saveAs("dataBackground_%s_%s_%s_%s_%s_%s%s"%(sample, plotName ,selection.latex, runRange.label, scaleOrNot, onZOrNot, jetstring))
                                        
                                        template.clean()
        
def calcScaleFactor(sample, runRanges, noJetCuts=False):
        backgrounds = ["ZZTo4L", "ttZToLL", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
        
        srVeto = "!(nJets >= 2 && met > 150 && MT2 > 80)"
        
        toScale = ["ZZTo4L", "ttZToLL", "WZTo3LNu"]
        if noJetCuts:
                toScale = ["ZZTo4L", "WZTo3LNu"]
        
        if sample == "ZZTo4L":
                backgrounds = ["ZZTo4L", "ttZToLL", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleZZTo4LTwoJets"),]
                if noJetCuts:
                         selections = [getRegion("ControlScaleZZTo4L"),]
                plotNames = ["mllPlotZCand4LScaleFactors",] # "nJetsPlot", "metPlot", "mt2Plot"
                systErr = 0.5
                additionalWeight = "bTagWeightLoose"
                
        elif sample == "ttZToLL":
                backgrounds = ["ttZToLL", "ZZTo4L", "WZTo3LNu", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleTTZToLLTwoJets"),] # getRegion("ControlScaleTTZToLL")
                plotNames = ["mllPlotZCand3LScaleFactors",] # "nJetsPlot", "metPlot", "mt2Plot"
                systErr = 0.3
                additionalWeight = "bTagWeight"
                
        elif sample == "WZTo3LNu": 
                backgrounds = ["WZTo3LNu", "ZZTo4L", "ttZToLL", "DrellYan", "DrellYanTauTau", "TT_Powheg", "DibosonRest", "SingleTop", "RareRest"]
                selections = [getRegion("ControlScaleWZTo3LNuTwoJets"),] # getRegion("ControlScaleWZTo3LNu")
                if noJetCuts:
                        selections = [getRegion("ControlScaleWZTo3LNu"),]
                plotNames = ["mllPlotZCand3LScaleFactors",] # "nJetsPlot", "metPlot", "mt2Plot"
                systErr = 0.3
                additionalWeight = "bTagWeightLoose"
        
        template = plotTemplate()
        for runRange in runRanges:
                for selection in selections:
                        era = runRange.era
                        for plotName in plotNames:
                                plot = getPlot(plotName)
                                plot.addRegion(selection)
                                plot.addRunRange(runRange)
                                
                                plot.cuts = plot.cuts[:-1] + " && " + srVeto + ")"
                                
                                plot.cuts = additionalWeight+"*"+plot.cuts
                                print plot.cuts
                                scaling = {}
                                
                                # set scale factor for current sample to 1 in case it isnt already
                                initializeScaleFactor(runRange, sample, noJetCuts)
                                for s in toScale:
                                        scaling[s] = readScaleFactor(runRange, s, noJetCuts)
                                
                                histos, processes = getHistograms(plot, runRange, backgrounds, scaling)
                                
                                legend = ROOT.TLegend(0.6, 0.4, 0.9, 0.85)
                                legend.AddEntry(histos["data"]["SF"], "Data", "PE")
                                    
                                for background in backgrounds:
                                        process = processes[background]
                                        legend.AddEntry(histos[background]["SF"], process.label, "F")
                                
                                for combination in ["SF",]:
                                        template.maximumScale = 1.6
                                        template.plotData = True
                                        template.labelX = plot.xaxis
                                        template.labelY = plot.yaxis
                                        
                                        template.minimumY = 0.0
                                        
                                        template.latexCuts.text = plot.label2
                                        template.latexCuts.posY = 0.90
                                        
                                        template.lumiInt = runRange.printval
                                        
                                        template.hasRatio = True
                                        stack = ROOT.THStack()
                                        first = True
                                        total = 0.0
                                        sig = 0.0
                                        
                                        counts = {}
                                        
                                        for background in reversed(backgrounds):
                                                if first:
                                                        denom = histos[background][combination].Clone()
                                                        first = False
                                                else:
                                                        denom.Add(histos[background][combination], 1)
                                                        
                                                if "mllPlotZCand" in plotName:
                                                        counts[background] = histos[background][combination].GetBinContent(histos[background][combination].FindBin(91))
                                                        counts[background+"Err"] = histos[background][combination].GetBinError(histos[background][combination].FindBin(91))
                                                        
                                                stack.Add(histos[background][combination])
                                        
                                        
                                        
                                        if "mllPlotZCand" in plotName:
                                                sig = counts[sample]
                                                total = denom.GetBinContent(denom.FindBin(91))
                                                
                                                
                                                
                                                counts["Total"] = total
                                                counts["TotalErr"] = denom.GetBinError(denom.FindBin(91))
                                                counts["Data"] = histos["data"][combination].GetBinContent(histos["data"][combination].FindBin(91))
                                                if counts["Data"] < counts["Total"]:
                                                        counts["DataErr"] = histos["data"][combination].GetBinErrorUp(histos["data"][combination].FindBin(91))
                                                else:
                                                        counts["DataErr"] = histos["data"][combination].GetBinErrorLow(histos["data"][combination].FindBin(91))
                                                #counts["DataErr"] = histos["data"][combination].GetBinError(histos["data"][combination].FindBin(91))
                                                
                                                bkg = 0
                                                bkgErr = 0
                                                for background in backgrounds:
                                                        if background != sample and counts[background] > 0:
                                                                bkg     += counts[background]
                                                                bkgErr  += (counts[background+"Err"])**2
                                                bkgErr = bkgErr**0.5
                                                
                                                signalYield = counts["Data"] - bkg
                                                signalYieldErr = (counts["DataErr"]**2 + bkgErr**2)**0.5
                                                
                                                scaleFac = signalYield / counts[sample]
                                                scaleFacErr = scaleFac*( (signalYieldErr/signalYield)**2 + (counts[sample+"Err"]/counts[sample])**2 )**0.5
                                                
                                                counts["background"] = bkg
                                                counts["backgroundErr"] = bkgErr
                                                
                                                counts["signalYield"] = signalYield
                                                counts["signalYieldErr"] = signalYieldErr
                                                
                                                counts["scaleFac"] = scaleFac
                                                counts["scaleFacStatErr"] = scaleFacErr
                                                counts["scaleFacSystErr"] = scaleFac * systErr
                                                counts["scaleFacErr"] = (counts["scaleFacStatErr"]**2 + counts["scaleFacSystErr"]**2)**0.5
                                                
                                                template.addLabel(LatexLabel(posX=0.6, posY=0.35, text="Purity: %.2f"%(sig/total)))
                                                template.addLabel(LatexLabel(posX=0.6, posY=0.30, text="Scale factor: %.2f #pm %.2f"%(scaleFac, scaleFacErr)))
                                                
                                                writeScaleFactor(runRange, sample, counts, noJetCuts)
                                                
                                                print counts["Data"], bkg, counts[sample]
                                                print scaleFac, scaleFacErr
                                                
                                        
                                        template.setPrimaryPlot(histos["data"][combination], "P")
                                        template.addSecondaryPlot(stack, "hist")
                                        
                                        stack.Draw("hist")
                                        template.addRatioPair(histos["data"][combination], denom)
                                        template.ratioLabel = "Data / MC"
                                        
                                        template.setFolderName(runRange.label)
                                        if noJetCuts:
                                                template.setFolderName(runRange.label+"_noJetCut")
                                        template.draw()
                                        template.plotPad.cd()
                                        legend.Draw("same")
                                        template.saveAs("calcScaleFac_%s_%s_%s_%s"%(sample, plotName ,selection.latex, runRange.label))
                                        
                                        template.clean()

def main():
        parser = argparse.ArgumentParser(description='produce cut & count event yields.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-s", "--scaled", action="store_true", dest="scaled", default=False,
                                                  help="Make scaled plots")
        parser.add_argument("-u", "--unscaled", action="store_true", dest="unscaled", default=False,
                                                  help="Make unscaled plots")             
        parser.add_argument("-c", "--calc", action="store_true", dest="calc", default=False,
                                                  help="Calculate scale factors")             
        parser.add_argument("-z", "--onz", action="store_true", dest="onZ", default=False,
                                                  help="Apply onZ cut for dependency studies")             
        parser.add_argument("-j", "--nojetcuts", action="store_true", dest="noJetCuts", default=False,
                                                  help="Calculate scale factors without nJets requirement")             
        parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
                                                  help="select dependencies to study, default is all.")
        parser.add_argument("-r", "--runRange", dest="runRanges", action="append", default=[],
                                                  help="name of run range.")
        #parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
                                                  #help="backgrounds to plot.")  
        parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
                                                  help="write results to central repository")   
        
        args = parser.parse_args()
        
        runRanges = [getRunRange(runRange) for runRange in args.runRanges]
        
        order = ["ZZTo4L",] # , "ttZToLL","WZTo3LNu",
        # order = ["ttZToLL"]
        if args.noJetCuts:
                order = ["ZZTo4L", "WZTo3LNu"]
        # if args.plots == []:
                # args.plots = ["nJetsPlotScaleFactors", "metPlotScaleFactors", "mt2PlotScaleFactors"]
        
        for runRange in runRanges:
                if args.calc:
                        for s in order: # 
                                if not existsScaleFactor(runRange, s, args.noJetCuts):
                                        initializeScaleFactor(runRange, s, args.noJetCuts)
                        for s in order: # 
                                calcScaleFactor(s, [runRange,], args.noJetCuts)
                
                for s in order:
                        if args.unscaled:
                                doPlots(s, [runRange,], args.plots, onZ=args.onZ, scaled=False, noJetCuts=args.noJetCuts)
                        if args.scaled:                             
                                doPlots(s, [runRange,], args.plots, onZ=args.onZ, scaled=True, noJetCuts=args.noJetCuts)
                

main()

