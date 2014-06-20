import ROOT
from src.messageLogger import messageLogger as log
from src.processes import SubProcesses7TeV, SubProcesses8TeV, Processes7TeV, Processes8TeV, TreePaths, Trees
from src.defs import Cuts, Colors, Titles, Constants, UnderLegendAnnotation, Lumi8TeVAnnotation1, Lumi8TeVAnnotation2, Lumi8TeVAnnotation3, Lumi8TeVAnnotationMll1, Lumi8TeVAnnotationMll2, Lumi8TeVAnnotationMll3, MuMuAnnotation, EEAnnotation
from src.treeTools import getEntriesFromTree, getHistoFromProcess
from src.plotTools import histoStack, save, legende, setPalette, makeAnnotation
import src.Styles as Styles

class nJets_mumu():
	variable = "nJets"
	filename = "mumuNJets"
	tree = Trees.mumu
	nBins=8
	xMin=-0.5
	xMax=7.5
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.nJets
class nJets_ee():
	variable = "nJets"
	filename = "eeNJets"
	tree = Trees.ee
	nBins=8
	xMin=-0.5
	xMax=7.5
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.nJets

class nBJets_mumu():
	variable = "nBJets"
	filename = "mumuNBJets"
	tree = Trees.mumu
	nBins=11
	xMin=-0.5
	xMax=10.5
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.nBJets
class nBJets_ee():
	variable = "nBJets"
	filename = "eeNBJets"
	tree = Trees.ee
	nBins=11
	xMin=-0.5
	xMax=10.5
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.nBJets

class id1_mumu():
	variable = "id1"
	filename= "mumuid1"
	tree = Trees.mumu
	nBins=11
	xMin=-0.01
	xMax=0.16
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.id1
class id1_ee():
	variable = "id1"
	filename= "eeid1"
	tree = Trees.ee
	nBins=11
	xMin=-0.01
	xMax=0.16
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.id1

class id2_mumu():
	variable = "id2"
	filename= "mumuid2"
	tree = Trees.mumu
	nBins=11
	xMin=-0.01
	xMax=0.16
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.id2
class id2_ee():
	variable = "id2"
	filename= "eeid2"
	tree = Trees.ee
	nBins=11
	xMin=-0.01
	xMax=0.16
	yMin=1
	yMax=2e4
	cut=Cuts.basicPlusInvMassCut
	xaxis=Titles.id2

class nVertices_mumu():
	variable = "nVertices"
	filename = "mumuNVertices"
	tree = Trees.mumu
	nBins=31
	xMin=0
	xMax=30.1
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.nVertices
class nVertices_ee():
	variable = "nVertices"
	filename = "eeNVertices"
	tree = Trees.ee
	nBins=31
	xMin=0
	xMax=30.5
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.nVertices

class ht_mumu():
	variable = "ht"
	filename = "mumuHt"
	tree = Trees.mumu
	nBins=11
	xMin=0
	xMax=800.5
	yMin=1
	yMax=2e7
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.ht
class ht_ee():
	variable = "ht"
	filename = "eeHt"
	tree = Trees.ee
	nBins=11
	xMin=0
	xMax=800.5
	yMin=1
	yMax=2e7
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.ht

class pt1_mumu():
	variable = "pt1"
	filename = "mumuPt1"
	tree = Trees.mumu
	nBins=10
	xMin=0
	xMax=100
	yMin=1
	yMax=2e6
	cut=Cuts.basicCutOhnePt
	xaxis=Titles.pt1
class pt1_ee():
	variable = "pt1"
	filename = "eePt1"
	tree = Trees.ee
	nBins=10
	xMin=0
	xMax=100
	yMin=1
	yMax=2e6
	cut=Cuts.basicCutOhnePt
	xaxis=Titles.pt1

class p4M_mumu():
	variable = "p4.M()"
	filename = "mumuP4M"
	tree = Trees.mumu
	nBins=100
	xMin=015
	xMax=250
	yMin=1
	yMax=2e7
	cut=Cuts.basicCutohneN
	xaxis=Titles.mmumu
class p4M_ee():
	variable = "p4.M()"
	filename = "eeP4M"
	tree = Trees.ee
	nBins=100
	xMin=15
	xMax=250
	yMin=1
	yMax=2e7
	cut=Cuts.basicCutohneN
	xaxis=Titles.mee

