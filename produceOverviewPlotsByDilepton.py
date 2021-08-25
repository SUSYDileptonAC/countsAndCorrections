import pickle
import os
import sys
import ctypes
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)
from setTDRStyle import setTDRStyle

from corrections import corrections
#from corrections import rSFOF,rSFOFDirect,rSFOFTrig, rEEOF, rMMOF, rOutIn
from centralConfig import zPredictions, regionsToUse, runRanges, OtherPredictions, OnlyZPredictions,systematics
from helpers import createMyColors
from defs import myColors,thePlots,getPlot,theCuts,getRunRange

import ratios

from array import array

import ROOT
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphErrors, TF1, gStyle, TGraphAsymmErrors, TFile, TH2F
# ROOT.gROOT.SetBatch(True)

def readPickle(name,regionName,runName,MC=False):
        
        if MC:
                if os.path.isfile("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName)):
                        result = pickle.load(open("shelves/%s_%s_%s_MC.pkl"%(name,regionName,runName),"rb"))
                else:
                        print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName)               
                        sys.exit()              
        else:
                if os.path.isfile("shelves/%s_%s_%s.pkl"%(name,regionName,runName)):
                        result = pickle.load(open("shelves/%s_%s_%s.pkl"%(name,regionName,runName),"rb"))
                else:
                        print "shelves/%s_%s_%s.pkl not found, exiting"%(name,regionName,runName)               
                        sys.exit()

        return result   
        
### load pickles for the systematics
def loadPickles(path):
        from glob import glob
        result = {}
        for pklPath in glob(path):
                pklFile = open(pklPath, "r")
                result.update(pickle.load(pklFile))
        return result

def getWeightedAverage(val1,err1,val2,err2):
        
        weightedAverage = (val1/(err1**2) +val2/(err2**2))/(1./err1**2+1./err2**2)
        weightedAverageErr = 1./(1./err1**2+1./err2**2)**0.5
        
        return weightedAverage, weightedAverageErr

