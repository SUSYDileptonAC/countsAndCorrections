import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)



def readTreeFromFile(path):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/genWeightSum74FinalTrees/Tree"%(path))
	return result

	
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
	for filePath in glob("%s/genWeights*.root"%path):
		sampleName = match(".*genWeights.*\.genWeightSum74.*\.(.*).root", filePath).groups()[0]
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
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		rootFile = TFile(filePath, "read")
		result[sampleName] = rootFile.FindObjectAny("analysis paths").GetBinContent(1)
	return result
	
def readTrees(path):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFile(filePath)
		
	return result
	
def createHistoFromTree(tree, variable, weight, nBins, firstBin, lastBin, nEvents = -1,isMC=False):
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

	
	if isMC and tree.CopyTree("genWeight < 0").GetEntries() > 0:
		posWeight = "(genWeight > 0)*"+weight
		negWeight = "(genWeight < 0)*"+weight
		
		resultPos = TH1F(name+"Pos", "", nBins, firstBin, lastBin)
		resultPos.Sumw2()
		tree.Draw("%s>>%s"%(variable, name+"Pos"), posWeight, "goff", nEvents)		
		resultNeg = TH1F(name+"Neg", "", nBins, firstBin, lastBin)
		resultNeg.Sumw2()
		tree.Draw("%s>>%s"%(variable, name+"Neg"), negWeight, "goff", nEvents)
		
		
		
		#~ for binNumber in range(0,nBins+1):
							
		
	
	return result
	
	
if (__name__ == "__main__"):
	path = "/home/jan/Trees/genWeightTrees/"
	from sys import argv
	import pickle	

	
	cutsNeg = "genWeight < 0"
	cutsPos = "genWeight > 0"


	

	trees = readTrees(path)	
	for name, tree in trees.iteritems():
		print name
		print "events with pos. weight: %d"%tree.CopyTree(cutsPos).GetEntries()
		print "events with neg. weight: %d"%tree.CopyTree(cutsNeg).GetEntries()
		print "fraction: %.3f"%(float(tree.CopyTree(cutsNeg).GetEntries())/(tree.CopyTree(cutsPos).GetEntries() + tree.CopyTree(cutsNeg).GetEntries()))


