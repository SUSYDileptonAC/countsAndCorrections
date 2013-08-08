#!/usr/bin/env python


slideTemplate = r"""
\begin{frame}
\frametitle{%(name)s}
\begin{columns}
  \begin{column}[l]{0.4\textwidth}
    \centering
     %(leftName)s
    \includegraphics[width=\columnwidth]{%(pathLeft)s}\\
 \end{column}
  \begin{column}[l]{0.4\textwidth}
    \centering
        %(rightName)s
    \includegraphics[width=\columnwidth]{%(pathRight)s}
 \end{column}
\end{columns}
	\begin{columns}
  \begin{column}[l]{0.22\textwidth}
    \centering
	Run A+B
    \includegraphics[width=\columnwidth]{%(pathLeft_Left)s}
 \end{column}
  \begin{column}[r]{0.22\textwidth}
    \centering
		Run C
   \includegraphics[width=\columnwidth]{%(pathLeft_Right)s}
 \end{column}
  \begin{column}[l]{0.22\textwidth}
    \centering
	Run A+B
    \includegraphics[width=\columnwidth]{%(pathRight_Left)s}
 \end{column}
  \begin{column}[r]{0.22\textwidth}
    \centering
		Run C
    \includegraphics[width=\columnwidth]{%(pathRight_Right)s}
 \end{column}
\end{columns}

%%      \begin{itemize}
%%      \item         $$
%%    \end{itemize} 
\end{frame}
\clearpage
"""

slideTemplate2011 = r"""
\begin{frame}
\frametitle{%(name)s}
\begin{columns}
  \begin{column}[l]{0.4\textwidth}
    \centering
     %(leftName)s
    \includegraphics[width=\columnwidth]{%(pathLeft)s}\\
 \end{column}
  \begin{column}[l]{0.4\textwidth}
    \centering
        %(rightName)s
    \includegraphics[width=\columnwidth]{%(pathRight)s}
 \end{column}
\end{columns}
	

%%      \begin{itemize}
%%      \item         $$
%%    \end{itemize} 
\end{frame}
"""

