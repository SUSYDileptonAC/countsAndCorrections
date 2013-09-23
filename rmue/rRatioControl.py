#!/usr/bin/env python
 # -*- coding: latin-1 -*-
 
import ROOT
from math import sqrt
from src.nurRatio import RatioPlots
from src.messageLogger import messageLogger as log
from src.processes import SubProcesses7TeV, SubProcesses8TeV, Processes7TeV, Processes8TeV, TreePaths, Trees
from src.defs import Cuts, Colors, Titles, Constants, UnderLegendAnnotation, Lumi8TeVAnnotation1, Lumi8TeVAnnotation2, Lumi8TeVAnnotation3, RatioAnnotation, Lumi8TeVAnnotationMll1, Lumi8TeVAnnotationMll2, Lumi8TeVAnnotationMll3
from src.treeTools import getEntriesFromTree, getHistoFromProcess, getEntriesFromProcesses
from src.plotTools import histoStack, save, legende, setPalette, histosqrt, makeAnnotation
import src.Styles as Styles
from src.latexTabelle import tableEnvironment, tabular
from array import array
from ROOT import TMath

modifiers = {"SS":["chargeProduct==-1","chargeProduct==1"],
			 "IsoSideBand":["&& id1 < 0.15 && id2 < 0.15","&& id1 > 0.15 && id2 > 0.15 && id1 < 1 && id2 < 1"],
			 "Central":["abs(eta1) < 2.4 && abs(eta2) < 2.4","abs(eta1) < 1.4 && abs(eta2) < 1.4"],
			 "Forward":["abs(eta1) < 2.4 && abs(eta2) < 2.4","1.6<=TMath::Max(abs(eta1),abs(eta2)) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) )"],
			 "BothEndcap":["abs(eta1) < 2.4 && abs(eta2) < 2.4","abs(eta1) > 1.6 && abs(eta2) > 1.6"],
			 "BothVeryEndcap":["abs(eta1) < 2.4 && abs(eta2) < 2.4","abs(eta1) > 1.6 && abs(eta2) > 1.6"],
			 "ExcludingGap":["abs(eta1) < 2.4 && abs(eta2) < 2.4","((abs(eta1) < 1.442) || (abs(eta1) > 1.56 && abs(eta1) < 2.4)) && ((abs(eta2) < 1.442) || (abs(eta2) > 1.56 && abs(eta2) < 2.4))"],
			}
centralValues = {"SS":0.2,
				 "IsoSideBand":1.0,
				 "Central":1.089,
				 "Forward":1.188,
				 "BothEndcap":1.34,
				 "BothVeryEndcap":1.163,
				 "ExcludingGap":1.155,
				}
relUncertainties = {"SS":0.1,
				 "IsoSideBand":0.1,
				 "Central":0.1,
				 "Forward":0.15,
				 "BothEndcap":0.15,
				 "BothVeryEndcap":0.15,
				 "ExcludingGap":0.1,
				 "default":0.1,
				}


