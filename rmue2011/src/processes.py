from defs import Titles,Colors


class SubProcesses7TeV:
    dataPath=""  #am Anfang einmal Setzen z.b. ~/BachelorArbeit/Daten/

    class Data:
	name="Data"
	file="sw428v0440.cutsV18SignalHighPt.Data_Run2011A.root"
	xSection=0.

    class DataHT_Run2011B:
        name="HT_Run2011B"
        file="sw428v0440trigger.cutsV18DileptonTriggerHT2.HT_Run2011B.root"
        xSection=0.

    class DataHT_Run2011BOld:
        name="HT_Run2011BOld"
        file="sw428v0440.cutsV18DileptonTriggerHT2.HT_Run2011B.root"
        xSection=0.

    class TTJetsHT:
        name= "TTJets_madgraph60M_Fall11"
        file= "sw428v0440trigger.cutsV18DileptonTriggerHT2.TTJets_madgraph60M_Fall11.root" 
        xSection=157.5

    class TTJets:
        name="TTJets"
        file="sw428v0440.cutsV18SignalHighPt.TTJets_madgraph60M_Fall11.root" 
        xSection=157.5 #pb

    class ZJets:
	name="ZJets"
	file="sw428v0440.cutsV18SignalHighPt.ZJets_madgraph_Fall11.root"
	xSection=3048.0

    class AstarJets:
	name="AstarJets"
	file = "sw428v0440.cutsV18SignalHighPt.AstarJets_madgraph_Summer11.root"
	xSection = 9611
    
    class T_tchannel:
	name="T_t-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_t_powheg_Fall11.root"
	xSection=41.92

    class Tbar_tchannel:
	name="Tbar_t-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_t_powheg_Fall11.root"
	xSection=22.65 

    class T_schannel:
	name="T_s-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_s_powheg_Fall11.root"
	xSection=3.19

    class Tbar_schannel:
	name="Tbar_s-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_s_powheg_Fall11.root"
	xSection=1.44
	
    class T_tWchannel:
	name="T_tW-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_tWDR_powheg_Fall11.root"
	xSection=7.87

    class Tbar_tWchannel:
	name="Tbar_tW-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_tWDR_powheg_Fall11.root"
	xSection=7.87

    class ZZTo2L2Nu:
	name="ZZTo2L2Nu"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJets_madgraph_Fall11.root"
	xSection=0.300

    class ZZTo2L2Q:
	name="ZZTo2L2Q"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJetsTo2L2Q_madgraph_Fall11.root"
	xSection=1.000

    class ZZTo4L:
	name="ZZTo4L"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJetsTo4L_madgraph_Fall11.root"
	xSection=0.076

    class WZTo3LNu:
	name="WZTo3LNu"
	file = "sw428v0440.cutsV18SignalHighPt.WZJets_madgraph_Fall11.root"
	xSection=0.856

    class WZTo2L2Q:
	name="WZTo2L2Q"
	file = "sw428v0440.cutsV18SignalHighPt.WZJetsTo2L2Q_madgraph_Fall11.root"
	xSection=1.786

    class WWTo2L2Nu:
	name="WWTo2LNu"
	file = "sw428v0440.cutsV18SignalHighPt.WWJets_madgraph_Fall11.root"
	xSection=4.783



