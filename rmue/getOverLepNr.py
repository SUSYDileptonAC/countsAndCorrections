import ROOT
from treeTools import getTreeFromProcess
from defs import Cuts
from messageLogger import messageLogger as log
import processes

def getOverLepNr(process, treeType):
	#print "Process : %s \nTreeType : %s"%(process, subProcess, treeType)
	# Achtung : Vorher muss ...dataPath = "../../Daten/"<<< o.ae. ausgefuehrt werden
	tree = getTreeFromProcess(process, treeType)
	print type(tree)
	
	elementsList = []
	overLepList = []
	nTotal = tree.GetEntries()
	overLep = 0
	for i in range(0, nTotal):
		tree.GetEntry(i)
		runNr = tree.runNr
		lumiSec = tree.lumiSec
		eventNr = tree.eventNr
		log.statusBar(i,nTotal,message = "Overlep-Durchlauf")
		if (runNr,lumiSec,eventNr) in elementsList:
			overLep +=1
			overLepList.append((runNr,lumiSec,eventNr))
		elif (runNr,lumiSec,eventNr) not in elementsList:
			elementsList.append((runNr,lumiSec,eventNr))
		else:
			log.logInfo("Something wrong with elementsList or the entries") 
	#print "overLepListe fuer %s : %s" % (treeType,overLepList)
	return overLep