class Ratio_nJets_MC(): #nJets
	variable = "nJets"
	filename = "r-Abh_nJets"
	cut=Cuts.basicOhneNJetPlusInvMassPlusMet50Cut
	binning=[i-0.5 for i in range(0,8)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.nJets
	xMin=-0.5
	xMax=8
class Ratio_nJets_Data():
	variable = "nJets"
	filename = "r-Abh_nJets_Data"
	cut=Cuts.basicOhneNJetPlusInvMassPlusMet50Cut
	binning=[i-0.5 for i in range(0,8)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.nJets
	xMin=-0.5
	xMax=8

class Ratio_nVertices_MC(): #nVertices
	variable = "nVertices"
	filename = "r-Abh_nVertices"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	#binning=[i-0.5 for i in range(0,15)] #7TeV
	binning=range(0,10,2)+range(10,30,2)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.nVertices
	xMin=-0.5
	xMax=30
class Ratio_nVertices_Data():
	variable = "nVertices"
	filename = "r-Abh_nVertices_Data"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	#binning=[i-0.5 for i in range(0,15)] #7TeV
	binning=range(0,10,2)+range(10,30,2)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.nVertices
	xMin=-0.5
	xMax=30

class Ratio_id1_MC(): #id1
	variable = "id1"
	filename = "r-Abh_id1"
	cut=Cuts.basicPlusInvMassPlusMet50Cut+" && id2 < 0.05"
	binning=[-0.01+i*0.01 for i in range(0,17)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.id1
	xMin=0.
	xMax=0.16
class Ratio_id1_Data():
	variable="id1"
	filename = "r-Abh_id1_Data"
	cut=Cuts.basicPlusInvMassPlusMet50Cut+" && id2 < 0.05"
	binning=[-0.01+i*0.01 for i in range(0,17)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.id1
	xMin=0.
	xMax=0.16

class Ratio_id2_MC(): #id2
	variable = "id2"
	filename = "r-Abh_id2"
	cut=Cuts.basicPlusInvMassPlusMet50Cut+" && id1 < 0.05"
	binning=[-0.01+i*0.01 for i in range(0,17)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.id2
	xMin=0.
	xMax=0.16
class Ratio_id2_Data():
	variable="id2"
	filename = "r-Abh_id2_Data"
	cut=Cuts.basicPlusInvMassPlusMet50Cut+" && id1 < 0.05"
	binning=[-0.01+i*0.01 for i in range(0,17)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.id2
	xMin=0.
	xMax=0.16

class Ratio_id1_002_MC(): #id1 bis 0.02
	variable = "id1"
	filename = "r-Abh_id1_002"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=[-0.01+i*0.0005 for i in range(0,80)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.id1
	xMin=0.
	xMax=0.015
class Ratio_id1_002_Data():
	variable="id1"
	filename = "r-Abh_id1_002_Data"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=[-0.01+i*0.0005 for i in range(0,80)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.id1
	xMin=0.
	xMax=0.015

class Ratio_id2_002_MC(): #id2 bis 0.02
	variable = "id2"
	filename = "r-Abh_id2_002"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=[-0.01+i*0.0005 for i in range(0,80)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.id2
	xMin=-0.
	xMax=0.015
class Ratio_id2_002_Data():
	variable="id2"
	filename = "r-Abh_id2_002_Data"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=[-0.01+i*0.0005 for i in range(0,80)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.id2
	xMin=0.
	xMax=0.015

class Ratio_ht_MC(): # H_t
	variable = "ht"
	filename = "r-AbhHt"
	binning=[i-0.5 for i in range(0,8)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.nJets
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=range(0,300,50)+range(300,800,100)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.ht
	xMin=0
	xMax=800
class Ratio_ht_Data():
	variable = "ht"
	filename = "r-AbhHtData"
	cut=Cuts.basicPlusInvMassPlusMet50Cut
	binning=range(0,300,50)+range(300,800,100)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.ht
	xMin=0
	xMax=800

class Ratio_pt_MC(): # p_t1
	variable = "pt1"
	filename = "r-Abhpt"
	cut=Cuts.basicCutOhnePt
	#binning=range(0,60,20)+range(60,100,5) # 7TeV
	binning=range(20,30,5)+range(30,60,5)+range(60,100,10)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.pt1
	xMin=0
	xMax=100
class Ratio_pt_Data():
	variable = "pt1"
	filename = "r-AbhptData"
	cut=Cuts.basicCutOhnePt
	#binning=range(0,60,20)+range(60,100,5) # 7TeV
	binning=range(20,30,5)+range(30,60,5)+range(60,100,10)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.pt1
	xMin=0
	xMax=100
	
class Ratio_pt2_MC(): # p_t1
	variable = "pt2"
	filename = "r-Abhpt2"
	cut=Cuts.basicPlusInvMassCut
	#binning=range(0,60,20)+range(60,100,5) # 7TeV
	binning=range(20,30,5)+range(30,60,5)+range(60,100,10)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.pt2
	xMin=0
	xMax=100
class Ratio_pt2_Data():
	variable = "pt2"
	filename = "r-Abhpt2Data"
	cut=Cuts.basicPlusInvMassCut
	#binning=range(0,60,20)+range(60,100,5) # 7TeV
	binning=range(20,30,5)+range(30,60,5)+range(60,100,10)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.pt2
	xMin=0
	xMax=100

class Ratio_DeltaR_MC(): #m_ll
	variable = "deltaR"
	filename = "r-AbhDeltaR"
	cut=Cuts.basicCutNoDeltaR
	#binning=range(15,255,5)
	binning=[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis="#DeltaR"
	xMin=0.
	xMax=5.
class Ratio_DeltaR_MCZ(): #m_ll
	variable = "deltaR"
	filename = "r-AbhDeltaR"
	cut=Cuts.basicCutNoDeltaR
	#binning=range(15,255,5)
	binning=[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.ZJets]
	xaxis="#DeltaR"
	xMin=0.
	xMax=5.
class Ratio_DeltaR_Data(): #m_ll
	variable = "deltaR"
	filename = "r-AbhDeltaR"
	cut=Cuts.basicCutNoDeltaR
	#binning=range(15,255,5)
	binning=[0.2*i for i in range(10)]+[2+0.5*i for i in range(7)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="#DeltaR"
	xMin=0.
	xMax=5.


class Ratio_p4M_MC(): #m_ll
	variable = "p4.M()"
	filename = "r-Abhp4M"
	cut=Cuts.basicCut
	#binning=range(15,255,5)
	binning=range(20,60,20)+range(60,120,20)+range(120,270,30)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.p4M
	xMin=15
	xMax=240
class Ratio_p4M_MCSS(): #m_ll
	variable = "p4.M()"
	filename = "r-Abhp4MSS"
	cut=Cuts.basicCutSS
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_MCControlSS(): #m_ll
	variable = "p4.M()"
	filename = "r-Abhp4MSS"
	cut=Cuts.commonControlRegionSS
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_MCIsoSideband(): #m_ll
	variable = "p4.M()"
	filename = "r-Abhp4MIsoSideband"
	cut=Cuts.basicCutIsoSideband
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis="m_{ll}^{Non-Iso} [GeV]"
	xMin=15
	xMax=250
class Ratio_p4M_MCZ(): #m_ll nur DY
	variable = "p4.M()"
	filename = "r-Abhp4M"
	cut=Cuts.basicCut
	#	binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.ZJets]
	xaxis=Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_MCtt(): #m_ll nur tt
	variable = "p4.M()"
	filename = "r-Abhp4M"
	cut=Cuts.basicCut
#	binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_Data():
	variable = "p4.M()"
	filename = "r-Abhp4MData"
	cut=Cuts.basicCut
	#binning=range(15,255,5)
	binning=range(20,60,20)+range(60,120,20)+range(120,270,30)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.p4M
	xMin=15
	xMax=240
class Ratio_p4M_DataSS():
	variable = "p4.M()"
	filename = "r-Abhp4MDataSS"
	cut=Cuts.basicCutSS
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_DataControlSS():
	variable = "p4.M()"
	filename = "r-Abhp4MDataControlSS"
	cut=Cuts.commonControlRegionSS
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.p4M
	xMin=15
	xMax=250
class Ratio_p4M_DataIsoSideband():
	variable = "p4.M()"
	filename = "r-Abhp4MDataIsoSideband"
	cut=Cuts.basicCutIsoSideband
	#binning=range(15,255,5)
	binning=range(20,60,10)+range(60,120,10)+range(120,250,25)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="m_{ll}^{Non-Iso} [GeV] from data"
	xMin=15
	xMax=250

class Ratio_nBJets_MC(): #nBJets
	variable = "nBJets"
	filename = "r-AbhNBJets"
	cut=Cuts.basicOhneNJetPlusInvMassPlusMet50Cut
	binning=[i-0.5 for i in range(0,6)]
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis=Titles.nBJets
	xMin=-0.5
	xMax=6
class Ratio_nBJets_Data():
	variable = "nBJets"
	filename = "r-AbhNBJetsData"
	cut=Cuts.basicOhneNJetPlusInvMassPlusMet50Cut
	binning=[i-0.5 for i in range(0,6)]
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.nBJets
	xMin=-0.5
	xMax=6

class Ratio_met_MC(): #MET
	variable = "met"
	filename = "r-AbhMet"
	cut=Cuts.basicPlusInvMassCut
	binning= range(0,100,10)+range(100,150,25)+range(150,250,50)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis="%s" %Titles.met
	xMin=0
	xMax=200
class Ratio_met_Data():
	variable = "met"
	filename = "r-AbhMetData"
	cut=Cuts.basicPlusInvMassCut
	binning= range(0,100,10)+range(100,150,25)+range(150,250,50)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis="%s from data" %Titles.met
	xMin=0
	xMax=200
class Ratio_met_MC_tt(): #MET nur tt
	variable = "met"
	filename = "r-AbhMet"
	cut=Cuts.basicPlusInvMassCut
	binning= range(0,100,10)+range(100,150,25)+range(150,250,50)
	processes=[Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV=[Processes8TeV.TTJets]
	xaxis="%s" %Titles.met
	xMin=0
	xMax=200

	
class Ratio_eta1_MC(): # eta1 (eta mit zweitgroeßtem Leptonimpuls)
	variable = "eta1"
	filename = "r-Abh_eta1"
	cut = Cuts.basicPlusInvMassPlusMet50Cut
	binning = [i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)] #*0.3132+1.566 for i in range(0,10)
	processes = [Processes7TeV.TTJets, Processes7TeV.ZJets,Processes7TeV.SingleT,Processes7TeV.DiBoson]
	processes8TeV = [Processes8TeV.TTJets]
	xaxis = "%s" %Titles.eta1
	xMin = 0
	xMax = 2.55
class Ratio_eta1_Data():
	variable = "eta1"
	filename = "r-Abh_eta1"
	cut = Cuts.basicPlusInvMassPlusMet50Cut
	binning = [i*0.14 for i in range(0,10)]+[i*0.2+1.4 for i in range(0,6)] #*0.3132+1.566 for i in range(0,10)
	processes=[Processes7TeV.Data]
	processes8TeV=[Processes8TeV.Data]
	xaxis = "%s" %Titles.eta1
	xMin = 0
	xMax = 2.55


def rRatioAll(plot,selectionModifier,isinput=False): #Tool, wird in rRatioDataVsMC verwendet
	log.outputLevel=5
#	SubProcesses7TeV.dataPath = "../Daten/"
#	SubProcesses8TeV.dataPath = "../Daten/"
	plotpath="fig/"
	rootContainer = []
	style=Styles.tdrStyle()
	style.SetPadRightMargin(0.1)
	style.SetTitleYOffset(0.9)
	setPalette()
	c1= ROOT.TCanvas("c1","c1",1024,768)

	histoEE=[]
	histoMM=[]
	for histList, ll in [(histoEE, Trees.ee), (histoMM,Trees.mumu)]:
		for process in plot.processes8TeV:
			histo = getHistoFromProcess(process, plot.variable, plot.cut, ll, len(plotMC.binning)-1, plot.binning, xMax=None)
			#getHistoFromTree(fileName, treePath, variable, cut, binning, treeType)
			histList.append(histo)

	c1.DrawFrame(plot.xMin,0.8,plot.xMax,1.6,"; %s; r_{#mue}" %plot.xaxis)	
	rplots = RatioPlots(histoMM,histoEE)
	r = rplots.globalRatio()
	rsqrt = histosqrt(r)
	rsqrt.Draw("hist ep same")
	c1.RedrawAxis()
	c1.Update()
	save(c1, plotpath, plot.filename)
	
	if isinput==True:
		raw_input("press enter to continue")

def rRatioDataVsMC(plotMC, plotData, variante=2,selectionModifier=[], isinput=False): #Ratio-Plots
	log.outputLevel=5
#	SubProcesses7TeV.dataPath = "../Daten/"
#	SubProcesses8TeV.dataPath = "../Daten/"
	plotpath="fig/"
	
	rootContainer = []
	style=Styles.tdrStyle()
	style.SetPadRightMargin(0.1)
	style.SetTitleYOffset(0.9)
	setPalette()
	c1= ROOT.TCanvas("c1","c1",1024,768)

	xMin = 0
	xMax = 1.
	xaxis = ""
	nameModifier = "_"
	if len(selectionModifier) >0:
		for modifier in selectionModifier:
			if plotData != None:			
				plotData.cut = plotData.cut.replace(modifiers[modifier][0],modifiers[modifier][1])
			if plotMC != None:	
				plotMC.cut = plotMC.cut.replace(modifiers[modifier][0],modifiers[modifier][1])
			nameModifier = nameModifier+modifier	
			
	# Trees einlesen
	if plotMC != None:
		histoEMC=[]
		histoMMC=[]
		for histList, ll in [(histoEMC, Trees.ee), (histoMMC,Trees.mumu)]:
			for process in plotMC.processes8TeV:
				histo = getHistoFromProcess(process, plotMC.variable, plotMC.cut, ll, len(plotMC.binning)-1, plotMC.binning, xMax=None)
				histList.append(histo)
		xMin = plotMC.xMin
		xMax = plotMC.xMax
		xaxis = plotMC.xaxis
		variable = plotMC.variable

	if plotData != None:
		histoEData=[]
		histoMData=[]
		for histList, ll in [(histoEData, Trees.ee), (histoMData,Trees.mumu)]:
			for process in plotData.processes8TeV:
				histo = getHistoFromProcess(process, plotData.variable, plotData.cut, ll,  len(plotData.binning)-1, plotData.binning, xMax=None)
				histList.append(histo)
		if plotMC == None:
			xMin = plotData.xMin
			xMax = plotData.xMax
			xaxis = plotData.xaxis
			variable = plotData.variable


	centralValue = 1.2057
	relUncertainty = 0.1
	if len(selectionModifier) == 1: 
		centralValue = centralValues[selectionModifier[0]]
		relUncertainty = relUncertainties[selectionModifier[0]]
		


	#Variante 1 = mit slope
	if variante==1: 
		filename="8TeVrRatioDataVsMCControl_slope_%s" %plotMC.variable
		linearMC = ROOT.TF1("linear", "[0]+[1]*x", xMin , xMax)
		linearMC.SetLineColor(Colors.mc)
		linearData = ROOT.TF1("linear", "[0]+[1]*x", xMin , xMax)
		linearData.SetLineColor(Colors.data)
		if plotMC==Ratio_id2_002_MC:
			filename="8TeVrRatioDataVsMCControl_id2_002"
		elif plotMC==Ratio_id1_002_MC:
			filename="8TeVrRatioDataVsMCControl_id1_002"
		elif plotMC==Ratio_p4M_MC:
			filename="8TeVrRatioDataVsMCControl_mll"
		elif plotMC==Ratio_p4M_MCtt:
			filename="8TeVrRatioDataVsMCControl_mll_tt"
		elif plotMC==Ratio_p4M_MCZ:
			filename="8TeVrRatioDataVsMCControl_mll_Z"
	
	# variante 2 = ohne slope
	elif variante==2:
		filename="8TeVrRatioDataVsMCControl_%s" %variable
		linearMC = ROOT.TF1("linear", "[0]", xMin , xMax)
		linearMC.SetLineColor(Colors.mc)
		linearData = ROOT.TF1("linear", "[0]", xMin , xMax)
		linearData.SetLineColor(Colors.data)
		if plotMC==Ratio_id2_002_MC:
			filename="8TeVrRatioDataVsMCControl_2_id2_002"
		elif plotMC==Ratio_id1_002_MC:
			filename="8TeVrRatioDataVsMCControl_2_id1_002"
		elif plotMC==Ratio_p4M_MC:
			filename="8TeVrRatioDataVsMCControl_mll"
		elif plotMC==Ratio_met_MC_tt:
			filename = "8TeVrRatioDataVsMCControl_met-tt"
		elif plotMC==Ratio_p4M_MCtt:
			filename="8TeVrRatioDataVsMCControl_mll_tt"
		elif plotMC==Ratio_p4M_MCZ:
			filename="8TeVrRatioDataVsMCControl_mll_Z"
		elif plotMC==Ratio_DeltaR_MCZ:
			filename="8TeVrRatioDataVsMCControl_DeltaR_Z"
		elif plotMC==Ratio_p4M_MCSS:
			filename="8TeVrRatioDataVsMCControl_mll_SS"
		elif plotMC==Ratio_p4M_MCIsoSideband:
			filename="8TeVrRatioDataVsMCControl_mll_IsoSideBand"
		elif plotMC==Ratio_p4M_MCControlSS:
			filename="8TeVrRatioDataVsMCControl_mll_SSControl"
	else:
		log.logError("Variante %s ungueltig! Waehle 1 fuer einen linearFit oder 2 fuer eine Horizontale." %variante)

	
	####################### Raw Inputs ##############################
	if plotData != None:	
		if len(histoMData) > 0:
			c1.DrawFrame(xMin,1,xMax,histoMData[0].GetBinContent(histoMData[0].GetMaximumBin())*10,"; %s; N_{Events}" %xaxis)

			latex = ROOT.TLatex()
			latex.SetTextSize(0.035)
			latex.SetNDC(True)
			latex.DrawLatex(0.15, 0.96, "CMS Preliminary  #sqrt{s} = 8 TeV,  #scale[0.6]{#int}Ldt = %s fb^{-1}"%(0.001*Constants.lumi8TeV))

			
			legend = ROOT.TLegend(0.65,0.7,0.9,0.9)
			legend.SetFillStyle(0)
			legend.SetBorderSize(0)	
			legend.AddEntry(histoMData[0],"#mu#mu events","p")
			legend.AddEntry(histoEData[0],"ee events","p")
			histoMData[0].SetMarkerColor(ROOT.kRed)
			histoMData[0].SetLineColor(ROOT.kRed)
			histoMData[0].Draw("samepe")
			histoEData[0].Draw("samepe")
			legend.Draw("same")
			ROOT.gPad.SetLogy(1)
			save(c1, plotpath, filename+"_RawInputsData")
			
			c1.Clear()
			ROOT.gPad.SetLogy(0)	
		####################### Fehlerband ##############################

	if plotMC==Ratio_p4M_MCControlSS or plotMC==Ratio_p4M_MCSS:
		c1.DrawFrame(xMin,0,xMax,1.7,"; %s; r_{#mue}" %xaxis)
	elif plotMC==Ratio_p4M_MCIsoSideband:
		c1.DrawFrame(xMin,0,xMax,5,"; %s; r_{#mue}" %xaxis)
	else:
		c1.DrawFrame(xMin,0.8,xMax,1.7,"; %s; r_{#mue}" %xaxis)

	x= array("f",[xMin, xMax]) 
 	#~ y= array("f", [1.175, 1.175]) # 1.237
 	y= array("f", [centralValue, centralValue]) # 1.237
   	ex= array("f", [0.,0.])
   	ey= array("f", [centralValue*relUncertainty, centralValue*relUncertainty])
   	ge= ROOT.TGraphErrors(2, x, y, ex, ey)
   	ge.SetFillColor(ROOT.kOrange-9)
   	ge.SetFillStyle(1001)
   	ge.SetLineColor(Colors.weiss)
   	ge.Draw("SAME 3")


	# Annotations

	#anno=makeAnnotation(RatioAnnotation, plotMC.cut)
	#~ lumianno1=makeAnnotation(Lumi8TeVAnnotationMll1)
	#~ lumianno2=makeAnnotation(Lumi8TeVAnnotationMll2)
	#~ lumianno3=makeAnnotation(Lumi8TeVAnnotationMll3)
	#anno.Draw("same")
	#~ lumianno1.Draw("SAME")
	#~ lumianno2.Draw("SAME")
	#~ lumianno3.Draw("SAME")
	latex = ROOT.TLatex()
	latex.SetTextSize(0.035)
	latex.SetNDC(True)
	if plotData != None:
		latex.DrawLatex(0.15, 0.96, "CMS Preliminary   #sqrt{s} = 8 TeV,  #scale[0.6]{#int}Ldt = %s fb^{-1}"%(0.001*Constants.lumi8TeV))
	else:
		latex.DrawLatex(0.15, 0.96, "CMS Private Work   #sqrt{s} = 8 TeV,  #scale[0.6]{#int}Ldt = %s fb^{-1}"%(0.001*Constants.lumi8TeV))




	if plotMC != None:
		rplotsMC = RatioPlots(histoMMC,histoEMC) # Ratio zw mu und e
		rMC = rplotsMC.globalRatio()
		rMCsqrt = histosqrt(rMC)

		# MC Farben etc setzen
		rMCsqrt.SetMarkerStyle(21)
		rMCsqrt.SetLineColor(ROOT.kGreen-2) 
		rMCsqrt.SetMarkerColor(ROOT.kGreen-2) 
		rMCsqrt.Draw("hist E1P SAME")
		rMCsqrt.Fit(linearMC,"nr","",20, xMax) #Fit
		
	
		# Data Farben etc setzen
		
		linearMC.SetLineWidth(2)
		linearMC.SetLineColor(ROOT.kBlack)
	else:
		linearMC = None
		
	#linearMC.Draw("SAME")

	rmueline= ROOT.TF1("rmueline","%f"%centralValue,xMin, xMax)
	rmueline.SetLineColor(ROOT.kOrange+3)
	rmueline.SetLineWidth(3)
	rmueline.SetLineStyle(2)
	rmueline.Draw("SAME")

	
	if plotData != None:
		rplotsData = RatioPlots(histoMData,histoEData)
		rData = rplotsData.globalRatio()
	
		rDatasqrt = histosqrt(rData)
		rDatasqrt.Fit(linearData, "nr","", 20, xMax)#Fit
		rDatasqrt.SetMarkerColor(Colors.data)
		rDatasqrt.SetLineColor(Colors.data)
		rDatasqrt.Draw("hist E1P SAME")
		linearData.SetLineColor(Colors.dataFit)
		linearData.SetLineWidth(2)
		#~ linearData.Draw("same")
   		
	# Legende
	
	leg = ROOT.TLegend(0.65,0.7,0.9,0.9)
	if plotData != None:
		leg.AddEntry(rDatasqrt, "Data", "p")
	if plotMC==Ratio_met_MC_tt or plotMC==Ratio_p4M_MCtt:
	   	leg.AddEntry(rMCsqrt,"t#bar{t} MC","p")
	elif plotMC==Ratio_p4M_MCZ:
		leg.AddEntry(rMCsqrt,"DY MC","p")
	elif plotMC!=None:
		leg.AddEntry(rMCsqrt,"t#bar{t} MC","p")  
  	leg.AddEntry(rmueline, "r_{#mu e}^{DY}", "l") 
  	leg.AddEntry(ge,"syst. unc. of r_{#mu e}","f")
	#leg.AddEntry(linearMC, "fitted constant b", "l") 
	
	
	leg.SetFillColor(ROOT.kWhite)
	leg.SetBorderSize(1)
	leg.SetLineWidth(2)
	leg.SetTextAlign(22)
	
	
	# Pfeile
	
	if plotMC == Ratio_eta1_MC:
		lineU1 = ROOT.TLine(1.4, 0., 1.4, 3.5)
		lineU1.SetLineColor(ROOT.kBlue-3)
		lineU1.SetLineWidth(2)
		lineU1.Draw("")
		lineU2 = ROOT.TLine(1.6, 0., 1.6, 3.5)
		lineU2.SetLineColor(ROOT.kBlue-3)
		lineU2.SetLineWidth(2)
		lineU2.Draw("")
		arrow1=ROOT.TArrow(1.5,1.5,1.6,1.5,0.01,"<|")
		arrow1.SetFillColor(ROOT.kBlue-3)
		arrow1.SetLineColor(ROOT.kBlue-3)
   		arrow1.SetLineWidth(3)
   		arrow1.Draw("")
   		arrow2=ROOT.TArrow(1.4,1.5,1.5,1.5,0.01,"|>")
		arrow2.SetFillColor(ROOT.kBlue-3)
		arrow2.SetLineColor(ROOT.kBlue-3)
   		arrow2.SetLineWidth(3)
   		arrow2.Draw("")

		lineE = ROOT.TLine(2.4, 0., 2.4, 3.0) #3.5 -> 1.7
		lineE.SetLineColor(ROOT.kRed-3)
		lineE.SetLineWidth(2)
		lineE.Draw("")
		#~ lineMu = ROOT.TLine(2.5, 0., 2.5, 3.0)
		#~ lineMu.SetLineColor(ROOT.kRed-3)
		#~ lineMu.SetLineWidth(2)
		#~ lineMu.Draw("")
		#~ arrow=ROOT.TArrow(2.3,1.5,2.4,1.5,0.02,"<|")
		#~ arrow.SetFillColor(ROOT.kRed-3)
		#~ arrow.SetLineColor(ROOT.kRed-3)
   		#~ arrow.SetLineWidth(3)
   		#~ arrow.Draw("")

	c1.RedrawAxis()
	leg.Draw("SAME")
	c1.Update()
	if len(selectionModifier) > 0:
		filename=filename+nameModifier
	save(c1, plotpath, filename)

	if isinput==True:
		raw_input("Press Enter to continue")
	return linearMC, linearData


def calculateRatio(cut, process,selectionModifier=[]): # berechnet rmue
	log.outputLevel=5
#	SubProcesses7TeV.dataPath = "../Daten/"
#	SubProcesses8TeV.dataPath = "../Daten/"
	variable = "p4.M()"
	if len(selectionModifier) >0:
		for modifier in selectionModifier:			
			cut = cut.replace(modifiers[modifier][0],modifiers[modifier][1])
	log.logHighlighted(cut)

	#Effizienzen
	
	effmumu=Constants.eff8TeVData_mumu
	effee=Constants.eff8TeVData_ee
	sigma_effmumu_p=Constants.sigma8TeVData_mumu_p
	sigma_effmumu_m=Constants.sigma8TeVData_mumu_m
	sigma_effee_p=Constants.sigma8TeVData_ee_p
	sigma_effee_m=Constants.sigma8TeVData_ee_m
	
   	anz_mumu, sigma_mumu= getEntriesFromProcesses(process, variable, cut, Trees.mumu)
	log.logHighlighted ("Anzahl mumu=%s /pm %s"%(anz_mumu, sigma_mumu)) #mit cut

	anz_ee, sigma_ee=getEntriesFromProcesses(process, variable, cut, Trees.ee)
	log.logHighlighted ("Anzahl ee = %s /pm %s"%(anz_ee, sigma_ee)) #mit cut
	r=pow(anz_mumu/anz_ee,0.5)

	anz_eeStar, sigma_eeStar= getEntriesFromProcesses(process, variable, cut, Trees.ee, triggerscaling=False)
	anz_mumuStar, sigma_mumuStar= getEntriesFromProcesses(process, variable, cut, Trees.mumu, triggerscaling=False)
	rStar=pow(anz_mumuStar/anz_eeStar,0.5)

	sigma_r_stat= r/2*pow( pow(sigma_mumu/anz_mumu,2) + pow(sigma_ee/anz_ee,2), 0.5)
	sigma_r_syst_p= rStar/2*pow( pow(sigma_effmumu_p/effmumu,2) + pow(sigma_effee_p/effee,2), 0.5)
	sigma_r_syst_m= rStar/2*pow( pow(sigma_effmumu_m/effmumu,2) + pow(sigma_effee_m/effee,2), 0.5)

#	rZ_mumu = (anz_mumu*Constants.lumi8TeV*SubProcesses8TeV.ZJets.xSection)/(anz_mumu2011*Constants.lumi7TeV*SubProcesses7TeV.ZJets.xSection) #2012/2011
#	rZ_ee = (anz_ee*Constants.lumi8TeV*SubProcesses8TeV.ZJets.xSection)/(anz_ee2011*Constants.lumi7TeV*SubProcesses7TeV.ZJets.xSection)

#	rtt_mumu = (anz_mumu*Constants.lumi8TeV*SubProcesses8TeV.TTJets.xSection)/(anz_mumu2011*Constants.lumi7TeV*SubProcesses7TeV.TTJets.xSection)
#	rtt_ee = (anz_ee*Constants.lumi8TeV*SubProcesses8TeV.TTJets.xSection)/(anz_ee2011*Constants.lumi7TeV*SubProcesses7TeV.ZJets.xSectio)


	#log.logHighlighted("anz_mumu= %f und anz_ee=%f" %(anz_mumu, anz_ee))

	#log.logHighlighted ("\t Das Verhaeltnis mit %s \t ist r=sqrt(#mumu/#ee) \pm sigma_r_stat \pm sigma_r_syst= %f \pm %f \pm %f \pm %f" %(cut, r, sigma_r_stat, sigma_r_syst_p, sigma_r_syst_m)) # =1,128109 (2011) =1,124820 (2012)

	return anz_mumu, anz_ee, r, sigma_r_stat, sigma_r_syst_p, sigma_r_syst_m


# Latex-Tabelle mit Ratio
def tableRatio(n_mumu_R3MC, n_ee_R3MC, rR3MC, sigma_rR3MC, sigma_rR3MC_syst_p, sigma_rR3MC_syst_m, 
	n_mumu_R3Data, n_ee_R3Data, rR3Data, sigma_rR3Data, sigma_rR3Data_syst_p, sigma_rR3Data_syst_m,selectionModifier):
	rkeytitle=["empty", "n_mumu", "n_ee", "r"]
	rkeys=["empty", "n_mumu", "n_ee", "r", "sigma_r_stat", "sigmaUp_r", "sigmaDown_r"]
	rkeylist=[rkeytitle, rkeys, rkeys]
	dictr0={"region":"region", "empty":"", "n_mumu":"n_{\mu\mu}", "n_ee":"n_{ee}", "r":"r_{\mu e} \pm \sigma_{stat} \pm \sigma_{syst}", "leer":""}
	
	if len(selectionModifier) > 0:
		dictr5={"empty":"MC", "n_mumu":n_mumu_R3MC, "n_ee":n_ee_R3MC, "r":rR3MC, "sigma_r_stat":sigma_rR3MC, "sigmaUp_r":sqrt(sigma_rR3MC_syst_p**2 + (relUncertainties[selectionModifier[0]]*rR3MC)**2), "sigmaDown_r":sqrt(sigma_rR3MC_syst_m**2 + (relUncertainties[selectionModifier[0]]*rR3MC)**2)}
		dictr6={"empty":"Data", "n_mumu":n_mumu_R3Data, "n_ee":n_ee_R3Data, "r":rR3Data, "sigma_r_stat":sigma_rR3Data, "sigmaUp_r":rR3Data*relUncertainties[selectionModifier[0]], "sigmaDown_r":rR3Data*relUncertainties[selectionModifier[0]]}
	else:
		dictr5={"empty":"MC", "n_mumu":n_mumu_R3MC, "n_ee":n_ee_R3MC, "r":rR3MC, "sigma_r_stat":sigma_rR3MC, "sigmaUp_r":sqrt(sigma_rR3MC_syst_p**2 + (relUncertainties["default"]*rR3MC)**2), "sigmaDown_r":sqrt(sigma_rR3MC_syst_m**2 + (relUncertainties["default"]*rR3MC)**2)}
		dictr6={"empty":"Data", "n_mumu":n_mumu_R3Data, "n_ee":n_ee_R3Data, "r":rR3Data, "sigma_r_stat":sigma_rR3Data, "sigmaUp_r":rR3Data*relUncertainties["default"], "sigmaDown_r":rR3Data*relUncertainties["default"]}

	rdictlist=[dictr0, dictr5, dictr6]
	#prozentlist=["r"]
	anzahlDezimalstellenDict = {"n_ee":0, "n_mumu":0,  "r":3, "sigma_r_stat":3}

	titel="$r_{\mu e}$-values for data and MC in the %s region with OS, $p_{T} > 20$ GeV, 60 GeV $< m_{ll} <$ 120 GeV, $N_{jets} >= 2$ and $E_T^{miss} < 50~GeV$"%selectionModifier
	nameModifier="_"
	if len(selectionModifier) >0:
		for modifier in selectionModifier:			
			nameModifier = nameModifier+modifier
	savename="Tables/new_r-ValuesControl%s.txt"%nameModifier
	verweis="RValuesControl%s"%nameModifier

	tabr=tabular(rdictlist,rkeylist, anzahlDezimalstellenDict, set([0,"1", 3]))
	tabrEnv=tableEnvironment(tabr, titel, verweis)
	tabDateiR=open(savename, "w")
	tabDateiR.writelines(tabrEnv)
	tabDateiR.close()

#Tabelle mit Steigungen + Achsenabschnitt
def tableDependency_slope(nJetsMC, nJetsData, nVerticesMC, nVerticesData, ptMC, ptData):

	keys=["variable","empty","intercept", "sigma_intercept", "slope", "sigma_slope", "significance", "chi"]
	keytitle=["variable","empty","intercept","slope", "significance", "chi"]
	keylist=[keytitle, keys, keys, keys, keys, keys, keys]
	dict0={"variable":"variable", "empty":"", "intercept":"axis\ intercept", "slope":"slope","significance":"significance", "chi":"\\frac{\chi^{2}}{dof}" }
	dict1={"variable":"nJets", "empty":"Data", "intercept":nJetsData.GetParameter(0), "sigma_intercept": nJetsData.GetParError(0), "slope":nJetsData.GetParameter(1), "sigma_slope": nJetsData.GetParError(1),"significance":nJetsData.GetParameter(1)/nJetsData.GetParError(1), "chi":(nJetsData.GetChisquare()/nJetsData.GetNDF())}
	dict2={"variable":"nJets", "empty":"MC", "intercept":nJetsMC.GetParameter(0), "sigma_intercept": nJetsMC.GetParError(0), "slope": nJetsMC.GetParameter(1), "sigma_slope":nJetsMC.GetParError(1), "significance":nJetsMC.GetParameter(1)/nJetsMC.GetParError(1), "chi":(nJetsMC.GetChisquare()/nJetsMC.GetNDF())}
	dict3={"variable":"nVertices", "empty":"Data", "intercept": nVerticesData.GetParameter(0), "sigma_intercept": nVerticesData.GetParError(0), "slope": nVerticesData.GetParameter(1), "sigma_slope": nVerticesData.GetParError(1), "significance":nVerticesData.GetParameter(1)/nVerticesData.GetParError(1), "chi":(nVerticesData.GetChisquare()/nVerticesData.GetNDF())}
	dict4={"variable":"", "empty":"MC", "intercept": nVerticesMC.GetParameter(0), "sigma_intercept": nVerticesMC.GetParError(0), "slope": nVerticesMC.GetParameter(1), "sigma_slope":nVerticesMC.GetParError(1), "significance":nVerticesMC.GetParameter(1)/nVerticesMC.GetParError(1), "chi":(nVerticesMC.GetChisquare()/nVerticesMC.GetNDF())}
	dict5={"variable":"p_{t}^{1st}", "empty":"Data", "intercept": ptData.GetParameter(0), "sigma_intercept": ptData.GetParError(0), "slope": ptData.GetParameter(1), "sigma_slope": ptData.GetParError(1), "significance":ptData.GetParameter(1)/ptData.GetParError(1), "chi":(ptData.GetChisquare()/ptData.GetNDF())}
	dict6={"variable":"", "empty":"MC", "intercept": ptMC.GetParameter(0), "sigma_intercept":  ptMC.GetParError(0), "slope": ptMC.GetParameter(1), "sigma_slope": ptMC.GetParError(1), "significance":ptMC.GetParameter(1)/ptMC.GetParError(1), "chi":(ptMC.GetChisquare()/ptMC.GetNDF())}

	dictlist=[dict0, dict1, dict2, dict3, dict4, dict5, dict6]
	titel="$r_{\mu e}$-Dependency of different variables received from a linear fit with a slope around zero and an axis intercept of approximately $r_{\mu e}$"
	verweis="RDependency_slope"
	savename="Tables/new_r-Dependency_slope.txt"
	#prozentlist=["intercept", "slope"]
	anzahlDezimalstellenDict={"intercept":4, "slope":4}

	tab=tabular(dictlist,keylist, anzahlDezimalstellenDict, set([0,"1", 3, 5, 7]))
	tabEnv=tableEnvironment(tab, titel, verweis)
	tabDatei=open(savename, "w")
	tabDatei.writelines(tabEnv)
	tabDatei.close()


#Tabelle mit Abh. ohne Steigung
def tableDependency(ptMC, ptData, htMC, htData, metMC, metData, nVerticesMC, nVerticesData, nJetsMC, nJetsData, etaMC, etaData, mllMC, mllData):

	keys=["variable","empty", "intercept", "sigma_intercept", "chi"]
	keytitle=["variable","empty", "intercept", "chi"]
	keylist=[keytitle, keys, keys, keys, keys, keys, keys, keys, keys, keys, keys, keys, keys, keys, keys]
	dict0={"variable":"variable", "empty":"", "intercept":"axis\ intercept","chi":"\\frac{\chi^{2}}{dof}" }
	dict1={"variable":"p_{T}^{\ell_{1}}", "empty":"Data", "intercept": ptData.GetParameter(0), "sigma_intercept": ptData.GetParError(0), "chi":(ptData.GetChisquare()/ptData.GetNDF())}
	dict2={"variable":"p_{T}^{\ell_{1}}", "empty":"MC","intercept": ptMC.GetParameter(0), "sigma_intercept": ptMC.GetParError(0), "chi":(ptMC.GetChisquare()/ptMC.GetNDF())}
	dict3={"variable":"H_{T}", "empty":"Data", "intercept": htData.GetParameter(0), "sigma_intercept": htData.GetParError(0), "chi":(htData.GetChisquare()/htData.GetNDF())}
	dict4={"variable":"H_{T}",  "empty":"MC", "intercept": htMC.GetParameter(0), "sigma_intercept": htMC.GetParError(0), "chi":(htMC.GetChisquare()/htMC.GetNDF())}
	dict5={"variable":"E_{T}^{miss}", "empty":"Data", "intercept": metData.GetParameter(0), "sigma_intercept": metData.GetParError(0), "chi":(metData.GetChisquare()/metData.GetNDF())}
	dict6={"variable":"E_{T}^{miss}",  "empty":"MC", "intercept": metMC.GetParameter(0), "sigma_intercept": metMC.GetParError(0), "chi":(metMC.GetChisquare()/metMC.GetNDF())}
	dict7={"variable":"nVertices", "empty":"Data", "intercept": nVerticesData.GetParameter(0), "sigma_intercept": nVerticesData.GetParError(0), "chi":(nVerticesData.GetChisquare()/nVerticesData.GetNDF())}
	dict8={"variable":"nVertices",  "empty":"MC", "intercept": nVerticesMC.GetParameter(0), "sigma_intercept": nVerticesMC.GetParError(0), "chi":(nVerticesMC.GetChisquare()/nVerticesMC.GetNDF())}
	dict9={"variable":"nJets", "empty":"Data", "intercept": nJetsData.GetParameter(0), "sigma_intercept": nJetsData.GetParError(0), "chi":(nJetsData.GetChisquare()/nJetsData.GetNDF())}
	dict10={"variable":"nJets", "empty":"MC","intercept": nJetsMC.GetParameter(0), "sigma_intercept": nJetsMC.GetParError(0), "chi":(nJetsMC.GetChisquare()/nJetsMC.GetNDF())}
	dict11={"variable":"\eta", "empty":"Data", "intercept": etaData.GetParameter(0), "sigma_intercept": etaData.GetParError(0), "chi":(etaData.GetChisquare()/etaData.GetNDF())}
	dict12={"variable":"\eta", "empty":"MC", "intercept": etaMC.GetParameter(0), "sigma_intercept": etaMC.GetParError(0), "chi":(etaMC.GetChisquare()/etaMC.GetNDF())}
	dict13={"variable":"m_{\ell\ell}", "empty":"Data", "intercept": mllData.GetParameter(0), "sigma_intercept": mllData.GetParError(0), "chi":(mllData.GetChisquare()/mllData.GetNDF())}
	dict14={"variable":"m_{\ell\ell}", "empty":"MC", "intercept": mllMC.GetParameter(0), "sigma_intercept": mllMC.GetParError(0), "chi":(mllMC.GetChisquare()/mllMC.GetNDF())}

	dictlist=[dict0, dict1, dict2,dict3, dict4,dict5,  dict6, dict7, dict8,dict9,  dict10, dict11, dict12, dict3, dict14]
	titel="$r_{\mu e}$-Dependency of different variables for data and MC with OS, $p_T>20(10)\,\unit{GeV}$ and $60\,\unit{GeV}<m_{ell\ell}<120\,\unit{GeV}$ received from a line with slope=0 and an axis intercept of approximately $r_{\mu e}$"
	verweis="RDependency"
	savename="Tables/new_r-Dependency.txt"
	#prozentlist=["intercept"]
	anzahlDezimalstellenDict={"intercept":3}

	tab=tabular(dictlist,keylist, anzahlDezimalstellenDict, set([0,"1", 2,3,4,5,6,7,8,9, 10, 11, 12, 13, 14, 15]))
	tabEnv=tableEnvironment(tab, titel, verweis)
	tabDatei=open(savename, "w")
	tabDatei.writelines(tabEnv)
	tabDatei.close()


def main():
	from sys import argv
	if len(argv) > 2:
		selectionModifier = argv[2:]
	else: 
		selectionModifier = []
	Constants.setLumi(Constants.lumi8TeV)
	if argv[1] == "CentralValue":
		n_mumu_R3Data, n_ee_R3Data, rR3Data, rR3Data_stat, rR3Data_up, rR3Data_down = calculateRatio(Cuts.basicPlusInvMassPlusMet50Cut, Processes8TeV.Data,selectionModifier)
		n_mumu_R3MC, n_ee_R3MC, rR3MC, rR3MC_stat, rR3MC_up, rR3MC_down = calculateRatio(Cuts.basicPlusInvMassPlusMet50Cut, Processes8TeV.ZJets,selectionModifier)
	#
		tableRatio(n_mumu_R3MC, n_ee_R3MC, rR3MC, rR3MC_stat, rR3MC_up, rR3MC_down,
			n_mumu_R3Data, n_ee_R3Data, rR3Data, rR3Data_stat, rR3Data_up, rR3Data_down,selectionModifier)	
#	
	elif argv[1] == "Dependencies":
		etaMC, etaData = rRatioDataVsMC(Ratio_eta1_MC, Ratio_eta1_Data, variante=2,selectionModifier=selectionModifier)
		metMC, metData=rRatioDataVsMC(Ratio_met_MC, Ratio_met_Data, variante=2,selectionModifier=selectionModifier)
		metMCtt, metDatatt=rRatioDataVsMC(Ratio_met_MC_tt, None, variante=2,selectionModifier=selectionModifier)
		nJetsMC, nJetsData = rRatioDataVsMC(Ratio_nJets_MC, Ratio_nJets_Data, variante=2,selectionModifier=selectionModifier)
		nVerticesMC, nVerticesData = rRatioDataVsMC(Ratio_nVertices_MC, Ratio_nVertices_Data, variante=2,selectionModifier=selectionModifier)
		htMC, htData=rRatioDataVsMC(Ratio_ht_MC, Ratio_ht_Data,variante=2,selectionModifier=selectionModifier)
		ptMC, ptData = rRatioDataVsMC(Ratio_pt_MC, Ratio_pt_Data, variante=2,selectionModifier=selectionModifier)
		pt2MC, pt2Data = rRatioDataVsMC(Ratio_pt2_MC, Ratio_pt2_Data, variante=2,selectionModifier=selectionModifier)
		nBJetsMC, nBJetsData=rRatioDataVsMC(Ratio_nBJets_MC, Ratio_nBJets_Data, variante=2,selectionModifier=selectionModifier)
		iso1MC, iso1Data = rRatioDataVsMC(Ratio_id1_MC, Ratio_id1_Data, variante=2,selectionModifier=selectionModifier)
		iso2MC, iso2Data = rRatioDataVsMC(Ratio_id2_MC, Ratio_id2_Data, variante=2,selectionModifier=selectionModifier)
	#~ #	iso1_002_MC, iso1_002_Data = rRatioDataVsMC(Ratio_id1_002_MC, Ratio_id1_002_Data, variante=2,selectionModifier=selectionModifier)
	#~ #	iso2_002_MC, iso2_002_Data = rRatioDataVsMC(Ratio_id2_002_MC, Ratio_id2_002_Data, variante=2,selectionModifier=selectionModifier)
		mllMC, mllData=rRatioDataVsMC(Ratio_p4M_MC, Ratio_p4M_Data, variante=2,selectionModifier=selectionModifier)
		mllMCZ, mllDataZ=rRatioDataVsMC(Ratio_p4M_MCZ, Ratio_p4M_Data, variante=2,selectionModifier=selectionModifier)
		mllMCtt, mllDataZtt=rRatioDataVsMC(Ratio_p4M_MCtt, Ratio_p4M_Data, variante=2,selectionModifier=selectionModifier)
		deltRMC, deltaRData=rRatioDataVsMC(Ratio_DeltaR_MC, Ratio_DeltaR_Data, variante=2,selectionModifier=selectionModifier)
		deltRMCZ, deltaRDataZ=rRatioDataVsMC(Ratio_DeltaR_MCZ, Ratio_DeltaR_Data, variante=2,selectionModifier=selectionModifier)
		
		
		MllNonIsoMC, MllNonIsoData=rRatioDataVsMC(Ratio_p4M_MCIsoSideband, Ratio_p4M_DataIsoSideband, variante=2,selectionModifier=selectionModifier)

	#	mllMC, mllData=rRatioDataVsMC(None, Ratio_p4M_Data, variante=2,selectionModifier=selectionModifier)
	#	mllMCZ, mllDataZ=rRatioDataVsMC(Ratio_p4M_MCZ, None, variante=2,selectionModifier=selectionModifier)
	#	mllMCtt, mllDataZtt=rRatioDataVsMC(Ratio_p4M_MCtt, None, variante=2,selectionModifier=selectionModifier)
		tableDependency(ptMC, ptData, htMC, htData, metMC, metData, nVerticesMC, nVerticesData, nJetsMC, nJetsData, etaMC, etaData, mllMC, mllData)
	
		#~ 
	else:
		print "Nothing to do, exiting"


	


if __name__ == "__main__":
    	main()


