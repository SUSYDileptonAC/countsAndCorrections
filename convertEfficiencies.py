#!/usr/bin/env python
def convertPickle(path, correction = "data", boundName = None, objectDefinition = "pfCombRelIso04EACorr<012_Tight", etaBins = {"ptabseta<1.2":(0,1.2), "ptabseta>1.2":(1.2, 2.5)}):
	import pickle
	result = {}
	effFile = open(path, "r")
	effDict = pickle.load(effFile)[objectDefinition]
	effFile.close()
	for etaName, (etaMin, etaMax) in etaBins.iteritems():
		result[(etaMin, etaMax)] = {}
		result[(-1.*etaMax, -1.*etaMin)] = {}		
		for ptName, ptDict in effDict[etaName].iteritems():
			ptMin, ptMax = [float(i) for i in ptName.split("_")]
			weight = effDict[etaName][ptName][correction]["efficiency"]
			if boundName == "Upper":
				weight += effDict[etaName][ptName][correction]["err_hi"]
			if boundName == "Lower":
				weight -= effDict[etaName][ptName][correction]["err_low"]
			result[(etaMin, etaMax)][(ptMin, ptMax)] = weight
			result[(-1.*etaMax, -1.*etaMin)][(ptMin, ptMax)] = weight
			
	return result

def convertTxt(path, boundName = "Center"):
	result = {}
	effFile = open(path, "r")
	rawTxt = effFile.read()
	effFile.close()
	for line in rawTxt.splitlines()[7:]:
		ptMin, ptMax, etaMin, etaMax, weight, weightUp, weightDown = [float(i) for i in line.split()]
		if not (etaMin, etaMax) in result:
			result[(etaMin, etaMax)] = {}
			result[(-1.*etaMax, -1.*etaMin)] = {}
		if boundName == "Upper":
			weight += weightUp
		if boundName == "Lower":
			weight -= weightDown
		result[(etaMin, etaMax)][(ptMin, ptMax)] = weight
		result[(-1.*etaMax, -1.*etaMin)][(ptMin, ptMax)] = weight
	return result

def createEfficiencyCfg(efficiencies, name ,outPath):
	result = 'if not "cms" in globals(): import FWCore.ParameterSet.Config as cms\n\n'
	for boundName, bins in efficiencies.iteritems():
		result += "%(name)s%(boundName)sEfficiencies = cms.VPSet(\n"%locals()
		for (etaMin, etaMax), ptBins in bins.iteritems():
			for (ptMin, ptMax), weight in ptBins.iteritems():
				result += """    cms.PSet(
        weight = cms.double(%(weight)f),
        etaMin = cms.double(%(etaMin)f),
        etaMax = cms.double(%(etaMax)f),
        ptMin = cms.double(%(ptMin)f),
        ptMax = cms.double(%(ptMax)f),
	),
"""%locals()
		result +=  "    )\n"
	outFile = open(outPath, "w")
	outFile.write(result)
	outFile.close()
	return result
				
	


def main():
	from sys import argv

	mode = argv[1]
	path = argv[2]

	effData = None
	effSim = None
	flavour = None
	if mode == "muonPkl":
		flavour = "muon"
		effData ={
			"Center": convertPickle(path, correction = "data"),
			"Upper":  convertPickle(path, correction = "data", boundName = "Upper"),
			"Lower":convertPickle(path, correction = "data", boundName = "Lower"),
				   }
		effSim ={
			"Center": convertPickle(path, correction = "mc"),
			"Upper":  convertPickle(path, correction = "mc", boundName = "Upper"),
			"Lower":convertPickle(path, correction = "mc", boundName = "Lower"),
				   }
	elif mode == "electronTxt":
		flavour = "electron"
		eff ={
			"Center": convertTxt(path, boundName="Center"),
			"Upper":  convertTxt(path, boundName="Upper"),
			"Lower":convertTxt(path, boundName="Lower"),
				   }
		if path.endswith("Data.txt"):
			effData = eff
		elif path.endswith("MC.txt"):
			effSim = eff
	else:
		print "unknown mode '%s'. aborting."%mode
		return

	if effData is not None:
		print createEfficiencyCfg(effData, flavour,  "cfg/%sDataRecoEfficiencies_cff.py"%flavour)
	if effSim is not None:
		print createEfficiencyCfg(effSim, flavour, "cfg/%sSimRecoEfficiencies_cff.py"%flavour)


main()
