import ROOT
from ConfigParser import ConfigParser

config_path = "../SubmitScripts/Input"
config = ConfigParser()
config.read("%s/Master53XOnTheFly.ini"%config_path)



tableTemplateMC = r"""
\begin{tabular}{c|c}
 process & sample \\
%s
\end{tabular}
"""
tableTemplateData = r"""
\begin{tabular}{c|c|c}
 Primary dataset & purpose & dataset \\
%s
\end{tabular}
"""
tableTemplateMCReduced = r"""
\begin{tabular}{c|c|c|c|c|c}
category & process & generator &  cross section [pb] & processed events & weight\\
%s
\end{tabular}
"""


class Process:
	samples = []
	xsecs = []
	DBSPaths = []
	nEvents = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = ROOT.TH1F()
	uncertainty = 0.
	scaleFac = 1.
	additionalSelection = None
	
	
	def __init__(self, samplename=["none"],Counts={"none":-1},labels = "none",sublabels = [],color=0,lineColor=0,uncertainty=0.,scaleFac=1.,Run2011=False, additionalSelection=None,data=False):
		self.samples = []
		self.xsecs = []
		self.nEvents = []
		self.DBSPaths = []
		self.label = labels
		self.labels = sublabels
		self.theColor = color
		self.theLineColor = lineColor
		self.histo.SetLineColor(lineColor)
		self.histo.SetFillColor(color)
		self.uncertainty = uncertainty
		self.scaleFac = scaleFac
		self.additionalSelection = additionalSelection
		for sample in samplename:
			self.samples.append(sample)					
			if Run2011:
				if not data:
					self.xsecs.append(eval(config42.get(sample,"crosssection")))
				self.DBSPaths.append(config42.get(sample,"datasetpath"))
			else:
				if not data:
					self.xsecs.append(eval(config.get(sample,"crosssection")))
				self.DBSPaths.append(config.get(sample,"datasetpath"))
				if not data:
					self.nEvents.append(Counts[sample])
			if data:
				self.xsecs.append(0)
				self.nEvents.append(0)
		
