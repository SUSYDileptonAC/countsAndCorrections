#!/usr/bin/env python
import math
import ROOT
from ROOT import TMath
tableTemplate = r"""
\begin{tabular}{l|ccc|cc|c}
selection & $ee$ & $\mu\mu$ & $e\mu$ & $SF$ & $OF prediction$ & measured $n_{SF, OS}$\\
\hline
%s
\end{tabular}
"""

	
def readWeightedEntries(tree, variable, cut):
	
	nBins=55
	firstBin=15
	lastBin=70
	nEvents = -1
	histo = createHistoFromTree(tree,  variable, cut, nBins, firstBin, lastBin, nEvents)
	#(weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M()>15 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3) ) && (nJets >= 2 && ht > 100 && met > 150) && ((p4.M() < 70))
	events = histo.Integral()
	error =0
	if histo.GetEntries() > 0:
		error= math.sqrt(histo.GetEntries())*histo.Integral()/histo.GetEntries()	
	#~ if histo.GetEntries() > 0:
		#~ error = math.sqrt(histo.GetEntries())*histo.Integral()/histo.GetEntries()
	#print cut 	
	counts = {
		"events" : events,
		"error"  : error	
		}
	#~ print events
	#~ print error
	#~ print histo.GetEffectiveEntries()
	#~ print histo.GetEntries()

	return counts


