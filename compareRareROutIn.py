import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
from ROOT import gROOT, gStyle, TFile, TH1F, TCanvas, TPad, TDirectory, TMath, TLorentzVector, TGraphAsymmErrors, TFile, TH2F,TLegend
from setTDRStyle import setTDRStyle

from messageLogger import messageLogger as log
import argparse 

from defs import getRegion, getPlot, getRunRange, Backgrounds, theCuts,defineMyColors, myColors
from corrections import corrections

from array import array

import pickle

from plotTemplate import plotTemplate

def main():
    parser = argparse.ArgumentParser(description='edge fitter reloaded.')
    
    parser.add_argument("-r", "--runRange", dest="runRange", action="store", default=None,
                          help="name of run range.")
                    
    args = parser.parse_args()  
    
    
    
    runRange = getRunRange(args.runRange)
    
    predictions = pickle.load(open("shelves/RareOnZBG_%s.pkl"%(runRange.label)))
    
    for key in predictions.keys():
        if "bySample" in key: 
            print key
    #exit()
    
    
    rOutIn = corrections["Combined"].rOutIn
    rOutInVals = {"mass20To60":rOutIn.mass20To60.inclusive.val,"mass60To86":rOutIn.mass60To86.inclusive.val,"mass96To150":rOutIn.mass96To150.inclusive.val,"mass150To200":rOutIn.mass150To200.inclusive.val,"mass200To300":rOutIn.mass200To300.inclusive.val,"mass300To400":rOutIn.mass300To400.inclusive.val,"mass400":rOutIn.mass400.inclusive.val}
    rOutInErrs = {"mass20To60":rOutIn.mass20To60.inclusive.err,"mass60To86":rOutIn.mass60To86.inclusive.err,"mass96To150":rOutIn.mass96To150.inclusive.err,"mass150To200":rOutIn.mass150To200.inclusive.err,"mass200To300":rOutIn.mass200To300.inclusive.err,"mass300To400":rOutIn.mass300To400.inclusive.err,"mass400":rOutIn.mass400.inclusive.err}
    
    masses = ["mass20To60", "mass60To86", "mass96To150", "mass150To200", "mass200To300", "mass300To400", "mass400"]
    middlePoints = [40, 70, 120, 175, 250, 350, 450]
    
    bins = [20,60,86,96,150,200,300,400,500]
    bins = array("f", bins)
    
    nLLRegions = ["lowNLL","highNLL"]
    #MT2Regions = ["highMT2"]
    nBJetsRegions = ["zeroBJets", "oneOrMoreBJets"]
    
    
    
    signalBins = []
    for nLLRegion in nLLRegions:
            for nBJetsRegion in nBJetsRegions:
                signalBins.append("%s_%s_highMT2_%s"%("%s",nLLRegion,nBJetsRegion))
                            
    
    for signalBin in signalBins:
        template = plotTemplate()
        template.lumiInt = runRange.printval
        template.maximumScale = 2.5
        template.hasLegend = True
        histPred = ROOT.TH1F("", "", len(bins)-1, bins)
        histPredROutIn = ROOT.TH1F("", "", len(bins)-1, bins)
        
        graphErr = ROOT.TGraphAsymmErrors()
        graphErr.SetFillColor(ROOT.kBlack)
        graphErr.SetFillStyle(3354)
        
        histPred.SetLineColor(ROOT.kRed)
        histPred.SetLineWidth(2)
        histPredROutIn.SetLineColor(ROOT.kBlack)
        histPredROutIn.SetLineWidth(2)
        
        template.cutsText = signalBin[3:]
        
        template.labelX = "m_{ll} [GeV]"
        template.labelY = "Events / Bin"
        
        predOnZ = predictions[signalBin%"mass86To96"+"_bySample"]["ZZ"]
        i = 0
        for mass, middle in zip(masses, middlePoints):
            fullBin = signalBin%(mass)
            if middle > 60:
                pred = predictions[fullBin+"_bySample"]["ZZ"]
            else:
                pred = predictions[fullBin+"_bySample"]["VV"]
            predROutIn = predOnZ * rOutInVals[mass]
            predROutInErr = predOnZ * rOutInErrs[mass]
            
            histPred.SetBinContent(histPred.FindBin(middle), pred)
            histPredROutIn.SetBinContent(histPredROutIn.FindBin(middle), predROutIn)
            #histPredROutIn.SetBinError(histPredROutIn.FindBin(middle), predROutInErr)
            graphErr.SetPoint(i, histPred.GetBinCenter(histPred.FindBin(middle)), predROutIn)
            graphErr.SetPointError(i, histPred.GetBinWidth(histPred.FindBin(middle))*0.5,histPred.GetBinWidth(histPred.FindBin(middle))*0.5, predROutInErr, predROutInErr)
            i += 1
        template.setPrimaryPlot(histPred, "hist", "Prediction MC")
        template.addSecondaryPlot(histPredROutIn, "hist", "Prediction ROutIn")
        template.addSecondaryPlot(graphErr, "02", "Uncertainty ROutIn")
        template.setFolderName("RarePredictionROutIn")
        
        template.draw()
        template.saveAs("comparison_%s_%s"%(signalBin[3:], runRange.label))

if __name__ == "__main__":
    main()