tableHeaders = {"default":"being inclusive in the number of b-tagged jets","geOneBTags":"requiring at least one b-tagged jet","geTwoBTags":"requiring at least two b-tagged jets"}
tableColumnHeaders = {"default":"no b-tag requirement","noBTags":"veto on b-tagged jets","geOneBTags":"$\geq$ 1 b-tagged jets","geTwoBTags":"$\geq$ 2 b-tagged jets"}

                        
def getResultsNLL(shelves, signalRegion):
       
        NLLRegions = ["lowNLL","highNLL",]
        massRegions = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]       
        nBJetsRegions = [ "zeroBJets","oneOrMoreBJets",]
        MT2Regions = ["highMT2"]
        result = {}
        
        region = "inclusive"
        
        result["onZPrediction_highNLL_highMT2_zeroBJets_EE"]            = 66.3*0.28
        result["onZPrediction_highNLL_highMT2_zeroBJets_Err_EE"]        = 24.8*0.28
        result["onZPrediction_lowNLL_highMT2_zeroBJets_EE"]             = 66.3*0.72 
        result["onZPrediction_lowNLL_highMT2_zeroBJets_Err_EE"]         = 24.8*0.72 
        result["onZPrediction_highNLL_highMT2_zeroBJets_MM"]            = 82.2*0.28  
        result["onZPrediction_highNLL_highMT2_zeroBJets_Err_MM"]        = 30.4*0.28  
        result["onZPrediction_lowNLL_highMT2_zeroBJets_MM"]             = 82.2*0.72 
        result["onZPrediction_lowNLL_highMT2_zeroBJets_Err_MM"]         = 30.4*0.72 
        
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_EE"]       = 40.9*0.28
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err_EE"]   = 15.8*0.28
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_EE"]        = 40.9*0.72
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err_EE"]    = 15.8*0.72
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_MM"]       = 52.8*0.28
        result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err_MM"]   = 20.4*0.28
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_MM"]        = 52.8*0.72
        result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err_MM"]    = 20.4*0.72
        
        runRanges = shelves.keys()
        
        
        for selection in NLLRegions:
                result[selection] = {}
                for MT2Region in MT2Regions:
                        for nBJetsRegion in nBJetsRegions:
                                for massRegion in massRegions: 
                                        
                                        
                                        currentBin = getattr(theCuts.mt2Cuts,MT2Region).name+"_"+getattr(theCuts.nBJetsCuts,nBJetsRegion).name+"_"+getattr(theCuts.massCuts,massRegion).name
                                        resultsBinName = "%s_%s_%s"%(MT2Region,nBJetsRegion,massRegion)
                                        
                                        print resultsBinName
                                        print currentBin
                                        result[selection]["%s_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta_EE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt_MM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta_MM"%(resultsBinName)] = 0.0
                                        
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                                
                                                
                                                result[selection]["%s_EE"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"]
                                                result[selection]["%s_MM"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_OF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EM"]
                                                result[selection]["%s_OFRMuEScaled"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                result[selection]["%s_OFRMuEScaled_EE"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled_EE"]
                                                result[selection]["%s_OFRMuEScaled_MM"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled_MM"]
                                                
                                                
                                                runRange = getRunRange(runRangeName)
                                                RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                                                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.err

                                                rmuepred_EE = shelve[signalRegion][selection][currentBin]["EMRMuEScaled_EE"]
                                                OFRMuEScaledErrRT_EE = shelve[signalRegion][selection][currentBin]["EMRMuEScaled_EE"]*RTErr/RT
                                                OFRMuEScaledErrFlat_EE =  max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat_EE"]-rmuepred_EE), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat_EE"]-rmuepred_EE))
                                                OFRMuEScaledErrPt_EE = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpPt_EE"]-rmuepred_EE), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownPt_EE"]-rmuepred_EE))
                                                OFRMuEScaledErrEta_EE = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpEta_EE"]-rmuepred_EE), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownEta_EE"]-rmuepred_EE))
                                                # print rmuepred_EE, shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat_EE"], shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat_EE"]
                                                
                                                rmuepred_MM = shelve[signalRegion][selection][currentBin]["EMRMuEScaled_MM"]
                                                OFRMuEScaledErrRT_MM = shelve[signalRegion][selection][currentBin]["EMRMuEScaled_MM"]*RTErr/RT
                                                OFRMuEScaledErrFlat_MM = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat_MM"]-rmuepred_MM), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat_MM"]-rmuepred_MM))
                                                OFRMuEScaledErrPt_MM = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpPt_MM"]-rmuepred_MM), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownPt_MM"]-rmuepred_MM))
                                                OFRMuEScaledErrEta_MM = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpEta_MM"]-rmuepred_MM), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownEta_MM"]-rmuepred_MM))
                                                
                                                result[selection]["%s_OFRMuEScaledErrRT_EE"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrRT_EE"%(resultsBinName)] + OFRMuEScaledErrRT_EE**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrFlat_EE"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrFlat_EE"%(resultsBinName)]**2 + OFRMuEScaledErrFlat_EE**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrPt_EE"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrPt_EE"%(resultsBinName)]**2 + OFRMuEScaledErrPt_EE**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrEta_EE"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrEta_EE"%(resultsBinName)]**2 + OFRMuEScaledErrEta_EE**2)**0.5
                                        
                                                result[selection]["%s_OFRMuEScaledErrRT_MM"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrRT_MM"%(resultsBinName)] + OFRMuEScaledErrRT_MM**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrFlat_MM"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrFlat_MM"%(resultsBinName)]**2 + OFRMuEScaledErrFlat_MM**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrPt_MM"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrPt_MM"%(resultsBinName)]**2 + OFRMuEScaledErrPt_MM**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrEta_MM"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrEta_MM"%(resultsBinName)]**2 + OFRMuEScaledErrEta_MM**2)**0.5
                                        
                                        shelve=None # safety so it is not used outside the loop
                                        
                                        yield_up = ROOT.Double(1.0)
                                        yield_down = ROOT.Double(1.0)
                                
                                        
                                        ## calculate poisson error for FS prediction
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_OF"%(resultsBinName)]),yield_down,yield_up,1.)
                                        
                                        ## calculate poisson error for observed data
                                        yieldEE_up = ROOT.Double(1.0)
                                        yieldEE_down = ROOT.Double(1.0)
                                        yieldMM_up = ROOT.Double(1.0)
                                        yieldMM_down = ROOT.Double(1.0)
                                        
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_EE"%(resultsBinName)]),yieldEE_down,yieldEE_up,1.)
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_MM"%(resultsBinName)]),yieldMM_down,yieldMM_up,1.)
                                        
                                        result[selection]["%s_EEUp"%(resultsBinName)] = yieldEE_up - result[selection]["%s_EE"%(resultsBinName)]
                                        result[selection]["%s_EEDown"%(resultsBinName)] = result[selection]["%s_EE"%(resultsBinName)] - yieldEE_down
                                        
                                        result[selection]["%s_MMUp"%(resultsBinName)] = yieldMM_up - result[selection]["%s_MM"%(resultsBinName)]
                                        result[selection]["%s_MMDown"%(resultsBinName)] = result[selection]["%s_MM"%(resultsBinName)] - yieldMM_down
                                        
                                        # fs backgrounds
                                        
                                        result[selection]["%s_PredFactEE"%(resultsBinName)] = result[selection]["%s_OFRMuEScaled_EE"%(resultsBinName)]
                                        result[selection]["%s_PredFactMM"%(resultsBinName)] = result[selection]["%s_OFRMuEScaled_MM"%(resultsBinName)]
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                        
                                                eff_reeof = result[selection]["%s_PredFactEE"%(resultsBinName)]/result[selection]["%s_OF"%(resultsBinName)]
                                                eff_rmmof = result[selection]["%s_PredFactMM"%(resultsBinName)]/result[selection]["%s_OF"%(resultsBinName)]
                                        
                                                result[selection]["%s_PredFactStatUpEE"%(resultsBinName)] = yield_up*eff_reeof - result[selection]["%s_PredFactEE"%(resultsBinName)]
                                                result[selection]["%s_PredFactStatUpMM"%(resultsBinName)] = yield_up*eff_rmmof - result[selection]["%s_PredFactMM"%(resultsBinName)]
                                        
                                                result[selection]["%s_PredFactStatDownEE"%(resultsBinName)] = result[selection]["%s_PredFactEE"%(resultsBinName)] - yield_down*eff_reeof
                                                result[selection]["%s_PredFactStatDownMM"%(resultsBinName)] = result[selection]["%s_PredFactMM"%(resultsBinName)] - yield_down*eff_rmmof
                                                systErrFact_EE = (result[selection]["%s_OFRMuEScaledErrRT_EE"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrFlat_EE"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrPt_EE"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrEta_EE"%(resultsBinName)]**2)**0.5
                                                systErrFact_MM = (result[selection]["%s_OFRMuEScaledErrRT_MM"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrFlat_MM"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrPt_MM"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrEta_MM"%(resultsBinName)]**2)**0.5
                                                
                                                result[selection]["%s_PredFactSystErrEE"%(resultsBinName)] = systErrFact_EE
                                                result[selection]["%s_PredFactSystErrMM"%(resultsBinName)] = systErrFact_MM
                                        else:
                                                result[selection]["%s_PredFactStatUpEE"%(resultsBinName)] = 1.8*0.4
                                                result[selection]["%s_PredFactStatDownEE"%(resultsBinName)] = yield_down
                                                result[selection]["%s_PredFactSystErrEE"%(resultsBinName)] = 0
                                                result[selection]["%s_PredFactStatUpMM"%(resultsBinName)] = 1.8*0.6
                                                result[selection]["%s_PredFactStatDownMM"%(resultsBinName)] = yield_down
                                                result[selection]["%s_PredFactSystErrMM"%(resultsBinName)] = 0
                                        
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                result[selection]["%s_REEOF_Fact"%(resultsBinName)] = result[selection]["%s_PredFactEE"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                result[selection]["%s_REEOF_Fact_Err"%(resultsBinName)] = result[selection]["%s_PredFactSystErrEE"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                
                                                result[selection]["%s_RMMOF_Fact"%(resultsBinName)] = result[selection]["%s_PredFactMM"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                result[selection]["%s_RMMOF_Fact_Err"%(resultsBinName)] = result[selection]["%s_PredFactSystErrMM"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                
                                                
                                        else:
                                                result[selection]["%s_REEOF_Fact"%(resultsBinName)] = 0.
                                                result[selection]["%s_REEOF_Fact_Err"%(resultsBinName)] = 0.
                                                result[selection]["%s_RMMOF_Fact"%(resultsBinName)] = 0.
                                                result[selection]["%s_RMMOF_Fact_Err"%(resultsBinName)] = 0.
                                        
                                        result[selection]["%s_PredEE"%(resultsBinName)] = result[selection]["%s_PredFactEE"%(resultsBinName)]
                                        result[selection]["%s_PredMM"%(resultsBinName)] = result[selection]["%s_PredFactMM"%(resultsBinName)]
      
                                        if result[selection]["%s_PredEE"%(resultsBinName)] > 0:
                                                result[selection]["%s_PredStatUpEE"%(resultsBinName)] = result[selection]["%s_PredFactStatUpEE"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_PredStatUpEE"%(resultsBinName)] = 1.8
                                                
                                        if result[selection]["%s_PredMM"%(resultsBinName)] > 0:
                                                result[selection]["%s_PredStatUpMM"%(resultsBinName)] = result[selection]["%s_PredFactStatUpMM"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_PredStatUpMM"%(resultsBinName)] = 1.8
                                                
                                        result[selection]["%s_PredStatDownEE"%(resultsBinName)] = result[selection]["%s_PredFactStatDownEE"%(resultsBinName)] 
                                        result[selection]["%s_PredSystErrEE"%(resultsBinName)] = result[selection]["%s_PredFactSystErrEE"%(resultsBinName)]
                                        
                                        result[selection]["%s_PredStatDownMM"%(resultsBinName)] = result[selection]["%s_PredFactStatDownMM"%(resultsBinName)] 
                                        result[selection]["%s_PredSystErrMM"%(resultsBinName)] = result[selection]["%s_PredFactSystErrMM"%(resultsBinName)]
                                        
                                       
                                        # Drell-Yan
                                        rOutIn = corrections["Combined"].rOutIn
                                        onZPredName = "onZPrediction_%s_%s_%s"%(selection,MT2Region,nBJetsRegion)
                                        onZPredErrName = "onZPrediction_%s_%s_%s_Err"%(selection,MT2Region,nBJetsRegion)
                                        
                                        result[selection]["%s_ZPredEE"%(resultsBinName)] = result[onZPredName+"_EE"]*getattr(getattr(rOutIn,massRegion),region).val
                                        result[selection]["%s_ZPredErrEE"%(resultsBinName)] = ((result[onZPredName+"_EE"]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result[onZPredErrName+"_EE"] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5

                                        result[selection]["%s_ZPredMM"%(resultsBinName)] = result[onZPredName+"_MM"]*getattr(getattr(rOutIn,massRegion),region).val
                                        result[selection]["%s_ZPredErrMM"%(resultsBinName)] = ((result[onZPredName+"_MM"]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result[onZPredErrName+"_MM"] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5

                                        # ttz,wz,zz
                                        
                                        
                                        result[selection]["%s_RarePredEE"%(resultsBinName)] = 0.0
                                        result[selection]["%s_RarePredErrEE"%(resultsBinName)] = 0.0
                                        
                                        result[selection]["%s_RarePredMM"%(resultsBinName)] = 0.0
                                        result[selection]["%s_RarePredErrMM"%(resultsBinName)] = 0.0
                                        
                                        rarePredName ="%s_%s_%s_%s"%(massRegion,selection,MT2Region,nBJetsRegion)
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                           
                                                rarePred_EE = shelve["Rares"]["%s_EE"%(rarePredName)] - 0.4*shelve["Rares"]["%s_OF"%(rarePredName)]
                                                rareUp_EE = shelve["Rares"]["%s_EE_Up"%(rarePredName)] - 0.4*shelve["Rares"]["%s_OF_Up"%(rarePredName)]
                                                rareDown_EE = shelve["Rares"]["%s_EE_Down"%(rarePredName)] - 0.4*shelve["Rares"]["%s_OF_Down"%(rarePredName)]
                                                
                                                rarePred_MM = shelve["Rares"]["%s_MM"%(rarePredName)] - 0.6*shelve["Rares"]["%s_OF"%(rarePredName)]
                                                rareUp_MM = shelve["Rares"]["%s_MM_Up"%(rarePredName)] - 0.6*shelve["Rares"]["%s_OF_Up"%(rarePredName)]
                                                rareDown_MM = shelve["Rares"]["%s_MM_Down"%(rarePredName)] - 0.6*shelve["Rares"]["%s_OF_Down"%(rarePredName)]
                                                
                                               
                                                result[selection]["%s_RarePredEE"%(resultsBinName)] += rarePred_EE
                                                result[selection]["%s_RarePredMM"%(resultsBinName)] += rarePred_MM
                                                
                                                errRare_EE = max(abs(rareUp_EE-rarePred_EE), abs(rarePred_EE-rareDown_EE))
                                                errRare_MM = max(abs(rareUp_MM-rarePred_MM), abs(rarePred_MM-rareDown_MM))
                                                statErrRare_EE = shelve["Rares"]["%s_EE_Stat"%(rarePredName)]
                                                statErrRare_MM = shelve["Rares"]["%s_MM_Stat"%(rarePredName)]
                                                result[selection]["%s_RarePredErrEE"%(resultsBinName)] = (result[selection]["%s_RarePredErrEE"%(resultsBinName)]**2 + errRare_EE**2 + statErrRare_EE**2)**0.5
                                                result[selection]["%s_RarePredErrMM"%(resultsBinName)] = (result[selection]["%s_RarePredErrMM"%(resultsBinName)]**2 + errRare_MM**2 + statErrRare_MM**2)**0.5
                                                
                        


                                        result[selection]["%s_TotalPredEE"%(resultsBinName)] = result[selection]["%s_PredEE"%(resultsBinName)] + result[selection]["%s_ZPredEE"%(resultsBinName)] + result[selection]["%s_RarePredEE"%(resultsBinName)]
                                        result[selection]["%s_TotalPredErrUpEE"%(resultsBinName)]   = ( result[selection]["%s_PredStatUpEE"%(resultsBinName)]**2   +  result[selection]["%s_PredSystErrEE"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrEE"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrEE"%(resultsBinName)]**2)**0.5
                                        result[selection]["%s_TotalPredErrDownEE"%(resultsBinName)] = ( result[selection]["%s_PredStatDownEE"%(resultsBinName)]**2 +  result[selection]["%s_PredSystErrEE"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrEE"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrEE"%(resultsBinName)]**2)**0.5

                                        result[selection]["%s_TotalPredMM"%(resultsBinName)] = result[selection]["%s_PredMM"%(resultsBinName)] + result[selection]["%s_ZPredMM"%(resultsBinName)] + result[selection]["%s_RarePredMM"%(resultsBinName)]
                                        result[selection]["%s_TotalPredErrUpMM"%(resultsBinName)]   = ( result[selection]["%s_PredStatUpMM"%(resultsBinName)]**2   +  result[selection]["%s_PredSystErrMM"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrMM"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrMM"%(resultsBinName)]**2)**0.5
                                        result[selection]["%s_TotalPredErrDownMM"%(resultsBinName)] = ( result[selection]["%s_PredStatDownMM"%(resultsBinName)]**2 +  result[selection]["%s_PredSystErrMM"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrMM"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrMM"%(resultsBinName)]**2)**0.5

        return result
        

def makeOverviewPlot(shelves, nBJetsRegion, blind = False, ratio=True, dilepton="EE"):

        #from helpers import createMyColors
        from defs import myColors
        #colors = createMyColors()       

        ROOT.gROOT.SetBatch(True)
        resultsNLL = getResultsNLL(shelves,"NLL")
        
        hCanvas = TCanvas("hCanvas%s%s"%(ratio, nBJetsRegion), "Distribution", 1000,1000)
        
        if not ratio:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0,1,1)
                style=setTDRStyle()
                style.SetPadBottomMargin(0.28)
                style.SetPadLeftMargin(0.13)
                style.SetTitleYOffset(0.9)
                plotPad.UseCurrentStyle()
                plotPad.Draw()  
                plotPad.cd()
                plotPad.SetLogy()       
        else:
                plotPad = ROOT.TPad("plotPad","plotPad",0,0.5,1,1)
                ratioPad = ROOT.TPad("ratioPad","ratioPad",0,0.,1,0.5)
                style=setTDRStyle()
                style.SetPadBottomMargin(0.28)
                style.SetPadLeftMargin(0.13)
                style.SetTitleYOffset(0.9)
                plotPad.UseCurrentStyle()
                ratioPad.UseCurrentStyle()
                
                plotPad.SetBottomMargin(0)
                ratioPad.SetTopMargin(0)
                ratioPad.SetBottomMargin(0.5)
                
                
                plotPad.Draw()  
                ratioPad.Draw() 
                plotPad.cd() 
                plotPad.SetLogy()       
        
        
        
        histObs = ROOT.TH1F("histObs%s%s"%(ratio, nBJetsRegion),"histObs",14,0,14)
        
        histObs.UseCurrentStyle()
        histObs.SetMarkerColor(ROOT.kBlack)
        histObs.SetLineColor(ROOT.kBlack)
        histObs.SetMarkerStyle(20)
        
        
        histPred = ROOT.TH1F("histPred%s%s"%(ratio, nBJetsRegion),"histPred",14,0,14)
        histFlavSym = ROOT.TH1F("histFlavSym%s%s"%(ratio, nBJetsRegion),"histFlavSym",14,0,14)
        histDY = ROOT.TH1F("histDY%s%s"%(ratio, nBJetsRegion),"histDY",14,0,14)
        histRare = ROOT.TH1F("histRare%s%s"%(ratio, nBJetsRegion),"histRare",14,0,14)
        
        
        
        if not blind:
                histObs.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_%s"%(nBJetsRegion, dilepton)])     
                
                histObs.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_%s"%(nBJetsRegion, dilepton)])
                histObs.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_%s"%(nBJetsRegion, dilepton)])   
        else:
                for i in range(1, 15):
                        histObs.SetBinContent(i,-100)
        
        
        names = ["m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV"]
        
        if not ratio:
                for index, name in enumerate(names):
                
                        histObs.GetXaxis().SetBinLabel(index+1,name)
                
        histFlavSym.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_Pred%s"%(nBJetsRegion, dilepton)])     
        
        histFlavSym.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_Pred%s"%(nBJetsRegion, dilepton)])
        histFlavSym.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_Pred%s"%(nBJetsRegion, dilepton)])   

        histDY.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_ZPred%s"%(nBJetsRegion, dilepton)]) 
        
        histDY.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_ZPred%s"%(nBJetsRegion, dilepton)])
        histDY.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_ZPred%s"%(nBJetsRegion, dilepton)])       

        histRare.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_RarePred%s"%(nBJetsRegion, dilepton)])    
        
        histRare.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_RarePred%s"%(nBJetsRegion, dilepton)])
        histRare.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_RarePred%s"%(nBJetsRegion, dilepton)])  

        errGraph = ROOT.TGraphAsymmErrors()
        errGraphRatio = ROOT.TGraphAsymmErrors()
        graphObs = ROOT.TGraphAsymmErrors()
        
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                if ratio:
                        errGraphRatio.SetPoint(i,histFlavSym.GetBinCenter(i),1)
                

        graphObs.SetPointError(1,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_%sDown"%(nBJetsRegion, dilepton)],  resultsNLL["lowNLL"]["highMT2_%s_mass20To60_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(2,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_%sDown"%(nBJetsRegion, dilepton)],  resultsNLL["lowNLL"]["highMT2_%s_mass60To86_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(3,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_%sDown"%(nBJetsRegion, dilepton)], resultsNLL["lowNLL"]["highMT2_%s_mass96To150_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(4,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_%sDown"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(5,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_%sDown"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(6,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_%sDown"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(7,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass400_%sDown"%(nBJetsRegion, dilepton)],     resultsNLL["lowNLL"]["highMT2_%s_mass400_%sUp"%(nBJetsRegion, dilepton)])

        graphObs.SetPointError(8,0,0,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_%sDown"%(nBJetsRegion, dilepton)],   resultsNLL["highNLL"]["highMT2_%s_mass20To60_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(9,0,0,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_%sDown"%(nBJetsRegion, dilepton)],   resultsNLL["highNLL"]["highMT2_%s_mass60To86_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(10,0,0,resultsNLL["highNLL"]["highMT2_%s_mass96To150_%sDown"%(nBJetsRegion, dilepton)],  resultsNLL["highNLL"]["highMT2_%s_mass96To150_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(11,0,0,resultsNLL["highNLL"]["highMT2_%s_mass150To200_%sDown"%(nBJetsRegion, dilepton)], resultsNLL["highNLL"]["highMT2_%s_mass150To200_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(12,0,0,resultsNLL["highNLL"]["highMT2_%s_mass200To300_%sDown"%(nBJetsRegion, dilepton)], resultsNLL["highNLL"]["highMT2_%s_mass200To300_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(13,0,0,resultsNLL["highNLL"]["highMT2_%s_mass300To400_%sDown"%(nBJetsRegion, dilepton)], resultsNLL["highNLL"]["highMT2_%s_mass300To400_%sUp"%(nBJetsRegion, dilepton)])
        graphObs.SetPointError(14,0,0,resultsNLL["highNLL"]["highMT2_%s_mass400_%sDown"%(nBJetsRegion, dilepton)],      resultsNLL["highNLL"]["highMT2_%s_mass400_%sUp"%(nBJetsRegion, dilepton)])


        errGraph.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        
        errGraph.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])
        errGraph.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrDown%s"%(nBJetsRegion, dilepton)],resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrUp%s"%(nBJetsRegion, dilepton)])

        if ratio:
                errGraphRatio.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPred"+dilepton])
                errGraphRatio.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPred"+dilepton])
                errGraphRatio.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPred"+dilepton])
                errGraphRatio.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPred"+dilepton])
                errGraphRatio.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPred"+dilepton])
                errGraphRatio.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPred"+dilepton])
                errGraphRatio.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDown"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPred"+dilepton],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUp"+dilepton]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPred"+dilepton])
                
                errGraphRatio.SetPointError(8,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPred"+dilepton])
                errGraphRatio.SetPointError(9,0.5*histFlavSym.GetBinWidth(9),0.5*histFlavSym.GetBinWidth(9),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPred"+dilepton])
                errGraphRatio.SetPointError(10,0.5*histFlavSym.GetBinWidth(10),0.5*histFlavSym.GetBinWidth(10),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPred"+dilepton])
                errGraphRatio.SetPointError(11,0.5*histFlavSym.GetBinWidth(11),0.5*histFlavSym.GetBinWidth(11),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPred"+dilepton])
                errGraphRatio.SetPointError(12,0.5*histFlavSym.GetBinWidth(12),0.5*histFlavSym.GetBinWidth(12),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPred"+dilepton])
                errGraphRatio.SetPointError(13,0.5*histFlavSym.GetBinWidth(13),0.5*histFlavSym.GetBinWidth(13),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPred"+dilepton])
                errGraphRatio.SetPointError(14,0.5*histFlavSym.GetBinWidth(14),0.5*histFlavSym.GetBinWidth(14),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDown"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPred"+dilepton],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUp"+dilepton]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPred"+dilepton])
        
        

        errGraph.SetFillColor(ROOT.kGray+3)     
        errGraph.SetFillStyle(3244)     
        errGraphRatio.SetFillColor(ROOT.kGray+3)     
        errGraphRatio.SetFillStyle(3244)   
        #errGraph.SetLineStyle(3244)     
        histFlavSym.SetLineColor(ROOT.kBlack)
        histFlavSym.SetFillColor(17)    
        histDY.SetFillColor(ROOT.kGreen+2)  
        histRare.SetFillColor(38)
        histDY.SetLineColor(ROOT.kBlack)
        histRare.SetLineColor(ROOT.kBlack)
        from ROOT import THStack
        
        stack = THStack()
        stack.Add(histDY)       
        stack.Add(histRare)     
        stack.Add(histFlavSym)  
        
        histObs.GetYaxis().SetRangeUser(0.5,2000000)
        histObs.GetYaxis().SetTitle("Events")
        histObs.SetTitleOffset(0.7, "Y")
        histObs.GetYaxis().SetTitleSize(0.07)
        if ratio:
                histObs.GetXaxis().SetLabelSize(0)
        #histObs.LabelsOption("v")
        
        
   
        histObs.Draw("pe")

        
        
        #~ hCanvas.DrawFrame(-0.5,0,30.5,65,"; %s ; %s" %("","Events"))
        
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(0.04)
        latex.SetNDC(True)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        #latexCMS.SetTextAlign(31)
        latexCMS.SetTextSize(0.06)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        #latexCMSExtra.SetTextAlign(31)
        latexCMSExtra.SetTextSize(0.045)
        latexCMSExtra.SetNDC(True)              
        


        intlumi = ROOT.TLatex()
        intlumi.SetTextAlign(12)
        intlumi.SetTextSize(0.03)
        intlumi.SetNDC(True)            

        latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"137")
        
        cmsExtra = "Preliminary"
        #cmsExtra = ""
        latexCMS.DrawLatex(0.17,0.88,"CMS")
        if "Simulation" in cmsExtra:
                yLabelPos = 0.81        
        else:
                yLabelPos = 0.84        

        #latexCMSExtra.DrawLatex(0.17,yLabelPos,"%s"%(cmsExtra))
        leg = ROOT.TLegend(0.37, 0.7, 0.93, 0.93,"","brNDC")
        leg.SetNColumns(3)
        leg.SetFillColor(10)
        leg.SetLineColor(10)
        leg.SetShadowColor(0)
        leg.SetBorderSize(1)
        leg.SetTextSize(0.052)
        
        bkgHistForLegend = histFlavSym.Clone("bkgHistForLegend")
        bkgHistForLegend.SetLineColor(ROOT.kBlack)
        bkgHistForLegend.SetFillColor(17)
        bkgHistForLegend.SetLineWidth(1)
        
        obsGraph = ROOT.TGraphAsymmErrors()
        leg.AddEntry(obsGraph,"Data","pe")
        leg.AddEntry(histDY,"DY+jets", "f")
        #~ leg.AddEntry(histFlavSym, "Total backgrounds","l")
        leg.AddEntry(bkgHistForLegend, "Flavor-symmetric","f")
        leg.AddEntry(errGraph,"Tot. unc.", "f") 
        leg.AddEntry(histRare,"Z+#nu", "f")
        
        stack.Draw("samehist")  
        errGraph.Draw("same02")
        
  
        graphObs.Draw("pesame")
        
        leg.Draw("same")

        
        
        line1 = ROOT.TLine(7,0,7,500)
        line1.SetLineColor(ROOT.kBlack)
        line1.SetLineWidth(2)
        line1.Draw("same")


        label = ROOT.TLatex()
        label.SetTextAlign(12)
        label.SetTextSize(0.06)
        label.SetTextColor(ROOT.kBlack) 
        label.SetTextAlign(22)  
        #~ label.SetTextAngle(-45)      
        
        label.DrawLatex(3.5,2000,"t#bar{t}-like")
        label.DrawLatex(10.5,2000,"non-t#bar{t}-like")
        
        label.SetNDC(True)
        label.SetTextAlign(32) 
        if nBJetsRegion == "oneOrMoreBJets":
                label.DrawLatex(0.9,0.67,"n_{b} #geq 1")
        else:
                label.DrawLatex(0.9,0.67,"n_{b} = 0")
        label.DrawLatex(0.9,0.55,dilepton)
        
        plotPad.RedrawAxis()
        
        # ratios
        if ratio:
                ratioPad.cd()

                xs = []
                ys = []
                yErrorsUp = []
                yErrorsDown = []
                widths = []
                
                for i in range(0,histObs.GetNbinsX()+1):
                        xs.append(histObs.GetBinCenter(i))
                        widths.append(0.5*histObs.GetBinWidth(i)) 
                        predI = histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i)              
                        if predI > 0:
                                ys.append(histObs.GetBinContent(i)/predI)
                                yErrorsUp.append(graphObs.GetErrorYhigh(i)/predI)                 
                                yErrorsDown.append(graphObs.GetErrorYlow(i)/predI)                                
                        else:
                                ys.append(10.)
                                yErrorsUp.append(0)                     
                                yErrorsDown.append(0)
                
                ratioPad.cd()

                        # axis
                nBinsX = 14
                nBinsY = 10
                hAxis = ROOT.TH2F("hAxis", "", nBinsX, 0, 14, nBinsY, 0, 2.2)
                hAxis.Draw("AXIS")
                
                
                hAxis.GetXaxis().SetLabelSize(0.1)

                for index, name in enumerate(names):
                        hAxis.GetXaxis().SetBinLabel(index+1,name)   
                        hAxis.GetXaxis().ChangeLabel(index+1,270)   
                
                hAxis.GetYaxis().CenterTitle()
                hAxis.GetYaxis().SetNdivisions(408)
                hAxis.SetTitleOffset(0.7, "Y")
                #hAxis.SetTitleSize(0.08, "Y")
                hAxis.GetYaxis().SetTitleSize(0.07)
                hAxis.GetYaxis().SetTitle("#frac{Data}{Prediction}    ")
                hAxis.GetYaxis().SetLabelSize(0.05)

                oneLine = ROOT.TLine(0, 1.0, 14, 1.0)
                #~ oneLine.SetLineStyle(2)
                oneLine.Draw()
                oneLine2 = ROOT.TLine(0, 0.5, 14, 0.5)
                oneLine2.SetLineStyle(2)
                oneLine2.Draw()
                oneLine3 = ROOT.TLine(0, 1.5, 14, 1.5)
                oneLine3.SetLineStyle(2)
                oneLine3.Draw()
                
                errGraphRatio.Draw("same02")
                
                ratioGraph = ROOT.TGraphAsymmErrors(len(xs), array("d", xs), array("d", ys), array("d", widths), array("d", widths), array("d", yErrorsDown), array("d", yErrorsUp))
                        
                ratioGraph.Draw("same pe0")     
                
                line2 = ROOT.TLine(7,0,7,2.2)
                line2.SetLineColor(ROOT.kBlack)
                line2.SetLineWidth(2)
                line2.Draw("same")

        
                ROOT.gPad.RedrawAxis()
                plotPad.RedrawAxis()
                ratioPad.RedrawAxis()
        
        

        hCanvas.Print("edgeOverview_%s_%s.pdf"%(nBJetsRegion, dilepton))
        ROOT.gROOT.SetBatch(False)
        ROOT.gROOT.Clear()
        #~ hCanvas.Print("edgeOverview.root")
       
                

        
def main():
        
        #OnZPickleICHEP = loadPickles("shelves/OnZBG_ICHEPLegacy_36fb.pkl")
        #RaresPickle8TeVLegacy = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        RaresPickle2016 = loadPickles("shelves/RareOnZBG_Run2016_36fb.pkl")
        RaresPickle2017 = loadPickles("shelves/RareOnZBG_Run2017_42fb.pkl")
        RaresPickle2018 = loadPickles("shelves/RareOnZBG_Run2018_60fb.pkl")
        #RaresPickle = loadPickles("shelves/RareOnZBG_8TeVLegacy_36fb.pkl")
        
        
        name = "cutAndCount"
        countingShelves2016= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2016_36fb"),"Rares":RaresPickle2016}      
        countingShelves2017= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2017_42fb"),"Rares":RaresPickle2017}      
        countingShelves2018= {"NLL":readPickle("cutAndCountNLL",regionsToUse.signal.inclusive.name , "Run2018_60fb"),"Rares":RaresPickle2018}      
        
        countingShelves = {"Run2016_36fb": countingShelves2016,"Run2017_42fb": countingShelves2017,"Run2018_60fb": countingShelves2018}
        

        makeOverviewPlot(countingShelves, "zeroBJets", ratio=True)
        makeOverviewPlot(countingShelves, "oneOrMoreBJets", ratio=True)
        
        makeOverviewPlot(countingShelves, "zeroBJets", ratio=True, dilepton="MM")
        makeOverviewPlot(countingShelves, "oneOrMoreBJets", ratio=True, dilepton="MM")
        
main()