def readTreeFromFile(path, dileptonCombination):
	"""
	helper functionfrom argparse import ArgumentParser
	path: path to .root file containing simulated events
	dileptonCombination: EMu, EMu, or EMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	result = TChain()
	result.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
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
	for filePath in glob("%s/sw532*.root"%path):

		sampleName = match(".*sw532v.*\.processed.*\.(.*).root", filePath).groups()[0]
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
	
def readTrees(path, dileptonCombination):
	"""
	path: path to directory containing all sample files
    dileptonCombination: "EMu", "EMu", or pyroot"EMu" for electron-electron, electron-muon, or muon-muon events

	returns: dict of sample names ->  trees containing events (for all samples for one dileptonCombination)
	"""
	result = {}
	print (path)
	for sampleName, filePath in getFilePathsAndSampleNames(path).iteritems():
		
		result[sampleName] = readTreeFromFile(filePath, dileptonCombination)
		
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
	return chain



def getCounts(trees, cut,Samples,group,groupmembers):
	lumi = 9200
	from math import sqrt
	rmue = 1.206
	#~ trigger = {
		#~ "EE":93.0,
		#~ "EMu":92.5,
		#~ "MuMu":94.4
		#~ }
	#~ trigger = {
		#~ "EE":0.912,
		#~ "EMu":0.5*(0.918+0.883),
		#~ "MuMu": 0.936
		#~ }
	trigger = {
		"EE":0.970,
		"EMu":0.942,
		"MuMu": 0.964
		}
	#~ trigger = {
		#~ "EE":1.,
		#~ "EMu":1.,
		#~ "MuMu": 1.
		#~ }
	cut = cut.replace("inv", "p4.M()")
	#~ nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
	#~ snllPredictionScale = sqrt((0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(1.-1./(rmue)**2)*0.1*rmue)**2 + (0.05*0.5*(rmue+1./rmue))**2*((1/trigger["EE"])**2 + (1/2*trigger["MuMu"])**2 +(1/2*trigger["EMu"])**2))
	nllPredictionScale = 1.02
	snllPredictionScale = 0.07
	
	n = {
		"MuMu" : 0.,
		"EE"   : 0.,
		"EMu"  : 0.,
		"sMuMu" : 0.,
		"sEE"   : 0.,
		"sEMu"  : 0.,
		"MuMuJESDown" : 0.,
		"EEJESDown"   : 0.,
		"EMuJESDown"  : 0.,
		"MuMuJESUp" : 0.,
		"EEJESUp"   : 0.,
		"EMuJESUp"  : 0.,
		"xsecMuMu"	: 0.,
		"xsecEE"	: 0.,
		"xsecEMu"	: 0.
		}
		
	for index, sample in enumerate(groupmembers):
		#~ print sample
		#~ print n["sEE"]
		for name, tree in trees["EEtrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					#~ print name
					counts = readWeightedEntries(tree, "p4.M()", cut)		
					n["EE"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					n["xsecEE"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2]
					#~ n["sEE"] += sqrt(n["sEE"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					n["sEE"] = sqrt(n["sEE"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					
		for name, tree in trees["MuMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]
					n["xsecMuMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2] 
					n["sMuMu"] = sqrt(n["sMuMu"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					
		for name, tree in trees["EMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]
					n["xsecEMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2] 
					n["sEMu"] = sqrt(n["sEMu"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
		

	"""
	4% Z 15% TTbar 6% ST 4% Diboson 50% Rares
	"""
	"""
	4.5% JES, 4.5% Luminosity error, 10% r_emu
	"""
	
	#~ print n["EE"]
	#~ print n["MuMu"]
	#~ print n["EMu"]
	
	n["LumiEE"] = n["EE"]*0.045	
	n["LumiMuMu"] = n["MuMu"]*0.045	
	n["LumiEMu"] = n["EMu"]*0.045
	
	
	cut = cut.replace("met", "met*1.01")
	cut = cut.replace("ht", "ht*1.01")


	for index, sample in enumerate(groupmembers):
		
		for name, tree in trees["EEtrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EEJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["MuMutrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMuJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["EMutrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMuJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
	
	cut = cut.replace("met*1.01" , "met*0.99")
	cut = cut.replace("ht*1.01" , "ht*0.99")
	
	for index, sample in enumerate(groupmembers):
		
		for name, tree in trees["EEtrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EEJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["MuMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMuJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["EMutrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMuJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
	

	#~ n["systEE"] = sqrt((max(abs(n["EEJESDown"]-n["EE"]),abs(n["EEJESUp"]-n["EE"])))**2 + n["xsecEE"]**2 + n["LumiEE"]**2)
	#~ n["systMuMu"] = sqrt((max(abs(n["MuMuJESDown"]-n["MuMu"]),abs(n["MuMuJESUp"]-n["MuMu"])))**2 + n["xsecMuMu"]**2 + n["LumiMuMu"]**2)
	#~ n["systEMu"] = sqrt((max(abs(n["EMuJESDown"]-n["EMu"]),abs(n["EMuJESUp"]-n["EMu"])))**2 + n["xsecEMu"]**2 + n["LumiEMu"]**2)
	print n["EE"], n["xsecEE"]
	n["systEE"] = sqrt((max(abs(n["EEJESDown"]-n["EE"]),abs(n["EEJESUp"]-n["EE"])))**2 + n["xsecEE"]**2 + n["LumiEE"]**2)
	#~ n["systEE"] = 0.5*n["EE"]
	n["systMuMu"] = sqrt((max(abs(n["MuMuJESDown"]-n["MuMu"]),abs(n["MuMuJESUp"]-n["MuMu"])))**2 + n["xsecMuMu"]**2 + n["LumiMuMu"]**2)
	#~ n["systMuMu"] = 0.5*n["MuMu"]
	n["systEMu"] = sqrt((max(abs(n["EMuJESDown"]-n["EMu"]),abs(n["EMuJESUp"]-n["EMu"])))**2 + n["xsecEMu"]**2 + n["LumiEMu"]**2)
	#~ n["systEMu"] = 0.5*n["EMu"]
	
	n["nS"] = n["EE"]  + n["MuMu"] - n["EMu"]*nllPredictionScale
	n["nSF"] = n["EE"] + n["MuMu"]
	n["systSF"] = sqrt(n["systMuMu"]**2 + n["systEE"]**2)
	#~ n["systSF"] = 0.5*n["nSF"]
	
	n["nOF"] = n["EMu"]*nllPredictionScale
	n["systOF"] = math.sqrt((n["systEMu"]*nllPredictionScale*nllPredictionScale)**2 + (snllPredictionScale*n["EMu"]*nllPredictionScale)**2)
	#~ n["systOF"] = 0.5*n["nOF"]

	n["nS-debug"] = "nS=%s + %s - %s = %s"%(n["EE"] , n["MuMu"], n["EMu"]*nllPredictionScale,
	
											n["EE"]  + n["MuMu"] - n["EMu"]*nllPredictionScale)
	if n["EE"]	>0.:									
		n["rmueSR"] = sqrt(n["MuMu"]*1./n["EE"])
	else: 
		n["rmueSR"] = 0.
	n["rmueSR-reldiff"] =  n["rmueSR"]*100./rmue -100.
	n["statSF"] = sqrt(n["sMuMu"]**2 + n["sEE"]**2)
	n["totalsSF"] = sqrt(n["statSF"]**2 + n["systSF"]**2)
	n["totalsEE"] = sqrt(n["sEE"]**2 + n["systEE"]**2)
	n["totalsMuMu"] = sqrt(n["sMuMu"]**2 + n["systMuMu"]**2)
	n["totalsEMu"] = sqrt(n["sEMu"]**2 + n["systEMu"]**2)
	n["statOF"] = n["sEMu"]*nllPredictionScale
	n["totalsOF"] = sqrt(n["statOF"]**2 + n["systOF"]**2)
	
	#~ n["totalsS"] = 	sqrt(n["EE"]+n["MuMu"]+n["EMu"]*nllPredictionScale**2 + n["EMu"]*snllPredictionScale + max(abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESDown"]+n["MuMuJESDown"]-n["EMuJESDown"]*nllPredictionScale)),abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESUp"]+n["MuMuJESUp"]-n["EMuJESUp"]*nllPredictionScale))))
	n["statS"] = 	sqrt(n["sEE"]**2 + n["sMuMu"]**2 + (n["sEMu"]*nllPredictionScale)**2)
	n["systS"] = 	sqrt((n["EMu"]*snllPredictionScale)**2+ (max(abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESDown"]+n["MuMuJESDown"]-n["EMuJESDown"]*nllPredictionScale)),abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESUp"]+n["MuMuJESUp"]-n["EMuJESUp"]*nllPredictionScale))))**2 + (n["xsecEE"]+n["xsecMuMu"]-n["xsecEMu"])**2)
	#~ n["systS"] = sqrt(n["systSF"]**2+n["systOF"]**2)
	
	

	return n
def getCountsRare(trees, cut,Samples,group,groupmembers):
	lumi = 9200
	from math import sqrt
	rmue = 1.206
	#~ trigger = {
		#~ "EE":93.0,
		#~ "EMu":92.5,
		#~ "MuMu":94.4
		#~ }
	#~ trigger = {
		#~ "EE":0.912,
		#~ "EMu":0.5*(0.918+0.883),
		#~ "MuMu": 0.936
		#~ }
	trigger = {
		"EE":0.970,
		"EMu":0.942,
		"MuMu": 0.964
		}
	#~ trigger = {
		#~ "EE":1.,
		#~ "EMu":1.,
		#~ "MuMu": 1.
		#~ }
	cut = cut.replace("inv", "p4.M()")
	#~ nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
	#~ snllPredictionScale = sqrt((0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(1.-1./(rmue)**2)*0.1*rmue)**2 + (0.05*0.5*(rmue+1./rmue))**2*((1/trigger["EE"])**2 + (1/2*trigger["MuMu"])**2 +(1/2*trigger["EMu"])**2))
	nllPredictionScale = 1.02
	snllPredictionScale = 0.07
	
	n = {
		"MuMu" : 0.,
		"EE"   : 0.,
		"EMu"  : 0.,
		"sMuMu" : 0.,
		"sEE"   : 0.,
		"sEMu"  : 0.,
		"MuMuJESDown" : 0.,
		"EEJESDown"   : 0.,
		"EMuJESDown"  : 0.,
		"MuMuJESUp" : 0.,
		"EEJESUp"   : 0.,
		"EMuJESUp"  : 0.,
		"xsecMuMu"	: 0.,
		"xsecEE"	: 0.,
		"xsecEMu"	: 0.
		}
		
	for index, sample in enumerate(groupmembers):
		#~ print sample
		#~ print n["sEE"]
		for name, tree in trees["EEtrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					#~ print name
					counts = readWeightedEntries(tree, "p4.M()", cut)		
					n["EE"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					n["xsecEE"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2]
					#~ n["sEE"] += sqrt(n["sEE"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					n["sEE"] = sqrt(n["sEE"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					
		for name, tree in trees["MuMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]
					n["xsecMuMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2] 
					n["sMuMu"] = sqrt(n["sMuMu"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
					
		for name, tree in trees["EMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]
					n["xsecEMu"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0]*Samples[sample][2] 
					n["sEMu"] = sqrt(n["sEMu"]**2 + (counts["error"]*Samples[sample][1]*lumi/Samples[sample][0])**2)
		

	"""
	4% Z 15% TTbar 6% ST 4% Diboson 50% Rares
	"""
	"""
	4.5% JES, 4.5% Luminosity error, 10% r_emu
	"""
	
	#~ print n["EE"]
	#~ print n["MuMu"]
	#~ print n["EMu"]
	
	n["LumiEE"] = n["EE"]*0.045	
	n["LumiMuMu"] = n["MuMu"]*0.045	
	n["LumiEMu"] = n["EMu"]*0.045
	
	
	cut = cut.replace("met", "met*1.01")
	cut = cut.replace("ht", "ht*1.01")


	for index, sample in enumerate(groupmembers):
		
		for name, tree in trees["EEtrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EEJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["MuMutrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMuJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["EMutrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMuJESDown"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
	
	cut = cut.replace("met*1.01" , "met*0.99")
	cut = cut.replace("ht*1.01" , "ht*0.99")
	
	for index, sample in enumerate(groupmembers):
		
		for name, tree in trees["EEtrees"].iteritems():
			
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EEJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["MuMutrees"].iteritems():
			if name[0:sample.__len__()] == sample: 
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["MuMuJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
					
		for name, tree in trees["EMutrees"].iteritems():
			if name[0:sample.__len__()] == sample:
					counts = readWeightedEntries(tree, "p4.M()", cut)
					n["EMuJESUp"] += counts["events"]*Samples[sample][1]*lumi/Samples[sample][0] 
	

	#~ n["systEE"] = sqrt((max(abs(n["EEJESDown"]-n["EE"]),abs(n["EEJESUp"]-n["EE"])))**2 + n["xsecEE"]**2 + n["LumiEE"]**2)
	#~ n["systMuMu"] = sqrt((max(abs(n["MuMuJESDown"]-n["MuMu"]),abs(n["MuMuJESUp"]-n["MuMu"])))**2 + n["xsecMuMu"]**2 + n["LumiMuMu"]**2)
	#~ n["systEMu"] = sqrt((max(abs(n["EMuJESDown"]-n["EMu"]),abs(n["EMuJESUp"]-n["EMu"])))**2 + n["xsecEMu"]**2 + n["LumiEMu"]**2)
	print n["EE"], n["xsecEE"]
	n["systEE"] = sqrt((max(abs(n["EEJESDown"]-n["EE"]),abs(n["EEJESUp"]-n["EE"])))**2 + n["xsecEE"]**2 + n["LumiEE"]**2)
	#~ n["systEE"] = 0.5*n["EE"]
	n["systMuMu"] = sqrt((max(abs(n["MuMuJESDown"]-n["MuMu"]),abs(n["MuMuJESUp"]-n["MuMu"])))**2 + n["xsecMuMu"]**2 + n["LumiMuMu"]**2)
	#~ n["systMuMu"] = 0.5*n["MuMu"]
	n["systEMu"] = sqrt((max(abs(n["EMuJESDown"]-n["EMu"]),abs(n["EMuJESUp"]-n["EMu"])))**2 + n["xsecEMu"]**2 + n["LumiEMu"]**2)
	#~ n["systEMu"] = 0.5*n["EMu"]
	
	n["nS"] = n["EE"]  + n["MuMu"] - n["EMu"]*nllPredictionScale
	n["nSF"] = n["EE"] + n["MuMu"]
	#~ n["systSF"] = sqrt(n["systMuMu"]**2 + n["systEE"]**2)
	n["systSF"] = 0.5*n["nSF"]
	
	n["nOF"] = n["EMu"]*nllPredictionScale
	#~ n["systOF"] = math.sqrt((n["systEMu"]*nllPredictionScale*nllPredictionScale)**2 + (snllPredictionScale*n["EMu"]*nllPredictionScale)**2)
	n["systOF"] = 0.5*n["nOF"]

	n["nS-debug"] = "nS=%s + %s - %s = %s"%(n["EE"] , n["MuMu"], n["EMu"]*nllPredictionScale,
	
											n["EE"]  + n["MuMu"] - n["EMu"]*nllPredictionScale)
	if n["EE"]	>0.:									
		n["rmueSR"] = sqrt(n["MuMu"]*1./n["EE"])
	else: 
		n["rmueSR"] = 0.
	n["rmueSR-reldiff"] =  n["rmueSR"]*100./rmue -100.
	n["statSF"] = sqrt(n["sMuMu"]**2 + n["sEE"]**2)
	n["totalsSF"] = sqrt(n["statSF"]**2 + n["systSF"]**2)
	n["totalsEE"] = sqrt(n["sEE"]**2 + n["systEE"]**2)
	n["totalsMuMu"] = sqrt(n["sMuMu"]**2 + n["systMuMu"]**2)
	n["totalsEMu"] = sqrt(n["sEMu"]**2 + n["systEMu"]**2)
	n["statOF"] = n["sEMu"]*nllPredictionScale
	n["totalsOF"] = sqrt(n["statOF"]**2 + n["systOF"]**2)
	
	#~ n["totalsS"] = 	sqrt(n["EE"]+n["MuMu"]+n["EMu"]*nllPredictionScale**2 + n["EMu"]*snllPredictionScale + max(abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESDown"]+n["MuMuJESDown"]-n["EMuJESDown"]*nllPredictionScale)),abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESUp"]+n["MuMuJESUp"]-n["EMuJESUp"]*nllPredictionScale))))
	n["statS"] = 	sqrt(n["sEE"]**2 + n["sMuMu"]**2 + (n["sEMu"]*nllPredictionScale)**2)
	#~ n["systS"] = 	sqrt((n["EMu"]*snllPredictionScale)**2+ (max(abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESDown"]+n["MuMuJESDown"]-n["EMuJESDown"]*nllPredictionScale)),abs((n["EE"]+n["MuMu"]-n["nOF"])-(n["EEJESUp"]+n["MuMuJESUp"]-n["EMuJESUp"]*nllPredictionScale))))**2 + (n["xsecEE"]+n["xsecMuMu"]-n["xsecEMu"])**2)
	n["systS"] = sqrt(n["systSF"]**2+n["systOF"]**2)
	
	

	return n

def getTable( trees, cuts, Samples,groups,order,titles = None, cutOrder = None):
	if cutOrder is None:
		cutOrder = cuts.keys()

	if titles is None:
		titles = {}
			
	for name in cutOrder:
		if not name in titles:
			titles[name] = name

	result = ""
	for name in cutOrder:
		n = {}
		#~ lineTemplate = r"%(title)50s & $%(EE)4i\pm%(sEE)4i^{+%(JESEEdown)4i}_{%(JESEEup)4i}$ &$ %(MuMu)4i\pm%(sMuMu)4i^{+%(JESMuMudown)4i}_{%(JESMuMuup)4i}$ &$ %(EMu)4i\pm%(sEMu)4i^{+%(JESEMudown)4i}_{%(JESEMuup)4i}$ &$ %(nSF)4i\pm%(sSF)4i^{+%(snSFup)4i}_{%(snSFdown)4i}$ &$ %(nOF)4i\pm%(sOF)4i^{+%(snOFup)4i}_{%(snOFdown)4i} $& $%(rmueSR)5.2f$ ($%(rmueSR-reldiff)3.2f$) & $%(nS)3.1f$ \\"+"\n"
		lineTemplate = r"%(title)50s & $%(EE).1f\pm%(totalsEE).1f$ &$ %(MuMu).1f\pm%(totalsMuMu).1f$ &$ %(EMu).1f\pm%(totalsEMu).1f$ &$ %(nSF).1f\pm%(statSF).1f\pm%(systSF).1f$ &$ %(nOF).1f\pm%(statOF).1f\pm%(systOF).1f$& $%(nS)3.2f\pm%(statS).2f\pm%(systS).2f$ \\"+"\n"
		
		for group in order:
			repMap = { "title": group[1]}
			nTemp = getCounts(trees,cuts,Samples,group[0],groups[group[0]])
			repMap.update( nTemp )
			result += lineTemplate%repMap
		
		
	return tableTemplate%result
def getTableRare( trees, cuts, Samples,groups,order,titles = None, cutOrder = None):
	if cutOrder is None:
		cutOrder = cuts.keys()

	if titles is None:
		titles = {}
			
	for name in cutOrder:
		if not name in titles:
			titles[name] = name

	result = ""
	for name in cutOrder:
		n = {}
		#~ lineTemplate = r"%(title)50s & $%(EE)4i\pm%(sEE)4i^{+%(JESEEdown)4i}_{%(JESEEup)4i}$ &$ %(MuMu)4i\pm%(sMuMu)4i^{+%(JESMuMudown)4i}_{%(JESMuMuup)4i}$ &$ %(EMu)4i\pm%(sEMu)4i^{+%(JESEMudown)4i}_{%(JESEMuup)4i}$ &$ %(nSF)4i\pm%(sSF)4i^{+%(snSFup)4i}_{%(snSFdown)4i}$ &$ %(nOF)4i\pm%(sOF)4i^{+%(snOFup)4i}_{%(snOFdown)4i} $& $%(rmueSR)5.2f$ ($%(rmueSR-reldiff)3.2f$) & $%(nS)3.1f$ \\"+"\n"
		lineTemplate = r"%(title)50s & $%(EE).1f\pm%(totalsEE).1f$ &$ %(MuMu).1f\pm%(totalsMuMu).1f$ &$ %(EMu).1f\pm%(totalsEMu).1f$ &$ %(nSF).1f\pm%(statSF).1f\pm%(systSF).1f$ &$ %(nOF).1f\pm%(statOF).1f\pm%(systOF).1f$& $%(nS)3.2f\pm%(statS).2f\pm%(systS).2f$ \\"+"\n"
		
		for group in order:
			repMap = { "title": group[1]}
			nTemp = getCountsRare(trees,cuts,Samples,group[0],groups[group[0]])
			repMap.update( nTemp )
			result += lineTemplate%repMap
		
		
	return tableTemplate%result

def main():
	from sys import argv
	path = "/user/schomakers/trees"
	EMutrees = readTrees(path, "EMu")
	EEtrees = readTrees(path, "EE")
	MuMutrees = readTrees(path, "MuMu")
	trees = {
		"EMutrees" : EMutrees,
		"EEtrees"   : EEtrees,
		"MuMutrees": MuMutrees
		}
	
	import ROOT
	from ROOT import TFile

	eventCounts = totalNumberOfGeneratedEvents(path)
	Samples = { 
		"ZJets"         : [eventCounts["ZJets_madgraph_Summer12"],3503.71,0.04],
		"TT_Powheg_Summer12_v2"        : [eventCounts["TT_Powheg_Summer12_v2"], 225.2,0.15], 
		"ZZJetsTo2L2Q"  : [eventCounts["ZZJetsTo2L2Q_madgraph_Summer12"],2.46,0.5], 
		"ZZJetsTo2L2Nu" : [eventCounts["ZZJetsTo2L2Nu_madgraph_Summer12"],0.365,0.5], 
		"ZZJetsTo4L"    : [eventCounts["ZZJetsTo4L_madgraph_Summer12"],0.177,0.5],
		"WZJetsTo3LNu"  : [eventCounts["WZJetsTo3LNu_madgraph_Summer12"],1.06,0.5],
		"WZJetsTo2L2Q"  : [eventCounts["WZJetsTo2L2Q_madgraph_Summer12"],2.32,0.5],
		"WWJetsTo2L2Nu" : [eventCounts["WWJetsTo2L2Nu_madgraph_Summer12"],4.7,0.04],
		"AStar"			: [eventCounts["AStar_madgraph_Summer12"],877,0.04],
		"TTZJets"		: [eventCounts["TTZJets_madgraph_Summer12"],0.208,0.5],
		"TTWWJets"		: [eventCounts["TTWWJets_madgraph_Summer12"],0.002037,0.5],
		"TTWJets"		: [eventCounts["TTWJets_madgraph_Summer12"],0.2149,0.5],
		"WZZNoGstar"	: [eventCounts["WZZNoGstar_madgraph_Summer12"],0.01922,0.5],
		"TTGJets"		: [eventCounts["TTGJets_madgraph_Summer12"],1.444,0.5],
		"WWZNoGstarJets": [eventCounts["WWZNoGstarJets_madgraph_Summer12"],0.0633,0.5],
		"WWGJets"		: [eventCounts["WWGJets_madgraph_Summer12"],0.528,0.5],
		"WWWJets"		: [eventCounts["WWWJets_madgraph_Summer12"],0.08217,0.5],
		"TBar_tWChannel": [eventCounts["TBar_tWChannel_Powheg_Summer12"],11.1,0.06],
		"TBar_tChannel" : [eventCounts["TBar_tChannel_Powheg_Summer12"],30.7,0.06],
		"TBar_sChannel" : [eventCounts["TBar_sChannel_Powheg_Summer12"],1.76,0.06],
		"T_tWChannel"   : [eventCounts["T_tWChannel_Powheg_Summer12"],11.1,0.06],
		"T_tChannel"    : [eventCounts["T_tChannel_Powheg_Summer12"],56.4,0.06],
		"T_sChannel"    : [eventCounts["T_sChannel_Powheg_Summer12"],3.79,0.06]
		}

		
		
	order = [["TT_Powheg_Summer12_v2","\ttbar"],["DY","Drell-Yan"],["Diboson","Diboson"],["SingleTop","Single top"],["Rare","Other SM"],["All","All Backgrounds"]]
	groups ={
		"All":["AStar","ZJets","TT_Powheg_Summer12_v2","ZZJetsTo2L2Q","ZZJetsTo2L2Nu","ZZJetsTo4L","WZJetsTo3LNu","WZJetsTo2L2Q","WWJetsTo2L2Nu","TBar_tWChannel","TBar_tChannel","TBar_sChannel","T_tWChannel","T_tChannel","T_sChannel","WWWJets","WWGJets","WWZNoGstarJets","TTGJets","WZZNoGstar","TTWJets","TTZJets","TTWWJets"],
		"Rare":["WWWJets","WWGJets","WWZNoGstarJets","TTGJets","WZZNoGstar","TTWJets","TTZJets","TTWWJets"],		
		#~ "Rare":["TTWJets","TTZJets"],		
		"SingleTop":["TBar_tWChannel","TBar_tChannel","TBar_sChannel","T_tWChannel","T_tChannel","T_sChannel"],
		"Diboson":["ZZJetsTo2L2Q","ZZJetsTo2L2Nu","ZZJetsTo4L","WZJetsTo3LNu","WZJetsTo2L2Q","WWJetsTo2L2Nu"],		
		"DY":["AStar","ZJets"],
		"TT_Powheg_Summer12_v2":["TT_Powheg_Summer12_v2"]
		
	}

	
	#	cut= "  chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && nJets >= 2 && ht > 100 & met > 150"
	#~ base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && p4.M()>15 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 2 && ht > 100 && met > 150 && abs(motherPdgId)==15 ) "
	#~ base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>15 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 2 && ht > 100 && met > 150 && abs(matched==7)) "
	#~ base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 2 && ht > 100 && met > 150 ) "
	#~ base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 2 && ht > 100 && met > 150 ) "
	base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && ((nJets >= 2 && met > 150) ||(nJets >= 3 && met > 100)) ) "
	baseCentral = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && ((nJets >= 2 && met > 150) ||(nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 ) "
	baseForward = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && ((nJets >= 2 && met > 150) ||(nJets >= 3 && met > 100)) && 1.4 < TMath::Max(abs(eta1),abs(eta2)) ) "
	#~ baseBarrel = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<1.4 && abs(eta2)<1.4 && deltaR > 0.3 && nJets >= 2 && ht > 100 && met > 150  ) "
	#~ base = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 3  && met > 100 ) "
	baseLowMET = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<1.4 && abs(eta2)<1.4 && deltaR > 0.3 && nJets >= 3  && met > 100 ) "
	baseLowMETFullEta = "weight*(chargeProduct < 0 && ((pt1 > 20 && pt2 > 20 ) || (pt2 > 20 && pt1 > 20 )) && p4.M()>20 && p4.M()< 70 && abs(eta1)<2.4 && abs(eta2)<2.4 && deltaR > 0.3 && nJets >= 3  && met > 100 ) "
	edgeMass = "(inv < 70)"
	highMass = "(inv > 110)"
	jzbMass = "(70 < inv && inv < 110)"
	tightEta = "(abs(eta1) <1.4 && abs(eta2) < 1.4)"
	inclusiveSR = "nJets >= 2 && ht > 100 && met > 150"
	jzb = "nJets >= 3 && jzb > 100"
	pt2020 = "pt1 > 20 && pt2 > 20"
	inverseNJets = "met > 100 && nJets <= 2"
	central = "abs(eta1) < 1.4 && abs(eta2) < 1.4"
	forward = "1.4 < TMath::Max(abs(eta1),abs(eta2))"
	

	sigReg = inclusiveSR
	#inclusiveSR
	cuts= {
		"SignalNonRectCentral": [base, central],
		"SignalNonRectForward": [base, forward],
		"inclusiveMass": [base, sigReg],
		"edgeMass":        [base, sigReg, edgeMass ],
		"jzbMass": [base, sigReg, jzbMass],
		"highMass": [base, sigReg, highMass]
		}
	
	titles = {
		"SignalNonRectCentral": "Central Signal Region",
		"SignalNonRectForward": "Forward Signal Region",
		"inclusiveMass": "--",
		"edgeMass":        "$\mll <70~\GeV$",
		"jzbMass": "$70 < \mll <110~\GeV$",
		"highMass": "$110~\GeV < \mll$"
		}

	for name in cuts.keys():
		cuts[name+"Eta"]  = [tightEta] + cuts[name]
		titles[name+"Eta"] = "$|\eta| < 1.4 \wedge$ %s"%titles[name]
		titles[name+"Eta"] = titles[name+"Eta"].replace(r"\wedge$ --","$")

	for name in cuts.keys():
		cuts[name+"2020"]  = [pt2020] + cuts[name]
		titles[name+"2020"] = "$p_T > 20 GeV \wedge$ %s"%titles[name]
		titles[name+"2020"] = titles[name+"2020"].replace(r"\wedge$ --","$")


	cutAndCount = getTable(trees, baseCentral,Samples,groups,order, titles = titles, cutOrder = ["SignalNonRectCentral"])

	print cutAndCount
	outFile = open("tab/table_cutAndCountCrosscheckSignalNonRectCentral.tex","w")
	outFile.write(cutAndCount)
	outFile.close()

	cutAndCount = getTable(trees, baseForward,Samples,groups,order, titles = titles, cutOrder = ["SignalNonRectForward"])

	print cutAndCount
	outFile = open("tab/table_cutAndCountCrosscheckSignalNonRectForward.tex","w")
	outFile.write(cutAndCount)
	outFile.close()

	order = [["Diboson","WZ,ZZ"],["Rare","ttZ"],["TTWJets","TTWJets"],["All","All Backgrounds"]]
	groups ={
		"All":["ZZJetsTo2L2Q","ZZJetsTo2L2Nu","ZZJetsTo4L","WZJetsTo3LNu","TTZJets"],
		"Rare":["TTZJets"],
		"TTWJets":["TTWJets"],		
		#~ "SingleTop":["TBar_tWChannel","TBar_tChannel","TBar_sChannel","T_tWChannel","T_tChannel","T_sChannel"],
		"Diboson":["ZZJetsTo2L2Q","ZZJetsTo2L2Nu","ZZJetsTo4L","WZJetsTo3LNu"],		
		#~ "DY":["AStar","ZJets"],
		#~ "TT_Powheg_Summer12_v2":["TT_Powheg_Summer12_v2"]
		#~ 
	}

	
	cutAndCount = getTable(trees, baseCentral,Samples,groups,order, titles = titles, cutOrder = ["SignalNonRectCentral"])

	print cutAndCount
	outFile = open("tab/table_cutAndCountCrosscheck_Rares_SignalNonRectCentral.tex","w")
	outFile.write(cutAndCount)
	outFile.close()
	
	cutAndCount = getTable(trees, baseForward,Samples,groups,order, titles = titles, cutOrder = ["SignalNonRectForward"])

	print cutAndCount
	outFile = open("tab/table_cutAndCountCrosscheck_Rares_SignalNonRectForward.tex","w")
	outFile.write(cutAndCount)
	outFile.close()
	
	#~ cutAndCount = getTableRare(trees, baseBarrel,Samples,groups,order, titles = titles, cutOrder = ["edgeMass"])
#~ 
	#~ print cutAndCount
	#~ outFile = open("cutAndCountCrosscheck_RaresBarrel.tex","w")
	#~ outFile.write(cutAndCount)
	#~ outFile.close()
	#~ cutAndCount = getTableRare(trees, baseLowMETFullEta,Samples,groups,order, titles = titles, cutOrder = ["edgeMass"])
#~ 
	#~ print cutAndCount
	#~ outFile = open("cutAndCountCrosscheck_RaresLowMETFullEta.tex","w")
	#~ outFile.write(cutAndCount)
	#~ outFile.close()	
	

main()
