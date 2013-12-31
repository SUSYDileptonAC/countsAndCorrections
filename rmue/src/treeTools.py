import ROOT
from messageLogger import messageLogger as log
from defs import Constants, Cuts, Test
from processes import TreePaths, Trees, SubProcesses7TeV
from array import array
from copy import deepcopy
#import numpy as n
import math


def getHistoFromTree(fileName, treePath, variable, cut , nBins=100, xMin=0, xMax=1000):
    """fuer verschiedenes Binning: 
    binning=range(0,100,10)+range(100,200,20)+[200,300]
    getHistoFromTree(fileName, treePath, variable, cut, binning, treeType)"""
    log.logDebug("Getting Histogram '%s'\n  from file %s" % (variable, fileName)) #bestimmt was angezeigt wird (verschiedene Stufen)
    name=variable.replace(",","")
    name=name.replace("::","")
    name=name.replace("(","")
    name=name.replace(")","")
    hTree=None
    if xMax==None:
        if not type(xMin)==type([]):
            log.logError("xMin ist %s und keine Liste" %xMin)
        if not nBins==len(xMin)-1:
            log.logError("Binning nicht gleich")
    
        hTree = ROOT.TH1F("%s" % name, "%s" % variable, nBins, array("f",xMin))
    else:
        hTree = ROOT.TH1F("%s" % name, "%s" % variable, nBins, xMin, xMax)

    hTree.Sumw2()      #Berechnet und speichert Fehlerquadrate
    Tree = getTreeFromFile(fileName, treePath)
    if Test.test==True:
        Tree.Draw("%s >> %s" % (variable, name), cut, "",10000,0)  #malt Variable und speichert sie ins Histo
    else:
        Tree.Draw("%s >> %s" % (variable, name), cut)
    hTree = ROOT.gDirectory.Get("%s" % name) #hol Histo
    
    if hTree != None:
        hTree.SetDirectory(0)  #hat funktioniert, SetDir damit Histo nicht verschwindet (Eltern weg)

    return hTree



#########################################################################################################################

def get2DHistoFromTree(fileName, treePath, cut, variablex, variabley, nxBins=100, xMin=0, xMax=100,nyBins=100,yMin=0,yMax=100):
    log.logDebug("Getting 2DHistogram from file %s" %fileName)
    #name=variable.replace("()","")
    hTree = ROOT.TH2F("hist", "hist", nxBins, xMin, xMax, nyBins, yMin, yMax)

    Tree=getTreeFromFile(fileName, treePath)

    Tree.Draw("%s:%s>> hist" % (variabley, variablex), cut)
    hTree = ROOT.gDirectory.Get("hist") 

    if hTree != None:
        hTree.SetDirectory(0)  

    return hTree


  
#########################################################################################################################

def getTreeFromFile(fileName, treePath):
    log.logDebug("Getting tree '%s'\n  from file %s" % (treePath, fileName))

    tree = ROOT.TChain(treePath)
    tree.Add(fileName)

    if (tree == None):
        log.logError("Could not get tree '%s'\n  from file %s" % (treePath, fileName))
        return None
    else:
        tree.SetDirectory(0)
        return tree



#########################################################################################################################

