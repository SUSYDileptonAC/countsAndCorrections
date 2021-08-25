#!/usr/bin/env python

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
ROOT.gROOT.SetBatch(True)
from ROOT import TCanvas, TEfficiency, TPad, TH1F, TH1I, THStack, TLegend, TMath, TGraphAsymmErrors, TF1, gStyle


from defs import getRegion, getPlot, getRunRange, Backgrounds

from setTDRStyle import setTDRStyle
from helpers import readTrees, getDataHist, TheStack, totalNumberOfGeneratedEvents, Process, ensurePathExists, getTriggerScaleFactor

#from corrections import rSFOF, rEEOF, rMMOF, triggerEffs
from centralConfig import regionsToUse,  backgroundLists, plotLists, systematics,  mllBins
from centralConfig import runRanges as RR
from corrections import corrections



from locations import locations


def getHistograms(plot,runRange,isMC,backgrounds,region):
        path = locations[runRange.era].dataSetPath
        treesEE = readTrees(path,"EE")
        treesEM = readTrees(path,"EMu")
        treesMM = readTrees(path,"MuMu")
                        
        if isMC:
                
                eventCounts = totalNumberOfGeneratedEvents(path)        
                processes = []
                for background in backgrounds:
                        processes.append(Process(getattr(Backgrounds[runRange.era],background),eventCounts))
                
                triggerSF_EE,_ = getTriggerScaleFactor("EE",   region, runRange)
                triggerSF_MM,_ = getTriggerScaleFactor("MuMu", region, runRange)
                triggerSF_EM,_ = getTriggerScaleFactor("EMu",  region, runRange)
                
                histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,triggerSF_EE,1.0,useTriggerEmulation=True).theHistogram               
                histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,triggerSF_MM,1.0,useTriggerEmulation=True).theHistogram
                histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,triggerSF_EM,1.0,useTriggerEmulation=True).theHistogram
                
                #~ histoEE = TheStack(processes,runRange.lumi,plot,treesEE,"None",1.0,1.0,1.0).theHistogram             
                #~ histoMM = TheStack(processes,runRange.lumi,plot,treesMM,"None",1.0,1.0,1.0).theHistogram
                #~ histoEM = TheStack(processes,runRange.lumi,plot,treesEM,"None",1.0,1.0,1.0).theHistogram
                #~ histoEE.Scale(getattr(triggerEffs,region).effEE.valMC)
                #~ histoMM.Scale(getattr(triggerEffs,region).effMM.valMC)       
                #~ histoEM.Scale(getattr(triggerEffs,region).effEM.valMC)                               
                
        else:
                histoEE = getDataHist(plot,treesEE)
                histoMM = getDataHist(plot,treesMM)
                histoEM = getDataHist(plot,treesEM)
        
        return histoEE , histoMM, histoEM


        
def plotMllSpectra(SFhist,EMuhist,runRanges,selection,suffix,cmsExtra,additionalLabel):

                
        #SFhist.Rebin(5)
        #EMuhist.Rebin(5)

        hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
        plotPad = TPad("plotPad","plotPad",0,0,1,1)
        
        style=setTDRStyle()
        style.SetTitleYOffset(1.6)
        style.SetPadLeftMargin(0.19)            
        plotPad.UseCurrentStyle()
        plotPad.Draw()  
        plotPad.cd()                                    

        
        SFhist.SetMarkerStyle(20)
        SFhist.SetMarkerColor(ROOT.kBlack)
        
        #~ EMuhist.Draw("samehist")
        #~ SFhist.Draw("samepe")
        EMuhist.SetFillColor(855)
        legend = TLegend(0.6, 0.7, 0.95, 0.95)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        ROOT.gStyle.SetOptStat(0)       
        legend.AddEntry(SFhist,"%s events"%suffix,"p")
        legend.AddEntry(EMuhist,"OF events","f")
        #~ legend.Draw("same")
        
        lines = {}
        massBins = ["mass20To60","mass60To86","onZ","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]
        #massBins = ["edgeMass"]
        
        for mllBin in massBins:
                lines[mllBin] = ROOT.TLine(getattr(mllBins,mllBin).low,0,getattr(mllBins,mllBin).low,SFhist.GetBinContent(SFhist.GetMaximumBin()))
                lines[mllBin].SetLineWidth(2)
                if mllBin == "onZ" or mllBin == "mass96To150":
                        lines[mllBin].SetLineColor(ROOT.kRed+2)
                else:
                        lines[mllBin].SetLineColor(ROOT.kBlack)
                        
                lines[mllBin].Draw("same")


        Labelin = ROOT.TLatex()
        Labelin.SetTextAlign(12)
        Labelin.SetTextSize(0.025)
        Labelin.SetTextColor(ROOT.kRed+2)
        Labelout = ROOT.TLatex()
        Labelout.SetTextAlign(12)
        Labelout.SetTextSize(0.025)
        Labelout.SetTextColor(ROOT.kBlack)      
        
        
        latex = ROOT.TLatex()
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(0.04)
        latex.SetNDC(True)
        latexCMS = ROOT.TLatex()
        latexCMS.SetTextFont(61)
        latexCMS.SetTextSize(0.055)
        latexCMS.SetNDC(True)
        latexCMSExtra = ROOT.TLatex()
        latexCMSExtra.SetTextFont(52)
        latexCMSExtra.SetTextSize(0.03)
        latexCMSExtra.SetNDC(True) 
        
        
        hCanvas.Clear()
        
        plotPad = TPad("plotPad","plotPad",0,0,1,1)
        
        style=setTDRStyle()
        plotPad.UseCurrentStyle()
        plotPad.Draw()  
        plotPad.cd()                            
        

        
        plotPad.DrawFrame(mllBins.mass20To60.low,0.1,500,SFhist.GetBinContent(SFhist.GetMaximumBin())*500,"; %s ; %s" %("m_{ll} [GeV]","Events / Bin"))               
        
        plotPad.SetLogy()

        
        EMuhist.Draw("samehist")
        SFhist.Draw("samepe")
        legend.Draw("same")
        

        for mllBin in massBins:
                lines[mllBin].SetY2(SFhist.GetBinContent(SFhist.GetMaximumBin()))
                lines[mllBin].Draw("same")
                
        Labelin.SetTextAngle(90)
        Labelin.DrawLatex(91.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"on Z")
        Labelout.SetTextAngle(90)
        Labelout.DrawLatex(40.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"20-60 GeV")
        Labelout.DrawLatex(73.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"60-86 GeV")
        Labelout.DrawLatex(123.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"96-150 GeV")
        Labelout.DrawLatex(175.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"150-200 GeV")
        Labelout.DrawLatex(250.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"200-300 GeV")
        Labelout.DrawLatex(350.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"300-400 GeV")
        Labelout.DrawLatex(450.,SFhist.GetBinContent(SFhist.GetMaximumBin())/18,"400+ GeV")
        # lumi = "+".join([runRange.printval for runRange in runRanges])
        lumi = "137"
        latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%lumi)
        

        latexCMS.DrawLatex(0.19,0.88,"CMS")
        if "Simulation" in cmsExtra:
                yLabelPos = 0.825       
        else:
                yLabelPos = 0.84        

        latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))         
        plotPad.RedrawAxis()
        
        if len(runRanges) > 1:
                label = "Combined"
        else:
                label = runRanges[0].label
        
        
        if additionalLabel is not "":
                if additionalLabel is "_MC":
                        hCanvas.Print("fig/rOutIn_%s_%s_%s_%s.pdf"%(suffix,selection.name,label,additionalLabel))      
                else:   
                        ensurePathExists("fig/dependencies/%s"%(label))
                        hCanvas.Print("fig/dependencies/%s/rOutIn_%s_%s_%s_%s.pdf"%(label, suffix,selection.name,label,additionalLabel))      
        else:
                hCanvas.Print("fig/rOutIn_%s_%s_%s.pdf"%(suffix,selection.name,label)) 
        
        