class Backgrounds:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph_Summer12"]
		label = "Madgraph t\\bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TTJetsSystematic:
		subprocesses = ["TTJets_madgraph_Summer12","TTJets_mass166_5_madgraph_Summer12_v1","TTJets_mass169_5_madgraph_Summer12_v1","TTJets_mass175_5_madgraph_Summer12_v1","TTJets_mass178_5_madgraph_Summer12_v1","TTJets_matchingup_madgraph_Summer12_v1","TTJets_matchingdown_madgraph_Summer12_v1","TTJets_scaleup_madgraph_Summer12_v1","TTJets_scaledown_madgraph_Summer12_v1"]
		label = "$t\\bar{t}$ Systematics"
		labels = ["$t\\bar{t}$","$t\\bar{t}$, $m_{top} =$ 166.5 GeV","$t\\bar{t}$, $m_{top} =$ 169.5 GeV","$t\\bar{t}$, $m_{top} =$ 175.5 GeV","$t\\bar{t}$, $m_{top} =$ 178.5 GeV","$t\\bar{t}$, Matching scale up","$t\\bar{t}$, Matching scale down","$t\\bar{t}$, Factorization scale up","$t\\bar{t}$, Factorization scale down"]
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class WJets:
		subprocesses = ["WJets_madgraph_Summer12"]
		label = "W"
		labels = ["$W \\rightarrow l\\nu$"]
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TTJets_SpinCorrelations:
		subprocesses = ["TTJets_MGDecays_madgraph_Summer12","TTJets_MGDecays_SemiLept_madgraph_Summer12","TTJets_MGDecays_FullHad_madgraph_Summer12"]
		labels = ["$t\\bar{t} \\rightarrow b\\bar{b}l\\nu l\\nu$","$t\\bar{t} \\rightarrow b\\bar{b}q\\bar{q}l\\nu$","$t\\bar{t} \\rightarrow b\\bar{b}q\\bar{q}q\\bar{q}$"]
		label = "$t\\bar{t}$"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TT:
		subprocesses = ["TT_Powheg_Summer12_v2"] 
		label = "t\\bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class TT_Dileptonic:
		subprocesses = ["TT_Dileptonic_Powheg_Summer12_v1"] 
		label = "Powheg t\\bar{t} Dileptonic"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
		additionalSelection = None
	class TT_MCatNLO:
		subprocesses = ["TT_MCatNLO_Summer12_v1"] 
		label = "MCatNLO t\\bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class Diboson:
		subprocesses = ["ZZJetsTo2L2Q_madgraph_Summer12","ZZJetsTo2L2Nu_madgraph_Summer12","ZZJetsTo4L_madgraph_Summer12","WZJetsTo3LNu_madgraph_Summer12","WZJetsTo2L2Q_madgraph_Summer12","WWJetsTo2L2Nu_madgraph_Summer12"]
		label = "WW,WZ,ZZ"
		labels = ["$ZZ \\rightarrow l^{+}l^{-}q\\bar{q}$","$ZZ \\rightarrow l^{+}l^{-}\\nu\\nu$","$ZZ \\rightarrow l^{+}l^{-}l^{+}l^{-}$","$WZ \\rightarrow l\\nu l^{+}l^{-}$","$WZ \\rightarrow qq'l^{+}l^{-}$","$WW \\rightarrow l\\nu l\\nu$"]
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class Rare:
		subprocesses = ["WWWJets_madgraph_Summer12","WWGJets_madgraph_Summer12","WWZNoGstarJets_madgraph_Summer12","WZZNoGstar_madgraph_Summer12","TTGJets_madgraph_Summer12","TTWJets_madgraph_Summer12","TTZJets_madgraph_Summer12","TTWWJets_madgraph_Summer12"]
		label = "Other SM"
		labels = ["$WWW$","$WW\\gamma$","$WWZ$","$WZZ$","$t\\bar{t}\\gamma$","$t\\bar{t}W$","$t\\bar{t}Z$","$t\\bar{t}WW$"]
		fillcolor = 630
		linecolor = ROOT.kBlack
		uncertainty = 0.5
		scaleFac     = 1.	
		additionalSelection = None	
	class DrellYan:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "Drell-Yan"
		labels = ["$Z/\\gamma^{*} \\rightarrow l^{+}l^{-}$ 10 GeV $< m_{ll} <$ 50 GeV","$Z/\\gamma^{*} \\rightarrow l^{+}l^{-}$ $m_{ll} >$ 50 GeV"]
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) != 15 || abs(motherPdgId2) != 15)"
	class DrellYanTauTau:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "DY+jets (#tau#tau)"
		fillcolor = ROOT.kOrange
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = "(abs(motherPdgId1) == 15 && abs(motherPdgId2) == 15)"
	class SingleTop:
		subprocesses = ["T_sChannel_Powheg_Summer12","T_tChannel_Powheg_Summer12","T_tWChannel_Powheg_Summer12","TBar_sChannel_Powheg_Summer12","TBar_tChannel_Powheg_Summer12","TBar_tWChannel_Powheg_Summer12"]
		label = "single top"
		labels = ["$t$ s-Channel","$t$ t-Channel","$t$ tW-Channel","$\\bar{t}$ s-Channel","$\\bar{t}$ t-Channel","$\\bar{t}$ tW-Channel"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class DoubleElectron:
		subprocesses = ["DoubleElectron_Run2012A_22Jan2013","DoubleElectron_Run2012B_22Jan2013","DoubleElectron_Run2012C_22Jan2013","DoubleElectron_Run2012D_22Jan2013"]
		label = "\\verb+DoubleElectron+"
		labels = ["Signal","Dielectron","Dielectron","Dielectron"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class DoubleMu:
		subprocesses = ["DoubleMu_Run2012A_22Jan2013","DoubleMu_Run2012B_22Jan2013","DoubleMu_Run2012C_22Jan2013","DoubleMu_Run2012D_22Jan2013"]
		label = "\\verb+DoubleMu+"
		labels = ["Signal","Dimuon","Dimuon","Dimuon"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class MuEG:
		subprocesses = ["MuEG_Run2012A_22Jan2013","MuEG_Run2012B_22Jan2013","MuEG_Run2012C_22Jan2013","MuEG_Run2012D_22Jan2013"]
		label = "MuEG"
		labels = ["Background prediction","$e+\mu$","$e+\mu$","$e+\mu$"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class HT:
		subprocesses = ["HT_Run2012A_22Jan2013","HT_Run2012B_22Jan2013","HT_Run2012C_22Jan2013","HT_Run2012D_22Jan2013"]
		label = "\\verb+HT+, \\verb+JetHT+"
		labels = ["trigger efficiencies","PFHT","PFHT","PFHT"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class HTMHT:
		subprocesses = ["HTMHT_Run2012B_22Jan","HTMHT_Run2012C_22Jan","HTMHT_Run2012D_22Jan"]
		label = "\\verb+HTMHT+"
		labels = ["additional trigger studies","$\\alpha_T$","$\\alpha_T$","$\\alpha_T$"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class SingleElectron:
		subprocesses = ["SingleElectron_Run2012A_22Jan","SingleElectron_Run2012B_22Jan","SingleElectron_Run2012C_22Jan","SingleElectron_Run2012D_22Jan"]
		label = "\\verb+SingleElectron+"
		labels = ["additional trigger studies","Single electron","Single electron","Single electron"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
	class SingleMu:
		subprocesses = ["SingleMu_Run2012A_22Jan","SingleMu_Run2012B_22Jan","SingleMu_Run2012C_22Jan","SingleMu_Run2012D_22Jan"]
		label = "\\verb+SingleMu+"
		labels = ["additional trigger studies","Single muon","Single muon","Single muon"]
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None

def getFilePathsAndSampleNames(path):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	for filePath in glob("%s/sw538*.root"%path):

		sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]
		#for the python enthusiats: yield sampleName, filePath is more efficient here :)
		result[sampleName] = filePath
	return result

def totalNumberOfGeneratedEvents(path):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path

	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		#~ print filePath
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result


def main():
	
	path = "/home/jan/Trees/sw538v0478"
	
	eventCounts = totalNumberOfGeneratedEvents(path)
		
	TTJets = Process(Backgrounds.TTJets_SpinCorrelations.subprocesses,eventCounts,Backgrounds.TTJets_SpinCorrelations.label,Backgrounds.TTJets_SpinCorrelations.labels,Backgrounds.TTJets_SpinCorrelations.fillcolor,Backgrounds.TTJets_SpinCorrelations.linecolor,Backgrounds.TTJets_SpinCorrelations.uncertainty,1)	
	Diboson = Process(Backgrounds.Diboson.subprocesses,eventCounts,Backgrounds.Diboson.label,Backgrounds.Diboson.labels,Backgrounds.Diboson.fillcolor,Backgrounds.Diboson.linecolor,Backgrounds.Diboson.uncertainty,1)	
	Rare = Process(Backgrounds.Rare.subprocesses,eventCounts,Backgrounds.Rare.label,Backgrounds.Rare.labels,Backgrounds.Rare.fillcolor,Backgrounds.Rare.linecolor,Backgrounds.Rare.uncertainty,1)	
	DY = Process(Backgrounds.DrellYan.subprocesses,eventCounts,Backgrounds.DrellYan.label,Backgrounds.DrellYan.labels,Backgrounds.DrellYan.fillcolor,Backgrounds.DrellYan.linecolor,Backgrounds.DrellYan.uncertainty,1,additionalSelection=Backgrounds.DrellYan.additionalSelection)	
	W = Process(Backgrounds.WJets.subprocesses,eventCounts,Backgrounds.WJets.label,Backgrounds.WJets.labels,Backgrounds.WJets.fillcolor,Backgrounds.WJets.linecolor,Backgrounds.WJets.uncertainty,1,additionalSelection=Backgrounds.WJets.additionalSelection)	
	Syst = Process(Backgrounds.TTJetsSystematic.subprocesses,eventCounts,Backgrounds.TTJetsSystematic.label,Backgrounds.TTJetsSystematic.labels,Backgrounds.TTJetsSystematic.fillcolor,Backgrounds.TTJetsSystematic.linecolor,Backgrounds.TTJetsSystematic.uncertainty,1,additionalSelection=Backgrounds.TTJetsSystematic.additionalSelection)	
	#~ DYTauTau = Process(Backgrounds.DrellYanTauTau.subprocesses,eventCounts,Backgrounds.DrellYanTauTau.label,Backgrounds.DrellYanTauTau.fillcolor,Backgrounds.DrellYanTauTau.linecolor,Backgrounds.DrellYanTauTau.uncertainty,1,additionalSelection=Backgrounds.DrellYanTauTau.additionalSelection)	
	SingleTop = Process(Backgrounds.SingleTop.subprocesses,eventCounts,Backgrounds.SingleTop.label,Backgrounds.SingleTop.labels,Backgrounds.SingleTop.fillcolor,Backgrounds.SingleTop.linecolor,Backgrounds.SingleTop.uncertainty,1)		
	DoubleElectron = Process(Backgrounds.DoubleElectron.subprocesses,eventCounts,Backgrounds.DoubleElectron.label,Backgrounds.DoubleElectron.labels,Backgrounds.DoubleElectron.fillcolor,Backgrounds.DoubleElectron.linecolor,Backgrounds.DoubleElectron.uncertainty,1,data=True)		
	DoubleMu = Process(Backgrounds.DoubleMu.subprocesses,eventCounts,Backgrounds.DoubleMu.label,Backgrounds.DoubleMu.labels,Backgrounds.DoubleMu.fillcolor,Backgrounds.DoubleMu.linecolor,Backgrounds.DoubleMu.uncertainty,1,data=True)		
	MuEG = Process(Backgrounds.MuEG.subprocesses,eventCounts,Backgrounds.MuEG.label,Backgrounds.MuEG.labels,Backgrounds.MuEG.fillcolor,Backgrounds.MuEG.linecolor,Backgrounds.MuEG.uncertainty,1,data=True)		
	SingleElectron = Process(Backgrounds.SingleElectron.subprocesses,eventCounts,Backgrounds.SingleElectron.label,Backgrounds.SingleElectron.labels,Backgrounds.SingleElectron.fillcolor,Backgrounds.SingleElectron.linecolor,Backgrounds.SingleElectron.uncertainty,1,data=True)		
	SingleMu = Process(Backgrounds.SingleMu.subprocesses,eventCounts,Backgrounds.SingleMu.label,Backgrounds.SingleMu.labels,Backgrounds.SingleMu.fillcolor,Backgrounds.SingleMu.linecolor,Backgrounds.SingleMu.uncertainty,1,data=True)		
	HT = Process(Backgrounds.HT.subprocesses,eventCounts,Backgrounds.HT.label,Backgrounds.HT.labels,Backgrounds.HT.fillcolor,Backgrounds.HT.linecolor,Backgrounds.HT.uncertainty,1,data=True)		
	HTMHT = Process(Backgrounds.HTMHT.subprocesses,eventCounts,Backgrounds.HTMHT.label,Backgrounds.HTMHT.labels,Backgrounds.HTMHT.fillcolor,Backgrounds.HTMHT.linecolor,Backgrounds.HTMHT.uncertainty,1,data=True)		
	
	
	processes = [TTJets,DY,W,Diboson,SingleTop,Rare,Syst]
	processesData = [DoubleElectron,DoubleMu,MuEG,HT,HTMHT,SingleElectron,SingleMu]
	
	
	
	lineTemplate = r"%s & \verb+%s+ \\"+"\n"
	lineTemplateData = r"%s & %s & \verb+%s+\\"+"\n"
	lineTemplateReduced = r"%s & %s & %s & %.2f & %d & %.2f \\"+"\n"
	result = ""
	resultData = ""
	resultReduced = ""
	generator = "Madgraph"
	for process in processes:
		result += "\hline \n"
		resultReduced += "\hline \n"
		first = True
		for index, subprocess in enumerate(process.samples):
			generator = "Madgraph"
			if first:
				firstEntry = process.label
			else:
				firstEntry = ""
			result += lineTemplate%(process.labels[index],process.DBSPaths[index])	
			if "powheg" in process.DBSPaths[index]:
				generator = "Powheg"
			elif "CT10" in process.DBSPaths[index]:
				generator = "MC@NLO"
			resultReduced += lineTemplateReduced%(firstEntry,process.labels[index],generator,process.xsecs[index],eventCounts[subprocess],(19800*process.xsecs[index])/eventCounts[subprocess])	
			first = False
	for process in processesData:
		resultData += "\hline \n"
		first = True
		for index, subprocess in enumerate(process.samples):
			if first:
				firstEntry = process.label
				secondEntry = process.labels[index]
			else:
				firstEntry = ""
				secondEntry = ""
			resultData += lineTemplateData%(firstEntry,secondEntry,process.DBSPaths[index])	
			first = False
			
	table = tableTemplateMC%result
	tableData = tableTemplateData%resultData
	tableReduced = tableTemplateMCReduced%resultReduced
	outFile = open("tab/table_MCSamples.tex","w")
	outFile.write(table)
	outFile.close()	
	outFile = open("tab/table_MCSamplesReduced.tex","w")
	outFile.write(tableReduced)
	outFile.close()	
	outFile = open("tab/table_DataSamples.tex","w")
	outFile.write(tableData)
	outFile.close()	
main()
