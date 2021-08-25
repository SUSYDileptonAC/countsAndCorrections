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
        result.Add("%s/genWeightSumFinalTrees/Tree"%(path))
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
        for filePath in glob("%s/*.root"%path):
                sampleName = match(".*.*\..*\.(.*).root", filePath).groups()[0]
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
                result[sampleName].SetDirectory(0)
                rootFile.Close()
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
        path = "/net/data_cms1b/user/teroerde/trees/genWeightSum2018/"
        path_masterList = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/SubmitScripts/Input/Master102X_2018_MC.ini"
        from sys import argv
        import pickle   

        
        cutsNeg = "genWeight < 0"
        cutsPos = "genWeight > 0"

        from ConfigParser import ConfigParser
        config = ConfigParser()
        config.read(path_masterList)
        
        #print "test"
        
        #for section in config.sections():
                #if config.has_option(section, "datasetpath"):
                        #dspath = config.get(section, "datasetpath")
                        #import subprocess as sp
                        #try:
                                #out = sp.check_output("dasgoclient --query 'parent dataset=%s'"%(dspath), shell=True)
                                #if not "PU2017" in out:
                                        #print dspath, "wrong PU"
                        #except:
                                #print dspath, "not valid"
                        #print out
                        #exit()
        
        
        trees = readTrees(path) 
        for name, tree in trees.iteritems():
                ROOT.gROOT.Reset()
                print name
                pos = tree.CopyTree(cutsPos).GetEntries()
                neg = tree.CopyTree(cutsNeg).GetEntries()
                print "events with pos. weight: %d"%pos
                print "events with neg. weight: %d"%neg
                frac = float(neg)/(neg + pos)
                print "fraction: %.3f"%(frac)
                config.set(name, 'negWeightFraction', "%.3f"%(frac))
                trees[name] = None
        
        with open("newConfig.ini", "w+") as configfile:
                config.write(configfile)
