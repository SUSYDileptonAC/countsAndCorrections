import sys
sys.path.append('cfg/')
from frameworkStructure import pathes
sys.path.append(pathes.basePath)

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)
#from setTDRStyle import setTDRStyle

from plotTemplate import plotTemplate, plotTemplate2D, getNewColor

from messageLogger import messageLogger as log

from helpers import *
from defs import Backgrounds, getPlot, getRegion, getRunRange

from locations import locations

path = "/net/data_cms1b/user/teroerde/trees/synch94X"
#sampleName = "Synch_2017"
sampleName = "Synch_2016"
#sampleName = "102XSynch"
basecuts = "(p4.Pt() > 25 && chargeProduct < 0 && ((pt1 > 25 && pt2 > 20) || (pt1 > 20 && pt2 > 25))   && p4.M() > 20 && deltaR > 0.1)" # && 

jetCuts = "nJets >= 2"
fatJetCuts = "nFatJets >= 1"
bJetCuts = "nBJets35 >= 1"
metCuts = "met > 150"
isoTrackCuts = "(nIsoTracksEl+nIsoTracksMu) <= 2 && nIsoTracksHad == 0"
mt2Cuts = "MT2 > 80"

#cuts = "{} && {}".format(basecuts, additionalCuts)
      
emTrees = readTrees(path, "EMu")  
nGenEvents = totalNumberOfGeneratedEvents(path)

#print "Original file /store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/00000/20221200-78F4-E711-8E0B-B499BAAC082E.root"

print "Yield generated events ", nGenEvents[sampleName]

emTree = emTrees[sampleName].CopyTree("")
print "Yield EMu channel ",emTree.GetEntries()

#emTree = emTree.CopyTree(basecuts)
#print "Yield baseline cuts ",emTree.GetEntries()

#emTree = emTree.CopyTree(jetCuts)
#print "Yield two jets ",emTree.GetEntries()

#emTree = emTree.CopyTree(bJetCuts)
#print "Yield one bjet ",emTree.GetEntries()

#emTree = emTree.CopyTree(metCuts)
#print "Yield met cut ",emTree.GetEntries()


#emTree = emTree.CopyTree(fatJetCuts)
#print "Yield fat jet cuts ",emTree.GetEntries()

#emTree = emTree.CopyTree(isoTrackCuts)
#print "Iso track veto ",emTree.GetEntries()

#emTree = emTree.CopyTree(mt2Cuts)
#print "Yield MT2 cut",emTree.GetEntries()

#print "Final EMu yield ",emTree.GetEntries()

emTree.SetScanField(0)

print "EMu events"
#print "run number; lumi section; event number; electron pt; muon pt; ptll; mll; nJets; jet1pt; jet2pt; ptmiss; electron SF; muon SF"
emTree.Scan("runNr:lumiSec: eventNr>0 ? eventNr : eventNr+4294967296 : pt1 : pt2 :eta1 :eta2 :nJets : met : jet1pt : jet2pt","","colsize=12")
#emTree.Scan("runNr:lumiSec: eventNr>0 ? eventNr : eventNr+4294967296 : uncorrectedMet : met","","colsize=12")