class SubProcesses8TeV:  #noch zu bearbeiten!
    dataPath="../processedTrees/"  #am Anfang einmal Setzen z.b. ~/BachelorArbeit/Daten/Daten2012/
    
    class Data:#ist neu
    	name="data"
        #~ file="/user/schomakers/trees/sw532v0470.processed.MergedData.root"
        file="/home/jan/Trees/sw532v0474/sw532v0463.processed.MergedData2011.root"
        #file="../processedTrees/sw532v0457.processed.MergedData.root"
		#"sw532v0456.cutsV22Dilepton.Data_Run2012A.root"
	#"sw525v0451b.cutsV22Dilepton.Data_Run2012A.root" # fix vom 30.6.
    	xSection=0
        
    class DataHT_Run2012A_Old1:
        name="HT_Run2012A"
        file="sw524v0442.cutsV20DileptonTriggerHT.HT_Run2012A.root"
        xSection=0.

    class DataHT_Run2012A_Old2:
        name="HT_Run2012A"
        file="sw525v0445.cutsV21DileptonTriggerHT.HT_Run2012A.root"
        xSection=0.

    class DataHT_Run2012_Old3:
        name="HT_Run2012"
        file="sw525v0446.cutsV21DileptonTriggerHT.HT_Run2012.root"
        xSection=0.

    class DataHT_Run2012_Old4: #24.05.2012
        name="HT_Run2012"
        file="sw525v0447.cutsV22DileptonTriggerHT.HT_Run2012.root"
        xSection=0.

    class DataHT_Run2012: #30.05.2012
        name="HT_Run2012"
        #file="sw525v0445.cutsV21DileptonTriggerHT.HT_Run2012A.root" #18.05.2012
        file="sw525v0447.cutsV22DileptonTriggerHT.HT_Run2012.root" #24.05.2012
        #file="sw525v0448.cutsV22DileptonTriggerHT.HT_Run2012.root" #30.05.2012 #Aktuell Data
        xSection=0.
        
    class TTJetsHT_Old1:
        name= "TTJets_madgraph_Summer12"
        file= "sw524v0441.cutsV20DileptonTriggerHT.TTJets_madgraph_Summer12.root" #18.05.2012
        xSection=225.197

    class TTJetsHT_Old2:
        name= "TTJetsHT_madgraph_Summer12"
        file= "sw524v0442.cutsV20DileptonTriggerHT.TTJets_madgraph_Summer12.root"
        xSection=225.197

    class TTJetsHT:
        name= "TTJetsHT_madgraph_Summer12"
        #file= "sw524v0441.cutsV20DileptonTriggerHT.TTJets_madgraph_Summer12.root" #18.05.2012
        file= "sw525v0447.cutsV22DileptonTriggerHT.TTJets_madgraph_Summer12.root" #Aktuell MC
        xSection=225.197
        
    class TTJetsDilepton:
        name= "TTJetsDilepton_madgraph_Summer12"
        file= "sw525v0447.cutsV22DileptonTrigger.TTJets_madgraph_Summer12.root" #Aktuell MCTrue
        xSection=225.197

    class TTJets:#ist neu

        name="TTJets"
        #file= "sw525v0453.cutsV22Dilepton.TTJets_madgraph_Summer12.root" #6M Ereignisse fuer Vergleichsplot
        file="/home/jan/Trees/sw532v0474/sw532v0474.processed.TTJets_MGDecays_madgraph_Summer12.root"#sw532v0456.cutsV22Dilepton.TTJets_madgraph_Summer12.root"
		
	#"sw525v0451.cutsV22Dilepton.TTJets_madgraph_Summer12.root" #12.6.2012
        xSection=23.6 #pb

    class ZJets:#ist neu
        name="ZJets"
        file="/home/jan/Trees/sw532v0474/sw532v0474.processed.ZJets_madgraph_Summer12.root"#sw532v0456.cutsV22Dilepton.ZJets_madgraph_Summer12.root"
	#"sw525v0451.cutsV22Dilepton.ZJets_madgraph_Summer12.root" # 12.6.2012
        xSection=3503.71

    class AstarJets:
        name="AstarJets"
        file = "../processedTrees/sw532v0458.cutsV22Dilepton.AStar_madgraph_Summer12.root"
        xSection = 9611
    
    class T_tchannel:
	name="T_t-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_t_powheg_Fall11.root"
	xSection=55.531

    class Tbar_tchannel:
	name="Tbar_t-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_t_powheg_Fall11.root"
	xSection=30.0042 

    class T_schannel:# t+
	name="T_s-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_s_powheg_Fall11.root"
	xSection=3.89394

    class Tbar_schannel:# t-
	name="Tbar_s-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_s_powheg_Fall11.root"
	xSection=1.75776
	
    class T_tWchannel: #W+tbar
	name="T_tW-channel"
	file="sw428v0440.cutsV18SignalHighPt.T_tWDR_powheg_Fall11.root"
	xSection=11.1773

    class Tbar_tWchannel:
	name="Tbar_tW-channel"
	file="sw428v0440.cutsV18SignalHighPt.Tbar_tWDR_powheg_Fall11.root"
	xSection=11.1773

    class ZZTo2L2Nu: #2 Zs in 2 Leptonen und 2 Neutrinos
	name="ZZTo2L2Nu"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJets_madgraph_Fall11.root"
	xSection=0.300 

    class ZZTo2L2Q:
	name="ZZTo2L2Q"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJetsTo2L2Q_madgraph_Fall11.root"
	xSection=1.000
        
    class ZZTo4L:
	name="ZZTo4L"
	file = "sw428v0440.cutsV18SignalHighPt.ZZJetsTo4L_madgraph_Fall11.root"
	xSection=0.076

    class WZTo3LNu:
	name="WZTo3LNu"
	file = "sw428v0440.cutsV18SignalHighPt.WZJets_madgraph_Fall11.root"
	xSection=0.856

    class WZTo2L2Q:
	name="WZTo2L2Q"
	file = "sw428v0440.cutsV18SignalHighPt.WZJetsTo2L2Q_madgraph_Fall11.root"
	xSection=1.786

    class WWTo2L2Nu:
	name="WWTo2LNu"
	file = "sw428v0440.cutsV18SignalHighPt.WWJets_madgraph_Fall11.root"
	xSection=4.783
