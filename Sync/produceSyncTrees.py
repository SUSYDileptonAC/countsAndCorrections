def getEventLists(trees, cut, colNames = ["eventNr","lumiSec","runNr"]):
	result = {
		"columns": colNames,
		"cut": cut
		}
	for comb in trees:
		print comb
		if comb != "EE":
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

	return result

def saveEventList(eventContainer, name):
	lineTemplate = r"%s:%s:%s"+"\n"
	eventList = ""
	for event in eventContainer:
		
		eventList += lineTemplate%(event[2],event[1],event[0])
			
	listFile = open("eventLists/%s"%name, "w")
	listFile.write(eventList)
	listFile.close()
	
def printEvent(event,trees):
	for comb in trees:
		print comb
		if comb != "EE":
			subtree = trees[comb]
			subtree.Scan("runNr:lumiSec:eventNr")
		#~ print comb
			for ev in subtree:
				
				#~ print "%d:%d:%d"%(ev.runNr,ev.lumiSec,ev.eventNr)
				eventId = "%s:%s:%s"%(getattr(ev, "runNr"),getattr(ev, "lumiSec"),getattr(ev, "eventNr"))
				if event == eventId:
					print ev.pt1	
				
			del subtree	

def main():
	from sys import argv
	import ROOT
	from src.defs import Regions
	from src.datasets import readTreeFromFile538
	import pickle
	#~ cutString = "chargeProduct == -1 && (pt1 > 20 && pt2 > 20 || pt1 > 20 && pt2 > 20) && abs(eta1) < 2.4 && abs(eta2) < 2.4 && !(abs(eta1) > 1.4 && abs(eta1) < 1.6) && !(abs(eta2) > 1.4 && abs(eta2) < 1.6) && p4.M() > 20 && p4.M() < 300 && deltaR > 0.3 && nJets >= 2 && met < 50 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	#~ cutString = "(runNr == 195113 && lumiSec == 449 && eventNr == 537957865)"
	cutString = "nJets >= 2"
	#~ cutString = "(runNr == 199318 && lumiSec == 73 && eventNr == 45731711)"
	#~ cutString = "runNr == 201097  || runNr == 195399"
	
	trees = {
		"MuMu": readTreeFromFile538(argv[1], "MuMu", cutString,SingleLepton=False),
		"EMu": readTreeFromFile538(argv[1], "EMu", cutString,SingleLepton=False),
		"EE": readTreeFromFile538(argv[1], "EE", cutString,SingleLepton=False),
		}	

	
	#~ subTrees = {}
	#~ subTrees["MuMu"] = trees["MuMu"].copyTree(cutString)
	#~ subTrees["EE"] = trees["EE"].copyTree(cutString)
	#~ subTrees["EMu"] = trees["EMu"].copyTree(cutString)
	
	outFile = ROOT.TFile("sw538v0476.processed.MergedData_2Jets.root","RECREATE")
	
	outFile.mkdir("cutsV23DileptonFinalTrees")
	outFile.cd("cutsV23DileptonFinalTrees")
	
	trees["MuMu"].Write()
	trees["EE"].Write()
	trees["EMu"].Write()
	
	outFile.Write()
	outFile.Close()
		
	#~ eventLists = getEventLists(trees, "")
	#~ name = "sync"
	#~ outFile = open("shelves/eventLists_%s.pkl"%name,"w")
	#~ pickle.dump(eventLists, outFile)
	outFile.close()	
	#~ saveEventList(eventLists["EMu"],"EMu")
	#~ saveEventList(eventLists["MuMu"],"MuMu")
	#~ saveEventList(eventLists["EE"],"EE")
	
	#~ if argv[2] != "":
		#~ printEvent(argv[2],trees)
main()
