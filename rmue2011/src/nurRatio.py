from messageLogger import messageLogger as log
from plotTools import histoStack
import ROOT
from array import array
from math import sqrt

class RatioPlots():
#"macht einen Ratioplot"

    def __init__(self,histosZaehler, histosNenner):
#	"Teilt die Histos durcheinander"
#       "Histos muessen Listen sein!"
        self.ratio=[]
	self.zHistos=[]
	self.nHistos=[]
        for (histoZ,histoN) in zip(histosZaehler,histosNenner):
            self.ratio.append(histoZ.Clone(histoZ.GetName()+"Ratio"))
            self.ratio[-1].Divide(histoN)  #teile durch Referenzsample #-1 nimmt letzten Eintrag usw
	    self.zHistos.append(histoZ)
	    self.nHistos.append(histoN)
	    #log.logDebug("ratioEntries for  %s  numerator %s and denominator %s" % (histoZ.GetName(),histoZ.GetEntries(),histoN.GetEntries()))

    def stack(self):#self=&Instanz
        ratioStacked=histoStack(self.ratio, isRatio=True)  #nachher mit "nostack" zeichnen
        return ratioStacked

    def globalRatio(self, efficiency=False):
	if len(self.zHistos)==0:
	    #log.logError("Zaehlerliste leer")
	    return None
        else:
    	    zaehlersumme = []
	    zaehlersumme = self.zHistos[0].Clone("zaehlerhisto")
	    for hi in self.zHistos[1:]:
                zaehlersumme.Add(hi)
	if len(self.nHistos)==0:
	    #log.logError("Nennerliste leer")
	    return None
        else:
    	    nennersumme = []
	    nennersumme = self.nHistos[0].Clone("nennerhisto")
	    for hi in self.nHistos[1:]:
                nennersumme.Add(hi)
        if not efficiency:
            zaehlersumme.Divide(nennersumme)
            return zaehlersumme
        if efficiency:
            """c1 = ROOT.TCanvas ("c1","c1",1024,1024)#
            zaehlersumme.Draw()#
            c1.Update()#
            raw_input("ende")#
            c2 = ROOT.TCanvas ("c2","c2",1024,1024)#
            nennersumme.Draw()#
            c2.Update()#
            raw_input("ende")#"""
            efficiencyGraph=ROOT.TEfficiency(zaehlersumme, nennersumme)
            return efficiencyGraph

class IntegratedRatio():
    def __init__(self,histosZaehler, histosNenner):
        self.graphenRatios=[]
        for (histoZ,histoN) in zip(histosZaehler,histosNenner):
            listex=[]
            listey=[]
            listeFehlerx=[]
            listeFehlery=[]
            for i in range(1,histoZ.GetNbinsX()+1):
                intErrorZ=ROOT.Double()
                intErrorN=ROOT.Double()
                intZ=histoZ.IntegralAndError(i,histoZ.GetXaxis().GetNbins(),intErrorZ)
                intN=histoN.IntegralAndError(i,histoN.GetXaxis().GetNbins(),intErrorN)
                #print "intZ %s+-%s, intN %s+-%s" %(intZ,errorZ, intN, errorN)
                listex.append(histoN.GetBinLowEdge(i))
                listeFehlerx.append(0)
                if intN==0:
                    listey.append(0)
                    listeFehlery.append(0)
                else:
                    ratio=intZ/intN
                    errorRatio=ratio*sqrt((intErrorN/intN)**2+(intErrorZ/intZ)**2)
                    listey.append(ratio)
                    listeFehlery.append(errorRatio)
                    #print "ratio %s+-%s" %(intZ/intN, errorRatio)
            graphRatioInt=ROOT.TGraphErrors(len(listex),array("f",listex), array("f",listey), array("f",listeFehlerx),
                                            array("f", listeFehlery))
            self.graphenRatios.append(graphRatioInt)

    def drawRatio(self,canvas,colors):
        for (graph,color) in zip(self.graphenRatios, colors):
            graph.SetMarkerColor(color)
            graph.SetMarkerStyle(ROOT.kFullCircle)
            graph.Draw("same P")
        
                
            
    

            

          	    

    



