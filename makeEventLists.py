#!/usr/bin/env python
def saveEventList(eventContainer, name):
	lineTemplate = r"%s:%s:%s"+"\n"
	eventList = ""
	for event in eventContainer:
		
		eventList += lineTemplate%(event[2],event[1],event[0])
			
	listFile = open("eventLists/%s"%name, "w")
	listFile.write(eventList)
	listFile.close()

def main():
	from sys import argv
	from src.datasets import loadPickles
	allPkls = loadPickles("shelves/eventLists_*.pkl")
	for regionName in allPkls:		
		for subcut, nSub in allPkls[regionName].iteritems():
			for massRegion, eventLists in nSub.iteritems():
				name = "eventList_%s_%s_%s_%s.txt"%(regionName,subcut,massRegion,"MuMu")
				saveEventList(eventLists["MuMu"],name)
				name = "eventList_%s_%s_%s_%s.txt"%(regionName,subcut,massRegion,"EE")
				saveEventList(eventLists["EE"],name)
				name = "eventList_%s_%s_%s_%s.txt"%(regionName,subcut,massRegion,"EMu")
				saveEventList(eventLists["EMu"],name)

main()
