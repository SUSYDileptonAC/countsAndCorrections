# This script compares the mass shape and normalization of the VVTo2L2Nu aMC@NLO sample and the ZZTo2L2Nu Powheg sample (as the latter is not simulated for low masses)
# VVTo2L2Nu does not have enough simulated events to be used (20% negative events -> 60% eff stats, 1/3 BR to ZZ -> 20% eff stats in total, significantly fewer gen events in general)

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
from locations import locations

from array import array

import pickle

from helpers import *

from plotTemplate import plotTemplate

def main():
    parser = argparse.ArgumentParser(description='edge fitter reloaded.')
    
    parser.add_argument("-r", "--runRange", dest="runRange", action="store", default=None,
                        help="name of run range.")
    parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                        help="selection which to apply.")
    parser.add_argument("-p", "--plot", dest = "plots" , action="append", default=[],
                        help="selection which to apply.")

    
    
    backgroundZZ = "RareZZOnZ"
    backgroundVV = "RareZZLowMassOnZ" # taking only the onZ part from this one
    
    args = parser.parse_args()  

    runRange = getRunRange(args.runRange)
    if args.plots == []:
        args.plots = ["mllPlot", "mllWidePlotC"]
    
    if args.selection == []:
        args.selection = ["SignalLowNLL24HighMT2ZeroB", "SignalLowNLL24HighMT2OneB","SignalHighNLL24HighMT2ZeroB", "SignalHighNLL24HighMT2OneB"]
    
    path = locations[runRange.era].dataSetPathNLL
    #path = locations[runRange.era].dataSetPath
    eventCounts = totalNumberOfGeneratedEvents(path,"","")   
    
    procZZ = Process(getattr(Backgrounds[runRange.era],backgroundZZ),eventCounts)
    procVV = Process(getattr(Backgrounds[runRange.era],backgroundVV),eventCounts)
    
    
    for selectionName in args.selection:
        selection = getRegion(selectionName)
        for plotName in args.plots:
            plot = getPlot(plotName)
            plot.addRegion(selection)
            plot.addRunRange(runRange)
            
            plot.cuts = plot.cuts.replace("metFilterSummary > 0 &&", "")
            plot.cuts = plot.cuts.replace("&& metFilterSummary > 0", "")
            #plot.cuts = plot.cuts.replace("chargeProduct < 0", "chargeProduct < 0 && mll > 40 && mll < 60")
            treesEE = readTrees(path, "EE")
            treesMM = readTrees(path, "MuMu")
            treesEM = readTrees(path, "EMu")
            
            template = plotTemplate()
            
            picklePath = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/frameWorkBase/shelves/scaleFactor_{runRange}_ZZTo4L.pkl"
            with open(picklePath.format(runRange=runRange.label), "r") as fi:
                scaleFac = pickle.load(fi)
            sf = scaleFac["scaleFac"]
            
            histZZ = procZZ.createCombinedHistogram(runRange.lumi,plot,treesEE,treesMM,shift = 1.,scalefacTree1=sf,scalefacTree2=sf)
            
            #print histZZ.GetEntries()
            
            histVV = procVV.createCombinedHistogram(runRange.lumi,plot,treesEE,treesMM,shift = 1.,scalefacTree1=sf,scalefacTree2=sf)
            
            # rMuE subtraction
            from corrections import corrections
            corrs = corrections[runRange.era].rMuELeptonPt.inclusive
            corrMap =  {}
            corrMap["offset"] = corrs.ptOffset
            corrMap["falling"] = corrs.ptFalling
            corrMap["etaParabolaBase"] = corrs.etaParabolaBase
            corrMap["etaParabolaMinus"] = corrs.etaParabolaMinus
            corrMap["etaParabolaPlus"] = corrs.etaParabolaPlus
            corrMap["norm"] = corrs.norm
            rt = corrections[runRange.era].rSFOFTrig.inclusive.val
            
            RT = "%.3f"%(rt)
            rMuEDummy = "({norm:.3f}*(({offset:.3f} + {falling:.3f}/{pt})*({etaParabolaBase} + ({eta}<-1.6)*{etaParabolaMinus:.3f}*pow({eta}+1.6, 2)+({eta}>1.6)*{etaParabolaPlus:.3f}*pow({eta}-1.6,2) )))"
            rMuE_El = rMuEDummy.format(pt="pt1", eta="eta1", **corrMap)
            rMuE_Mu = rMuEDummy.format(pt="pt2", eta="eta2", **corrMap)
            rMuEWeight = "(0.5*(%s + pow(%s, -1)))*%s"%(rMuE_El, rMuE_Mu, RT)
            plot.cuts = plot.cuts.replace("weight*", "weight*%s*"%(rMuEWeight))
            
            histVV_OF = procVV.createCombinedHistogram(runRange.lumi,plot,treesEM,"None",shift = 1.,scalefacTree1=sf,scalefacTree2=sf)
            histVV.Add(histVV_OF, -1)
            
             #normalize in Z-peak region (only properly works for mll plots and with correct binning)
            ZZCount = histZZ.Integral(histZZ.FindBin(86+0.1), histZZ.FindBin(96-0.1))
            VVCount = histVV.Integral(histVV.FindBin(86+0.1), histVV.FindBin(96-0.1))
            
            #histVV.Scale(ZZCount/VVCount)
            print ZZCount/VVCount
            
            if "Wide" in plotName:
                print selectionName, ZZCount/VVCount
            
            
            histZZ.SetLineColor(ROOT.kRed)
            histZZ.SetLineWidth(2)
            histZZ.SetMarkerSize(0)
            histZZ.SetFillStyle(0)
            histVV.SetLineColor(ROOT.kBlack)
            histVV.SetLineWidth(2)
            histVV.SetMarkerSize(0)
            histVV.SetFillStyle(0)
            
            template.setPrimaryPlot(histZZ, "histE", "ZZTo2L2Nu")
            template.addSecondaryPlot(histVV, "histE", "ZZTo2L2NuMass18")
            template.hasLegend = True
            template.cutsText = selection.labelSubRegion
            template.lumiInt = runRange.printval
            template.maximumScale = 1e3
            template.logY = True
            template.minimumY = 0.01
            
            
            template.setFolderName("compareMCSamples")
            template.draw()
            template.saveAs("comparison_%s_%s_%s"%(plotName, selection.name, runRange.label))
            template.clean()
    
if __name__ == "__main__":
    main()
