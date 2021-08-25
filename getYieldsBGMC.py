#! /usr/bin/env python

import sys
sys.path.append("../frameWorkBase")

from helpers import readTrees, totalNumberOfGeneratedEvents,createHistoFromTree, Process, TheStack
from locations import locations

from math import sqrt
from array import array

import ROOT
import argparse 

from sys import argv
import pickle   
from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TF1, TH2F, TH2D, TFile, TMath
import ratios
from defs import Backgrounds,Signals,Region,Regions,Plot,getRunRange,getRegion, getPlot,theCuts
from helpers import getTriggerScaleFactor
#from corrections import triggerEffs, rSFOF, rSFOFDirect,rMuELeptonPt, rSFOFTrig
from corrections import corrections
from centralConfig import systematics, runRanges

from math import sqrt
from setTDRStyle import setTDRStyle

from ConfigParser import ConfigParser
config = ConfigParser()
config.read("../SubmitScripts/Input/Master80X_MC.ini")


ROOT.gStyle.SetOptStat(0)

massCuts = {
                        "mass20To50":"mll < 50 && mll > 20",
                        "mass20To60":"mll < 60 && mll > 20",
                        "mass20To70":"mll < 70 && mll > 20",
                        "mass20To81":"mll < 81 && mll > 20",
                        "mass20To86":"mll < 86 && mll > 20",
                        "mass50To81":"mll < 81 && mll > 50",
                        "mass50To86":"mll < 86 && mll > 50",
                        "mass60To81":"mll < 81 && mll > 60",
                        "mass60To86":"mll < 86 && mll > 60",
                        "mass70To81":"mll < 81 && mll > 70",
                        "mass70To86":"mll < 86 && mll > 70",
                        "mass81To101":"mll < 101 && mll > 81",
                        "mass86To96":"mll < 96 && mll > 86",
                        "mass96To150":"mll < 150 && mll > 96",
                        "mass96To200":"mll < 200 && mll > 96",
                        "mass101To150":"mll < 150 && mll > 101",
                        "mass101To200":"mll < 200 && mll > 101",
                        "mass150To200":"mll < 200 && mll > 150",
                        "mass200To300":"mll > 200 && mll < 300",
                        "mass200To400":"mll > 200 && mll < 400",
                        "mass300To400":"mll > 300 && mll < 400",
                        "massAbove300":"mll > 300 ",
                        "mass400":"mll > 400 ",
                        "edgeMass":"mll < 70  && mll > 20 ",
                        "lowMass":"mll > 20 && mll < 86 ",
                        "highMass":"mll > 96 ",
                        "highMassOld":"mll > 101 ",
                        }                       
                        
nLLCuts = {
                        "default":"nLL > 0",
                        "lowNLL":getattr(theCuts.nLLCuts,"lowNLL").cut,
                        "highNLL":getattr(theCuts.nLLCuts,"highNLL").cut,
                        }
                        
HTCuts = {
                        "lowHT":"ht < 400",
                        "mediumHT":"ht > 400 && ht < 800",
                        "highHT":"ht > 800",
                        }
                        
MT2Cuts = {
                        "lowMT2":getattr(theCuts.mt2Cuts,"lowMT2").cut,
                        "highMT2":getattr(theCuts.mt2Cuts,"highMT2").cut,
                        }