class met_ee():
	variable = "met"
	filename = "eeMet"
	tree = Trees.ee
	nBins=20
	xMin=0
	xMax=400
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.met

class met_mumu():
	variable = "met"
	filename = "mumuMet"
	tree = Trees.mumu
	nBins=20
	xMin=0
	xMax=400
	yMin=1
	yMax=2e6
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.met

class met_eeZoom():
	variable = "met"
	filename = "eeMet8TeV_50-100"
	tree = Trees.ee
	nBins=20
	xMin=50
	xMax=100
	yMin=1
	yMax=2e4
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.met

class met_mumuZoom():
	variable = "met"
	filename = "mumuMet8TeV_50-100"
	tree = Trees.mumu
	nBins=20
	xMin=50
	xMax=100
	yMin=1
	yMax=2e4
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.met

class eta1_ee():
	variable = "eta1"
	filename = "eeEta"
	tree = Trees.ee
	binning = [i*0.1442 for i in range(0,10)]+[i*0.1218+1.442 for i in range(0,1)]+[i*0.3132+1.566 for i in range(0,5)]#[i*0.20 for i in range(0,40)]
	nBins=25
	xMin=0
	xMax=3
	yMin=1
	yMax=2e5
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.eta1
class eta1_mumu():
	variable = "eta1"
	filename = "mumuEta"
	tree = Trees.mumu
	binning = [i*0.1442 for i in range(0,10)]+[i*0.1218+1.442 for i in range(0,1)]+[i*0.3132+1.566 for i in range(0,5)]#[i*0.20 for i in range(0,40)]
	nBins=25
	xMin=0
	xMax=3
	yMin=1
	yMax=2e5
	cut=Cuts.basicOhneNJetPlusInvMass
	xaxis=Titles.eta1


