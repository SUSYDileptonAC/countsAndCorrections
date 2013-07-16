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
	from src.defs import Regions
	from src.datasets import readTreeFromFile
	import pickle
	trees = {
		"MuMu": readTreeFromFile(argv[1], "MuMu", "",SingleLepton=False),
		"EMu": readTreeFromFile(argv[1], "EMu", "",SingleLepton=False),
		"EE": readTreeFromFile(argv[1], "EE", "",SingleLepton=False),
		}	
	print "hier"	
	eventLists = getEventLists(trees, "")
	name = "sync"
	outFile = open("shelves/eventLists_%s.pkl"%name,"w")
	pickle.dump(eventLists, outFile)
	outFile.close()	
	saveEventList(eventLists["EMu"],"EMu")
	saveEventList(eventLists["MuMu"],"MuMu")
	
	if argv[2] != "":
		printEvent(argv[2],trees)
main()