NBJetsCuts = {
                        "zeroBJets" : getattr(theCuts.nBJetsCuts,"zeroBJets").cut,
                        "oneOrMoreBJets" : getattr(theCuts.nBJetsCuts,"oneOrMoreBJets").cut
}

                           
def getYields(runRange):
        import ratios
        
        import pickle   

        path = locations[runRange.era].dataSetPathNLL
        

        EE = readTrees(path, "EE")
        EM = readTrees(path, "EMu")
        MM = readTrees(path, "MuMu")
        
        ### Mass bins for Morion 2017 SRs, summed low and high mass regions + legacy regions
        massRegions = ["mass20To60","mass60To86","mass86To96","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        
        ### Two likelihood bins and MT2 cut
        nLLRegions = ["lowNLL","highNLL"]
        MT2Regions = ["highMT2"]
        nBJetsRegions = ["zeroBJets", "oneOrMoreBJets"]
        
        signalBins = []
        signalCuts = {} 
        
        plot = getPlot("mllPlotROutIn")
        

        for massRegion in massRegions:
                for nLLRegion in nLLRegions:
                        for MT2Region in MT2Regions:
                                for nBJetsRegion in nBJetsRegions:
                                        signalBins.append("%s_%s_%s_%s"%(massRegion,nLLRegion,MT2Region,nBJetsRegion))
                                        signalCuts["%s_%s_%s_%s"%(massRegion,nLLRegion,MT2Region,nBJetsRegion)] = "%s && %s && %s && %s"%(massCuts[massRegion],nLLCuts[nLLRegion],MT2Cuts[MT2Region], NBJetsCuts[nBJetsRegion])
                                
        selection = getRegion("SignalHighMT2DeltaPhiJetMet")
        backgrounds = ["RareWZOnZ","RareZZLowMassOnZ","RareTTZOnZ","RareRestOnZ"]
        

        plot.addRegion(selection)
        plot.addRunRange(runRange)
        plot.cuts = plot.cuts.replace("p4.M()","mll")   
        plot.variable = plot.variable.replace("p4.M()","mll")   
        
        if runRange.era == "2018":
                plot.cuts = plot.cuts.replace("chargeProduct < 0 &&","chargeProduct < 0 && vetoHEM == 1 &&")
        
        counts = {}
        
        eventCounts = totalNumberOfGeneratedEvents(path)
        
        defaultCut = plot.cuts

        ### loop over signal regions
        for signalBin in signalBins:
                
                ### Add signal cut and remove those that are renamed or already applied
                ### on NLL datasets
                plot.cuts = defaultCut.replace("chargeProduct < 0","chargeProduct < 0 && %s"%(signalCuts[signalBin]))   
                plot.cuts = plot.cuts.replace("metFilterSummary > 0 &&","")    
                plot.cuts = plot.cuts.replace("&& metFilterSummary > 0","")    
                plot.cuts = plot.cuts.replace("triggerSummary > 0 &&","")      
                plot.cuts = plot.cuts.replace("p4.Pt()","pt")
                
                plot.cuts = "bTagWeight*"+plot.cuts
                
                #print plot.cuts
                
                eventCountSF = 0
                eventYieldSF = 0
                eventYieldEE = 0
                eventYieldMM = 0
                eventYieldSFTotErr = 0
                eventYieldSFStatErr = 0
                eventYieldEEStatErr = 0
                eventYieldMMStatErr = 0
                eventYieldSFSystErr = 0
                eventYieldSFUp = 0
                eventYieldEEUp = 0
                eventYieldMMUp = 0
                eventYieldSFDown = 0
                eventYieldEEDown = 0
                eventYieldMMDown = 0
                
                eventYieldOF = 0
                eventYieldOFTotErr = 0
                eventYieldOFStatErr = 0
                eventYieldOFSystErr = 0
                eventYieldOFUp = 0
                eventYieldOFDown = 0
                
                counts["%s_bySample"%signalBin] = {}
                
                processes = []
                for background in backgrounds:
                        proc = Process(getattr(Backgrounds[runRange.era],background),eventCounts)
                        processes.append(proc)
                        
                        picklePath = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/frameWorkBase/shelves/scaleFactor_{runRange}_{background}.pkl"
                        sf = 1.0
                        sferr = 0.0
                        if proc.label in ["WZ", "ZZ", "TTZ"]:
                                if proc.label == "WZ":
                                        backgroundName = "WZTo3LNu"
                                elif proc.label == "ZZ":
                                        backgroundName = "ZZTo4L"
                                elif proc.label == "TTZ":
                                        backgroundName = "ttZToLL"
                                import pickle
                                with open(picklePath.format(runRange=runRange.label, background = backgroundName), "r") as fi:
                                        scaleFac = pickle.load(fi)
                                sf = scaleFac["scaleFac"]
                                sferr = scaleFac["scaleFacErr"] 
                        else:
                                sferr = proc.uncertainty
                        
                        sfErrRel = sferr/sf        
                        
                        
                        
                        saveCut = plot.cuts
                        
                        histoEE = proc.createCombinedHistogram(runRange.lumi,plot,EE,"None",1.0,getTriggerScaleFactor("EE", "inclusive", runRange)[0]*sf, 1.0, TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True,doPUWeights=False,normalizeToBinWidth=False,useTriggerEmulation=False)
                        histoMM = proc.createCombinedHistogram(runRange.lumi,plot,MM,"None",1.0,getTriggerScaleFactor("MM", "inclusive", runRange)[0]*sf, 1.0, TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True,doPUWeights=False,normalizeToBinWidth=False,useTriggerEmulation=False)
                        
                        # RSFOF weighted EMu sample with rMuE parametrization
                        rMuEPars = corrections[runRange.era].rMuELeptonPt.inclusive
                        RT = corrections[runRange.era].rSFOFTrig.inclusive.val
                        corrMap = {}
                        corrMap["offset"] = rMuEPars.ptOffsetMC
                        corrMap["falling"] = rMuEPars.ptFallingMC
                        corrMap["etaParabolaBase"] = rMuEPars.etaParabolaBaseMC
                        corrMap["etaParabolaMinus"] = rMuEPars.etaParabolaMinusMC
                        corrMap["etaParabolaPlus"] = rMuEPars.etaParabolaPlusMC
                        corrMap["norm"] = rMuEPars.normMC
                        
                        rMuEDummy = "({norm:.3f}*(({offset:.3f} + {falling:.3f}/{pt})*({etaParabolaBase} + ({eta}<-1.6)*{etaParabolaMinus:.3f}*pow({eta}+1.6, 2)+({eta}>1.6)*{etaParabolaPlus:.3f}*pow({eta}-1.6,2) )))"
                        rMuE_El = rMuEDummy.format(pt="pt1", eta="eta1", **corrMap)
                        rMuE_Mu = rMuEDummy.format(pt="pt2", eta="eta2", **corrMap)
                        rMuEWeight = "(0.5*(%s + pow(%s, -1)))*%.3f"%(rMuE_Mu, rMuE_El,RT)
                        
                        #tmpCut = plot.cuts
                        plot.cuts = "%s*%s"%(rMuEWeight, plot.cuts)
                        histoEM = proc.createCombinedHistogram(runRange.lumi,plot,EM,"None",1.0,getTriggerScaleFactor("EM", "inclusive", runRange)[0]*sf, 1.0, TopWeightUp=False,TopWeightDown=False,signal=False,doTopReweighting=True,doPUWeights=False,normalizeToBinWidth=False,useTriggerEmulation=False)
                        #plot.cuts = tmpCut
                        
                        plot.cuts = saveCut
                        
                        statErrEE = ROOT.Double()
                        statErrMM = ROOT.Double()
                        statErrEM = ROOT.Double()
                        
                        eventCountSF += histoEE.GetEntries()+histoMM.GetEntries()
                        
                        procYield = histoEE.IntegralAndError(0, -1, statErrEE)+histoMM.IntegralAndError(0, -1, statErrMM)
                        procYield_EE = histoEE.IntegralAndError(0, -1, statErrEE)
                        procYield_MM = histoMM.IntegralAndError(0, -1, statErrMM)
                        
                        #if "mass20To60" in signalBin and proc.label == "ZZ": 
                                #print signalBin, procYield
                        
                        eventYieldSF += procYield
                        eventYieldSFUp   += (procYield)*(1+sfErrRel) 
                        eventYieldSFDown += (procYield)*(1-sfErrRel) 
                        
                        eventYieldEE += procYield_EE
                        eventYieldEEUp   += (procYield_EE)*(1+sfErrRel) 
                        eventYieldEEDown += (procYield_EE)*(1-sfErrRel) 
                        
                        eventYieldMM += procYield_MM
                        eventYieldMMUp   += (procYield_MM)*(1+sfErrRel) 
                        eventYieldMMDown += (procYield_MM)*(1-sfErrRel) 
                        
                        eventYieldSFStatErr = (eventYieldSFStatErr**2 + statErrEE**2 + statErrMM**2)**0.5
                        eventYieldEEStatErr = (eventYieldEEStatErr**2 + statErrEE**2)**0.5
                        eventYieldMMStatErr = (eventYieldMMStatErr**2 + statErrMM**2)**0.5
                        eventYieldSFSystErr = (eventYieldSFSystErr**2 + (eventYieldSF*sfErrRel)**2)**0.5
                        
                        eventYieldOF += histoEM.IntegralAndError(0, -1, statErrEM)
                        eventYieldOFUp   += histoEM.Integral(0, -1)*(1+proc.uncertainty)
                        eventYieldOFDown += histoEM.Integral(0, -1)*(1-proc.uncertainty)
                        
                        eventYieldOFStatErr = (eventYieldOFStatErr**2 + statErrEM**2)**0.5
                        eventYieldOFSystErr = (eventYieldOFSystErr**2 + (eventYieldOF*sfErrRel)**2)**0.5
                        
                        counts["%s_bySample"%signalBin][proc.label] = procYield
                        
                        if proc.label in ["WZ", "ZZ", "TTZ", "Rare"]:
                                # uncertainty from just this one sample. Used to treat uncertainties uncorrelated between WZ,ZZ,TTZ,Rare
                                counts["%s_SingleErr%s"%(signalBin,proc.label)] =  ( ((procYield)*sfErrRel)**2 + statErrEE**2 + statErrMM**2 )**0.5
                        
                        
                        #if proc.label == "ZZ" and "highNLL" in signalBin:
                                #print signalBin, gotten
                        
                        
                eventYieldSFTotErr = (eventYieldSFStatErr**2 + eventYieldSFSystErr**2)**0.5
                eventYieldOFTotErr = (eventYieldOFStatErr**2 + eventYieldOFSystErr**2)**0.5
                

                
                eventCountSF = histoEE.GetEntries()+histoMM.GetEntries()
 

                counts["%s_SF"%signalBin] = eventYieldSF
                counts["%s_EE"%signalBin] = eventYieldEE
                counts["%s_MM"%signalBin] = eventYieldMM
                counts["%s_SF_Stat"%signalBin] = eventYieldSFStatErr
                counts["%s_EE_Stat"%signalBin] = eventYieldEEStatErr
                counts["%s_MM_Stat"%signalBin] = eventYieldMMStatErr
                counts["%s_SF_Syst"%signalBin] = eventYieldSFSystErr
                counts["%s_SF_Up"%signalBin] = eventYieldSFUp
                counts["%s_EE_Up"%signalBin] = eventYieldEEUp
                counts["%s_MM_Up"%signalBin] = eventYieldMMUp
                counts["%s_SF_Down"%signalBin] = eventYieldSFDown
                counts["%s_EE_Down"%signalBin] = eventYieldEEDown
                counts["%s_MM_Down"%signalBin] = eventYieldMMDown
                counts["MCEvents_%s_SF"%signalBin] = eventCountSF
                

                counts["%s_OF"%signalBin] = eventYieldOF
                counts["%s_OF_Stat"%signalBin] = eventYieldOFStatErr
                counts["%s_OF_Syst"%signalBin] = eventYieldOFSystErr
                counts["%s_OF_Err"%signalBin] = eventYieldOFTotErr
                counts["%s_OF_Up"%signalBin] = eventYieldOFUp
                counts["%s_OF_Down"%signalBin] = eventYieldOFDown

 
        fileName = "RareOnZBG_%s"%(runRange.label)

        outFilePkl = open("shelves/%s.pkl"%fileName,"w")
        pickle.dump(counts, outFilePkl)
        outFilePkl.close()                      
                        

                                
        

# This method just waits for a button to be pressed
def waitForInput():
    raw_input("Press any key to continue!")
    return


    
def main():
        parser = argparse.ArgumentParser(description='MC yields in signal region')
        parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
                                                  help="write results to central repository")   
        parser.add_argument("-a", "--useAllMC", action="store_true", dest="useAllMC", default=False,
                                                  help="Use all MC samples instead of only (rare) on Z") 
        parser.add_argument("-d", "--drellYan", action="store_true", dest="useDY", default=False,
                                                  help="Use only on Z (not rare)") 
        parser.add_argument("-r", "--runRange", dest="runRanges", action="append", default=[],
                                                  help="name of run range.")                                                 
                                        
        args = parser.parse_args()
    
        
        if args.write:
                import subprocess

                bashCommand1 = "cp shelves/RareOnZBG_Run2016_36fb.pkl ../frameWorkBase/shelves"          
                bashCommand2 = "cp shelves/RareOnZBG_Run2017_42fb.pkl ../frameWorkBase/shelves"          
                bashCommand3 = "cp shelves/RareOnZBG_Run2018_60fb.pkl ../frameWorkBase/shelves"                   

                process = subprocess.Popen(bashCommand1.split())
                process = subprocess.Popen(bashCommand2.split())
                process = subprocess.Popen(bashCommand3.split())

                
        else:   
                for rr in args.runRanges:
                        runRange = getRunRange(rr)
                        getYields(runRange)

 



# entry point
#-------------
if (__name__ == "__main__"):
        main()