def Histo(plot, isinput=False): # Histogramme

	log.outputLevel=5
	rootContainer = []
	style=Styles.tdrStyle()
	style.SetPadRightMargin(0.1)
	style.SetTitleYOffset(0.9)
	setPalette()
	c1= ROOT.TCanvas("c1","c1",800,800)
	c1.SetLogy()

	SubProcesses8TeV.dataPath = "../Daten/"
	SubProcesses7TeV.dataPath = "../Daten/"
	
	# Histos einlesen 

	if plot==eta1_mumu() or plot==eta1_ee():
		histoTT = getHistoFromProcess(Processes8TeV.TTJets, plot.variable, plot.cut, plot.tree, plot.tree, len(plotMC.binning)-1, plot.binning, xMax=None)
		histoZ = getHistoFromProcess(Processes8TeV.ZJets, plot.variable, plot.cut, plot.tree, plot.tree, len(plotMC.binning)-1, plot.binning, xMax=None)

	else:	
		histoTT = getHistoFromProcess(Processes8TeV.TTJets, plot.variable, plot.cut, plot.tree, plot.nBins, plot.xMin, plot.xMax)
		histoZ = getHistoFromProcess(Processes8TeV.ZJets, plot.variable, plot.cut, plot.tree, plot.nBins, plot.xMin, plot.xMax)
		#histoT =  getHistoFromProcess(Processes8TeV.SingleT, plot.variable, plot.cut, plot.tree, plot.nBins, plot.xMin, plot.xMax)
		#histoDiBo = getHistoFromProcess(Processes8TeV.DiBoson, plot.variable, plot.cut, plot.tree, plot.nBins, plot.xMin, plot.xMax)
	histoData = getHistoFromProcess(Processes8TeV.Data, plot.variable, plot.cut, plot.tree, plot.nBins, plot.xMin, plot.xMax, trigger = False, triggerscaling=False, weights=True)
	
	# Farben setzen

	#histoT.SetFillColor(Colors.singleT)
	histoZ.SetFillColor(Colors.zLightJets)
	histoTT.SetFillColor(Colors.ttJets)
	#histoDiBo.SetFillColor(Colors.diBoson)
	histoData.SetFillColor(Colors.data)

	histos=[#histoT,
	 histoTT, 
	 #histoDiBo, 
	histoZ]
	histosbackw=[histoZ, #histoDiBo, 
	histoTT, #histoT
	]
	names=[Titles.zJets,#Titles.diBoson,
	Titles.ttJets,
	#Titles.singleT
	]

	stack=histoStack(histos)
	frame=c1.DrawFrame(plot.xMin,plot.yMin,plot.xMax,plot.yMax,"; %s ; Entries" %plot.xaxis)	
	frame.GetYaxis().SetTitleOffset(1.2)
	stack.Draw("hist SAME")
	histoData.SetMarkerStyle(20)
	histoData.Draw("SAMEEP")
	stack.SetTitle("; %s ; Entries" %plot.xaxis)
	
	#Legende
	leg=legende(histosbackw, names, "f")
	leg.AddEntry(histoData, "Data", "p")
	

	# Linien zur Signal Region 
	
	if plot == met_mumu or plot == met_ee:
		line = ROOT.TLine(150., 0., 150., 10000)
		line.SetLineColor(ROOT.kRed-3)
		line.SetLineWidth(2)
		arrow=ROOT.TArrow(150,1000,200,1000,0.02,"|>")
		arrow.SetFillColor(ROOT.kRed-3)
		arrow.SetLineColor(ROOT.kRed-3)
   		arrow.SetLineWidth(3)
   		arrow.Draw("")
		line.Draw("SAME")

	elif plot == ht_mumu or plot == ht_ee:
		line = ROOT.TLine(300., 0., 300., 100000)
		line.SetLineColor(ROOT.kRed-3)
		line.SetLineWidth(2)
		arrow=ROOT.TArrow(300,10000,400,10000,0.02,"|>")
   		arrow.SetLineWidth(3)
   		arrow.SetFillColor(ROOT.kRed-3)
   		arrow.SetLineColor(ROOT.kRed-3)
   		arrow.Draw("")
		line.Draw("SAME")

	elif plot == nJets_mumu or plot == nJets_ee:
		line = ROOT.TLine(2., 0., 2., 20000)
		line.SetLineColor(ROOT.kRed-3)
		line.SetLineWidth(2)
		arrow=ROOT.TArrow(2,1000,3,1000,0.02,"|>")
   		arrow.SetLineWidth(3)
   		arrow.SetFillColor(ROOT.kRed-3)
   		arrow.SetLineColor(ROOT.kRed-3)
   		arrow.Draw("")
		line.Draw("SAME")

	
	# Annotations

	#anno=makeAnnotation(UnderLegendAnnotation, plot.cut)
	#anno.Draw("same")

	if plot == p4M_mumu or plot == p4M_ee:
		lumianno1=makeAnnotation(Lumi8TeVAnnotationMll1)
		lumianno2=makeAnnotation(Lumi8TeVAnnotationMll2)
		lumianno3=makeAnnotation(Lumi8TeVAnnotationMll3)
		lumianno1.Draw("same")
		lumianno2.Draw("same")
		lumianno3.Draw("same")
	else:
		lumianno1=makeAnnotation(Lumi8TeVAnnotation1)
		lumianno2=makeAnnotation(Lumi8TeVAnnotation2)
		lumianno3=makeAnnotation(Lumi8TeVAnnotation3)
		lumianno1.Draw("same")
		lumianno2.Draw("same")
		lumianno3.Draw("same")
	
	if plot.tree == Trees.mumu:
		llanno=makeAnnotation(MuMuAnnotation)
	elif plot.tree == Trees.ee:
		llanno=makeAnnotation(EEAnnotation)
		
	c1.RedrawAxis()
	leg.Draw("SAME")
	c1.Update()
	plotpath="Plots/Histos/8TeV/neueDaten/"
	save(c1, plotpath, "%s8TeV"%plot.filename)

	if isinput==True:
		raw_input("Press Enter to continue")

def main():
	Constants.setLumi(Constants.lumi8TeV)

	Histo(p4M_mumu)
	Histo(p4M_ee)

#	Histo(nJets_mumu)
#	Histo(nJets_ee)

#	Histo(nBJets_mumu)
#	Histo(nBJets_ee)

#	Histo(nVertices_mumu)
#	Histo(nVertices_ee)

#	Histo(ht_mumu)
#	Histo(ht_ee)

#	Histo(pt1_mumu)
#	Histo(pt1_ee)

#	Histo(met_mumu)
#	Histo(met_ee)
#	Histo(met_eeZoom)
#	Histo(met_mumuZoom)

#	Histo(id1_ee)
#	Histo(id1_mumu)

#	Histo(id2_ee)
#	Histo(id2_mumu)

#	Histo(eta1_ee)
#	Histo(eta1_mumu)

if __name__ == "__main__":
    	main()
