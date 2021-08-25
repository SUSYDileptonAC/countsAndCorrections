import pickle
import os
import sys
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
        
        runRanges = shelves.keys()
        runRange = runRanges[0]
        
        if "2016" in runRange:
                result["onZPrediction_lowNLL_highMT2_zeroBJets"]                = 28.9*0.72 
                result["onZPrediction_lowNLL_highMT2_zeroBJets_Err"]            = 10.1*0.72
                result["onZPrediction_highNLL_highMT2_zeroBJets"]               = 28.9*0.28
                result["onZPrediction_highNLL_highMT2_zeroBJets_Err"]           = 10.1*0.28
                
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets"]           = 12.5*0.72
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err"]       = 4.75*0.72
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets"]          = 12.5*0.28
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err"]      = 4.75*0.28
                
        if "2017" in runRange:
                result["onZPrediction_lowNLL_highMT2_zeroBJets"]                = 71.5*0.72
                result["onZPrediction_lowNLL_highMT2_zeroBJets_Err"]            = 26.7*0.72
                result["onZPrediction_highNLL_highMT2_zeroBJets"]               = 71.5*0.28
                result["onZPrediction_highNLL_highMT2_zeroBJets_Err"]           = 26.7*0.28
                
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets"]           = 42.8*0.72
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err"]       = 17.0*0.72
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets"]          = 42.8*0.28
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err"]      = 17.0*0.28
                
        if "2018" in runRange:
                result["onZPrediction_lowNLL_highMT2_zeroBJets"]                = 64.4*0.72
                result["onZPrediction_lowNLL_highMT2_zeroBJets_Err"]            = 23.7*0.72
                result["onZPrediction_highNLL_highMT2_zeroBJets"]               = 64.4*0.28
                result["onZPrediction_highNLL_highMT2_zeroBJets_Err"]           = 23.7*0.28
                
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets"]           = 45.6*0.72
                result["onZPrediction_lowNLL_highMT2_oneOrMoreBJets_Err"]       = 19.2*0.72
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets"]          = 45.6*0.28
                result["onZPrediction_highNLL_highMT2_oneOrMoreBJets_Err"]      = 19.2*0.28
                
        
        
        
        
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
                                        result[selection]["%s_SF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaled"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = 0.0
                                        result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = 0.0
                                        
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                                
                                                
                                                result[selection]["%s_EE"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"]
                                                result[selection]["%s_MM"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_SF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EE"] + shelve[signalRegion][selection][currentBin]["MM"]
                                                result[selection]["%s_OF"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EM"]
                                                result[selection]["%s_OFRMuEScaled"%(resultsBinName)] += shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                
                                                
                                                runRange = getRunRange(runRangeName)
                                                RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                                                RTErr = corrections[runRange.era].rSFOFTrig.inclusive.err

                                                rmuepred = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]
                                                OFRMuEScaledErrRT = shelve[signalRegion][selection][currentBin]["EMRMuEScaled"]*RTErr/RT
                                                OFRMuEScaledErrFlat = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpFlat"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownFlat"]-rmuepred))
                                                OFRMuEScaledErrPt = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpPt"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownPt"]-rmuepred))
                                                OFRMuEScaledErrEta = max(abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledUpEta"]-rmuepred), abs(shelve[signalRegion][selection][currentBin]["EMRMuEScaledDownEta"]-rmuepred))
                                                
                                                result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)] + OFRMuEScaledErrRT**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + OFRMuEScaledErrFlat**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + OFRMuEScaledErrPt**2)**0.5
                                                result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)] = (result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2 + OFRMuEScaledErrEta**2)**0.5
                                        
                                        shelve=None # safety so it is not used outside the loop
                                        
                                        yield_up = ROOT.Double(1.)
                                        yield_down = ROOT.Double(1.)
                                
                                        
                                        ## calculate poisson error for FS prediction
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_OF"%(resultsBinName)]),yield_down,yield_up,1.)
                                        
                                        ## calculate poisson error for observed data
                                        yieldSF_up = ROOT.Double(1.)
                                        yieldSF_down = ROOT.Double(1.)
                                        ROOT.RooHistError.instance().getPoissonInterval(int(result[selection]["%s_SF"%(resultsBinName)]),yieldSF_down,yieldSF_up,1.)
                                        result[selection]["%s_SFUp"%(resultsBinName)] = yieldSF_up - result[selection]["%s_SF"%(resultsBinName)]
                                        result[selection]["%s_SFDown"%(resultsBinName)] = result[selection]["%s_SF"%(resultsBinName)] - yieldSF_down
                                        
                                        # fs backgrounds
                                        result[selection]["%s_PredFactSF"%(resultsBinName)] = result[selection]["%s_OFRMuEScaled"%(resultsBinName)]
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                eff_rsfof = result[selection]["%s_PredFactSF"%(resultsBinName)]/result[selection]["%s_OF"%(resultsBinName)]
                                                
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = yield_up*eff_rsfof - result[selection]["%s_PredFactSF"%(resultsBinName)]
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] - yield_down*eff_rsfof
                                                systErrFact = (result[selection]["%s_OFRMuEScaledErrRT"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrFlat"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrPt"%(resultsBinName)]**2 + result[selection]["%s_OFRMuEScaledErrEta"%(resultsBinName)]**2)**0.5
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = systErrFact
                                        else:
                                                result[selection]["%s_PredFactStatUpSF"%(resultsBinName)] = 1.8
                                                result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] = yield_down
                                                result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] = 0
                                        
                                        if result[selection]["%s_OF"%(resultsBinName)] > 0:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)] / result[selection]["%s_OF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_RSFOF_Fact"%(resultsBinName)] = 0.
                                                result[selection]["%s_RSFOF_Fact_Err"%(resultsBinName)] = 0.
                                        
                                        result[selection]["%s_PredSF"%(resultsBinName)] = result[selection]["%s_PredFactSF"%(resultsBinName)]
                                        if result[selection]["%s_PredSF"%(resultsBinName)] > 0:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = result[selection]["%s_PredFactStatUpSF"%(resultsBinName)]
                                        else:
                                                result[selection]["%s_PredStatUpSF"%(resultsBinName)] = 1.8
                                                
                                        result[selection]["%s_PredStatDownSF"%(resultsBinName)] = result[selection]["%s_PredFactStatDownSF"%(resultsBinName)] 
                                        result[selection]["%s_PredSystErrSF"%(resultsBinName)] = result[selection]["%s_PredFactSystErrSF"%(resultsBinName)]
                                        
                                        
                                        # Drell-Yan
                                        rOutIn = corrections["Combined"].rOutIn
                                        onZPredName = "onZPrediction_%s_%s_%s"%(selection,MT2Region,nBJetsRegion)
                                        onZPredErrName = "onZPrediction_%s_%s_%s_Err"%(selection,MT2Region,nBJetsRegion)
                                        
                                        result[selection]["%s_ZPredSF"%(resultsBinName)] = result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).val
                                        result[selection]["%s_ZPredErrSF"%(resultsBinName)] = ((result[onZPredName]*getattr(getattr(rOutIn,massRegion),region).err)**2 + (result[onZPredErrName] * getattr(getattr(rOutIn,massRegion),region).val)**2 )**0.5

                                        # ttz,wz,zz
                                        
                                        
                                        result[selection]["%s_RarePredSF"%(resultsBinName)] = 0.0
                                        result[selection]["%s_RarePredErrSF"%(resultsBinName)] = 0.0
                                        
                                        rarePredName ="%s_%s_%s_%s"%(massRegion,selection,MT2Region,nBJetsRegion)
                                        
                                        for runRangeName in runRanges:
                                                shelve = shelves[runRangeName]
                                        
                                                rarePred = shelve["Rares"]["%s_SF"%(rarePredName)] - shelve["Rares"]["%s_OF"%(rarePredName)]
                                                rareUp = shelve["Rares"]["%s_SF_Up"%(rarePredName)] - shelve["Rares"]["%s_OF_Up"%(rarePredName)]
                                                rareDown = shelve["Rares"]["%s_SF_Down"%(rarePredName)] - shelve["Rares"]["%s_OF_Down"%(rarePredName)]
                                                
                                                result[selection]["%s_RarePredSF"%(resultsBinName)] += rarePred
                                                
                                                errRare = max(abs(rareUp-rarePred), abs(rarePred-rareDown))
                                                statErrRare = shelve["Rares"]["%s_SF_Stat"%(rarePredName)]
                                                result[selection]["%s_RarePredErrSF"%(resultsBinName)] = (result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2 + errRare**2 + statErrRare**2)**0.5
                                                
                        

                                        result[selection]["%s_TotalPredSF"%(resultsBinName)] = result[selection]["%s_PredSF"%(resultsBinName)] + result[selection]["%s_ZPredSF"%(resultsBinName)] + result[selection]["%s_RarePredSF"%(resultsBinName)]
                                        result[selection]["%s_TotalPredErrUpSF"%(resultsBinName)]   = ( result[selection]["%s_PredStatUpSF"%(resultsBinName)]**2   +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5
                                        result[selection]["%s_TotalPredErrDownSF"%(resultsBinName)] = ( result[selection]["%s_PredStatDownSF"%(resultsBinName)]**2 +  result[selection]["%s_PredSystErrSF"%(resultsBinName)]**2 + result[selection]["%s_ZPredErrSF"%(resultsBinName)]**2 + result[selection]["%s_RarePredErrSF"%(resultsBinName)]**2)**0.5

        return result
        

        
def makeOverviewPlot(shelves, nBJetsRegion, blind = False, ratio=True, lumi=""):

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
                histObs.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SF"%nBJetsRegion])
                histObs.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SF"%nBJetsRegion])
                histObs.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SF"%nBJetsRegion])
                histObs.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SF"%nBJetsRegion])
                histObs.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SF"%nBJetsRegion])
                histObs.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SF"%nBJetsRegion])
                histObs.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_SF"%nBJetsRegion])     
                
                histObs.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_SF"%nBJetsRegion])
                histObs.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_SF"%nBJetsRegion])
                histObs.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_SF"%nBJetsRegion])
                histObs.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_SF"%nBJetsRegion])
                histObs.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_SF"%nBJetsRegion])
                histObs.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_SF"%nBJetsRegion])
                histObs.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_SF"%nBJetsRegion])   
        else:
                for i in range(1, 15):
                        histObs.SetBinContent(i,-100)
        
        
        names = ["m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV","m_{ll}: 20-60 GeV","m_{ll}: 60-86 GeV","m_{ll}: 96-150 GeV","m_{ll}: 150-200 GeV","m_{ll}: 200-300 GeV","m_{ll}: 300-400 GeV","m_{ll}: > 400 GeV"]
        
        if not ratio:
                for index, name in enumerate(names):
                
                        histObs.GetXaxis().SetBinLabel(index+1,name)
                
        histFlavSym.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_PredSF"%nBJetsRegion])     
        
        histFlavSym.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_PredSF"%nBJetsRegion])
        histFlavSym.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_PredSF"%nBJetsRegion])   

        histDY.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_ZPredSF"%nBJetsRegion]) 
        
        histDY.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_ZPredSF"%nBJetsRegion])
        histDY.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_ZPredSF"%nBJetsRegion])       

        histRare.SetBinContent(1,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(2,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(3,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(4,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(6,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(7,resultsNLL["lowNLL"]["highMT2_%s_mass400_RarePredSF"%nBJetsRegion])    
        
        histRare.SetBinContent(8,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(9,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(10,resultsNLL["highNLL"]["highMT2_%s_mass96To150_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(11,resultsNLL["highNLL"]["highMT2_%s_mass150To200_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(12,resultsNLL["highNLL"]["highMT2_%s_mass200To300_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(13,resultsNLL["highNLL"]["highMT2_%s_mass300To400_RarePredSF"%nBJetsRegion])
        histRare.SetBinContent(14,resultsNLL["highNLL"]["highMT2_%s_mass400_RarePredSF"%nBJetsRegion])  

        errGraph = ROOT.TGraphAsymmErrors()
        errGraphRatio = ROOT.TGraphAsymmErrors()
        graphObs = ROOT.TGraphAsymmErrors()
        
        
        for i in range(1,histFlavSym.GetNbinsX()+1):
                graphObs.SetPoint(i,histObs.GetBinCenter(i),histObs.GetBinContent(i))
                errGraph.SetPoint(i,i-0.5,histFlavSym.GetBinContent(i)+histDY.GetBinContent(i)+histRare.GetBinContent(i))
                if ratio:
                        errGraphRatio.SetPoint(i,histFlavSym.GetBinCenter(i),1)
                

        graphObs.SetPointError(1,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SFDown"%nBJetsRegion],  resultsNLL["lowNLL"]["highMT2_%s_mass20To60_SFUp"%nBJetsRegion])
        graphObs.SetPointError(2,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SFDown"%nBJetsRegion],  resultsNLL["lowNLL"]["highMT2_%s_mass60To86_SFUp"%nBJetsRegion])
        graphObs.SetPointError(3,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SFDown"%nBJetsRegion], resultsNLL["lowNLL"]["highMT2_%s_mass96To150_SFUp"%nBJetsRegion])
        graphObs.SetPointError(4,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_SFUp"%nBJetsRegion])
        graphObs.SetPointError(5,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_SFUp"%nBJetsRegion])
        graphObs.SetPointError(6,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SFDown"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_SFUp"%nBJetsRegion])
        graphObs.SetPointError(7,0,0,resultsNLL["lowNLL"]["highMT2_%s_mass400_SFDown"%nBJetsRegion],     resultsNLL["lowNLL"]["highMT2_%s_mass400_SFUp"%nBJetsRegion])

        graphObs.SetPointError(8,0,0,resultsNLL["highNLL"] ["highMT2_%s_mass20To60_SFDown"%nBJetsRegion],   resultsNLL["highNLL"]["highMT2_%s_mass20To60_SFUp"%nBJetsRegion])
        graphObs.SetPointError(9,0,0,resultsNLL["highNLL"] ["highMT2_%s_mass60To86_SFDown"%nBJetsRegion],   resultsNLL["highNLL"]["highMT2_%s_mass60To86_SFUp"%nBJetsRegion])
        graphObs.SetPointError(10,0,0,resultsNLL["highNLL"]["highMT2_%s_mass96To150_SFDown"%nBJetsRegion],  resultsNLL["highNLL"]["highMT2_%s_mass96To150_SFUp"%nBJetsRegion])
        graphObs.SetPointError(11,0,0,resultsNLL["highNLL"]["highMT2_%s_mass150To200_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass150To200_SFUp"%nBJetsRegion])
        graphObs.SetPointError(12,0,0,resultsNLL["highNLL"]["highMT2_%s_mass200To300_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass200To300_SFUp"%nBJetsRegion])
        graphObs.SetPointError(13,0,0,resultsNLL["highNLL"]["highMT2_%s_mass300To400_SFDown"%nBJetsRegion], resultsNLL["highNLL"]["highMT2_%s_mass300To400_SFUp"%nBJetsRegion])
        graphObs.SetPointError(14,0,0,resultsNLL["highNLL"]["highMT2_%s_mass400_SFDown"%nBJetsRegion],      resultsNLL["highNLL"]["highMT2_%s_mass400_SFUp"%nBJetsRegion])


        errGraph.SetPointError(1,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass20To60_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(2,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass60To86_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(3,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass96To150_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(4,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass150To200_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(5,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass200To300_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(6,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass300To400_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(7,0.5,0.5,resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["lowNLL"]["highMT2_%s_mass400_TotalPredErrUpSF"%nBJetsRegion])
        
        errGraph.SetPointError(8,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass20To60_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(9,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass60To86_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(10,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass96To150_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(11,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass150To200_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(12,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass200To300_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(13,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass300To400_TotalPredErrUpSF"%nBJetsRegion])
        errGraph.SetPointError(14,0.5,0.5,resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrDownSF"%nBJetsRegion],resultsNLL["highNLL"]["highMT2_%s_mass400_TotalPredErrUpSF"%nBJetsRegion])

        if ratio:
                errGraphRatio.SetPointError(1,0.5*histFlavSym.GetBinWidth(1),0.5*histFlavSym.GetBinWidth(1),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"])
                errGraphRatio.SetPointError(2,0.5*histFlavSym.GetBinWidth(2),0.5*histFlavSym.GetBinWidth(2),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"])
                errGraphRatio.SetPointError(3,0.5*histFlavSym.GetBinWidth(4),0.5*histFlavSym.GetBinWidth(4),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"])
                errGraphRatio.SetPointError(4,0.5*histFlavSym.GetBinWidth(5),0.5*histFlavSym.GetBinWidth(5),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"])
                errGraphRatio.SetPointError(5,0.5*histFlavSym.GetBinWidth(6),0.5*histFlavSym.GetBinWidth(6),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"])
                errGraphRatio.SetPointError(6,0.5*histFlavSym.GetBinWidth(7),0.5*histFlavSym.GetBinWidth(7),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"])
                errGraphRatio.SetPointError(7,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"],resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"]/resultsNLL["lowNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"])
                
                errGraphRatio.SetPointError(8,0.5*histFlavSym.GetBinWidth(8),0.5*histFlavSym.GetBinWidth(8),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass20To60_TotalPredSF"])
                errGraphRatio.SetPointError(9,0.5*histFlavSym.GetBinWidth(9),0.5*histFlavSym.GetBinWidth(9),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass60To86_TotalPredSF"])
                errGraphRatio.SetPointError(10,0.5*histFlavSym.GetBinWidth(10),0.5*histFlavSym.GetBinWidth(10),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass96To150_TotalPredSF"])
                errGraphRatio.SetPointError(11,0.5*histFlavSym.GetBinWidth(11),0.5*histFlavSym.GetBinWidth(11),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass150To200_TotalPredSF"])
                errGraphRatio.SetPointError(12,0.5*histFlavSym.GetBinWidth(12),0.5*histFlavSym.GetBinWidth(12),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass200To300_TotalPredSF"])
                errGraphRatio.SetPointError(13,0.5*histFlavSym.GetBinWidth(13),0.5*histFlavSym.GetBinWidth(13),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass300To400_TotalPredSF"])
                errGraphRatio.SetPointError(14,0.5*histFlavSym.GetBinWidth(14),0.5*histFlavSym.GetBinWidth(14),resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrDownSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"],resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredErrUpSF"]/resultsNLL["highNLL"]["highMT2_"+nBJetsRegion+"_mass400_TotalPredSF"])
        
        

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

        latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%lumi)
        
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
        
        if "35" in lumi:
                year = "2016"
        elif "41" in lumi:
                year = "2017"
        elif "59" in lumi:
                year = "2018"

        hCanvas.Print("edgeOverview_%s_%s.pdf"%(nBJetsRegion, year))
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
        
        countingShelves_2016 = {"Run2016_36fb": countingShelves2016}
        countingShelves_2017 = {"Run2017_42fb": countingShelves2017}
        countingShelves_2018 = {"Run2018_60fb": countingShelves2018}
        
        #makeOverviewPlot(countingShelves, "zeroBJets")
        #makeOverviewPlot(countingShelves, "oneOrMoreBJets")
        # setTDRStyle()
        makeOverviewPlot(countingShelves_2016, "zeroBJets", ratio=True, lumi="35.9")
        makeOverviewPlot(countingShelves_2016, "oneOrMoreBJets", ratio=True, lumi="35.9")
        
        makeOverviewPlot(countingShelves_2017, "zeroBJets", ratio=True, lumi="41.5")
        makeOverviewPlot(countingShelves_2017, "oneOrMoreBJets", ratio=True, lumi="41.5")
        
        makeOverviewPlot(countingShelves_2018, "zeroBJets", ratio=True, lumi="59.7")
        makeOverviewPlot(countingShelves_2018, "oneOrMoreBJets", ratio=True, lumi="59.7")
        
    
main()
