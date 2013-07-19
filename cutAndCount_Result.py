#!/usr/bin/env python
import gc
def getEventLists(trees, cut, colNames = ["eventNr","lumiSec","runNr"]):
	result = {
		"columns": colNames,
		"cut": cut
		}
	for comb in trees:
		print cut
		subtree = trees[comb].CopyTree(cut)
		result[comb] = set()
		#~ print comb
		for ev in subtree:
			
			#~ print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
			cols = []
			for varName in colNames:
				cols.append( getattr(ev, varName) )
			result[comb].add(tuple(cols))
		del subtree
		gc.collect()
	return result

def getCounts(trees, cut):
	
	n= {
		"MuMu": trees["MuMu"].GetEntries(cut),
		"EE": trees["EE"].GetEntries(cut),
		"EMu": trees["EMu"].GetEntries(cut),
		}
	#~ print cut, n
	n["cut"] = cut
	return n


def getTable( trees, cuts, titles = None, cutOrder = None):
	if cutOrder is None:
		cutOrder = cuts.keys()

	if titles is None:
		titles = {}
			
	for name in cutOrder:
		if not name in titles:
			titles[name] = name

	result = ""
	for name in cutOrder:
		lineTemplate = r"%(title)50s & %(EE)4i & %(MuMu)4i & %(EMu)4i & $%(nS)3.1f \pm %(nSUncert)3.1f$ \\"+"\n"
		oldLineTemplate = r"%(title)50s & %(EE)4i & %(MuMu)4i & %(EMu)4i & $%(rmueSR)5.2f$ ($%(rmueSR-reldiff)3.2f$) & $%(nS)3.1f$ \\"+"\n"
		repMap = { "title": titles[name]}
		#print "%20s"%name, "(%s)"%(") && (".join(cuts[name]))
#		print cuts[name]
		repMap.update( getCounts(trees, "(%s)"%(") && (".join(cuts[name]))) )
		result += lineTemplate%repMap
	return tableTemplate%result