#_________________________________________________________________________________________________________________________________






class TreePaths:

    default="cutsV18SignalHighPtFinalTrees/" #praefix
    default8TeV= "cutsV20DileptonFinalTrees/"
    default8TeV_neu= "cutsV22DileptonFinalTrees/" # neu 4.6.2012
    ee_extension="EEDileptonTree"
    mumu_extension="MuMuDileptonTree"
    emu_extension="EMuDileptonTree"

    defaultDiLeptData="cutsV18DileptonTriggerHT2"
    defaultDiLeptMC="cutsV18DileptonTriggerHT2"
    
    DiLept8TeVDataComponentList=SubProcesses8TeV.DataHT_Run2012.file.split(".")
    defaultDiLept8TeVData=DiLept8TeVDataComponentList[1]
    #defaultDiLept8TeVData="cutsV22DileptonTriggerHT" #Aktuelle Daten
    #defaultDiLept8TeVData="cutsV22DileptonTriggerHTv2"
    
    DiLept8TeVMCComponentList=SubProcesses8TeV.TTJetsHT.file.split(".")
    defaultDiLept8TeVMC=DiLept8TeVMCComponentList[1]
    #defaultDiLept8TeVMC="cutsV22DileptonTriggerHT"
    
    DiLept8TeVMCTrueComponentList=SubProcesses8TeV.TTJetsDilepton.file.split(".")
    defaultDiLept8TeVMCTrue=DiLept8TeVMCTrueComponentList[1]
    #defaultDiLept8TeVMCTrue="cutsV22DileptonTrigger"
    
    triggerDiEle="HLTDiEleFinalTrees"   
    triggerDiMu="HLTDiMuFinalTrees"    
    triggerMuEle="HLTMuEleFinalTrees"
    triggerOhne="FinalTrees"
    treeDiEle="EEDileptonTree"
    treeMuEle="EMuDileptonTree"
    treeDiMu="MuMuDileptonTree"
#_________________________________________________________________________________________________________________________________    




class Trees:
    ee=1
    mumu=2
    emu=3
    noneee=4
    nonemumu=5
    noneemu=6
#_________________________________________________________________________________________________________________________________