def readTreeFromFile(path, dileptonCombination, selection = "OS"):
	"""
	helper function
	path: path to .root file containing simulated events
	dileptonCombination: EE, EMu, or MuMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	chain = TChain()
#	chain.Add("%s/ETH2AachenNtuples/%sDileptonTree"%(path, dileptonCombination))
	chain.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	chain.SetName("%sDileptonTree"%dileptonCombination)
	result = chain.CopyTree("nJets >= 2")
	#~ result = chain
	return result

def makePlot(trees, cut, variable, combination, name, title = None, datasetName="Data"):
	from ROOT import TCanvas, TPad, TLegend, kBlue, kRed, TLatex
	from src.ratios import RatioGraph
	from src.histos import getHisto
	from math import sqrt
	from random import random
	if title is None:
		title =name

	cut = cut.replace("inv", "p4.M()")
	if "iso" in variable:
		cut = cut.replace("id1 < 0.15","id1 < 10")
		cut = cut.replace("id2 < 0.15","id2 < 10")
	print cut
	baseColor = kBlue
	if "jzb" in name:
		baseColor = kRed
	
	rmue = 1.21
	trigger = {
		"EE":0.970,
		"EMu":0.942,
		"MuMu":0.964
		}

	histos= {
		"MuMu": getHisto( trees["MuMu"], cut, variable),
		"EE": getHisto( trees["EE"], cut, variable),
		"EMu": getHisto( trees["EMu"], cut, variable),
		"EMu_MuLead": getHisto( trees["EMu"], "(%s) * (pt2 > pt1)"%cut , variable),
		}

	rmueSys = 0
	predictionSrc = "EMu"
	if combination == "Both":
		sameFlavour = histos["MuMu"].Clone("sameFlavourSum")
		sameFlavour.Add(histos["EE"])
		#~ nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
		#~ rmueSys = sqrt(sum(i**2 for i in [0.5*(1-(1./rmue**2))*0.1 + (1./trigger["EMu"] + 0.5*(1./trigger["EE"]+1./trigger["MuMu"]))*0.05]))
		nllPredictionScale = 1.02
		rmueSys = 0.07
		#0.5*(1-1./rmue**2)*0.1
	elif combination in ["EE","MuMu"]:
		rmueFactor = rmue
		if combination == "EE":
					rmueFactor = 1./rmue
		nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *rmueFactor
		rmueSys = sqrt(0.1**2+(0.67/1.025)**2)*nllPredictionScale
		sameFlavour = histos[combination].Clone("sameFlavourSum")
	elif combination == "MuMuSF":
		predictionSrc = "MuMu"
		rmueFactor = 1./rmue
		nllPredictionScale =  trigger["EE"]*1./trigger["MuMu"] *(rmueFactor**2)
		rmueSys = (2*rmue)*0.1
		sameFlavour = histos["EE"].Clone("sameFlavourSum")
	else:
		raise StandardError, "unknown combination' %s'"%combination

	prediction = histos[predictionSrc].Clone("ofPrediction")
	predictionMuLead = histos["EMu_MuLead"].Clone("ofPrediction_MuLeading")
	prediction.Scale(nllPredictionScale)
	predictionMuLead.Scale(nllPredictionScale)
		
	rooTex = {
		"Both":"ee + #mu#mu",
		"EE":"ee",
		"MuMu":"#mu#mu",
		"MuMuSF":"ee",
		"EMu_Prediction": "OF-Prediciton",
		"MuMu_Prediction": "SF(#mu#mu)-Prediciton"
		}
	canv = TCanvas("canv","",800,800)

	canv.Draw()
	pad = TPad("main_%x"%(1e16*random()), "main", 0.01, 0.25, 0.99, 0.99)
	pad.SetNumber(1)
	pad.Draw()
	canv.cd()
	resPad = TPad("residual_%x"%(1e16*random()), "residual", 0.01, 0.01, 0.99, 0.25)
	resPad.SetNumber(2)
	resPad.Draw()
	pad.cd()
	#~ if "iso" in variable:
		#~ canv.SetLogy(1)
		#~ pad.SetLogy(1)
	sameFlavour.SetMarkerStyle(20)
	sameFlavour.SetLineColor(1)
	sameFlavour.Draw("E P")
	sameFlavour.SetTitle(title)
	import ROOT
	histos["MuMu"].SetLineColor(ROOT.kBlack)
	histos["MuMu"].SetFillColor(ROOT.kWhite)
	

	prediction.SetLineColor(1)
	prediction.SetFillColor(baseColor-7)
	prediction.Draw("SAME Hist")

	if predictionSrc == "EMu":
		predictionMuLead.SetLineColor(1)
		predictionMuLead.SetFillColor(baseColor-9)
		predictionMuLead.Draw("SAME Hist")


	sameFlavour.Draw("E P SAME")
	histos["MuMu"].Draw("SAME Hist")	
	
	pad.RedrawAxis()
	canv.RedrawAxis()
	leg = TLegend(0.75,0.65,1,0.9)
	leg.SetFillColor(0)
	leg.AddEntry(sameFlavour, rooTex[combination], "P")
	leg.AddEntry(histos["MuMu"],"#mu#mu events","l")
	leg.AddEntry(prediction, rooTex[predictionSrc+"_Prediction"], "F")
	if predictionSrc == "EMu":
		leg.AddEntry(predictionMuLead, "#mu leading", "F")
	leg.Draw()
#	print "_".join([name,variable]),
#	print "EE",histos["EE"].GetEntries(),  "MuMu:", histos["MuMu"].GetEntries(),  "EMu:", histos["EMu"].GetEntries(),
#	print " SF:", sameFlavour.GetEntries(),  "OF:", prediction.GetEntries()
	
#	tex = TLatex()
#	tex.SetNDC()
#	tex.SetTextSize()
#	tex.DrawLatex(0.6, 0.7, title)
	residuals = RatioGraph(sameFlavour, prediction)
	residuals.addErrorBySize(rmueSys, rmueSys, add=False, color = kBlue-9 )
	residuals.draw(resPad, yMin = 0.5, yMax = 1.5)
	canv.Update()
	
	variable= variable.replace("(","").replace(")","")
	plotPath = "fig/%s.pdf"%("_".join([datasetName,name,combination,variable]))
	canv.Print(plotPath)
	pad.Delete()
	resPad.Delete()
	canv.Delete()
#	raw_input()
	return plotPath
	

def makeSlide(name, variable, plotPaths):
	repMap = {
		"name": (" ".join([name, variable])).replace("_", " "),
		"leftName":"$ee+\mu\mu$ (predicted from $e\mu$)",
		"pathLeft": plotPaths[(name, variable,"Both")],
		"rightName":r"$ee$  (predicted from $\mu\mu$)",
		"pathRight": plotPaths[(name, variable,"MuMuSF")],
#		"pathLeft_Left": plotPaths[(name, variable,"EE")],
#		"pathLeft_Right": plotPaths[(name, variable,"MuMu")],
		"pathLeft_Left": plotPaths[(name+"_RunAB", variable,"Both")],
		"pathLeft_Right": plotPaths[(name+"_RunC", variable,"Both")],

#		"rightName":r"$|\eta| < 1.4$",
#		"pathRight": plotPaths[(name+"_eta", variable,"Both")],
		"pathRight_Left": plotPaths[(name+"_RunAB", variable,"MuMuSF")],
		"pathRight_Right": plotPaths[(name+"_RunC", variable,"MuMuSF")],
#		"pathRight_Left": plotPaths[(name+"_eta", variable,"EE")],
#		"pathRight_Right": plotPaths[(name+"_eta", variable,"MuMu")],	 	

		}
	result = slideTemplate%repMap
#	print result
	return result
	
def makeSlide2011(name, variable, plotPaths):
	repMap = {
		"name": (" ".join([name, variable])).replace("_", " "),
		"leftName":"$ee+\mu\mu$ (predicted from $e\mu$)",
		"pathLeft": plotPaths[(name, variable,"Both")],
		"rightName":r"$ee$  (predicted from $\mu\mu$)",
		"pathRight": plotPaths[(name, variable,"MuMuSF")],
#		"pathLeft_Left": plotPaths[(name, variable,"EE")],
#		"pathLeft_Right": plotPaths[(name, variable,"MuMu")],
		#~ "pathLeft_Left": plotPaths[(name+"_RunAB", variable,"Both")],
		#~ "pathLeft_Right": plotPaths[(name+"_RunC", variable,"Both")],

#		"rightName":r"$|\eta| < 1.4$",
#		"pathRight": plotPaths[(name+"_eta", variable,"Both")],
		#~ "pathRight_Left": plotPaths[(name+"_RunAB", variable,"MuMuSF")],
		#~ "pathRight_Right": plotPaths[(name+"_RunC", variable,"MuMuSF")],
#		"pathRight_Left": plotPaths[(name+"_eta", variable,"EE")],
#		"pathRight_Right": plotPaths[(name+"_eta", variable,"MuMu")],	 	

		}
	result = slideTemplate2011%repMap
#	print result
	return result

def makeSlides(trees, cuts, variables,titles, selections, datasetName, runAB, runC):
	from itertools import product
	#~ for name in cuts.keys():
		#~ cuts[name+"_RunAB"]  = [runAB] + cuts[name]
		#~ cuts[name+"_RunC"]  = [runC] + cuts[name]
		#~ if name in selections:
			#~ selections.append(name+"_RunAB")
			#~ selections.append(name+"_RunC")
		#~ titles[name+"_RunAB"] = "Run A&B, %s"%titles[name]
		#~ titles[name+"_RunAB"] = titles[name+"_RunAB"].replace(r", inclusive","")
		#~ titles[name+"_RunC"] = "Run C, %s"%titles[name]
		#~ titles[name+"_RunC"] = titles[name+"_RunC"].replace(r", inclusive","")
		
	plotPaths = {}
	for name, variable, combination in product(selections, variables, ["Both","MuMuSF","EE","MuMu"]):
		plotPath = makePlot(trees, "(%s)"%(") * (".join(cuts[name])), variable, combination,  name,  title=titles[name], datasetName=datasetName)
		plotPaths[(name, variable, combination)] = plotPath

	slides = []
	lastName = ""
	for name, variable in product(filter(lambda x: not  (x.endswith("_RunAB") or x.endswith("_RunC")), selections), variables):
		if not name == lastName:
			slides.append("\section{%s}"%(name.replace("_"," ")))
			lastName = name
		slides.append(makeSlide2011(name,variable,  plotPaths))

	slideFile = open("slides_ofVsSf_XCheck_%s.tex"%datasetName, "w")
	slideFile.write("\n".join(slides))
	slideFile.close()
	
def makeSlides2011(trees, cuts, variables,titles, selections, datasetName):
	from itertools import product
	#~ for name in cuts.keys():
		#~ cuts[name+"_RunAB"]  = [runAB] + cuts[name]
		#~ cuts[name+"_RunC"]  = [runC] + cuts[name]
		#~ if name in selections:
			#~ selections.append(name+"_RunAB")
			#~ selections.append(name+"_RunC")
		#~ titles[name+"_RunAB"] = "Run A&B, %s"%titles[name]
		#~ titles[name+"_RunAB"] = titles[name+"_RunAB"].replace(r", inclusive","")
		#~ titles[name+"_RunC"] = "Run C, %s"%titles[name]
		#~ titles[name+"_RunC"] = titles[name+"_RunC"].replace(r", inclusive","")
		
	plotPaths = {}
	for name, variable, combination in product(selections, variables, ["Both","MuMuSF"]):
		plotPath = makePlot(trees, "(%s)"%(") * (".join(cuts[name])), variable, combination,  name,  title=titles[name], datasetName=datasetName)
		plotPaths[(name, variable, combination)] = plotPath

	slides = []
	lastName = ""
	for name, variable in product(filter(lambda x: not  (x.endswith("_RunAB") or x.endswith("_RunC")), selections), variables):
		if not name == lastName:
			slides.append("\section{%s}"%(name.replace("_"," ")))
			lastName = name
		slides.append(makeSlide2011(name,variable,  plotPaths))

	slideFile = open("slides_ofVsSf_XCheck_%s.tex"%datasetName, "w")
	slideFile.write("\n".join(slides))
	slideFile.close()



def main():
	from sys import argv
	from ROOT import gStyle, gROOT
	gStyle.SetOptStat(0)
	gROOT.SetBatch(True)
	trees = {
		"MuMu": readTreeFromFile(argv[1], "MuMu"),
		"EMu": readTreeFromFile(argv[1], "EMu"),
		"EE": readTreeFromFile(argv[1], "EE")
		}
	datasetName = argv[1].split("/")[-1].split(".")[2]
	isMC = (not datasetName=="MergedData")

	#	cut= "  chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && nJets >= 2 && ht > 100 & met > 150"
#	base = "chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2)<2.4 "
	base = "chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && ((nJets >= 2 && met > 150) ||(nJets >= 3 && met > 100)) && runNr < 201657 && (runNr < 198049 || runNr > 198522) && id1 < 0.15 && id2 < 0.15"
	baseSS = base.replace("chargeProduct < 0", "chargeProduct > 0")
	baseNonIso = base+"&& id1 > 0.15 && id1 < 1 && id2 > 0.15 && id2 < 1"
	edgeMass = "(20 < inv && inv < 70)"
	zMass = "(81 < inv && inv < 101)"
	highMass = "( inv > 120)"
	tightEta = "(abs(eta1) <1.4 && abs(eta2) < 1.4)"
	runAB = "(runNr <= 196531)"
	runC = "(runNr > 196531)"
#	effCorrected = "(1./eff1*1./eff2*weight)"
	highMET= "nJets >= 2 && ht > 100 && met > 150 && inv > 20"
	highMETBarrel= "nJets >= 2 && ht > 100 && met > 150 && (abs(eta1) <1.4 && abs(eta2) < 1.4) && inv > 20"
	highMETMll30to70= "nJets >= 2 && ht > 100 && met > 150 && p4.M() >30 && p4.M() < 70"
	METStudyControl= "nJets >= 2 && ht > 100 && met > 50 && met < 120 && p4.M() >30 && p4.M() < 70"
	highMETSignal2011= "nJets >= 2 && ht > 300 && met > 150"
	highMETControl2011= "nJets >= 2 && ht > 100 && ht <=300 && met > 150"
	lowMET= "nJets >= 3 && met > 100 && pt1 > 20 && pt2 > 20 && inv > 20 && (abs(eta1) <1.4 && abs(eta2) < 1.4)"
	lowMETBarrel= "nJets >= 3 && met > 100 && pt1 > 20 && pt2 > 20 && inv > 20 "
	control= "nJets == 2 && 100 < met && met > 150"
	ttbarLoose = "nBJets >= 1 && met > 75 && inv > 12 && (76 > inv || inv > 106)"# && pt1 > 20 && pt2 > 20"
	bTagged = "nJets >= 2 && ht > 100 && met > 50 && nBJets > 0"
	central = "abs(eta1) < 1.4 && abs(eta2) < 1.4"
	forward = "1.4 < TMath::Max(abs(eta1),abs(eta2))"

	cuts= {
		"SignalNonRectCentral_inclusiveMass": [base, central],
		"SignalNonRectCentral_edgeMass": [base, central, edgeMass],
		"SignalNonRectCentral_zMass": [base, central, zMass],
		"SignalNonRectCentral_highMass": [base, central, highMass],
		
		"SignalNonRectForward_inclusiveMass": [base, forward],
		"SignalNonRectForward_edgeMass": [base, forward, edgeMass],
		"SignalNonRectForward_zMass": [base, forward, zMass],
		"SignalNonRectForward_highMass": [base, forward, highMass],
		
		"HighMET_METStudy" : [highMETMll30to70],
		"METStudyControl" : [METStudyControl],
		"highMET_inclusiveMass": [base, highMET],
		"highMET_edgeMass":        [base, highMET, edgeMass ],
		"highMET_zMass": [base, highMET, zMass],
		"highMET_highMass": [base, highMET, highMass],
		"highMETBarrel_inclusiveMass": [base, highMETBarrel],
		"highMETBarrel_edgeMass":        [base, highMETBarrel, edgeMass ],
		"highMETBarrel_zMass": [base, highMETBarrel, zMass],
		"highMETBarrel_highMass": [base, highMETBarrel, highMass],
		
		#~ "Signal2011_inclusiveMass": [base, highMETSignal2011],
		#~ "Signal2011_edgeMass":        [base, highMETSignal2011, edgeMass ],
		#~ "Signal2011_zMass": [base, highMETSignal2011, zMass],
		#~ "Signal2011_highMass": [base, highMETSignal2011, highMass],
		
		#~ "Control2011_inclusiveMass": [base, highMET],
		#~ "Control2011_edgeMass":        [base, highMET, edgeMass ],
		#~ "Control2011_zMass": [base, highMET, zMass],
		#~ "Control2011_highMass": [base, highMET, highMass],
		
		"lowMET_inclusiveMass": [base, lowMET],
		"lowMET_edgeMass":       [base, lowMET, edgeMass ],
		"lowMET_zMass":             [base, lowMET, zMass],
		"lowMET_highMass":        [base, lowMET, highMass],
		"lowMETBarrel_inclusiveMass": [base, lowMETBarrel],
		"lowMETBarrel_edgeMass":       [base, lowMETBarrel, edgeMass ],
		"lowMETBarrel_zMass":             [base, lowMETBarrel, zMass],
		"lowMETBarrel_highMass":        [base, lowMETBarrel, highMass],

		"control_inclusiveMass": [base, control],
		"control_edgeMass":       [base, control, edgeMass ],
		"control_zMass":             [base, control, zMass],
		"control_highMass":        [base, control, highMass],

		"ttbarLoose_inclusiveMass": [base, ttbarLoose],
		"ttbarLoose_edgeMass": [base, ttbarLoose, edgeMass],
		"ttbarLoose_highMass": [base, ttbarLoose, highMass],

		"bTagged_inclusiveMass": [base, bTagged],
		"bTagged_edgeMass":        [base, bTagged, edgeMass ],
		"bTagged_zMass":     [base, bTagged, zMass],
		"bTagged_highMass": [base, bTagged, highMass],
		
		"OS_inclusiveMass": [base],
		"OS_edgeMass":        [base, edgeMass ],
		"OS_zMass":     [base, zMass],
		"OS_highMass": [base, highMass],


		"SS_inclusiveMass": [baseSS],
                "SS_edgeMass":        [baseSS, edgeMass ],
                "SS_zMass":     [baseSS, zMass],
                "SS_highMass": [baseSS, highMass],

				}
	
	titles = {
		"SignalNonRectCentral": "Central Signal Region",
		"SignalNonRectForward": "Forward Signal Region",
		"inclusiveMass": "m_{ll} > 20 GeV",
		"edgeMass":        "20 < m_{ll} < 70 GeV, ",
		"zMass": ", 81 < m_{ll} < 101 GeV, ",
		"highMass": ",  m_{ll} > 120 GeV, ",

		"HighMET_METStudy" : "E^{miss}_{T} > 150 GeV, H_{T} > 100 GeV, n_{Jets} #geq 2 30 GeV < m_{ll} < 70 GeV", 
		"METStudyControl" : "50 GeV < E^{miss}_{T} < 120 GeV, H_{T} > 100 GeV, n_{Jets} #geq 2 30 GeV < m_{ll} < 70 GeV", 

		"OS": "two OS leptons, n_{Jets} #geq 2",
		"SS": "two SS leptons, n_{Jets} #geq 2",
		"highMET":"E^{miss}_{T} > 150 GeV, H_{T} > 100 GeV, n_{Jets} #geq 2, |#eta| < 2.4",
		"highMETBarrel":"E^{miss}_{T} > 150 GeV, H_{T} > 100 GeV, n_{Jets} #geq 2 |#eta| < 1.4",
		#~ "Signal2011":"E^{miss}_{T} > 150 GeV, H_{T} > 300 GeV, n_{Jets} #geq 2",
		#~ "Control2011":"E^{miss}_{T} > 150 GeV, 100 < H_{T} <= 300 GeV, n_{Jets} #geq 2",
		"lowMET":"E^{miss}_{T} > 100 GeV, n_{Jets} #geq 3, |#eta| < 2.4",
		"lowMETBarrel":"E^{miss}_{T} > 100 GeV, n_{Jets} #geq 3, |#eta| < 1.4",
		"control":"100 < E^{miss}_{T} < 150 GeV,n_{Jets} = 2",
		"ttbarLoose":"1 b-tag, E^{miss}_{T} > 75 GeV, z-veto(76,106)",
		"bTagged":"1 b-tag, E^{miss}_{T} > 50 GeV, H_{T} > 100 GeV, n_{Jets} #geq 2",
		
		}

	for name in cuts.keys():
		title = ""
		for titleName, titlePart in titles.iteritems():
			if titleName in name:
				title += titlePart
		titles[name] = title

	selections = []
	#~ selections += ["HighMET_METStudy","METStudyControl"]
	selections += ["SignalNonRectCentral_inclusiveMass", "SignalNonRectCentral_edgeMass", "SignalNonRectCentral_zMass", "SignalNonRectCentral_highMass",]#
	selections += ["SignalNonRectForward_inclusiveMass", "SignalNonRectForward_edgeMass", "SignalNonRectForward_zMass", "SignalNonRectForward_highMass",]#
	#~ selections += ["highMET_inclusiveMass", "highMET_edgeMass", "highMET_zMass", "highMET_highMass",]
	#~ selections += ["highMETBarrel_inclusiveMass", "highMETBarrel_edgeMass", "highMETBarrel_zMass", "highMETBarrel_highMass",]#
	#~ selections += ["Signal2011_inclusiveMass", "Signal2011_edgeMass", "Signal2011_zMass", "Signal2011_highMass",]#
	#~ selections += ["Control2011_inclusiveMass", "Control2011_edgeMass", "Control2011_zMass", "Control2011_highMass",]#
	#~ selections += ["lowMET_inclusiveMass","lowMET_edgeMass",  "lowMET_zMass", "lowMET_highMass",]#
	#~ selections += ["lowMETBarrel_inclusiveMass","lowMETBarrel_edgeMass",  "lowMETBarrel_zMass", "lowMETBarrel_highMass",]#
	#~ selections += ["control_inclusiveMass","control_edgeMass",  "control_zMass", "control_highMass",]#
#	selections += [ "ttbarLoose_inclusiveMass", "ttbarLoose_edgeMass","ttbarLoose_highMass"] #
	#~ selections += [ "OS_inclusiveMass", "OS_edgeMass", "OS_zMass","OS_highMass"] #
	#~ selections += [ "SS_inclusiveMass", "SS_edgeMass", "SS_zMass","SS_highMass"] #   
	#~ selections += ["bTagged_inclusiveMass",  "bTagged_edgeMass","bTagged_zMass", "bTagged_highMass"]
				   #~ #"jzb100_inclusiveMass",  "jzb100_zMass","jzb50_inclusiveMass","jzb50_zMass"] #"","jzb100_edgeMass","jzb50_edgeMass",
	variables =["sqrts","inv","nJets", "nBJets","nLightLeptons","ht", "met","tcMet","type1Met","caloMet","mht","ptLead","ptTrail","isoLead","isoTrail" ,"etaLead","etaTrail" ,"deltaR", "deltaPhi","deltaPhiJetMET","deltaPhiSecondJetMET","deltaPhiLeptonMETHard","deltaPhiLeptonMETSoft","meanIP", "jzb","nVertices"]
	#~ variables = ["ptLead","ptTrail","invZoomed"]
	#~ variables = ["isoLead","isoTrail"]
	#selections = filter(lambda x: x.endswith("_highMass"), selections)

	if False:
		for name in cuts:
			cuts[name] += [effCorrected]

		makeSlides(trees, cuts, variables, titles, selections, datasetName, runAB, effAntiCorrected)
	else:
		if argv[2] == "2012":
			makeSlides(trees, cuts, variables, titles, selections, datasetName, runAB, runC)
		elif argv[2] == "2011":
			makeSlides2011(trees, cuts, variables, titles, selections, datasetName)
		else: 
			print "Nothing to do here"
			
main()