def getHistoFromProcess(process, variable, cut , treeType, nBins=100, xMin=0, xMax=1000,
                        trigger = False, triggerscaling=True, weights=True):
    log.logDebug("Getting Histogram '%s'\n  from process %s" % (variable, process)) #bestimmt was angezeigt wird (verschiedene Stufen)
    name=variable.replace(",","")
    name=name.replace("::","")
    name=name.replace("(","")
    name=name.replace(")","")

    
    log.logHighlighted("trigger: %s, triggerscaling: %s, weights: %s" %(trigger, triggerscaling, weights))

    hTree=None
    cutt=cut


    #Bool fuer Trigger

    if trigger == True:
        treePathDict = {str(Trees.ee): "%s/%s" % (TreePaths.triggerDiEle,TreePaths.treeDiEle),
                        str(Trees.mumu): "%s/%s" % (TreePaths.triggerDiMu,TreePaths.treeDiMu),
                        str(Trees.emu): "%s/%s" % (TreePaths.triggerMuEle,TreePaths.treeMuEle),
                        str(Trees.noneee): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeDiEle),
                        str(Trees.nonemumu): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeDiMu),
                        str(Trees.noneemu): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeMuEle)}
    elif trigger == False:
        treePathDict = {str(Trees.ee): "%s" % (TreePaths.treeDiEle),
                        str(Trees.mumu): "%s" % (TreePaths.treeDiMu),
                        str(Trees.emu): "%s" % (TreePaths.treeMuEle),
                        str(Trees.noneee): "%s" % (TreePaths.treeDiEle),
                        str(Trees.nonemumu): "%s" % (TreePaths.treeDiMu),
                        str(Trees.noneemu): "%s" % (TreePaths.treeMuEle)}

    helpString = "%s%%(%s)s" % (process.baseTreePath,treeType)
    treePath=helpString % treePathDict


    #Cut-String setzen

    if weights==True:
        if treeType==Trees.ee or treeType==Trees.noneee:
            if process.isData==False:
                if triggerscaling==True: # damit triggereffizienzen optional eingestellt werden koennen
                    cutt="(%s)*(%s)*(%s)" % (Cuts.weightEE(), Cuts.weight, cut)
                    log.logHighlighted("e Cut: %s, treeType %s" %(cutt, treeType))
                else:
                    cutt="(%s)*(%s)" % (Cuts.weight, cut)
                    log.logHighlighted("e Cut: %s, treeType %s" %(cutt, treeType))

        elif treeType==Trees.mumu or treeType==Trees.nonemumu:
            if process.isData==False:
                if triggerscaling==True:
                    cutt="(%s)*(%s)*(%s)" % (Cuts.weightMuMu(), Cuts.weight, cut)
                    log.logHighlighted("mumu Cut: %s, treeType %s"% (cutt,treeType))
                else:
                    cutt="(%s)*(%s)" % (Cuts.weight, cut)
                    log.logHighlighted("mumu Cut: %s, treeType %s"% (cutt,treeType))
        elif treeType==Trees.emu or treeType==Trees.noneemu:
            if process.isData==False:
                if triggerscaling==True:
                    cutt="(%s)*(%s)*(%s)"% (Cuts.weightEMu(), Cuts.weight, cut)
                    log.logHighlighted("emu Cut: %s, treeType %s"% (cutt,treeType))
                else:
                    cutt="(%s)*(%s)"% (Cuts.weight, cut)
                    log.logHighlighted("emu Cut: %s, treeType %s"% (cutt,treeType))
        else:
            log.logError("invalid TreeType: %s" %treeType)

    else:
        cutt=cut
        log.logHighlighted(cutt)


    #Histogramm aus Tree lesen

    for subProcess in process.subProcesses:
        fileName="%s%s" %(SubProcesses7TeV.dataPath, subProcess.file)
        file=ROOT.TFile(fileName)
        if file.IsOpen==False:
            log.logError("File %s does not exist" %file)
        else:
            histo=getHistoFromTree(fileName, treePath, variable, cutt , nBins, xMin, xMax)#kann man nur mit der gleichen Anzahl Bins etc aufaddieren
            count=file.FindObjectAny("analysis paths").GetBinContent(1)
            
            if process.isData == False:
                #print "%s unscaled: %s +Error %s + sumw2 %s" %(fileName,histo.GetBinContent(10),histo.GetBinError(10),
                                                              # math.sqrt(histo.GetSumw2()[10]))
																
                histo.Scale(subProcess.xSection*Constants.lumi/count)
                print Constants.lumi 
               # print "%s unscaled: %s +Error %s + sumw2 %s" %(fileName,histo.GetBinContent(10),histo.GetBinError(10),
                                                             #  math.sqrt(histo.GetSumw2()[10]))
                log.logDebug("Scalig histo: %f * %f / %f" %(subProcess.xSection,Constants.lumi,count))
            #log.logError("treeType: %s, xSection : %s, lumi : %s, count : %s" % (treeType,subProcess.xSection,Constants.lumi,count))
            if hTree==None:
                hTree=deepcopy(histo)
            else:
                hTree.Add(histo)
    hTree.SetName(process.name)

    #log.logHighlighted("Integral zu treeType %s = %s" % (treeType,hTree.Integral(0, histo.GetXaxis().GetNbins())))#############
    log.logDebug("entries=%f" %hTree.GetEntries())

    return hTree



#########################################################################################################################


def getHistoSumFromProcesses(process, variable,cut, treeTypes, nBins=100, xMin=0, xMax=1000, weights=True):
    "summiert fuer den Process die Types auf, treeType ist Liste"
    histoSum=None

    name=variable.replace(",","")
    name=name.replace("::","")
    name=name.replace("(","")
    name=name.replace(")","")
    if xMax==None:
        if not type(xMin)==type([]):
            log.logError("xMin ist %s und keine Liste" %xMin)
        histoSum = ROOT.TH1F("%s" % process.name, "%s" % process.name, nBins, array("f",xMin))
    else:
        histoSum = ROOT.TH1F("%s" % process.name, "%s" % process.name, nBins, xMin, xMax)

    for treeType in treeTypes:
        histo=getHistoFromProcess(process, variable, cut , treeType, nBins=nBins, xMin=xMin, xMax=xMax, weights=weights)
        histoSum.Add(histo)
    return histoSum
 
 