def cutAndCountForRegion(trees, cut, name):
	from src.defs import Regions
	cut = getattr(Regions, name).cut
	
	import pickle
	base = "1"#chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && abs(eta1) < 2.4  && abs(eta2) < 2.4 && deltaR > 0.3 &&  p4.M() > 30 && p4.M() < 80"
	edgeMass = "(20 < inv && inv < 70)"
	onShellMass = "(81 < inv && inv < 101)"
	highMass = "(inv > 110)"
	pt2010 = "((pt1 > 20 && pt2 > 10)||(pt2 > 20 && pt1 > 10))"
	pt2020 = "pt1 > 20 && pt2 > 20"
	pt3020 = "((pt1 > 30 && pt2 > 20)||(pt1 > 20 && pt2 > 30))"
	pt3010 = "((pt1 > 30 && pt2 > 10)||(pt1 > 10 && pt2 > 30))"
	pt3030 = "pt1 > 30 && pt2 > 30"
	tightEta = "(abs(eta1) <1.4 && abs(eta2) < 1.4)"
	lowPU = "nVertices < 11"
	midPU = "11 <= nVertices && nVertices < 16"
	highPU = "16 <= nVertices"
	MET50Ge2Jets = " nJets >= 2 && ht > 100 && met > 50"
	MET100Ge2Jets = " nJets >= 2 && ht > 100 && met > 100"
	highPU = "16 <= nVertices"
	bTag0 = "nBJets == 0"
	bTag1 = "nBJets == 1"
	bTagGe2 = "nBJets >= 2"
	lowHT = "100 < ht && ht < 300"
	highHT = "ht > 300"
	tightIso = "id1 < 0.05 && id2 < 0.05"
	countMass = " inv > 20"
	catA = "pt1 > 20 && pt2 > 20 && abs(eta1) < 1.4 && abs(eta2) < 1.4"
	catB = "pt1 > 20 && pt2 > 20 && !(abs(eta1) < 1.4 && abs(eta2) < 1.4)"
	catC = "!(pt1 > 20 && pt2 > 20) && abs(eta1) < 1.4 && abs(eta2) < 1.4"
	catD = "!(pt1 > 20 && pt2 > 20) && !(abs(eta1) < 1.4 && abs(eta2) < 1.4)"
	runAB = "(runNr <= 196531)"
	runC = "(runNr > 196531)"
	barrel = "abs(eta1) < 1.4 && abs(eta2) < 1.4"
	endcap = "((abs(eta1) < 2.4 && abs(eta2) > 1.4) || (abs(eta1) > 1.4 && abs(eta2) < 2.4))"
	type1Met = "(nJets >= 2 && type1Met > 150) || (nJets >=3 && type1Met > 100)"
	tcMet = "(nJets >= 2 && tcMet > 150) || (nJets >=3 && tcMet > 100)"
	caloMet = "(nJets >= 2 && caloMet > 150) || (nJets >=3 && caloMet > 100)"
	MHT = "(nJets >= 2 && mht > 150) || (nJets >=3 && mht > 100)"


	mllcuts= {
		"default": [],
		"edgeMass": [edgeMass ],
		"onShellMass": [onShellMass],
		"highMass": [highMass],
		}
	subcuts= {
		"default":[base, cut],
		"Pt3010":[base, cut,pt3010],
		"Pt3020":[base, cut,pt3020],
		"Pt3030":[base, cut,pt3030],
		"LowPU": [base, cut, lowPU],
		"MidPU": [base, cut, midPU],
		"HighPU": [base, cut, highPU],
		"0BTag":[base, cut, bTag0],
		"1BTag":[base, cut, bTag1],
		"Ge2BTag":[base, cut, bTagGe2],
		#~ "Barrel":[base, cut, tightEta],
		"LowHT": [base, cut, lowHT],
		"HighHT": [base, cut, highHT],
		"TightIso":[base, cut, tightIso],
		"Pt2020":[base,cut, pt2020],
		"Pt2010":[base,cut, pt2010],
		"CountCuts":[base,cut, pt2020, countMass],
		"CatA":[base, cut, catA],
		"CatB":[base, cut, catB],
		"CatC":[base, cut, catC],
		"CatD":[base, cut ,catD],
		"RunAB":[base, cut, runAB],
		"RunC":[base, cut, runC],
		"MET50Ge2Jets":[base, cut, MET50Ge2Jets],
		"MET100Ge2Jets":[base, cut, MET100Ge2Jets],
		"Barrel":[base, cut, barrel],
		"Endcap":[base, cut, endcap],
		"Type1MET":[base, cut, type1Met],
		"TcMET":[base, cut, tcMet],
		"CaloMET":[base, cut, caloMet],
		"MHTMET":[base, cut, MHT],
		}
		
	if "SingleLepton" in name:
		subcuts= {
			"default":[base, cut],
			"Pt3010":[base, cut,pt3010],
			"Pt3020":[base, cut,pt3020],
			"Pt3030":[base, cut,pt3030],
			"LowPU": [base, cut, lowPU],
			"MidPU": [base, cut, midPU],
			"HighPU": [base, cut, highPU],
			"0BTag":[base, cut, bTag0],
			"1BTag":[base, cut, bTag1],
			"Ge2BTag":[base, cut, bTagGe2],
			#~ "Barrel":[gc.collect()base, cut, tightEta],
			"LowHT": [base, cut, lowHT],
			"HighHT": [base, cut, highHT],
			"TightIso":[base, cut, tightIso],
			"Pt2020":[base,cut, pt2020],
			"Pt2010":[base,cut, pt2010],
			"CountCuts":[base,cut, pt2020, countMass],
			"CatA":[base, cut, catA],
			"CatB":[base, cut, catB],
			"CatC":[base, cut, catC],
			"CatD":[base, cut ,catD],
			"RunAB":[base, cut, runAB],
			"RunC":[base, cut, runC],
			"MET50Ge2Jets":[base, cut, MET50Ge2Jets],
			"MET100Ge2Jets":[base, cut, MET100Ge2Jets],
			"Barrel":[base, cut, barrel],
			"Endcap":[base, cut, endcap],
			"Type1MET":[base, cut, type1Met],
			"TcMET":[base, cut, tcMet],
			"CaloMET":[base, cut, caloMet],
			"MHTMET":[base, cut, MHT],
			}
	counts = {name:{}}
	eventLists = {name:{}}
	for subcutName, subcut in subcuts.iteritems():
		

		
		counts[name][subcutName] = {}
		eventLists[name][subcutName] = {}		
		for mllcutName, mllcut in mllcuts.iteritems():
			fullcut = "(%s)"%(") && (".join(subcut+mllcut))
			fullcut = fullcut.replace("inv", "p4.M()")
			if subcutName == "Pt3010" or subcutName == "Pt2010":
				fullcut = fullcut.replace("&& pt1 > 20 && pt2 > 20"," ")
			if subcutName == "Pt2010":
				fullcut = fullcut.replace("p4.M() > 20","p4.M() > 15 ")			
				fullcut = fullcut.replace("20 < p4.M() ","p4.M() > 15 ")		
			if subcutName == "MET50Ge2Jets" or subcutName == "MET100Ge2Jets" or subcutName == "Type1MET" or subcutName == "CaloMET" or subcutName == "TcMET" or subcutName == "MHTMET":
				fullcut = fullcut.replace("((nJets >= 2 && met > 150) || (nJets >=3 && met > 100)) &&"," ")			
				#~ print subcutName
				#~ print fullcut	
			counts[name][subcutName][mllcutName] = getCounts(trees, fullcut)
			#~ eventLists[name][subcutName][mllcutName] = getEventLists(trees, fullcut)

	outFile = open("shelves/cutAndCount_%s.pkl"%name,"w")
	pickle.dump(counts, outFile)
	outFile.close()

	#~ outFile = open("shelves/eventLists_%s.pkl"%name,"w")
	#~ pickle.dump(eventLists, outFile)
	#~ outFile.close()



def main():
	from sys import argv
	from src.defs import Regions
	from src.datasets import readTreeFromFile
	
	cuts = {}
	for regionName in filter(lambda x: not x.endswith("_"), dir(Regions)):
		cuts[regionName] = getattr(Regions, regionName).cut

	for cut in cuts.keys():
		cuts["%s_METPD"%cut] = cuts[cut]
		cuts["%s_SingleLepton"%cut] = cuts[cut]

	preselection = "met > 50 && nJets >= 2 && deltaR > 0.3"
	if "SingleLepton" in argv[2]:
		trees = {
			"MuMu": readTreeFromFile(argv[1], "MuMu", preselection,SingleLepton=True),
			"EMu": readTreeFromFile(argv[1], "EMu", preselection,SingleLepton=True),
			"EE": readTreeFromFile(argv[1], "EE", preselection,SingleLepton=True),
			}		
		
	else:
		trees = {
			"MuMu": readTreeFromFile(argv[1], "MuMu", preselection),
			"EMu": readTreeFromFile(argv[1], "EMu", preselection),
			"EE": readTreeFromFile(argv[1], "EE", preselection),
			}
	datasetName = argv[1].split("/")[-1].split(".")[2]
	isMC = (not "MergedData" in datasetName)

	cutAndCountForRegion(trees, preselection, argv[2])
		

main()