def dependencies(selection,plots,runRanges,mc,backgrounds,cmsExtra,useExisting, combine=False):
        hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
        legend = TLegend(0.5, 0.65, 0.9, 0.925)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        ROOT.gStyle.SetOptStat(0)
        
        if not combine:
                runRange = runRanges[0]
                
        else:
                runRange = getRunRange("Run2016_to_2018")
        label = runRange.label
        era = runRange.era
        
        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400"]            
        #massBins = ["edgeMass"]         
        #~ massBins = ["mass20To60","mass60To86","lowMass","highMass"]          
        #~ massBins = ["lowMass","highMass"]            
        
        for name in plots:
                print name
                hCanvas.Clear()
                
                plot = getPlot(name)
                plot.addRegion(selection)
                plot.cleanCuts()   
                plot.addRunRange(runRange)     
                #plot.cuts = plot.cuts % runRange.runCut 
                if plot.variable == "MT2":
                        plot.cuts = plot.cuts.replace("MT2 > 80 &&","")
                 
                if len(plot.binning) == 0:
                        bins = [plot.firstBin+(plot.lastBin-plot.firstBin)/plot.nBins*i for i in range(plot.nBins+1)]
                else:
                        bins = plot.binning
                print bins
                rOutIn = {}
                rOutInErr = {}
                rOutInMC = {}
                rOutInMCErr = {}
                for massBin in massBins:
                        #~ rOutIn[massBin] ={"EE":[],"MM":[],"SF":[]}
                        #~ rOutInErr[massBin] ={"EE":[],"MM":[],"SF":[]}
                        rOutIn[massBin] ={"SF":[]}
                        rOutInErr[massBin] ={"SF":[]}
                        rOutInMC[massBin] ={"SF":[]}
                        rOutInMCErr[massBin] ={"SF":[]}


                binningErrs     = []
                plotBinning = []
                for i in range(0,len(bins)-1):
                        binningErrs.append((bins[i+1]-bins[i])/2)
                        if i == 0:
                                plotBinning.append((bins[i+1]-abs(bins[i]))/2)
                        else:
                                plotBinning.append(plotBinning[i-1]+(bins[i+1]-bins[i])/2+binningErrs[i-1])

                        print plotBinning
                        tmpCuts = selection.cut 
                        cuts = selection.cut.split("&&")
                        cutsUp = [] 
                        cutsDown = [] 
                        cutsEqual = []
                        for cut in cuts:
                                if "%s >"%plot.variable in cut:
                                        cutsUp.append(cut+ "&&")
                                elif "%s <"%plot.variable in cut:
                                        cutsDown.append(cut+ "&&")
                                elif "%s =="%plot.variable in cut:
                                        cutsEqual.append(cut+ "&&")
                        for cut in cutsUp:
                                selection.cut = selection.cut.replace(cut,"")           
                        for cut in cutsDown:
                                selection.cut = selection.cut.replace(cut,"")           
                        for cut in cutsEqual:
                                selection.cut = selection.cut.replace(cut,"")           
                        
                        selection.cut = selection.cut + " && %s >= %f && %s < %f"%(plot.variable,bins[i],plot.variable,bins[i+1])
                        selection.cut = selection.cut.replace("&& &&","&&")
                        #if runRange.weight != None:
                                #selection.cut = "prefireWeight*("+selection.cut+")"
                        
                        
                        if plot.variable == "met":
                                selection.cut = selection.cut.replace("chargeProduct < 0","chargeProduct < 0 && !(nJets >= 3 && met > 100)")
                        print selection.cut
                                
                        additionalLabel = "%s_%.2f_%.2f"%(plot.variable,bins[i],bins[i+1])
                        if not useExisting:
                                centralVal = centralValues(selection,runRanges,False,backgrounds,cmsExtra,additionalLabel, combine=combine)
                                centralValMC = centralValues(selection,runRanges,True,backgrounds,cmsExtra,additionalLabel, combine=combine)
                                
                                outFilePkl = open("shelves/rOutIn_%s_%s_%s.pkl"%(selection.name,label,additionalLabel),"w")
                                pickle.dump(centralVal, outFilePkl)
                                outFilePkl.close()
                                
                                outFilePklMC = open("shelves/rOutIn_%s_%s_%s_MC.pkl"%(selection.name,label,additionalLabel),"w")
                                pickle.dump(centralValMC, outFilePklMC)
                                outFilePklMC.close()
                        
                        else:
                                if os.path.isfile("shelves/rOutIn_%s_%s_%s.pkl"%(selection.name,label,additionalLabel)):
                                        centralVal = pickle.load(open("shelves/rOutIn_%s_%s_%s.pkl"%(selection.name,label,additionalLabel),"rb"))
                                else:
                                        centralVal = centralValues(selection,[runRange,],False,backgrounds,cmsExtra,additionalLabel)
                                        outFilePkl = open("shelves/rOutIn_%s_%s_%s.pkl"%(selection.name,label,additionalLabel),"w")
                                        pickle.dump(centralVal, outFilePkl)
                                        outFilePkl.close()
                                        
                                if os.path.isfile("shelves/rOutIn_%s_%s_%s_MC.pkl"%(selection.name,label,additionalLabel)):
                                        centralValMC = pickle.load(open("shelves/rOutIn_%s_%s_%s_MC.pkl"%(selection.name,label,additionalLabel),"rb"))
                                else:
                                        centralValMC = centralValues(selection,[runRange,],True,backgrounds,cmsExtra,additionalLabel)
                                        outFilePklMC = open("shelves/rOutIn_%s_%s_%s_MC.pkl"%(selection.name,label,additionalLabel),"w")
                                        pickle.dump(centralValMC, outFilePklMC)
                                        outFilePklMC.close()
                        
   
                        print additionalLabel
                        ##~ for combination in ["EE","MM","SF"]:
                        for combination in ["SF"]:
                                for region in massBins:
                                        #if not "HighMT2" in selection.name:
                                                #rOutIn[region][combination].append(centralVal["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
                                                #rOutInErr[region][combination].append(centralVal["rOutIn_%s_NoMT2Cut_Err%s"%(region,combination)])
                                                #rOutInMC[region][combination].append(centralValMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
                                                #rOutInMCErr[region][combination].append(centralValMC["rOutIn_%s_NoMT2Cut_Err%s"%(region,combination)])
                                        #else:
                                        rOutIn[region][combination].append(centralVal["rOutIn_%s_%s"%(region,combination)])
                                        rOutInErr[region][combination].append(centralVal["rOutIn_%s_Err%s"%(region,combination)])
                                        rOutInMC[region][combination].append(centralValMC["rOutIn_%s_%s"%(region,combination)])
                                        rOutInMCErr[region][combination].append(centralValMC["rOutIn_%s_Err%s"%(region,combination)])


                        
                        selection.cut = tmpCuts

                                                                
                if os.path.isfile("shelves/rOutIn_%s_%s.pkl"%(selection.name,label)):
                        centralVals = pickle.load(open("shelves/rOutIn_%s_%s.pkl"%(selection.name,label),"rb"))
                else:
                        centralVals = centralValues(selection,[runRange,],False,backgrounds,cmsExtra) 
                if os.path.isfile("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,label)):
                        centralValsMC = pickle.load(open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,label),"rb"))
                else:
                        centralValsMC = centralValues(selection,[runRange,],True,backgrounds,cmsExtra)                
                
                #~ for combination in ["EE","MM","SF"]:
                for combination in ["SF",]:
                        
                        for region in massBins:    
                                if region == "mass20To60":
                                        relSyst = systematics.rOutIn[era].massBelow150.val
                                        ymax = 0.25     
                                elif region == "mass96To150" or region == "mass60To86":
                                        relSyst = systematics.rOutIn[era].massBelow150.val   
                                        ymax = 0.6
                                elif region == "mass150To200":
                                        relSyst = systematics.rOutIn[era].massAbove150.val
                                        ymax = 0.05
                                else:
                                        relSyst = systematics.rOutIn[era].massAbove150.val
                                        ymax = 0.06
                                                                
                                hCanvas = TCanvas("hCanvas", "Distribution", 800,800)
                                plotPad = TPad("plotPad","plotPad",0,0,1,1)
                                style=setTDRStyle()
                                style.SetTitleYOffset(1.3)
                                style.SetTitleXOffset(1.2)
                                style.SetPadLeftMargin(0.16)            
                                style.SetPadBottomMargin(0.15)          
                                plotPad.UseCurrentStyle()
                                plotPad.Draw()  
                                plotPad.cd()
                
                                dr = plotPad.DrawFrame(plot.firstBin,0.0,plot.lastBin,ymax,"; %s ; %s" %(plot.xaxis,"R_{out/in}"))           
                                dr.GetYaxis().SetTitleOffset(1.35)
                                
                                bandX = array("f",[plot.firstBin,plot.lastBin])
                                #if not "HighMT2" in selection.name:
                                        #bandY = array("f",[centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]])
                                        #bandYErr = array("f",[centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]*relSyst,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)]*relSyst])
                                #else:
                                bandY = array("f",[centralVals["rOutIn_%s_%s"%(region,combination)],centralVals["rOutIn_%s_%s"%(region,combination)]])
                                bandYErr = array("f",[centralVals["rOutIn_%s_%s"%(region,combination)]*relSyst,centralVals["rOutIn_%s_%s"%(region,combination)]*relSyst])
                                bandXErr = array("f",[0,0])
                                
                                
                                errorband = ROOT.TGraphErrors(2,bandX,bandY,bandXErr,bandYErr)
                                errorband.GetYaxis().SetRangeUser(0.0,0.15)
                                errorband.GetXaxis().SetRangeUser(-5,105)
                                errorband.Draw("3same")
                                errorband.SetFillColor(ROOT.kOrange-9)
                                errorband.SetLineColor(ROOT.kWhite)
                                #if not "HighMT2" in selection.name:
                                        #rOutInLine = ROOT.TLine(plot.firstBin,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],plot.lastBin,centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
                                #else:
                                rOutInLine = ROOT.TLine(plot.firstBin,centralVals["rOutIn_%s_%s"%(region,combination)],plot.lastBin,centralVals["rOutIn_%s_%s"%(region,combination)])
                                rOutInLine.SetLineStyle(ROOT.kDashed)
                                rOutInLine.SetLineWidth(2)
                                rOutInLine.Draw("same")
                                
                                #if not "HighMT2" in selection.name:
                                        #rOutInLineMC = ROOT.TLine(plot.firstBin,centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],plot.lastBin,centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)])
                                #else:
                                rOutInLineMC = ROOT.TLine(plot.firstBin,centralValsMC["rOutIn_%s_%s"%(region,combination)],plot.lastBin,centralValsMC["rOutIn_%s_%s"%(region,combination)])
                                rOutInLineMC.SetLineStyle(ROOT.kDashed)
                                rOutInLineMC.SetLineWidth(2)
                                rOutInLineMC.SetLineColor(ROOT.kGreen-2)
                                rOutInLineMC.Draw("same")

                                
                                
                                
                                binning = array("f",plotBinning)
                                binningErrs = array("f",binningErrs)
                                
                                rOutInVals = array("f",rOutIn[region][combination])
                                rOutInValsErrs = array("f",rOutInErr[region][combination])      
                                graph = ROOT.TGraphErrors(len(binning),binning,rOutInVals,binningErrs,rOutInValsErrs)
                                graph.Draw("Psame0")
                                
                                rOutInValsMC = array("f",rOutInMC[region][combination])
                                rOutInValsMCErrs = array("f",rOutInMCErr[region][combination])  
                                graphMC = ROOT.TGraphErrors(len(binning),binning,rOutInValsMC,binningErrs,rOutInValsMCErrs)
                                graphMC.SetLineColor(ROOT.kGreen-2) 
                                graphMC.SetMarkerColor(ROOT.kGreen-2) 
                                graphMC.SetMarkerStyle(21) 
                                graphMC.Draw("Psame0")
                                
                                legend.Clear()

                                
                                legend.AddEntry(graphMC,"R_{out,in} MC","p")
                                legend.AddEntry(graph,"R_{out,in} Data","p")
                                if not "HighMT2" in selection.name:
                                        legend.AddEntry(rOutInLine, "Mean R_{out,in} Data = %.3f"%centralVals["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],"l")
                                        legend.AddEntry(rOutInLineMC, "Mean R_{out,in} MC = %.3f"%centralValsMC["rOutIn_%s_NoMT2Cut_%s"%(region,combination)],"l")
                                else:
                                        legend.AddEntry(rOutInLine, "Mean R_{out,in} Data = %.3f"%centralVals["rOutIn_%s_%s"%(region,combination)],"l")
                                        legend.AddEntry(rOutInLineMC, "Mean R_{out,in} MC = %.3f"%centralValsMC["rOutIn_%s_%s"%(region,combination)],"l")
                                legend.AddEntry(errorband, "Mean R_{out,in} Data #pm %d %%"%(relSyst*100),"f")
                                legend.Draw("same")


                                latex = ROOT.TLatex()
                                latex.SetTextFont(42)
                                latex.SetTextAlign(31)
                                latex.SetTextSize(0.04)
                                latex.SetNDC(True)
                                latexCMS = ROOT.TLatex()
                                latexCMS.SetTextFont(61)
                                latexCMS.SetTextSize(0.055)
                                latexCMS.SetNDC(True)
                                latexCMSExtra = ROOT.TLatex()
                                latexCMSExtra.SetTextFont(52)
                                latexCMSExtra.SetTextSize(0.03)
                                latexCMSExtra.SetNDC(True) 
                                
                                latexLabel = ROOT.TLatex()
                                latexLabel.SetTextSize(0.03)    
                                latexLabel.SetNDC()
                                
                                #if "HighMT2" in selection.name:
                                        #if plot.variable == "met":
                                                #latexLabel.DrawLatex(0.225, 0.6, "N_{Jets} #geq 2, M_{T2} > 80 GeV")
                                        #elif plot.variable == "nJets":                                  
                                                #latexLabel.DrawLatex(0.225, 0.6, "p_{T}^{miss} < 50 GeV, M_{T2} > 80 GeV")
                                        #else:                                   
                                                #latexLabel.DrawLatex(0.225, 0.6, "N_{Jets} #geq 2, p_{T}^{miss} < 50 GeV, M_{T2} > 80 GeV")
                                        
                                        #if region == "edgeMass":
                                                #latexLabel.DrawLatex(0.225, 0.55, "20 < m_{ll} < 70 GeV")
                                        #elif region == "lowMass":
                                                #latexLabel.DrawLatex(0.225, 0.55, "20 < m_{ll} < 86 GeV")
                                        #elif region == "mass20To60":
                                                #latexLabel.DrawLatex(0.225, 0.55, "20 < m_{ll} < 60 GeV")
                                        #elif region == "mass60To86":
                                                #latexLabel.DrawLatex(0.225, 0.55, "60 < m_{ll} < 86 GeV")
                                        #elif region == "highMass":
                                                #latexLabel.DrawLatex(0.225, 0.55, "m_{ll} > 96 GeV")
                                        #else:
                                                #latexLabel.DrawLatex(0.225, 0.55, region)
                                                
                                #else:
                                if plot.variable == "met":
                                        latexLabel.DrawLatex(0.225, 0.6, "n_{j} #geq 2, M_{T2} > 80 GeV")
                                elif plot.variable == "nJets":                                  
                                        latexLabel.DrawLatex(0.225, 0.6, "p_{T}^{miss} < 50 GeV, M_{T2} > 80 GeV")
                                else:                                   
                                        latexLabel.DrawLatex(0.225, 0.6, "n_{j} #geq 2, p_{T}^{miss} < 50 GeV")
                                
                                if region == "mass20To60":
                                        latexLabel.DrawLatex(0.225, 0.55, "20 < m_{ll} < 60 GeV")
                                elif region == "mass60To86":
                                        latexLabel.DrawLatex(0.225, 0.55, "60 < m_{ll} < 86 GeV")
                                elif region == "mass96To150":
                                        latexLabel.DrawLatex(0.225, 0.55, "96 < m_{ll} < 150 GeV")
                                elif region == "mass150To200":
                                        latexLabel.DrawLatex(0.225, 0.55, "150 < m_{ll} < 200 GeV")
                                elif region == "mass200To300":
                                        latexLabel.DrawLatex(0.225, 0.55, "200 < m_{ll} < 300 GeV")
                                elif region == "mass300To400":
                                        latexLabel.DrawLatex(0.225, 0.55, "300 < m_{ll} < 400 GeV")
                                elif region == "mass400":
                                        latexLabel.DrawLatex(0.225, 0.55, "m_{ll} > 400 GeV")
                                else:
                                        latexLabel.DrawLatex(0.225, 0.55, region)
                                
                                # latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%runRange.printval)
                                latex.DrawLatex(0.95, 0.96, "%s fb^{-1} (13 TeV)"%"137")
                                

                                latexCMS.DrawLatex(0.19,0.89,"CMS")
                                yLabelPos = 0.85        

                                latexCMSExtra.DrawLatex(0.19,yLabelPos,"%s"%(cmsExtra))         
                                        
                                ROOT.gPad.RedrawAxis()
                                ensurePathExists("fig/dependencies/%s"%(label))
                                hCanvas.Print("fig/dependencies/%s/rOutInSyst_%s_%s_%s_%s_%s_%s.pdf"%(label, selection.name,label,plot.variablePlotName,region,combination,plot.additionalName))

        
        

def centralValues(selection,runRanges,isMC,backgrounds,cmsExtra,additionalLabel="", combine=False):
        result = {}
        hists = {}
        for runRange in runRanges:
                result[runRange.era] = {}
                hists[runRange.era] = {}
                massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","edgeMass","highMass","lowMass"]
                
                if "Forward" in selection.name:
                        region = "forward"
                elif "Central" in selection.name:
                        region = "central"
                else:           
                        region = "inclusive"            

                plot = getPlot("mllPlotROutIn")
                plot.addRegion(selection)
                plot.cleanCuts()
                plot.addRunRange(runRange)      
                print plot.cuts

                plotNoMT2Cut = getPlot("mllPlotROutIn")
                plotNoMT2Cut.addRegion(selection)
                plotNoMT2Cut.cleanCuts()
                plotNoMT2Cut.addRunRange(runRange) 
                plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("MT2 > 80 &&","")

                histEE, histMM, histEM = getHistograms(plot,runRange,isMC,backgrounds,region)
                histSF = histEE.Clone("histSF")
                histSF.Add(histMM.Clone())
                
                hists[runRange.era]["SF"] = histSF
                hists[runRange.era]["EE"] = histEE
                hists[runRange.era]["MM"] = histMM
                hists[runRange.era]["EM"] = histEM
                
                histEENoMT2Cut, histMMNoMT2Cut, histEMNoMT2Cut = getHistograms(plotNoMT2Cut,runRange,isMC,backgrounds,region)
                histSFNoMT2Cut = histEENoMT2Cut.Clone("histSFNoMT2Cut")
                histSFNoMT2Cut.Add(histMMNoMT2Cut.Clone())
                
                
                
                peakLow = mllBins.onZ.low
                peakHigh = mllBins.onZ.high
                
                result[runRange.era]["peak_EE"] = histEE.Integral(histEE.FindBin(peakLow+0.01),histEE.FindBin(peakHigh-0.01))
                result[runRange.era]["peak_MM"] = histMM.Integral(histMM.FindBin(peakLow+0.01),histMM.FindBin(peakHigh-0.01))
                result[runRange.era]["peak_SF"] = result[runRange.era]["peak_EE"] + result[runRange.era]["peak_MM"]
                result[runRange.era]["peak_OF"] = histEM.Integral(histEM.FindBin(peakLow+0.01),histEM.FindBin(peakHigh-0.01))
                
                result[runRange.era]["peak_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(peakLow+0.01),histEENoMT2Cut.FindBin(peakHigh-0.01))
                result[runRange.era]["peak_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(peakLow+0.01),histMMNoMT2Cut.FindBin(peakHigh-0.01))
                result[runRange.era]["peak_NoMT2Cut_SF"] = result[runRange.era]["peak_NoMT2Cut_EE"] + result[runRange.era]["peak_NoMT2Cut_MM"]
                result[runRange.era]["peak_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(peakLow+0.01),histEMNoMT2Cut.FindBin(peakHigh-0.01))
                
                for massBin in massBins:
                        lowerEdge = getattr(mllBins,massBin).low
                        upperEdge = getattr(mllBins,massBin).high
                        
                        result[runRange.era][massBin+"_EE"] = histEE.Integral(histEE.FindBin(lowerEdge+0.01),histEE.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_MM"] = histMM.Integral(histMM.FindBin(lowerEdge+0.01),histMM.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_OF"] = histEM.Integral(histEM.FindBin(lowerEdge+0.01),histEM.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_SF"] = result[runRange.era][massBin+"_EE"]+result[runRange.era][massBin+"_MM"]
                        
                        result[runRange.era][massBin+"_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(lowerEdge+0.01),histEENoMT2Cut.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(lowerEdge+0.01),histMMNoMT2Cut.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(lowerEdge+0.01),histEMNoMT2Cut.FindBin(upperEdge-0.01))
                        result[runRange.era][massBin+"_NoMT2Cut_SF"] = result[runRange.era][massBin+"_NoMT2Cut_EE"]+result[runRange.era][massBin+"_NoMT2Cut_MM"]


                #~ for combination in ["EE","MM","SF"]:
                for combination in ["SF",]:
                        if isMC:
                                corr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.valMC
                                corrErr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.errMC
                        else:
                                corr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.val
                                corrErr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.err
                                
                        peak = result[runRange.era]["peak_%s"%combination] - result[runRange.era]["peak_OF"]*corr                   
                        peakErr = sqrt(result[runRange.era]["peak_%s"%combination] + result[runRange.era]["peak_OF"]*corr**2 + (result[runRange.era]["peak_OF"]*corrErr)**2)
                        
                        peakNoMT2Cut = result[runRange.era]["peak_NoMT2Cut_%s"%combination] - result[runRange.era]["peak_NoMT2Cut_OF"]*corr                 
                        peakNoMT2CutErr = sqrt(result[runRange.era]["peak_NoMT2Cut_%s"%combination] + result[runRange.era]["peak_NoMT2Cut_OF"]*corr**2 + (result[runRange.era]["peak_NoMT2Cut_OF"]*corrErr)**2)
                        
                        result[runRange.era]["corrected_peak_%s"%combination] = peak
                        result[runRange.era]["peak_Error%s"%combination] = peakErr
                        
                        result[runRange.era]["corrected_peak_NoMT2Cut_%s"%combination] = peakNoMT2Cut
                        result[runRange.era]["peak_NoMT2Cut_Error%s"%combination] = peakNoMT2CutErr
                        
                        result[runRange.era]["correction"] =  corr
                        result[runRange.era]["correctionErr"] =       corrErr

                        for massBin in massBins:
                                if massBin == "mass150To200" or massBin  == "mass200To300" or massBin  == "mass300To400" or massBin  == "mass400":
                                        relSyst = systematics.rOutIn[runRange.era].massAbove150.val           
                                elif massBin == "mass20To60" or massBin  == "mass60To86" or massBin  == "mass96To150":
                                        relSyst = systematics.rOutIn[runRange.era].massBelow150.val
                                        
                                corrYield =  result[runRange.era][massBin+"_"+combination] - result[runRange.era][massBin+"_"+"OF"]*corr
                                if corrYield > 0:
                                        corrYieldErr = sqrt(result[runRange.era][massBin+"_"+combination] + result[runRange.era][massBin+"_OF"]*corr**2 + (result[runRange.era][massBin+"_OF"]*corrErr)**2)
                                else:
                                        corrYield = 0
                                        corrYieldErr = 0
                                
                                result[runRange.era]["corrected_"+massBin+"_"+combination] = corrYield
                                result[runRange.era][massBin+"_Error"+combination] = corrYieldErr
                                
                                corrYieldNoMT2Cut =  result[runRange.era][massBin+"_NoMT2Cut_"+combination] - result[runRange.era][massBin+"_NoMT2Cut_"+"OF"]*corr                  
                                corrYieldNoMT2CutErr = sqrt(result[runRange.era][massBin+"_NoMT2Cut_"+combination] + result[runRange.era][massBin+"_NoMT2Cut_OF"]*corr**2 + (result[runRange.era][massBin+"_NoMT2Cut_OF"]*corrErr)**2)
                                
                                result[runRange.era]["corrected_"+massBin+"_NoMT2Cut_"+combination] = corrYieldNoMT2Cut
                                result[runRange.era][massBin+"_NoMT2Cut_Error"+combination] = corrYieldNoMT2CutErr
                                
                                if peak > 0:
                                        rOutIn = corrYield / peak
                                        rOutInSystErr = rOutIn * relSyst
                                        rOutInErr = sqrt( (corrYieldErr/peak)**2 + (corrYield*peakErr/peak**2)**2 )
                                else:
                                        rOutIn = 0
                                        rOutInSystErr = 0
                                        rOutInErr = 0

                                rOutInNoMT2Cut = corrYieldNoMT2Cut / peakNoMT2Cut
                                rOutInNoMT2CutSystErr = rOutInNoMT2Cut * relSyst
                                rOutInNoMT2CutErr = sqrt( (corrYieldNoMT2CutErr/peakNoMT2Cut)**2 + (corrYieldNoMT2Cut*peakNoMT2CutErr/peakNoMT2Cut**2)**2 )
                                
                                result[runRange.era]["rOutIn_"+massBin+"_"+combination] = rOutIn
                                result[runRange.era]["rOutIn_"+massBin+"_"+"Err"+combination] = rOutInErr
                                result[runRange.era]["rOutIn_"+massBin+"_"+"Syst"+combination] = rOutInSystErr

                                result[runRange.era]["rOutIn_"+massBin+"_NoMT2Cut_"+combination] = rOutInNoMT2Cut
                                result[runRange.era]["rOutIn_"+massBin+"_NoMT2Cut_"+"Err"+combination] = rOutInNoMT2CutErr
                                result[runRange.era]["rOutIn_"+massBin+"_NoMT2Cut_"+"Syst"+combination] = rOutInNoMT2CutSystErr
                                
                        saveLabel = additionalLabel
                        tmpLabel = additionalLabel
                        if isMC:
                                tmpLabel += "_MC"

                        histEMToPlot = histEM.Clone()
                        histEMToPlot.Scale(corr)
                        additionalLabel = tmpLabel
                        if combination == "EE":
                                plotMllSpectra(histEE.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
                        elif combination == "MM":       
                                plotMllSpectra(histMM.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
                        else:   
                                plotMllSpectra(histSF.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
                                

                        additionalLabel = saveLabel
                        
        if not combine: 
                result = result[runRanges[0].era]
        else:   
                first = True
                histoSF = None
                histoEE = None
                histoMM = None
                histoEM = None
                
                combined = {}
                
                combined["peak_EE"] = 0.0
                combined["peak_MM"] = 0.0
                combined["peak_SF"] = 0.0
                combined["peak_OF"] = 0.0
                
                combined["peak_NoMT2Cut_EE"] = 0.0
                combined["peak_NoMT2Cut_MM"] = 0.0
                combined["peak_NoMT2Cut_SF"] = 0.0
                combined["peak_NoMT2Cut_OF"] = 0.0
                
                corr = 0
                corrErr = 0
                
                for runRange in runRanges:
                        combined["peak_EE"] += result[runRange.era]["peak_EE"] 
                        combined["peak_MM"] += result[runRange.era]["peak_MM"] 
                        combined["peak_SF"] += result[runRange.era]["peak_SF"] 
                        combined["peak_OF"] += result[runRange.era]["peak_OF"] 
                        
                        combined["peak_NoMT2Cut_EE"] += result[runRange.era]["peak_NoMT2Cut_EE"]
                        combined["peak_NoMT2Cut_MM"] += result[runRange.era]["peak_NoMT2Cut_MM"]
                        combined["peak_NoMT2Cut_SF"] += result[runRange.era]["peak_NoMT2Cut_SF"]
                        combined["peak_NoMT2Cut_OF"] += result[runRange.era]["peak_NoMT2Cut_OF"]
                        
                        if isMC:
                                corr    += getattr(corrections[runRange.era],"rSFOF").inclusive.valMC/(getattr(corrections[runRange.era],"rSFOF").inclusive.errMC)**2
                                corrErr += 1.0/getattr(corrections[runRange.era],"rSFOF").inclusive.errMC**2
                        else:
                                corr    += getattr(corrections[runRange.era],"rSFOF").inclusive.val/(getattr(corrections[runRange.era],"rSFOF").inclusive.err)**2
                                corrErr += 1.0/getattr(corrections[runRange.era],"rSFOF").inclusive.err**2
                
                corr = corr/corrErr
                corrErr = 1/ (corrErr)**0.5
                
                peak = 0;
                peakErr = 0;
                peakNoMT2Cut = 0;
                peakNoMT2CutErr = 0;
                for runRange in runRanges:
                        peak += result[runRange.era]["corrected_peak_SF"]
                        peakErr += (result[runRange.era]["peak_ErrorSF"])**2
                        
                        peakNoMT2Cut += result[runRange.era]["corrected_peak_NoMT2Cut_SF"]
                        peakNoMT2CutErr += (result[runRange.era]["peak_NoMT2Cut_ErrorSF"])**2
                        
                peakErr = (peakErr)**0.5        
                peakNoMT2CutErr = (peakNoMT2CutErr)**0.5        
                
                
                #peak = combined["peak_SF"] - combined["peak_OF"]*corr                   
                #peakErr = sqrt(combined["peak_SF"] + combined["peak_OF"]*corr**2 + (combined["peak_OF"]*corrErr)**2)
                
                #peakNoMT2Cut = combined["peak_NoMT2Cut_SF"] - combined["peak_NoMT2Cut_OF"]*corr                 
                #peakNoMT2CutErr = sqrt(combined["peak_NoMT2Cut_SF"] + combined["peak_NoMT2Cut_OF"]*corr**2 + (combined["peak_NoMT2Cut_OF"]*corrErr)**2)
                
                combined["corrected_peak_SF"] = peak
                combined["peak_ErrorSF"] = peakErr
                
                combined["corrected_peak_NoMT2Cut_SF"] = peakNoMT2Cut
                combined["peak_NoMT2Cut_ErrorSF"] = peakNoMT2CutErr
                
                combined["correction"] =  corr
                combined["correctionErr"] =       corrErr
                
                        
                for massBin in massBins:
                        combined[massBin+"_EE"] = 0.0
                        combined[massBin+"_MM"] = 0.0
                        combined[massBin+"_OF"] = 0.0
                        combined[massBin+"_SF"] = 0.0
                        
                        combined[massBin+"_NoMT2Cut_EE"] = 0.0
                        combined[massBin+"_NoMT2Cut_MM"] = 0.0
                        combined[massBin+"_NoMT2Cut_OF"] = 0.0
                        combined[massBin+"_NoMT2Cut_SF"] = 0.0
                        for runRange in runRanges:
                                combined[massBin+"_EE"] += result[runRange.era][massBin+"_EE"] 
                                combined[massBin+"_MM"] += result[runRange.era][massBin+"_MM"] 
                                combined[massBin+"_OF"] += result[runRange.era][massBin+"_OF"] 
                                combined[massBin+"_SF"] += result[runRange.era][massBin+"_SF"] 

                                combined[massBin+"_NoMT2Cut_EE"] += result[runRange.era][massBin+"_NoMT2Cut_EE"]
                                combined[massBin+"_NoMT2Cut_MM"] += result[runRange.era][massBin+"_NoMT2Cut_MM"]
                                combined[massBin+"_NoMT2Cut_OF"] += result[runRange.era][massBin+"_NoMT2Cut_OF"]
                                combined[massBin+"_NoMT2Cut_SF"] += result[runRange.era][massBin+"_NoMT2Cut_SF"]

                        if massBin == "mass150To200" or massBin  == "mass200To300" or massBin  == "mass300To400" or massBin  == "mass400":
                                relSyst = systematics.rOutIn["combined"].massAbove150.val           
                        elif massBin == "mass20To60" or massBin  == "mass60To86" or massBin  == "mass96To150":
                                relSyst = systematics.rOutIn["combined"].massBelow150.val
                                
                        corrYield =  combined[massBin+"_SF"] - combined[massBin+"_"+"OF"]*corr
                        if corrYield > 0:
                                corrYieldErr = sqrt(combined[massBin+"_SF"] + combined[massBin+"_OF"]*corr**2 + (combined[massBin+"_OF"]*corrErr)**2)
                        else:
                                corrYield = 0
                                corrYieldErr = 0
                        
                        combined["corrected_"+massBin+"_SF"] = corrYield
                        combined[massBin+"_ErrorSF"] = corrYieldErr
                        
                        corrYieldNoMT2Cut =  combined[massBin+"_NoMT2Cut_SF"] - combined[massBin+"_NoMT2Cut_"+"OF"]*corr                  
                        corrYieldNoMT2CutErr = sqrt(combined[massBin+"_NoMT2Cut_SF"] + combined[massBin+"_NoMT2Cut_OF"]*corr**2 + (combined[massBin+"_NoMT2Cut_OF"]*corrErr)**2)
                        
                        combined["corrected_"+massBin+"_NoMT2Cut_SF"] = corrYieldNoMT2Cut
                        combined[massBin+"_NoMT2Cut_ErrorSF"] = corrYieldNoMT2CutErr
                        
                        if peak > 0:
                                rOutIn = corrYield / peak
                                rOutInSystErr = rOutIn * relSyst
                                rOutInErr = sqrt( (corrYieldErr/peak)**2 + (corrYield*peakErr/peak**2)**2 )
                        else:
                                rOutIn = 0
                                rOutInSystErr = 0
                                rOutInErr = 0

                        rOutInNoMT2Cut = corrYieldNoMT2Cut / peakNoMT2Cut
                        rOutInNoMT2CutSystErr = rOutInNoMT2Cut * relSyst
                        rOutInNoMT2CutErr = sqrt( (corrYieldNoMT2CutErr/peakNoMT2Cut)**2 + (corrYieldNoMT2Cut*peakNoMT2CutErr/peakNoMT2Cut**2)**2 )
                        
                        combined["rOutIn_"+massBin+"_SF"] = rOutIn
                        combined["rOutIn_"+massBin+"_"+"ErrSF"] = rOutInErr
                        combined["rOutIn_"+massBin+"_"+"SystSF"] = rOutInSystErr

                        combined["rOutIn_"+massBin+"_NoMT2Cut_SF"] = rOutInNoMT2Cut
                        combined["rOutIn_"+massBin+"_NoMT2Cut_"+"ErrSF"] = rOutInNoMT2CutErr
                        combined["rOutIn_"+massBin+"_NoMT2Cut_"+"SystSF"] = rOutInNoMT2CutSystErr
                
                
                for era, hist in hists.iteritems(): 
                        if first:
                                histoSF = hist["SF"].Clone()
                                histoEE = hist["EE"].Clone()
                                histoMM = hist["MM"].Clone()
                                histoEM = hist["EM"].Clone()
                                first = False
                        else:
                                histoSF.Add(hist["SF"], 1)
                                histoEE.Add(hist["EE"], 1)
                                histoMM.Add(hist["MM"], 1)
                                histoEM.Add(hist["EM"], 1)
                
                saveLabel = additionalLabel
                tmpLabel = additionalLabel
                if isMC:
                        tmpLabel += "_MC"

                histEMToPlot = histoEM.Clone()
                histEMToPlot.Scale(corr)
                additionalLabel = tmpLabel

                plotMllSpectra(histoSF.Clone(),histEMToPlot,runRanges,selection,combination,cmsExtra,additionalLabel)
                additionalLabel = saveLabel
                
                result = combined
                
                
        return result
        
        
#def centralValues(selection,runRange,isMC,backgrounds,cmsExtra,additionalLabel=""):                        
#        
#        massBins = ["mass20To60","mass60To86","mass96To150","mass150To200","mass200To300","mass300To400","mass400","edgeMass","highMass","lowMass"]
#        
#        if "Forward" in selection.name:
#                region = "forward"
#        elif "Central" in selection.name:
#                region = "central"
#        else:           
#                region = "inclusive"            
#
#        plot = getPlot("mllPlotROutIn")
#        plot.addRegion(selection)
#        plot.cleanCuts()
#        plot.addRunRange(runRange)
#        #plot.cuts = plot.cuts % runRange.runCut 
#        plot.cuts = plot.cuts.replace("mll","p4.M()")
#        plot.cuts = plot.cuts.replace("pt > 25","p4.Pt() > 25")
#        #~ if additionalLabel != "":
#        #~ plot.cuts = plot.cuts.replace("MT2 > 80 &&","")
#        plot.variable = plot.variable.replace("mll","p4.M()")   
#        if      plot.variable == "pt":
#                plot.variable = plot.variable.replace("pt","p4.Pt()")
#                
#        print plot.cuts
#
#        plotNoMT2Cut = getPlot("mllPlotROutIn")
#        plotNoMT2Cut.addRegion(selection)
#        plotNoMT2Cut.cleanCuts()
#        #plotNoMT2Cut.cuts = plotNoMT2Cut.cuts % runRange.runCut 
#        plotNoMT2Cut.addRunRange(runRange) 
#        plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("mll","p4.M()")
#        plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("pt > 25","p4.Pt() > 25")
#        plotNoMT2Cut.cuts = plotNoMT2Cut.cuts.replace("MT2 > 80 &&","")
#        plotNoMT2Cut.variable = plotNoMT2Cut.variable.replace("mll","p4.M()")
#        if      plotNoMT2Cut.variable == "pt":
#                plotNoMT2Cut.variable = plotNoMT2Cut.variable.replace("pt","p4.Pt()")
#
#        histEE, histMM, histEM = getHistograms(plot,runRange,isMC,backgrounds,region)
#        histSF = histEE.Clone("histSF")
#        histSF.Add(histMM.Clone())
#        
#        histEENoMT2Cut, histMMNoMT2Cut, histEMNoMT2Cut = getHistograms(plotNoMT2Cut,runRange,isMC,backgrounds,region)
#        histSFNoMT2Cut = histEENoMT2Cut.Clone("histSFNoMT2Cut")
#        histSFNoMT2Cut.Add(histMMNoMT2Cut.Clone())
#        
#        result = {}
#        
#        peakLow = mllBins.onZ.low
#        peakHigh = mllBins.onZ.high
#        
#        result["peak_EE"] = histEE.Integral(histEE.FindBin(peakLow+0.01),histEE.FindBin(peakHigh-0.01))
#        result["peak_MM"] = histMM.Integral(histMM.FindBin(peakLow+0.01),histMM.FindBin(peakHigh-0.01))
#        result["peak_SF"] = result["peak_EE"] + result["peak_MM"]
#        result["peak_OF"] = histEM.Integral(histEM.FindBin(peakLow+0.01),histEM.FindBin(peakHigh-0.01))
#        
#        result["peak_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(peakLow+0.01),histEENoMT2Cut.FindBin(peakHigh-0.01))
#        result["peak_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(peakLow+0.01),histMMNoMT2Cut.FindBin(peakHigh-0.01))
#        result["peak_NoMT2Cut_SF"] = result["peak_NoMT2Cut_EE"] + result["peak_NoMT2Cut_MM"]
#        result["peak_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(peakLow+0.01),histEMNoMT2Cut.FindBin(peakHigh-0.01))
#        
#        for massBin in massBins:
#                lowerEdge = getattr(mllBins,massBin).low
#                upperEdge = getattr(mllBins,massBin).high
#                
#                result[massBin+"_EE"] = histEE.Integral(histEE.FindBin(lowerEdge+0.01),histEE.FindBin(upperEdge-0.01))
#                result[massBin+"_MM"] = histMM.Integral(histMM.FindBin(lowerEdge+0.01),histMM.FindBin(upperEdge-0.01))
#                result[massBin+"_OF"] = histEM.Integral(histEM.FindBin(lowerEdge+0.01),histEM.FindBin(upperEdge-0.01))
#                result[massBin+"_SF"] = result[massBin+"_EE"]+result[massBin+"_MM"]
#                
#                result[massBin+"_NoMT2Cut_EE"] = histEENoMT2Cut.Integral(histEENoMT2Cut.FindBin(lowerEdge+0.01),histEENoMT2Cut.FindBin(upperEdge-0.01))
#                result[massBin+"_NoMT2Cut_MM"] = histMMNoMT2Cut.Integral(histMMNoMT2Cut.FindBin(lowerEdge+0.01),histMMNoMT2Cut.FindBin(upperEdge-0.01))
#                result[massBin+"_NoMT2Cut_OF"] = histEMNoMT2Cut.Integral(histEMNoMT2Cut.FindBin(lowerEdge+0.01),histEMNoMT2Cut.FindBin(upperEdge-0.01))
#                result[massBin+"_NoMT2Cut_SF"] = result[massBin+"_NoMT2Cut_EE"]+result[massBin+"_NoMT2Cut_MM"]
#        
#        
#        
#
#        #~ for combination in ["EE","MM","SF"]:
#        for combination in ["SF",]:
#                if isMC:
#                        corr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.valMC
#                        corrErr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.errMC
#                else:
#                        corr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.val
#                        corrErr = getattr(corrections[runRange.era],"r%sOF"%combination).inclusive.err
#                        
#                peak = result["peak_%s"%combination] - result["peak_OF"]*corr                   
#                peakErr = sqrt(result["peak_%s"%combination] + result["peak_OF"]*corr**2 + (result["peak_OF"]*corrErr)**2)
#                
#                peakNoMT2Cut = result["peak_NoMT2Cut_%s"%combination] - result["peak_NoMT2Cut_OF"]*corr                 
#                peakNoMT2CutErr = sqrt(result["peak_NoMT2Cut_%s"%combination] + result["peak_NoMT2Cut_OF"]*corr**2 + (result["peak_NoMT2Cut_OF"]*corrErr)**2)
#                
#                result["corrected_peak_%s"%combination] = peak
#                result["peak_Error%s"%combination] = peakErr
#                
#                result["corrected_peak_NoMT2Cut_%s"%combination] = peakNoMT2Cut
#                result["peak_NoMT2Cut_Error%s"%combination] = peakNoMT2CutErr
#                
#                result["correction"] =  corr
#                result["correctionErr"] =       corrErr
#
#                for massBin in massBins:
#                        if massBin == "mass150To200" or massBin  == "mass200To300" or massBin  == "mass300To400" or massBin  == "mass400":
#                                relSyst = systematics.rOutIn[runRange.era].massAbove150.val           
#                        elif massBin == "mass20To60" or massBin  == "mass60To86" or massBin  == "mass96To150":
#                                relSyst = systematics.rOutIn[runRange.era].massBelow150.val
#                        else:
#                                relSyst = systematics.rOutIn[runRange.era].old.val
#                                
#                        corrYield =  result[massBin+"_"+combination] - result[massBin+"_"+"OF"]*corr
#                        if corrYield > 0:
#                                corrYieldErr = sqrt(result[massBin+"_"+combination] + result[massBin+"_OF"]*corr**2 + (result[massBin+"_OF"]*corrErr)**2)
#                        else:
#                                corrYield = 0
#                                corrYieldErr = 0
#                        
#                        result["corrected_"+massBin+"_"+combination] = corrYield
#                        result[massBin+"_Error"+combination] = corrYieldErr
#                        
#                        corrYieldNoMT2Cut =  result[massBin+"_NoMT2Cut_"+combination] - result[massBin+"_NoMT2Cut_"+"OF"]*corr                  
#                        corrYieldNoMT2CutErr = sqrt(result[massBin+"_NoMT2Cut_"+combination] + result[massBin+"_NoMT2Cut_OF"]*corr**2 + (result[massBin+"_NoMT2Cut_OF"]*corrErr)**2)
#                        
#                        result["corrected_"+massBin+"_NoMT2Cut_"+combination] = corrYieldNoMT2Cut
#                        result[massBin+"_NoMT2Cut_Error"+combination] = corrYieldNoMT2CutErr
#                        
#                        if peak > 0:
#                                rOutIn = corrYield / peak
#                                rOutInSystErr = rOutIn * relSyst
#                                rOutInErr = sqrt( (corrYieldErr/peak)**2 + (corrYield*peakErr/peak**2)**2 )
#                        else:
#                                rOutIn = 0
#                                rOutInSystErr = 0
#                                rOutInErr = 0
#
#                        rOutInNoMT2Cut = corrYieldNoMT2Cut / peakNoMT2Cut
#                        rOutInNoMT2CutSystErr = rOutInNoMT2Cut * relSyst
#                        rOutInNoMT2CutErr = sqrt( (corrYieldNoMT2CutErr/peakNoMT2Cut)**2 + (corrYieldNoMT2Cut*peakNoMT2CutErr/peakNoMT2Cut**2)**2 )
#                        
#                        result["rOutIn_"+massBin+"_"+combination] = rOutIn
#                        result["rOutIn_"+massBin+"_"+"Err"+combination] = rOutInErr
#                        result["rOutIn_"+massBin+"_"+"Syst"+combination] = rOutInSystErr
#
#                        result["rOutIn_"+massBin+"_NoMT2Cut_"+combination] = rOutInNoMT2Cut
#                        result["rOutIn_"+massBin+"_NoMT2Cut_"+"Err"+combination] = rOutInNoMT2CutErr
#                        result["rOutIn_"+massBin+"_NoMT2Cut_"+"Syst"+combination] = rOutInNoMT2CutSystErr
#
#                
#                saveLabel = additionalLabel
#                tmpLabel = additionalLabel
#                if isMC:
#                        tmpLabel += "_MC"
#
#                histEMToPlot = histEM.Clone()
#                histEMToPlot.Scale(corr)
#                additionalLabel = tmpLabel
#                if combination == "EE":
#                        plotMllSpectra(histEE.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
#                elif combination == "MM":       
#                        plotMllSpectra(histMM.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
#                else:   
#                        plotMllSpectra(histSF.Clone(),histEMToPlot,[runRange,],selection,combination,cmsExtra,additionalLabel)
#                        
#
#                additionalLabel = saveLabel
#                
#
#
#
#
#        return result
def main():



        parser = argparse.ArgumentParser(description='R(out/in) measurements.')
        
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False,
                                                  help="Verbose mode.")
        parser.add_argument("-m", "--mc", action="store_true", dest="mc", default=False,
                                                  help="use MC, default is to use data.")
        parser.add_argument("-s", "--selection", dest = "selection" , action="append", default=[],
                                                  help="selection which to apply.")
        parser.add_argument("-p", "--plot", dest="plots", action="append", default=[],
                                                  help="select dependencies to study, default is all.")
        parser.add_argument("-r", "--runRange", dest="runRange", action="append", default=[],
                                                  help="name of run range.")
        parser.add_argument("-C", "--combine", action="store_true", dest="combine", default=False,
                                                  help="combine multiple run ranges into one plot")
        parser.add_argument("-c", "--centralValues", action="store_true", dest="central", default=False,
                                                  help="calculate R(out/in) central values")
        parser.add_argument("-b", "--backgrounds", dest="backgrounds", action="append", default=[],
                                                  help="backgrounds to plot.")
        parser.add_argument("-d", "--dependencies", action="store_true", dest="dependencies", default= False,
                                                  help="make dependency plots")         
        parser.add_argument("-x", "--private", action="store_true", dest="private", default=False,
                                                  help="plot is private work.") 
        parser.add_argument("-u", "--useExisting", action="store_true", dest="useExisting", default=False,
                                                  help="use existing values from pickles for dependency plots.")        
        parser.add_argument("-w", "--write", action="store_true", dest="write", default=False,
                                                  help="write results to central repository")   
                                        
        args = parser.parse_args()



        if len(args.backgrounds) == 0:
                args.backgrounds = backgroundLists.default
        if len(args.plots) == 0:
                args.plots = plotLists.rOutIn
        if len(args.selection) == 0:
                #args.selection.append(regionsToUse.rOutIn.central.name) 
                #args.selection.append(regionsToUse.rOutIn.forward.name) 
                args.selection.append(regionsToUse.rOutIn.inclusive.name)     
                
        if len(args.runRange) == 0:
                pass
                #args.runRange.append(RR.name)    

        if args.combine:
                args.runRange = [RR["2016"].name, RR["2017"].name ,RR["2018"].name]
        


        cmsExtra = ""
        if args.private:
                cmsExtra = "Private Work"
                if args.mc:
                        cmsExtra = "#splitline{Private Work}{Simulation}"
        elif args.mc:
                cmsExtra = "Simulation" 
        else:
                cmsExtra = "Preliminary"
        
        if not args.combine:
                for runRangeName in args.runRange:
                        runRange = getRunRange(runRangeName)
                        for selectionName in args.selection:
                                
                                selection = getRegion(selectionName)


                                if args.central:
                                        centralVal = centralValues(selection,[runRange,],args.mc,args.backgrounds,cmsExtra)
                                        if args.mc:
                                                outFilePkl = open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,runRange.label),"w")
                                        else:
                                                outFilePkl = open("shelves/rOutIn_%s_%s.pkl"%(selection.name,runRange.label),"w")
                                        pickle.dump(centralVal, outFilePkl)
                                        outFilePkl.close()
                                        
                                if args.dependencies:
                                         dependencies(selection,args.plots,[runRange,],args.mc,args.backgrounds,cmsExtra,args.useExisting)    
                                         
                                if args.write:
                                        import subprocess
                                        if args.mc:
                                                bashCommand = "cp shelves/rOutIn_%s_%s_MC.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)               
                                        else:   
                                                bashCommand = "cp shelves/rOutIn_%s_%s.pkl %s/shelves"%(selection.name,runRange.label,pathes.basePath)
                                        process = subprocess.Popen(bashCommand.split())                                                                         
        else:
                runRanges = [getRunRange(runRangeName) for runRangeName in args.runRange]
                for selectionName in args.selection:
                        selection = getRegion(selectionName)
                        
                        if args.central:
                                centralVal = centralValues(selection,runRanges,args.mc,args.backgrounds,cmsExtra, combine=True)
                                if args.mc:
                                        outFilePkl = open("shelves/rOutIn_%s_%s_MC.pkl"%(selection.name,"Combined"),"w")
                                else:
                                        outFilePkl = open("shelves/rOutIn_%s_%s.pkl"%(selection.name,"Combined"),"w")
                                pickle.dump(centralVal, outFilePkl)
                                outFilePkl.close()
                        
                        if args.dependencies:
                                dependencies(selection,args.plots,runRanges,args.mc,args.backgrounds,cmsExtra,args.useExisting, combine=True)    
                                        
                        
                        if args.write:
                                import subprocess
                                if args.mc:
                                        bashCommand = "cp shelves/rOutIn_%s_%s_MC.pkl %s/shelves"%(selection.name,"Combined",pathes.basePath)               
                                else:   
                                        bashCommand = "cp shelves/rOutIn_%s_%s.pkl %s/shelves"%(selection.name,"Combined",pathes.basePath)
                                process = subprocess.Popen(bashCommand.split())
                        
                        
main()
