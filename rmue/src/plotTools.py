import ROOT
from array import array
from messageLogger import messageLogger as log
from processes import SubProcesses7TeV, Processes7TeV, TreePaths, Trees
from defs import Cuts, Colors, Titles, Replaces 
from treeTools import getEntriesFromTree, getHistoFromProcess
import Styles

def histoStack(histos, isRatio=False):  #Liste Histos muss von klein zu gross sortiert sein!
    histoStack=ROOT.THStack("histoStack","stacked Histos")
    for histo in histos:
        if isRatio == False:
            histoStack.Add(histo) 
	else:
            histoStack.Add(histo,"E1")
    return histoStack


def save(canvas,plotpath, filename):   #plotpath und filename jeweils selber definieren
    from os import makedirs
    from os import path
    if not path.exists(plotpath):
        makedirs(plotpath)
    for ext in ["png", "pdf", "root"]:
        canvas.Print("%s%s.%s"%(plotpath,filename, ext))


def legende(histos, namen, style, xposition = 0.9,yposition = 0.9):
    hight=0.875
    verrueckung = 0.9 - yposition
    for histo in (histos):
        hight-=0.035
    hight -= verrueckung
    leg = ROOT.TLegend(xposition-0.2,hight,xposition,yposition) #relative Koordinaten x1,y1,x2,y2
    for (histo,name) in zip(histos, namen):
        leg.AddEntry(histo,name,style)
	leg.SetFillColor(ROOT.kWhite)
	leg.SetBorderSize(1)
	leg.SetLineWidth(2)
	leg.SetTextAlign(22)
    return leg


def makeAnnotation(annotation,text=None):
    annot=ROOT.TLatex()
    annot.SetNDC()
    annot.SetTextAlign(annotation.align)
    annot.SetTextSize(annotation.size)
    annot.SetTextColor(annotation.color)
    ypos=annotation.yPos
    Replaces.forAnnos
    if text==None:
        splitText=annotation.text.split("&&")
        for text in splitText:
            annot.DrawLatex(annotation.xPos,ypos,text) #relative Koordinaten (alternativ: Koordinaten des Plots)
            ypos-=0.03
    else:
        for entry,target in Replaces.forAnnos.items():
            text=text.replace(entry,target)
        splitText=text.split("&&")
        split2=[]
        for entry in splitText:
            split2.extend(entry.split("*"))
        for wort in split2:
            annot.DrawLatex(annotation.xPos, ypos, wort)
            ypos-=0.03
    return annot


def setPalette():
    # color palette
    #ROOT.gStyle.SetPalette(1)
    stops = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
    red = [ 0.00, 0.00, 0.87, 1.00, 0.51 ]
    green = [0.00, 0.81, 1.00, 0.20, 0.00 ]
    blue = [ 0.51, 1.00, 0.12, 0.00, 0.00 ]
    ROOT.TColor.CreateGradientColorTable(5, array("d", stops), array("d", red), array("d", green), array("d", blue), 255)
    ROOT.gStyle.SetNumberContours(255);
    return

def histosqrt(histo):#wurzelt alle Eintraege eines Histogramms
    clonehist=histo.Clone("ClonedHisto")
    for i in range(1, clonehist.GetNbinsX()+1):
        entrie=clonehist.GetBinContent(i)
        clonehist.SetBinContent(i, pow(entrie,0.5))
    return clonehist

def plotHistos(histoKeyList,histoDict,xMinDict,xMaxDict,nBinsDict,xAxisTitle="xAxisTitle wurde nicht benannt",yAxisTitle="yAxisTitle wurde nicht benannt",title="ueberschrift wurde nicht benannt"):
    legendenListe=histoKeyList
    c1 = ROOT.TCanvas ("c1","c1",1024,1024)
    histoDict[histoLeyList[0]].SetTitle(title)
    xMinSmall=xMinDict[histoKeyList[0]]
    xMaxTall=xMaxDict[histoKeyList[0]]
    for histoKey in histoKeyList :
        xMin=xMinDict[histoKey]
        xMax=xMaxDict[histoKey]
        if xMinSmall>xMin:
            xMinSmall=xMin
        if xMaxTall<xMax:
            xMaxTall=xMax
        nBins=nBinsDict[histoKey]
        for i in range(1,nBins+1):
            yi=histo.GetBinContent(i)
            if i == 1:
                ySmall=yTall=yi
            elif ySmall>yi:
                ySmall=yi
            elif yTall<yi:
                yTall=yi
    c1.DrawFrame(xMinSmall,yMinSmall-0.02*(yMaxTall-yMinSmall),xMaxTall + 0.02*(xMaxTall-xMinSmall),yMaxTall+0.02*(yMaxTall-yMinSmall),"%s;%s;%s" % (title,xAxisTitle,yAxisTitle))
    histoListe=[]
    for histoKey in histoKeyList:
        
        histo=histoDict[histoKey]
        histo.Draw("SAME P")
        c1.RedrawAxis()
        c1.Update()
        raw_input("ende")
        histoListe.append(histo)
    leg=legende(histoListe,legendenListe,"pl",0.6)
    leg.Draw()
    c1.RedrawAxis()
    c1.Update()
    raw_input("ende")

        
    
    
    


