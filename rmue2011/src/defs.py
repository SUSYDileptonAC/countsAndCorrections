class Test:
    test=False

class Marker:
    dot=1
    plus=2
    stern=3
    kreis=4
    kreuz=5
    kreisVoll=20
    quadratVoll=21
    kreisLeer=24
    quadratLeer=25
    ricolaLeer=28
    ricolaVoll=34
    rauteLeer=27
    rauteVoll=33

    #Plots tuep,sqrtS
    data7TeV=plus
    data8TeV=kreuz
    mc7TeV=quadratVoll
    mc8TeV=quadratLeer
    mcTrue7TeV=rauteVoll
    mcTrue8TeV=kreuz

class Colors:
    gelb=400
    sandgelb=401
    blau=854
    mittelblau=855
    hellblau=856
    mintgruen=842
    grau=920
    schwarz=1
    weiss=0
    gruen=3
    rot=2
    mattrot=46
    mattblau=38
    mattgruen=30
    mattgelb=41
    braunrot=49

    #Zuordnung der Teilchen
    ttJets=mittelblau
    singleT=blau
    zLightJets=sandgelb
    zbJets=gelb
    diBoson=grau
    bemerkungen=hellblau
    ht = mintgruen
    zJets=sandgelb
    data=schwarz
    mc=mittelblau #zB fuer rRatio MC gegen Data
    dataFit=grau+2 #bitte nicht nochmal loeschen
    mcFit=blau # bitte nicht nochmal loeschen

    #Plots tuep,sqrtS
    data7TeV=mintgruen
    data8TeV=blau
    mc7TeV=schwarz
    mc8TeV=rot
    mcTrue7TeV=blau
    mcTrue8TeV=blau

    #Zuordnung der Leptonen
    eE = blau
    eMu = rot
    muMu = mintgruen

class ConstantsBorg(object):
    lumi7TeV=4982. #pb
    lumi8TeV=9200#9300#8700#5100 #1598. #2400.
    lumi = lumi8TeV

    #Triggereffizien 8TeV Data (aus same sign Analyse Juli 2012)
    eff8TeVData_ee=0.97/1
    sigma8TeVData_ee_p= 0.05
    sigma8TeVData_ee_m=-0.05

    eff8TeVData_emu=0.943/1 #3.2626-Faktor wegen Korrektur von weights
    sigma8TeVData_emu_p=0.05
    sigma8TeVData_emu_m=-0.05

    eff8TeVData_mumu=0.964/1
    sigma8TeVData_mumu_p=0.05
    sigma8TeVData_mumu_m=-0.05
    
    
    mumuTriggerDict={lumi7TeV:"0.921", lumi8TeV:eff8TeVData_mumu}
    mumuTrigger = mumuTriggerDict[lumi7TeV]
    
    eeTriggerDict={lumi7TeV:"0.985", lumi8TeV:eff8TeVData_ee}
    eeTrigger = eeTriggerDict[lumi7TeV]
    
    emuTriggerDict={lumi7TeV:"0.942", lumi8TeV:eff8TeVData_emu}
    emuTrigger = emuTriggerDict[lumi7TeV]
    
    def __init__(self):
        self.updateBorg()

    def setLumi(self, newLumi):
        self.__dict__["lumi"] = newLumi
        self.__dict__["mumuTrigger"] = ConstantsBorg.mumuTriggerDict[newLumi]
        self.__dict__["eeTrigger"] = ConstantsBorg.eeTriggerDict[newLumi]
        #self.__dict__["emuTrigger"] = ConstantsBorg.emuTriggerDict[newLumi]
        print str(self.__dict__)

    def updateBorg(self):
        for key, value in self.__dict__.items():
            self.__dict__[key]= value

Constants = ConstantsBorg() 
    

class Annotation:
    "default Annotation"
    color=Colors.schwarz
    size=0.05
    align=22
    xPos=0.93 #NDC
    yPos=0.9

class TitleAnnotation(Annotation):
    "Annotation fuer den Titel"
    xPos=0.4
    yPos=0.93
    size=0.05

class UnderLegendAnnotation(Annotation):
    "Annotation fuer Bemerkungen unter der Legende"
    xPos=0.8
    yPos=0.7
    size=0.03
    text="CMS, Lumi blabla" 

