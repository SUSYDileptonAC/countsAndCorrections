#!/usr/bin/env python
import gc
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

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import argparse 

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts

from setTDRStyle import setTDRStyle
from helpers import getDataTrees, TheStack, totalNumberOfGeneratedEvents, Process, readTrees, createHistoFromTree, getTriggerScaleFactor


from centralConfig import regionsToUse, runRanges, backgroundLists, plotLists, systematics, mllBins, cutNCountXChecks
#from corrections import rMuELeptonPt, triggerEffs
from corrections import corrections

from locations import locations


def getEventLists(trees, cut,isMC, colNames = ["eventNr","lumiSec","runNr"]):
        result = {
                "columns": colNames,
                "cut": cut
                }
        if not isMC:    
                for comb in trees:
                        subtree = trees[comb].CopyTree(cut)
                        result[comb] = set()
                        #~ print comb
                        for ev in subtree:
                                
                                #~ print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
                                cols = []
                                for varName in colNames:
                                        cols.append( getattr(ev, varName) )
                                result[comb].add(tuple(cols))
                        subtree.IsA().Destructor(subtree) ### ROOT destructor to really get the memeory released
                        gc.collect()
        return result

def getCounts(trees, cut, isMC, backgrounds,plot,runRange,path, blind=False):
        
        rMuEPars = corrections[runRange.era].rMuELeptonPt.inclusive
            
        corrMap =  {}
        corrMapUp =  {}
        corrMapDn =  {}
        if isMC:
                corrMap["offset"] = rMuEPars.ptOffsetMC
                corrMap["falling"] = rMuEPars.ptFallingMC
                corrMap["etaParabolaBase"] = rMuEPars.etaParabolaBaseMC
                corrMap["etaParabolaMinus"] = rMuEPars.etaParabolaMinusMC
                corrMap["etaParabolaPlus"] = rMuEPars.etaParabolaPlusMC
                corrMap["norm"] = rMuEPars.normMC    
        else:
                corrMap["offset"] = rMuEPars.ptOffset
                corrMap["falling"] = rMuEPars.ptFalling
                corrMap["etaParabolaBase"] = rMuEPars.etaParabolaBase
                corrMap["etaParabolaMinus"] = rMuEPars.etaParabolaMinus
                corrMap["etaParabolaPlus"] = rMuEPars.etaParabolaPlus
                corrMap["norm"] = rMuEPars.norm
                
                
        rMuEDummy = "({norm:.3f}*( ({offset:.3f} + {falling:.3f}/{pt})*({etaParabolaBase} + ({eta}<-1.6)*{etaParabolaMinus:.3f}*pow({eta}+1.6, 2)+({eta}>1.6)*{etaParabolaPlus:.3f}*pow({eta}-1.6,2) )))"
        rMuE_El = rMuEDummy.format(pt="pt1", eta="eta1", **corrMap)
        rMuE_Mu = rMuEDummy.format(pt="pt2", eta="eta2", **corrMap)
        rMuEWeight = "(0.5*(%s + pow(%s, -1)))"%(rMuE_El, rMuE_Mu)
        
        rMuEWeight_EE = "(0.5*pow(%s, -1))"%(rMuE_Mu)
        rMuEWeight_MM = "(0.5*(%s))"%(rMuE_El)
        
        variationUpFlat = "(1 + 0.05)" #
        variationDnFlat = "(1 - 0.05)" #
        variationUpPt = "(1 + 0.05*max(110.0 - {pt},0)/90.0)" #
        variationDnPt = "(1 - 0.05*max(110.0 - {pt},0)/90.0)" #
        variationUpEta = "(1 + 0.05*abs(max({eta}-1.2,0))/1.2 )" #
        variationDnEta = "(1 - 0.05*abs(max({eta}-1.2,0))/1.2 )" #
        
        
        # Flat uncertainty
        rMuE_ElUpFlat = "(%s*%s)"%(rMuE_El, variationUpFlat)
        rMuE_MuUpFlat = "(%s*%s)"%(rMuE_Mu, variationUpFlat)
        rMuEWeightUpFlat = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElUpFlat, rMuE_MuUpFlat)
        rMuEWeightUpFlat_MM = "(0.5*(%s))"%(rMuE_ElUpFlat)
        rMuEWeightUpFlat_EE = "(0.5*pow(%s, -1))"%(rMuE_MuUpFlat)
        
        rMuE_ElDnFlat = "(%s*%s)"%(rMuE_El, variationDnFlat)
        rMuE_MuDnFlat = "(%s*%s)"%(rMuE_Mu, variationDnFlat)
        rMuEWeightDnFlat = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElDnFlat, rMuE_MuDnFlat)
        rMuEWeightDnFlat_MM = "(0.5*(%s))"%(rMuE_ElDnFlat)
        rMuEWeightDnFlat_EE = "(0.5*pow(%s, -1))"%(rMuE_MuDnFlat)
        
        # Pt uncertainty
        rMuE_ElUpPt = "(%s*%s)"%(rMuE_El, variationUpPt.format(pt="pt1"))
        rMuE_MuUpPt = "(%s*%s)"%(rMuE_Mu, variationUpPt.format(pt="pt2"))
        rMuEWeightUpPt = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElUpPt, rMuE_MuUpPt)
        rMuEWeightUpPt_MM = "(0.5*(%s))"%(rMuE_ElUpPt)
        rMuEWeightUpPt_EE = "(0.5*pow(%s, -1))"%(rMuE_MuUpPt)
        
        rMuE_ElDnPt = "(%s*%s)"%(rMuE_El, variationDnPt.format(pt="pt1"))
        rMuE_MuDnPt = "(%s*%s)"%(rMuE_Mu, variationDnPt.format(pt="pt2"))
        rMuEWeightDnPt = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElDnPt, rMuE_MuDnPt)
        rMuEWeightDnPt_MM = "(0.5*(%s))"%(rMuE_ElDnPt)
        rMuEWeightDnPt_EE = "(0.5*pow(%s, -1))"%(rMuE_MuDnPt)
        
        # Pt uncertainty
        rMuE_ElUpEta = "(%s*%s)"%(rMuE_El, variationUpEta.format(eta="eta1"))
        rMuE_MuUpEta = "(%s*%s)"%(rMuE_Mu, variationUpEta.format(eta="eta2"))
        rMuEWeightUpEta = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElUpEta, rMuE_MuUpEta)
        rMuEWeightUpEta_MM = "(0.5*(%s))"%(rMuE_ElUpEta)
        rMuEWeightUpEta_EE = "(0.5*pow(%s, -1))"%(rMuE_MuUpEta)
        
        rMuE_ElDnEta = "(%s*%s)"%(rMuE_El, variationDnEta.format(eta="eta1"))
        rMuE_MuDnEta = "(%s*%s)"%(rMuE_Mu, variationDnEta.format(eta="eta2"))
        rMuEWeightDnEta = "(0.5*(%s + pow(%s, -1)))"%(rMuE_ElDnEta, rMuE_MuDnEta)
        rMuEWeightDnEta_MM = "(0.5*(%s))"%(rMuE_ElDnEta)
        rMuEWeightDnEta_EE = "(0.5*pow(%s, -1))"%(rMuE_MuDnEta)
        
        
        plot.cuts = cut.replace("prefireWeight*leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*", "")
        
        cutRMuEScaled = "%s*%s"%(rMuEWeight,plot.cuts)
        cutRMuEScaledUpFlat = "%s*%s"%(rMuEWeightUpFlat,plot.cuts)
        cutRMuEScaledDnFlat = "%s*%s"%(rMuEWeightDnFlat,plot.cuts)
        cutRMuEScaledUpPt = "%s*%s"%(rMuEWeightUpPt,plot.cuts)
        cutRMuEScaledDnPt = "%s*%s"%(rMuEWeightDnPt,plot.cuts)
        cutRMuEScaledUpEta = "%s*%s"%(rMuEWeightUpEta,plot.cuts)
        cutRMuEScaledDnEta = "%s*%s"%(rMuEWeightDnEta,plot.cuts)
        
        cutRMuEScaled_EE = "%s*%s"%(rMuEWeight_EE,plot.cuts)
        cutRMuEScaledUpFlat_EE = "%s*%s"%(rMuEWeightUpFlat_EE,plot.cuts)
        cutRMuEScaledDnFlat_EE = "%s*%s"%(rMuEWeightDnFlat_EE,plot.cuts)
        cutRMuEScaledUpPt_EE = "%s*%s"%(rMuEWeightUpPt_EE,plot.cuts)
        cutRMuEScaledDnPt_EE = "%s*%s"%(rMuEWeightDnPt_EE,plot.cuts)
        cutRMuEScaledUpEta_EE = "%s*%s"%(rMuEWeightUpEta_EE,plot.cuts)
        cutRMuEScaledDnEta_EE = "%s*%s"%(rMuEWeightDnEta_EE,plot.cuts)
        
        cutRMuEScaled_MM = "%s*%s"%(rMuEWeight_MM,plot.cuts)
        cutRMuEScaledUpFlat_MM = "%s*%s"%(rMuEWeightUpFlat_MM,plot.cuts)
        cutRMuEScaledDnFlat_MM = "%s*%s"%(rMuEWeightDnFlat_MM,plot.cuts)
        cutRMuEScaledUpPt_MM = "%s*%s"%(rMuEWeightUpPt_MM,plot.cuts)
        cutRMuEScaledDnPt_MM = "%s*%s"%(rMuEWeightDnPt_MM,plot.cuts)
        cutRMuEScaledUpEta_MM = "%s*%s"%(rMuEWeightUpEta_MM,plot.cuts)
        cutRMuEScaledDnEta_MM = "%s*%s"%(rMuEWeightDnEta_MM,plot.cuts)
        
        
        if isMC:
                RT = corrections[runRange.era].rSFOFTrig.inclusive.valMC
                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.errMC
        else:
                RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.err
        
        if isMC:
                source = ""
                modifier = ""
                eventCounts = totalNumberOfGeneratedEvents(path,source,modifier)        
                processes = []
                for background in backgrounds:
                        processes.append(Process(getattr(Backgrounds[runRange.era],background),eventCounts))
                
                n= {}
                for region in ["inclusive",]:                        
                        histEE = TheStack(processes,runRange.lumi,plot,trees["EE"],"None",1.0,getTriggerScaleFactor("EE", region, runRange),1.0).theHistogram             
                        histMM = TheStack(processes,runRange.lumi,plot,trees["MM"],"None",1.0,getTriggerScaleFactor("MM", region, runRange),1.0).theHistogram
                        histEM = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,getTriggerScaleFactor("EM", region, runRange),1.0).theHistogram
                                                
                        triggerEffs = corrections[runRange.era]
                        histEE.Scale(getattr(triggerEffs,region).effEE.val)
                        histMM.Scale(getattr(triggerEffs,region).effMM.val)     
                        histEM.Scale(getattr(triggerEffs,region).effEM.val)     
                        
                        # central value
                        plot.cuts = cutRMuEScaled
                        histEMRMuEScaled = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                           
                        histEMRMuEScaled.Scale(getattr(triggerEffs,region).effEM.val)   
                                       
                        # flat uncertainty
                        plot.cuts = cutRMuEScaledUpFlat
                        histEMRMuEScaledUpFlat = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                         
                        histEMRMuEScaledUpFlat.Scale(getattr(triggerEffs,region).effEM.val)         
                                
                        plot.cuts = cutRMuEScaledDnFlat
                        histEMRMuEScaledDownFlat = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                               
                        histEMRMuEScaledDownFlat.Scale(getattr(triggerEffs,region).effEM.val)                               
                        
                        # pt uncertainty
                        plot.cuts = cutRMuEScaledUpPt
                        histEMRMuEScaledUpPt = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                         
                        histEMRMuEScaledUpPt.Scale(getattr(triggerEffs,region).effEM.val)         
                                
                        plot.cuts = cutRMuEScaledDnPt
                        histEMRMuEScaledDownPt = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                               
                        histEMRMuEScaledDownPt.Scale(getattr(triggerEffs,region).effEM.val)                               
                        
                        # eta uncertainty
                        plot.cuts = cutRMuEScaledUpEta
                        histEMRMuEScaledUpEta = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                         
                        histEMRMuEScaledUpEta.Scale(getattr(triggerEffs,region).effEM.val)         
                                
                        plot.cuts = cutRMuEScaledDnEta
                        histEMRMuEScaledDownEta = TheStack(processes,runRange.lumi,plot,trees["EM"],"None",1.0,1.0,1.0).theHistogram                               
                        histEMRMuEScaledDownEta.Scale(getattr(triggerEffs,region).effEM.val)                               
                         
                        
                        
                        eeErr = ROOT.Double()
                        ee = histEE.IntegralAndError(0,-1,eeErr)
                        mmErr = ROOT.Double()
                        mm = histMM.IntegralAndError(0,-1,mmErr)
                        emErr = ROOT.Double()
                        em = histEM.IntegralAndError(0,-1,emErr)
                        
                        #central value
                        emRMuEScaledErr = ROOT.Double()
                        emRMuEScaled = histEMRMuEScaled.IntegralAndError(0,-1,emRMuEScaledErr)
                        
                        
                        # flat uncertainty
                        emRMuEScaledUpFlatErr = ROOT.Double()
                        emRMuEScaledUpFlat = histEMRMuEScaledUpFlat.IntegralAndError(0,-1,emRMuEScaledUpFlatErr)
                        emRMuEScaledDownFlatErr = ROOT.Double()
                        emRMuEScaledDownFlat = histEMRMuEScaledDownFlat.IntegralAndError(0,-1,emRMuEScaledDownFlatErr)
                        
                        # pt uncertainty
                        emRMuEScaledUpPtErr = ROOT.Double()
                        emRMuEScaledUpPt = histEMRMuEScaledUpPt.IntegralAndError(0,-1,emRMuEScaledUpPtErr)
                        emRMuEScaledDownPtErr = ROOT.Double()
                        emRMuEScaledDownPt = histEMRMuEScaledDownPt.IntegralAndError(0,-1,emRMuEScaledDownPtErr)
                        
                        # eta uncertainty
                        emRMuEScaledUpEtaErr = ROOT.Double()
                        emRMuEScaledUpEta = histEMRMuEScaledUpEta.IntegralAndError(0,-1,emRMuEScaledUpEtaErr)
                        emRMuEScaledDownEtaErr = ROOT.Double()
                        emRMuEScaledDownEta = histEMRMuEScaledDownEta.IntegralAndError(0,-1,emRMuEScaledDownEtaErr)
                        
                        
                        
                        n["EMRMuEScaled"] = emRMuEScaled*RT
                        n["EMRMuEScaledUpFlat"] = emRMuEScaledUpFlat*RT
                        n["EMRMuEScaledDownFlat"] = emRMuEScaledDownFlat*RT
                        n["EMRMuEScaledUpPt"] = emRMuEScaledUpPt*RT
                        n["EMRMuEScaledDownPt"] = emRMuEScaledDownPt*RT
                        n["EMRMuEScaledUpEta"] = emRMuEScaledUpEta*RT
                        n["EMRMuEScaledDownEta"] = emRMuEScaledDownEta*RT
                        
                        n["MM"] = mm
                        n["EE"] = ee
                        n["EM"] = em
                        n["MMStatErr"] = float(mmErr)
                        n["EEStatErr"] = float(eeErr)
                        n["EMStatErr"] = float(emErr)

                
        else:
                n= {}
                for region in ["inclusive",]:
                        if blind:
                                n["MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_MM,100,0,10000).Integral(0,-1)*RT
                                n["EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_EE,100,0,10000).Integral(0,-1)*RT
                        else:
                                n["MM"] = trees["MM"].GetEntries(plot.cuts)
                                n["EE"] = trees["EE"].GetEntries(plot.cuts)
                        n["EM"] = trees["EM"].GetEntries(plot.cuts)
                        
                        n["EMRMuEScaled"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled,100,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaled_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_EE,100,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaled_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_MM,100,0,10000).Integral(0,-1)*RT
                        
                        n["EMRMuEScaledUpRT"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled,10,0,10000).Integral(0,-1)*(RT+RTErr)
                        n["EMRMuEScaledDownRT"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled,10,0,10000).Integral(0,-1)*(RT-RTErr)
                        n["EMRMuEScaledUpFlat"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpFlat,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownFlat"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnFlat,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpPt"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpPt,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownPt"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnPt,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpEta"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpEta,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownEta"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnEta,10,0,10000).Integral(0,-1)*RT
                        
                        n["EMRMuEScaledUpRT_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_EE,10,0,10000).Integral(0,-1)*(RT+RTErr)
                        n["EMRMuEScaledDownRT_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_EE,10,0,10000).Integral(0,-1)*(RT-RTErr)
                        n["EMRMuEScaledUpFlat_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpFlat_EE,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownFlat_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnFlat_EE,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpPt_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpPt_EE,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownPt_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnPt_EE,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpEta_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpEta_EE,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownEta_EE"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnEta_EE,10,0,10000).Integral(0,-1)*RT
                        
                        n["EMRMuEScaledUpRT_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_MM,10,0,10000).Integral(0,-1)*(RT+RTErr)
                        n["EMRMuEScaledDownRT_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaled_MM,10,0,10000).Integral(0,-1)*(RT-RTErr)
                        n["EMRMuEScaledUpFlat_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpFlat_MM,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownFlat_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnFlat_MM,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpPt_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpPt_MM,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownPt_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnPt_MM,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledUpEta_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledUpEta_MM,10,0,10000).Integral(0,-1)*RT
                        n["EMRMuEScaledDownEta_MM"] = createHistoFromTree(trees["EM"],"mll",cutRMuEScaledDnEta_MM,10,0,10000).Integral(0,-1)*RT
                        
                        n["MMStatErr"] = n["MM"]**0.5   
                        n["EEStatErr"] = n["EE"]**0.5   
                        n["EMStatErr"] = n["EM"]**0.5   
                
        n["cut"] = cut
        return n
        


        
        
        
        


def cutAndCountForRegion(path,selection,plots,runRange,isMC,backgrounds, blind=False):
        
        
        if not isMC:
                trees = getDataTrees(path)
                for label, tree in trees.iteritems():
                        trees[label] = tree.CopyTree("nJets > 1")               
        else:
                treesEE = readTrees(path,"EE",source = "",modifier= "")
                treesEM = readTrees(path,"EMu",source = "",modifier= "")
                treesMM = readTrees(path,"MuMu",source = "",modifier= "")               
                trees = {
                                "EE":treesEE,
                                "MM":treesMM,
                                "EM":treesEM,
                }
                
                

        for plotName in plots:
                plot = getPlot(plotName)
                plot.addRegion(selection)
                plot.cleanCuts()
                plot.addRunRange(runRange)
                #plot.cuts = plot.cuts % runRange.runCut 

                counts = {}
                eventLists = {}
                # ,"highMassOld","highMass","lowMass","lowMassOld", "mass60To81", "mass81To101", "mass101To150",
                massBins = ["mass20To60","mass60To86","mass86To96","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
                nLLRegions = ["lowNLL","highNLL"]
                MT2Regions = ["highMT2"] # "lowMT2",
                nBJetsRegions = ["zeroBJets", "oneOrMoreBJets"]
                
                counts["default"] = {}
                eventLists["default"] = {}
                
                if runRange.era == "2018":
                        plot.cuts = plot.cuts.replace("chargeProduct < 0 &&","chargeProduct < 0 && vetoHEM == 1 &&")
                
                standardCut = plot.cuts
                #for mllCut in massBins:
                #        cut = standardCut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
                #        cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
                #        #~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
                #        if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
                #                cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
                #        cut = cut.replace("p4.M()","mll")
                #        cut = cut.replace("p4.Pt()","pt")
                #        cut = cut.replace("metFilterSummary > 0 &&","")
                #        cut = cut.replace("&& metFilterSummary > 0","")
                #        cut = cut.replace("triggerSummary > 0 &&","")
                #        cut = cut.replace("genWeight*","")
                #        cut = cut.replace("prefireWeight*","")
                #        cut = cut.replace("weight*","")
                #        cut = cut.replace("leptonFullSimScaleFactor1*","")
                #        cut = cut.replace("leptonFullSimScaleFactor2*","")
                #        cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
                #        if runRange.era != "2018":
                #                cut = "prefireWeight*"+cut
                #        #~ cut = "genWeight*weight*("+cut+")"
                #                
                #        
                #        counts["default"][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path, blind)
                #        #~ eventLists["default"][getattr(theCuts.massCuts,mllCut).name] = getEventLists(trees,cut,isMC)         

                for nLLRegion in nLLRegions:            
                        counts[nLLRegion] = {}
                        eventLists[nLLRegion] = {}                                      
                        
                        #for mllCut in massBins:
                        #        cut = standardCut+" && (%s)"%getattr(theCuts.nLLCuts,nLLRegion).cut
                        #        cut = cut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
                        #        cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
                        #        #~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
                        #        if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
                        #                cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
                        #        cut = cut.replace("p4.M()","mll")
                        #        cut = cut.replace("p4.Pt()","pt")
                        #        cut = cut.replace("metFilterSummary > 0 &&","")
                        #        cut = cut.replace("&& metFilterSummary > 0","")
                        #        cut = cut.replace("triggerSummary > 0 &&","")
                        #        cut = cut.replace("genWeight*","")
                        #        cut = cut.replace("prefireWeight*","")
                        #        cut = cut.replace("weight*","")
                        #        cut = cut.replace("leptonFullSimScaleFactor1*","")
                        #        cut = cut.replace("leptonFullSimScaleFactor2*","")
                        #        cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
                        #        if runRange.era != "2018":
                        #                cut = "prefireWeight*"+cut
                        #        #~ cut = "genWeight*weight*("+cut+")"
                        #
                        #        counts[nLLRegion][getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path, blind)
                                
                        for MT2Region in MT2Regions:
                                for mllCut in massBins:
                                        cut = standardCut+" && (%s)"%getattr(theCuts.nLLCuts,nLLRegion).cut
                                        cut = cut + " && (%s)"%getattr(theCuts.mt2Cuts,MT2Region).cut
                                        cut = cut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
                                        cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
                                        #~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
                                        if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
                                                cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
                                        cut = cut.replace("p4.M()","mll")
                                        cut = cut.replace("p4.Pt()","pt")
                                        cut = cut.replace("metFilterSummary > 0 &&","")
                                        cut = cut.replace("&& metFilterSummary > 0","")
                                        cut = cut.replace("triggerSummary > 0 &&","")
                                        cut = cut.replace("genWeight*","")
                                        cut = cut.replace("prefireWeight*","")
                                        cut = cut.replace("weight*","")
                                        cut = cut.replace("leptonFullSimScaleFactor1*","")
                                        cut = cut.replace("leptonFullSimScaleFactor2*","")
                                        cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
                                        if runRange.era != "2018":
                                                cut = "prefireWeight*"+cut
                                        #~ cut = "genWeight*weight*("+cut+")"
                        
                                        counts[nLLRegion][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path, blind)

                        for MT2Region in MT2Regions:
                                for nBJetsRegion in nBJetsRegions:
                                        for mllCut in massBins:
                                                cut = standardCut+" && (%s)"%getattr(theCuts.nLLCuts,nLLRegion).cut
                                                cut = cut + " && (%s)"%getattr(theCuts.nBJetsCuts,nBJetsRegion).cut
                                                cut = cut + " && (%s)"%getattr(theCuts.mt2Cuts,MT2Region).cut
                                                cut = cut + " && (%s)"%getattr(theCuts.massCuts,mllCut).cut
                                                cut = cut + " && (met / caloMet < 5. && nBadMuonJets == 0)"
                                                #~ cut = cut + " && (met / caloMet > 5. && nBadMuonJets > 0)" ### Inverse bad muon cuts
                                                if not (mllCut == "highMassOld" or mllCut == "lowMassOld"):
                                                        cut = cut+" && (abs(deltaPhiJetMet1) > 0.4 && abs(deltaPhiJetMet2) > 0.4)"
                                                cut = cut.replace("p4.M()","mll")
                                                cut = cut.replace("p4.Pt()","pt")
                                                cut = cut.replace("metFilterSummary > 0 &&","")
                                                cut = cut.replace("&& metFilterSummary > 0","")
                                                cut = cut.replace("triggerSummary > 0 &&","")
                                                cut = cut.replace("genWeight*","")
                                                cut = cut.replace("prefireWeight*","")
                                                cut = cut.replace("weight*","")
                                                cut = cut.replace("leptonFullSimScaleFactor1*","")
                                                cut = cut.replace("leptonFullSimScaleFactor2*","")
                                                cut = "leptonFullSimScaleFactor1*leptonFullSimScaleFactor2*genWeight*weight*("+cut+")"
                                                if runRange.era != "2018":
                                                        cut = "prefireWeight*"+cut
                                                #~ cut = "genWeight*weight*("+cut+")"
                                
                                                counts[nLLRegion][getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.nBJetsCuts,nBJetsRegion).name+"_"+getattr(theCuts.massCuts,mllCut).name] = getCounts(trees, cut,isMC,backgrounds,plot,runRange,path, blind)

                return counts


def main():
        parser = argparse.ArgumentParser(description='produce cut & count event yields.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-B", "--blind", action="store_true", dest="blind", default=False,
                                                  help="Blind SR in data")
        parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
                                                  help="use MC, default is to use data.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
        parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
                                                  help="select dependencies to study, default is all.")
        parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
                                                  help="name of run range.")
        parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
                                                  help="backgrounds to plot.")  
        parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
                                                  help="write results to central repository")   

                                        
        args = parser.parse_args()



        if len(args.backgrounds) == 0:
                args.backgrounds = backgroundLists.default
        if len(args.plots) == 0:
                args.plots = plotLists.signal
        if len(args.selection) == 0:
                args.selection.append(regionsToUse.signal.inclusive.name)       
        if len(args.runRange) == 0:
                args.runRange.append(runRanges.name)    


        for runRangeName in args.runRange:
                runRange = getRunRange(runRangeName)
                path = locations[runRange.era].dataSetPathNLL
                for selectionName in args.selection:
                        
                        selection = getRegion(selectionName)
                        
                        
                        if args.write:

                                import subprocess

                                bashCommand = "cp shelves/cutAndCountNLL_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
                                process = subprocess.Popen(bashCommand.split())         
                        
                        else:
                                counts = cutAndCountForRegion(path,selection,args.plots,runRange,args.mc,args.backgrounds, args.blind)
                                outFile = open("shelves/cutAndCountNLL_%s_%s.pkl"%(selection.name,runRange.label),"w")
                                pickle.dump(counts, outFile)
                                outFile.close()
                        


                

main()

