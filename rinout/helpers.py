import ROOT
from ROOT import TCanvas, TPad, TH1F, TH1I, THStack, TLegend, TMath
from defs import defineMyColors
from defs import myColors
from defs import mainConfig
from ConfigParser import ConfigParser

config_path = "/home/jan/Doktorarbeit/Dilepton/projects/SubmitScripts/Input"
config = ConfigParser()
config.read("%s/Master53X.ini"%config_path)

config42 = ConfigParser()
config42.read("%s/Master42Y.ini"%config_path)
nEvents = -1

def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

def readTreeFromFile(path, dileptonCombination,Run2011=False,use532=False):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	if Run2011:
		result.Add("%s/cutsV18SignalHighPtFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	elif use532:		
		result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	else:		
		result.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")	
	return result
def readMCTreeFromFile(path,dileptonTrigger, dileptonCombination,Run2011=False):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	if Run2011:
		result.Add("%s/cutsV18SignalHighPtFinalTrees/%sDileptonTree"%(path, dileptonCombination))		
	else:
		result.Add("%s/cutsV23Dilepton%sFinalTrees/%sDileptonTree"%(path,dileptonTrigger, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")	
	return result
def readVectorTreeFromFile(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonVectorTree"%(path, dileptonCombination))
	if mainConfig.preselect:
		result = result.CopyTree("nJets >= 2")
	return result

	
	
def totalNumberOfGeneratedEvents(path,Run2011=False):
	"""
	path: path to directory containing all sample files

	returns dict samples names -> number of simulated events in source sample
	        (note these include events without EMu EMu EMu signature, too )
	"""
	from ROOT import TFile
	result = {}
	#~ print path
	if Run2011:
			
		for sampleName, filePath in getFilePathsAndSampleNames(path,Run2011).iteritems():
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	else:
		for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
			#~ print filePath
			rootFile = TFile(filePath, "read")
			result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)				
	return result
	
def readTrees(path, dileptonCombination,Run2011=False,use532 = False):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	if Run2011:
			
		for sampleName, filePath in getFilePathsAndSampleNames(path,Run2011=True).iteritems():
			
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination,Run2011=True)
		
	elif use532:
		
		for sampleName, filePath in getFilePathsAndSampleNames(path,use532=True).iteritems():
		
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination,use532=True)
	else:

		for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
			result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
	return result
def readTreesMC(path,dileptonTrigger, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readMCTreeFromFile(filePath,dileptonTrigger, dileptonCombination)
		
	return result
def readVectorTrees(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	#~ print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readVectorTreeFromFile(filePath, dileptonCombination)
		
	return result

	
def getFilePathsAndSampleNames(path,Run2011=False,use532 = False):
	"""
	helper function
	path: path to directory containing all sample files

	returns: dict of smaple names -> path of .root file (for all samples in path)
	"""
	result = []
	from glob import glob
	from re import match
	result = {}
	if Run2011:
		for filePath in glob("%s/sw428*.root"%path):

			
			sampleName = match(".*sw428v.*\.cutsV18SignalHighPt.*\.(.*).root", filePath).groups()[0]			
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath		
	elif use532:
		for filePath in glob("%s/sw532*.root"%path):

			
			sampleName = match(".*sw532v.*\.processed.*\.(.*).root", filePath).groups()[0]				
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath		
	else:
		for filePath in glob("%s/sw538*.root"%path):
			
			sampleName = match(".*sw538v.*\.processed.*\.(.*).root", filePath).groups()[0]			
			#for the python enthusiats: yield sampleName, filePath is more efficient here :)
			result[sampleName] = filePath
	return result


	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1):
	"""
	tree: tree to create histo from)
	variable: variable to plot (must be a branch of the tree)
	weight: weights to apply (e.g. "var1*(var2 > 15)" will use weights from var1 and cut on var2 > 15
	nBins, firstBin, lastBin: number of bins, first bin and last bin (same as in TH1F constructor)
	nEvents: number of events to process (-1 = all)
	"""
	from ROOT import TH1F
	from random import randint
	from sys import maxint
	if nEvents < 0:
		nEvents = maxint
	#make a random name you could give something meaningfull here,
	#but that would make this less readable
	name = "%x"%(randint(0, maxint))
	result = TH1F(name, "", nBins, firstBin, lastBin)
	result.Sumw2()
	tree.Draw("%s>>%s"%(variable, name), weight, "goff", nEvents)
	return result


def createMyColors():
    iIndex = 2000

    containerMyColors = []
    for color in defineMyColors.keys():
        tempColor = ROOT.TColor(iIndex,
            float(defineMyColors[color][0]) / 255, float(defineMyColors[color][1]) / 255, float(defineMyColors[color][2]) / 255)
        containerMyColors.append(tempColor)

        myColors.update({ color: iIndex })
        iIndex += 1

    return containerMyColors
	
class Process:
	samples = []
	xsecs = []
	nEvents = []
	label = ""
	theColor = 0
	theLineColor = 0 
	histo = ROOT.TH1F()
	uncertainty = 0.
	scaleFac = 1.
	additionalSelection = None
	
	def __init__(self, samplename=["none"],Counts={"none",-1},labels = "none",color=0,lineColor=0,uncertainty=0.,scaleFac=1.,Run2011=False, additionalSelection=None):
		self.samples = []
		self.xsecs = []
		self.nEvents = []
		self.label = labels
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
				self.xsecs.append(eval(config42.get(sample,"crosssection")))
			else:
				self.xsecs.append(eval(config.get(sample,"crosssection")))
			self.nEvents.append(Counts[sample])

		
	def createCombinedHistogram(self,lumi,plot,tree1,tree2 = "None",shift = 1.,scalefacTree1=1.,scalefacTree2=1.,TopWeightUp=False,TopWeightDown=False):
		self.histo = TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		
		if self.additionalSelection != None:
			print "Applying additional selection: %s"%self.additionalSelection
			cut = plot.cuts.replace("weightBlockA*(","weightBlockA*(%s &&"%self.additionalSelection)
		else: 
			cut = plot.cuts
		#~ if "100" in cut:
			#~ weightNorm = 1./0.91
		#~ elif "150" in cut and not "100" in cut:
			#~ weightNorm = 1./0.87
		#~ else:
		weightNorm = 1./0.99
		
					
		for index, sample in enumerate(self.samples):
			from defs import mainConfig
			for name, tree in tree1.iteritems(): 
				if name == sample:
					if mainConfig.doTopReweighting and "TT" in name:
						#~ tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.148-0.00129*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
						
						if TopWeightUp:
							tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
						elif TopWeightDown:	
							tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
						else:	
							tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
					else:
						tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)				
		#~ 
					#~ print "-------------------------------------"
					#~ print "process: %s"%name
					#~ print "cut string: %s"%cut
					#~ print "raw count: %f"%tempHist.Integral()					
					#~ print "lumi: %f"%lumi
					#~ print "cross section %f"%self.xsecs[index]
					#~ print "number of events in sample: %f"%self.nEvents[index]
					#~ print "scale factor Data/MC: %f"%scalefacTree1
					#~ print "combined scale factor: %f"%(lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index])
					tempHist.Scale((lumi*scalefacTree1*self.xsecs[index]/self.nEvents[index]))
					#~ print "scaled number in signal region: %f"%tempHist.Integral()
					self.histo.Add(tempHist.Clone())
			if tree2 != "None":		
				for name, tree in tree2.iteritems(): 
					if name == sample:
						if mainConfig.doTopReweighting and "TT" in name:
							if TopWeightUp:
								tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
							elif TopWeightDown:	
								tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
							else:	
								tempHist = createHistoFromTree(tree, plot.variable , "%f*sqrt(exp(0.156-0.00137*genPtTop1)*exp(0.148-0.00129*genPtTop2))*"%weightNorm+cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
						else:
							tempHist = createHistoFromTree(tree, plot.variable , cut , plot.nBins, plot.firstBin, plot.lastBin, nEvents)
						

						tempHist.Scale((lumi*self.xsecs[index]*scalefacTree2/self.nEvents[index]))

						self.histo.Add(tempHist.Clone())
		self.histo.SetFillColor(self.theColor)
		self.histo.SetLineColor(self.theLineColor)
		self.histo.GetXaxis().SetTitle(plot.xaxis) 
		self.histo.GetYaxis().SetTitle(plot.yaxis)	
				
		return self.histo

	
class TheStack:
	from ROOT import THStack
	theStack = THStack()	
	theHistogram = ROOT.TH1F()	
	theHistogramXsecUp = ROOT.TH1F()
	theHistogramXsecDown = ROOT.TH1F()
	def  __init__(self,processes,lumi,plot,tree1,tree2,shift = 1.0,scalefacTree1=1.0,scalefacTree2=1.0,saveIntegrals=False,counts=None,JESUp=False,JESDown=False,TopWeightUp=False,TopWeightDown=False):
		self.theStack = THStack()
		self.theHistogram = ROOT.TH1F()
		self.theHistogram.Sumw2()
		self.theHistogramXsecDown = ROOT.TH1F()
		self.theHistogramXsecUp = ROOT.TH1F()
		self.theHistogram = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecDown = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)
		self.theHistogramXsecUp = ROOT.TH1F("","",plot.nBins,plot.firstBin,plot.lastBin)


			

			
			
		for process in processes:
			temphist = TH1F()
			temphist.Sumw2()
			if TopWeightUp:
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightUp=True)
			elif TopWeightDown:	
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2,TopWeightDown=True)
			else:	
				temphist = process.createCombinedHistogram(lumi,plot,tree1,tree2,shift,scalefacTree1,scalefacTree2)
			if saveIntegrals:
				
				errIntMC = ROOT.Double()
				intMC = temphist.IntegralAndError(0,temphist.GetNbinsX()+1,errIntMC)				
				
				val = float(intMC)
				err = float(errIntMC)
				if JESUp:
					jesUp = abs(counts[process.label]["val"]-val)
					counts[process.label]["jesUp"]=jesUp
				elif JESDown:
					jesDown = abs(counts[process.label]["val"]-val)
					counts[process.label]["jesDown"]=jesDown
				else:
					xSecUncert = val*process.uncertainty
					counts[process.label] = {"val":val,"err":err,"xSec":xSecUncert}
					#~ counts[process.label]["val"]=val
					#~ counts[process.label]["err"]=err
					#~ counts[process.label]["xSec"]=xSecUncert
				
			self.theStack.Add(temphist.Clone())
			self.theHistogram.Add(temphist.Clone())
			temphist2 = temphist.Clone()
			temphist2.Scale(1-process.uncertainty)
			self.theHistogramXsecDown.Add(temphist2.Clone())
			temphist3 = temphist.Clone()
			temphist3.Scale(1+process.uncertainty)
			self.theHistogramXsecUp.Add(temphist3.Clone())

def getDataHist(plot,tree1,tree2="None",Run2011=False,Run201153X=False,Block="None"):
	histo = TH1F()
	histo2 = TH1F()
	if Run201153X:
		dataname = "MergedData2011"
	elif Run2011: 
		dataname = "Data2011_42"
	else:
		if Block == "BlockA":
			dataname= "MergedData_BlockA"
		elif Block == "BlockB":
			dataname= "MergedData_BlockB"
		else:
			dataname = "MergedData"	
	for name, tree in tree1.iteritems():
		if name == dataname:
			histo = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
	if tree2 != "None":		
		for name, tree in tree2.iteritems():
			if name == dataname:
				histo2 = createHistoFromTree(tree, plot.variable , plot.cuts , plot.nBins, plot.firstBin, plot.lastBin)
				histo.Add(histo2.Clone())
	#~ print histo.Integral()					
	return histo	
				
def getTotalTopWeight(genPt1,genPt2):
	from math import exp,sqrt
	## 8 TeV Dilepton
	a = 0.148
	b = -0.00129 
	sf1 = exp(a*genPt1+b)
	sf2 = exp(a*genPt2+b)
	
	result = sqrt(sf1+sf2)
	
	return result