class RatioAnnotation(Annotation):
    "Annotation fuer Bemerkungen unter der Legende" #andere Position, die ist wichtig fuer rRatio
    xPos=0.8
    yPos=0.7
    size=0.03
    text="CMS, Lumi blabla"  

class Lumi7TeVAnnotation(Annotation):
    "Annotation fuer Luminositaet bei 7TeV" 
    color=Colors.hellblau
    xPos=0.5
    yPos=0.85
    size=0.03
    text="#sqrt{s} = 7 TeV. #scale[0.6]{#int}Ldt = %.2f fb^{-1}" %(0.001*Constants.lumi7TeV)

class Lumi8TeVAnnotation1(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.45
    yPos=0.90
    size=0.04
    text="CMS personal work" 
class Lumi8TeVAnnotation2(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.45
    yPos=0.86
    size=0.04
    text="#sqrt{s} = 8 TeV. #scale[0.6]{#int}Ldt = %.2f fb^{-1}" %(0.001*Constants.lumi8TeV)
class Lumi8TeVAnnotation3(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.45
    yPos=0.82
    size=0.04
    text="Simulation" 
class Lumi8TeVAnnotationDY(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.5
    yPos=0.82
    size=0.04
    text="DY Simulation" 

class Lumi8TeVAnnotationMll1(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.36
    yPos=0.90
    size=0.04
    text="CMS personal work" 
class Lumi8TeVAnnotationMll2(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.36
    yPos=0.86
    size=0.04
    text="#sqrt{s} = 8 TeV. #scale[0.6]{#int}Ldt = %.2f fb^{-1}" %(0.001*Constants.lumi8TeV)
class Lumi8TeVAnnotationMll3(Annotation):
    "Annotation fuer Luminositaet bei 8TeV" 
    color=Colors.hellblau
    xPos=0.36
    yPos=0.82
    size=0.04
    text="Simulation" 

class EEAnnotation(Annotation):
    color=Colors.hellblau
    xPos=0.77
    yPos=0.75
    size=0.04
    text="leptonpair: ee"

class EMuAnnotation(Annotation):
    color=Colors.hellblau
    xPos=0.77
    yPos=0.75
    size=0.04
    text="leptonpair: e\mu"

class MuMuAnnotation(Annotation):
    color=Colors.hellblau
    xPos=0.77
    yPos=0.75
    size=0.04
    text="leptonpair: \mu\mu"
    
class Titles:
    ht="H_{T} [GeV]"
    mee="m_{ee} [GeV]" #invariante Masse
    mmumu="m_{#mu#mu} [GeV]" # invariante Masse
    p4M="m_{ll} [GeV]" # fuer rRatio
    pt2="p_{T}^{#ell_{1}} [GeV]"
    pt1="p_{T}^{l_{trailing}} [GeV]"
    pt2="p_{T}^{l_{leading}} [GeV]"
    nJets="n_{Jets}"
    ttJets="t#bar{t}"
    jzb="JZB"
    met="#slash{E}_{T} [GeV]"
    mll="m_{\ell\ell} [GeV]"
    meemumu="m_{ee,#mu#mu} [GeV]"
    memu="m_{e#mu} [GeV]"
    iso="Lepton2 isolation" 
    id1="Lepton1 isolation"
    id2="Lepton2 isolation"
    zJets="Drell Yan"
    singleT="Single t"
    diBoson ="DiBoson"
    data = "Daten"
    nBJets="n_{BJets}"
    nJets="n_{Jets}"
    nVertices="n_{Vertices}"
    jet1pt="Jet1_{pt}"
    jet2pt="Jet2_{pt}"
    jet3pt="Jet3_{pt}"
    jet4pt="Jet4_{pt}"
    lumitext="CMS Preliminary 2012 && #sqrt{s} = 8 TeV. #scale[0.6]{#int}Ldt = %.2f fb^{-1}" %(0.001*Constants.lumi) #fuer Lumi8TeVAnnotation
    runNr="Run number"
    eta1 = "#eta^{l_{2}}"

class Replaces:
    forAnnos= {"met>":"#slash{E}_{T}", 
         "(pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20)":"p_{T}>20(10)",
         "chargeProduct==-1":"OS",
         "(p4.M()<120 && p4.M()>60)":"60GeV<m_{ll}<120GeV"}


class Cuts:
    #~ leptonPtCut="(pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20)"
    #~ leptonNoCut="pt1>0"
    #~ leptonPtCutGraph="pt2 > 0"
    #~ pt1Cut="pt2 > 20"
    #~ pt2Cut="pt1 > 10"
    #~ id1Cut="id2<0.1"
    #~ id2Cut="id1<0.1"
#~ 
    #~ basicCut="chargeProduct==-1 && nJets>=2 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20) && deltaR > 0.3"
    #~ basicCutNoDeltaR="chargeProduct==-1 && nJets>=2 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20)"
    #~ basicCut0="chargeProduct==-1 && nJets==0 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20) && deltaR > 0.3" # nJets!
    #~ basicCutR="chargeProduct==-1 && nJets==0 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20) && deltaR > 0.3" # nJets!
#~ 
    #~ topCut="met>50 && nBJets>=1 && abs(p4.M()-91)>15" 
    #~ nVerticesCut="nVertices<11 && nVertices >9"
    #~ ptCut="pt2>50"
#~ 
    #~ basicCutohneN="chargeProduct==-1 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20) && deltaR > 0.3"
    #~ basicCutohnePt="chargeProduct==-1 && nJets>=2 && deltaR > 0.3"
    #~ basicCutOhnePtOhneN= "chargeProduct==-1 && deltaR > 0.3"
#~ 
    #~ invMassCut="(p4.M()<120 && p4.M()>60)"
    leptonPtCut="pt1 > 20 && pt2 > 20"
    leptonNoCut="pt1>0"
    leptonPtCutGraph="pt2 > 0"
    pt1Cut="pt2 > 20"
    pt2Cut="pt1 > 20"
    id1Cut="id2<0.1"
    id2Cut="id1<0.1"

    basicCut="chargeProduct==-1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
    basicCutIsoSideband="chargeProduct==-1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 > 0.15 && id2 > 0.15 && id1 < 1 && id2 < 1"
    basicCutNoDeltaR="chargeProduct==-1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && pt1 > 20 && pt2 > 20 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
    basicCutNoDeltaRNoNJets="chargeProduct==-1  && pt1 > 20 && pt2 > 20 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
    basicCut0="chargeProduct==-1 && nJets==0 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15" # nJets!
    basicCutR="chargeProduct==-1 && nJets==0 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15" # nJets!
    
    basicCutSS="chargeProduct==1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)"
    basicCutNoDeltaRSS="chargeProduct==1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && pt1 > 20 && pt2 > 20 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)"
    basicCut0SS="chargeProduct==1 && nJets==0 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)" # nJets!
    basicCutRSS="chargeProduct==1 && nJets==0 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)" # nJets!
    
    met50Cut = "met < 50"
    topCut="met>50 && nBJets>=1 && abs(p4.M()-91)>15" 
    nVerticesCut="nVertices<11 && nVertices >9"
    ptCut="pt2>50"

    basicCutohneN="chargeProduct==-1 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
    basicCutohnePt="chargeProduct==-1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
    basicCutOhnePtOhneN= "chargeProduct==-1 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522) && id1 < 0.15 && id2 < 0.15"
  
    basicCutohneNSS="chargeProduct==1 && pt1 > 20 && pt2 > 20 && deltaR > 0.3 && abs(eta1) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && abs(eta2) < 2.4 && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)"
    basicCutohnePtSS="chargeProduct==1 && nJets>=2 && jet1pt > 40 && jet2pt > 40 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) ) && p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)"
    basicCutOhnePtOhneNSS= "chargeProduct==1 && deltaR > 0.3 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6) )&& p4.M()>20 && runNr <= 201678 && !(runNr >= 198049 && runNr <= 198522)"
 
    invMassCut="(p4.M()<120 && p4.M()>60)"

    weight = "weight" # um triggereffizeinzen und weight zu trennen nur MC/3.2626

    @staticmethod
    def weightEE():
        return Constants.eeTrigger
    @staticmethod
    def weightMuMu():
        return Constants.mumuTrigger
    @staticmethod
    def weightEMu():
        return Constants.emuTrigger

    basicPlusInvMassCut = "(%s)*(%s)" %(basicCut,invMassCut)
    basicPlusInvMassPlusMet50Cut = "(%s)*(%s)*(%s)" %(basicCut,invMassCut,met50Cut)
    basicPlusInvMassCut0 = "(%s)*(%s)" %(basicCut0,invMassCut)
    basicOhneNJetPlusInvMass = "(%s)*(%s)" %(basicCutohneN,invMassCut)
    basicOhneNJetPlusInvMassPlusMet50Cut = "(%s)*(%s)*(%s)" %(basicCutohneN,invMassCut,met50Cut)
    basicOhnePt50 = "(%s)*(%s)*(pt2>50)" %(basicCutohnePt,invMassCut)
    basicCutOhnePt= "(%s)*(%s)*(pt2>30)" %(basicCutOhnePtOhneN,invMassCut)
 
    lowHtSignalRegion="(%s) && met>150 && 100<ht && ht<300" %basicCut
    lowHtSignalRegion200="(%s) && met>200 && 100<ht && ht<300" %basicCut
    lowHtSignalRegion175="(%s) && met>175 && 100<ht && ht<300" %basicCut
    signalRegion="(%s) && met>150 && ht>300" %basicCut
    signalRegion200="(%s) && met>200 && ht>300" %basicCut
    signalRegion175="(%s) && met>175 && ht>300" %basicCut
    controlRegion="(%s) && met>100 && met< 150 && 100<ht && ht<300 && nBJets>=1" %basicCut
    commonControlRegion="(%s) && met>100 && met< 150 && nJets == 2  && jet1pt > 40 && jet2pt > 40" %basicCut
    nurHt="(%s) && ht>300" %basicCut
    nurMet="(%s) && met>150" %basicCut

    lowHtSignalRegionJZB="(%s) && jzb>100 && 100<ht && ht<300" %basicCut
    signalRegionJZB="(%s) && jzb>125 && ht>300" %basicCut
    controlRegionJZB="(%s) && jzb>75 && met< 150 && 100<ht && ht<300" %basicCut
    
    basicPlusInvMassCutSS = "(%s)*(%s)" %(basicCutSS,invMassCut)
    basicPlusInvMassCut0SS = "(%s)*(%s)" %(basicCut0SS,invMassCut)
    basicOhneNJetPlusInvMassSS = "(%s)*(%s)" %(basicCutohneNSS,invMassCut)
    basicOhnePt50SS = "(%s)*(%s)*(pt2>50)" %(basicCutohnePtSS,invMassCut)
    basicCutOhnePtSS= "(%s)*(%s)*(pt2>50)" %(basicCutOhnePtOhneNSS,invMassCut)
 
    lowHtSignalRegionSS="(%s) && met>150 && 100<ht && ht<300" %basicCutSS
    lowHtSignalRegion200SS="(%s) && met>200 && 100<ht && ht<300" %basicCutSS
    lowHtSignalRegion175SS="(%s) && met>175 && 100<ht && ht<300" %basicCutSS
    signalRegionSS="(%s) && met>150 && ht>300" %basicCutSS
    signalRegion200SS="(%s) && met>200 && ht>300" %basicCutSS
    signalRegion175SS="(%s) && met>175 && ht>300" %basicCutSS
    controlRegionSS="(%s) && met>100 && met< 150 && 100<ht && ht<300 && nBJets>=1" %basicCutSS
    nurHtSS="(%s) && ht>300" %basicCutSS
    nurMetSS="(%s) && met>150" %basicCutSS
    commonControlRegionSS="(%s) && met>100 && met< 150 && nJets == 2" %basicCutSS
    

    lowHtSignalRegionJZB="(%s) && jzb>100 && 100<ht && ht<300" %basicCut
    signalRegionJZB="(%s) && jzb>125 && ht>300" %basicCut
    controlRegionJZB="(%s) && jzb>75 && met< 150 && 100<ht && ht<300" %basicCut