class Processes7TeV:

    class Data:
	name="Data"
        sqrtS="7"
	title=Titles.data
	color=Colors.data
	subProcesses=[SubProcesses7TeV.Data]
	baseTreePath=TreePaths.default
	isData=True

    class DataHT:
        name="DataHT"
        sqrtS="7"
        title=Titles.ht
        color=Colors.ht
        subProcesses=[SubProcesses7TeV.DataHT_Run2011B]
        baseTreePath=TreePaths.defaultDiLeptData
        isData=True

    class TTJetsHT:
        name="TTJetsHT"
        sqrtS="7"
        title=Titles.ht
        color=Colors.ht
        subProcesses=[SubProcesses7TeV.TTJetsHT]
        baseTreePath=TreePaths.defaultDiLeptMC
        isData=False

    class TTJets:
        name="TTJets"
        sqrtS="7"
        title=Titles.ttJets
        color=Colors.ttJets
        subProcesses=[SubProcesses7TeV.TTJets]
        baseTreePath=TreePaths.default
        isData=False

    class ZJets:
        name="ZJets"
        sqrtS="7"
        title=Titles.zJets
        color=Colors.zJets
        subProcesses=[SubProcesses7TeV.ZJets, SubProcesses7TeV.AstarJets]
        baseTreePath=TreePaths.default
        isData=False

    class ZJetsOnly(ZJets):
        subProcesses=[SubProcesses7TeV.ZJets]

    class SingleT:
        name="SingleT"
        sqrtS="7"
        title=Titles.singleT
        color=Colors.singleT
        subProcesses=[SubProcesses7TeV.T_tchannel, SubProcesses7TeV.Tbar_tchannel, SubProcesses7TeV.T_schannel, SubProcesses7TeV.Tbar_schannel, SubProcesses7TeV.T_tWchannel, SubProcesses7TeV.Tbar_tWchannel]
        baseTreePath=TreePaths.default
	isData=False

    class DiBoson:
	name="DiBoson"
        sqrtS="7"
        title=Titles.diBoson
        color=Colors.diBoson
        subProcesses=[SubProcesses7TeV.ZZTo2L2Nu, SubProcesses7TeV.ZZTo2L2Q, SubProcesses7TeV.ZZTo4L, SubProcesses7TeV.WZTo3LNu, SubProcesses7TeV.WZTo2L2Q, SubProcesses7TeV.WWTo2L2Nu]
        baseTreePath=TreePaths.default
	isData=False



class Processes8TeV:

    class Data:
        name="Data"
        sqrtS="8"
        title=Titles.data
        color=Colors.data
        subProcesses=[SubProcesses8TeV.Data]
        baseTreePath=TreePaths.default8TeV_neu # _neu nacher loeschen!
        isData=True
        
    class DataHT:
        name="DataHT"
        sqrtS="8"
        title=Titles.ht
        color=Colors.ht
        subProcesses=[SubProcesses8TeV.DataHT_Run2012]
        baseTreePath=TreePaths.defaultDiLept8TeVData
        isData=True
        
    class TTJetsHT:
        name="TTJetsHT"
        sqrtS="8"
        title=Titles.ht
        color=Colors.ht
        subProcesses=[SubProcesses8TeV.TTJetsHT]
        baseTreePath=TreePaths.defaultDiLept8TeVMC
        isData=False

    class TTJetsDilepton:
        name="TTJetsHT"
        sqrtS="8"
        title=Titles.ht
        color=Colors.ht
        subProcesses=[SubProcesses8TeV.TTJetsDilepton]
        baseTreePath=TreePaths.defaultDiLept8TeVMCTrue
        isData=False

    class TTJets:
        name="TTJets"
        sqrtS="8"
        title=Titles.ttJets
        color=Colors.ttJets
        subProcesses=[SubProcesses8TeV.TTJets]
        baseTreePath=TreePaths.default8TeV_neu
        isData=False


    class ZJets:
        name="ZJets"
        sqrtS="8"
        title=Titles.zJets
        color=Colors.zJets
        subProcesses=[SubProcesses8TeV.ZJets] #AStarJets rausgenommen, da noch keine Daten
        baseTreePath=TreePaths.default8TeV_neu
        isData=False

    class SingleT:
        name="SingleT"
        sqrtS="8"
        title=Titles.singleT
        color=Colors.singleT
        subProcesses=[SubProcesses8TeV.T_tchannel, SubProcesses8TeV.Tbar_tchannel, SubProcesses8TeV.T_schannel, SubProcesses8TeV.Tbar_schannel, SubProcesses8TeV.T_tWchannel, SubProcesses8TeV.Tbar_tWchannel]
        baseTreePath=TreePaths.default8TeV
        isData=False

    class DiBoson:
        name="DiBoson"
        sqrtS="8"
        title=Titles.diBoson
        color=Colors.diBoson
        subProcesses=[SubProcesses8TeV.ZZTo2L2Nu, SubProcesses8TeV.ZZTo2L2Q, SubProcesses8TeV.ZZTo4L, SubProcesses8TeV.WZTo3LNu, SubProcesses8TeV.WZTo2L2Q, SubProcesses8TeV.WWTo2L2Nu]
        baseTreePath=TreePaths.default8TeV
        isData=False
#_________________________________________________________________________________________________________________________________