#########################################################################################################################      

def getTreeFromProcess(process, treeType): #z.B. (processes.Processes7TeV.DataHT , processes.Trees.ee)
    log.outputLevel=5
    treePathDict = {str(Trees.ee): "%s/%s" % (TreePaths.triggerDiEle,TreePaths.treeDiEle),
                    str(Trees.mumu): "%s/%s" % (TreePaths.triggerDiMu,TreePaths.treeDiMu),
                    str(Trees.emu): "%s/%s" % (TreePaths.triggerMuEle,TreePaths.treeMuEle),
                    str(Trees.noneee): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeDiEle),
                    str(Trees.nonemumu): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeDiMu),
                    str(Trees.noneemu): "%s/%s" % (TreePaths.triggerOhne,TreePaths.treeMuEle)}

    helpString = "%s%%(%s)s" % (process.baseTreePath,treeType)
    treePath=helpString % treePathDict #Hier: "cutsV18DileptonTriggerHT2_____EEDileptonTree/EEDileptonTree"

    for subProcess in process.subProcesses:
        fileName="%s%s" %(SubProcesses7TeV.dataPath, subProcess.file)
        file=ROOT.TFile(fileName)
        tree=getTreeFromFile(fileName, treePath)

    return tree



#########################################################################################################################

def getEntriesFromTree(fileName, treePath, variable, cut):
    histo = getHistoFromTree(fileName, treePath, variable, cut)
    log.logError("Muss noch geaendert werden, ist nicht skaliert!")
    #log.logInfo("HistoPointer:%s" % (histo))
    return histo.Integral(0, histo.GetXaxis().GetNbins())



#########################################################################################################################

def getEntriesFromProcesses(process, variable, cut , treeType, nBins=100, xMin=0, xMax=1000, trigger = False,
                            triggerscaling=True, weights=True):
    from math import sqrt
    histo=getHistoFromProcess(process, variable, cut, treeType, nBins=nBins, xMin=xMin, xMax=xMax, trigger=trigger, triggerscaling=triggerscaling, weights=weights)
    entries=histo.GetEntries()
    if entries==0:
        log.logError("Histo hat keine Eintraege")
        integral=0.00
        statError=0.00
    else:
        integral=histo.Integral(0, histo.GetXaxis().GetNbins())
        statError=1.0/sqrt(histo.GetEntries())*integral
    #log.logError("integral = %s"% integral)
    #log.logError("statError = %s bei treetype %s"% (statError,treeType))
    return integral, statError  #ergebnis, fehler=getEntriesFromProcesses

def cutTree(tree,variable,cut):
    name=variable.replace("()","")
    tree.Draw("%s >> %s" % (variable, name), cut)
    hTree = ROOT.gDirectory.Get("%s" % name) #hol Histo
    
#########################################################################################################################

def getEntriesAndJES(process, variable, cut , treeType, nBins=100, xMin=0, xMax=1000, trigger = False, 
                triggerscaling=True, weights=True, doJES=False):

    #entries
    entries,statError=getEntriesFromProcesses(process, variable, cut , treeType, nBins=nBins, xMin=xMin, xMax=xMax, 
                                              trigger=trigger, triggerscaling=triggerscaling, weights=weights)
    if doJES==True:
        sysCutUp1=cut.replace("ht","(1.04*ht)")
        sysCutUp=sysCutUp1.replace("met","(1.04*met)")
        sysCutDown1=cut.replace("ht","(0.96*ht)")
        sysCutDown=sysCutDown1.replace("met","(0.96*met)")
        #up
        entriesUp,statErrorUp=getEntriesFromProcesses(process, variable, sysCutUp , treeType, nBins=nBins, xMin=xMin, xMax=xMax, 
                                              trigger=trigger, triggerscaling=triggerscaling, weights=weights)
        #down
        entriesDown,statErrorDown=getEntriesFromProcesses(process, variable, sysCutDown , treeType,nBins=nBins, xMin=xMin, 
                                                          xMax=xMax,trigger=trigger, triggerscaling=triggerscaling, weights=weights)
        sysUp=entriesUp-entries
        sysDown=entriesDown-entries

        return entries,statError, sysUp, sysDown
    else:
        return entries, statError

