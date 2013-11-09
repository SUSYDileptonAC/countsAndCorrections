#DATA_TREES=../../../sw532v0458/processedTrees/sw532v0460.processed.MergedData.root
TREE_PATH=/user/edelhoff/trees/edgeAnalysis/sw532v0474/
DATA_TREES=$(TREE_PATH)/sw532v0474.processed.MergedData.root
DATA_TREES_2011=$(TREE_PATH)/sw532v0471.processed.MergedData_2011.root
DATA_TREES_METPD=$(TREE_PATH)/sw532v0474.processed.MergedData_METPD.root
DATA_TREES_SingleLepton=$(TREE_PATH)/sw532v0470.processed.MergedData_SingleLepton.root
SIGNAL_TREES=$(TREE_PATH)/sw532v0470.processed.SUSY_CMSSM_4610_202_Summer12.root
AN_PATH = /home/jan/Doktorarbeit/Dilepton/projects/DileptonAN
AN_TABLES=$(AN_PATH)/tables
AN_PLOTS=$(AN_PATH)/plots

TALK_PATH = /Users/heron/Documents/superSymmetry/doc/talks/edgeTaskForce/12-09-24_edelhoff_LowMassUnblinding

RELOADER = ~/projekte/scripts/skimReload.sh
MAKESLIDES = ./ofVsSF_XCheck.py
MAKECandCMC = ./cutAndCount_XCheck_MC.py
CONVERT_EFFICIENCIES = ./convertEfficiencies.py
COUNTER = ./cutAndCount_Result.py
MAKETABLES = ./makeSummaryTables.py
SSPlotter = ./SameSignPlotter.py

COUNTING_REGIONS = SignalNonRectInclusive SignalNonRectCentral SignalNonRectForward SignalNonRectInclusive_METPD SignalNonRectCentral_METPD SignalNonRectForward_METPD SignalHighMETLowNJetsCentral SignalHighMETLowNJetsForward SignalHighMETHighNJetsCentral SignalHighMETHighNJetsForward SignalLowMETHighNJetsCentral SignalLowMETHighNJetsForward SignalHighMET BarrelHighMET SignalLowMET SignalLowMETFullEta  ControlHighMET ControlLowMET ControlCentral ControlForward ControlInclusive SignalHighMET_METPD SignalLowMET_METPD BarrelHighMET_METPD SignalLowMETFullEta_METPD 

COUNTING_REGIONS_2011 = SignalNonRectInclusive_2011 SignalNonRectCentral_2011 SignalNonRectForward_2011  ControlCentral_2011 ControlForward_2011 ControlInclusive_2011

all: countPlots tables

slides.pdf: slides_ofVsSf_XCheck.tex
	pdflatex slides
	$(RELOADER) slides.pdf

copyAN:
	scp tab/table_*.tex $(AN_TABLES)
	scp fig/mll_Datadriven_SignalHighMET_*.pdf fig/mll_Datadriven_BarrelHighMET_*.pdf  fig/mll_Datadriven_SignalLowMET_*.pdf  fig/mll_Datadriven_SignalNonRectCentral_*.pdf fig/mll_Datadriven_SignalNonRectForward_*.pdf fig/mll_Datadriven_SignalNonRectInclusive_*.pdf $(AN_PLOTS)
	scp fig/MergedData_SignalNonRectCentral_*.pdf fig/MergedData_SignalNonRectForward_*.pdf  $(AN_PLOTS)/bluePlots
#	scp rmue/fig/8TeVrRatioDataVsMC_met.pdf rmue/fig/8TeVrRatioDataVsMC_ht.pdf rmue/fig/8TeVrRatioDataVsMC_eta1.pdf rmue/fig/8TeVrRatioDataVsMC_mll_Z.pdf rmue/fig/8TeVrRatioDataVsMC_nJets.pdf rmue/fig/8TeVrRatioDataVsMC_nVertices.pdf rmue/fig/8TeVrRatioDataVsMC_pt1.pdf rmue/fig/8TeVrRatioDataVsMC_mll_tt.pdf rmue/fig/8TeVrRatioDataVsMC_mll.pdf $(AN_PLOTS)

copyTalk:
	scp fig/mll_Datadriven_SignalHighMET_*.pdf  fig/mll_Datadriven_SignalLowMET_*.pdf $(TALK_PATH)/fig
	scp tab/table_region_SignalHighMET*.tex $(TALK_PATH)/tab

countPlots: $(foreach subcut, default, fig/mll_Datadriven_ControlCentral_$(subcut).pdf_NoSig fig/mll_Datadriven_ControlForward_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalNonRectInclusive_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalNonRectCentral_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalNonRectForward_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMETLowNJetsCentral_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMETLowNJetsForward_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMETHighNJetsCentral_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMETHighNJetsForward_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalLowMETHighNJetsCentral_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalLowMETHighNJetsForward_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMET_$(subcut).pdf_NoSig fig/mll_Datadriven_BarrelHighMET_$(subcut).pdf_NoSig  fig/mll_Datadriven_SignalLowMET_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalLowMETFullEta_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalLowMET_$(subcut).pdf_NoSig fig/mll_Datadriven_SignalHighMET_$(subcut).pdf_NoSig fig/mll_Datadriven_Pt2010HighMET_$(subcut).pdf_NoSig fig/mll_Datadriven_Pt3010HighMET_$(subcut).pdf_NoSig fig/mll_Datadriven_Pt3020HighMET_$(subcut).pdf_NoSig fig/mll_Datadriven_Pt3030HighMET_$(subcut).pdf_NoSig)

countPlots_Signal: $(foreach subcut, default RunAB RunC,fig/mll_Datadriven_SignalHighMET_$(subcut).pdf_Signal  fig/mll_Datadriven_SignalLowMET_$(subcut).pdf_Signal )

lumiPlots: $(foreach metric,nee nmumu nemu ns nsstar rmue simpleSig simpleSigStar,fig/lumi_vs_$(metric).pdf)

slides_ofVsSf_XCheck.tex: $(MAKESLIDES)
		$(MAKESLIDES) $(DATA_TREES) 2012

slides_ofVsSf_XCheck_2011.tex: $(MAKESLIDES)
		$(MAKESLIDES) $(DATA_TREES_2011)

slides_cutAndCount_XCheck_MC.tex: $(MAKECandCMC)
		$(MAKECandCMC)

tables: $(foreach region,$(COUNTING_REGIONS), shelves/cutAndCount_$(region).pkl)
	$(MAKETABLES)

tables2011: $(foreach region,$(COUNTING_REGIONS_2011), shelves/cutAndCount_$(region).pkl)
	$(MAKETABLES)

shelves/cutAndCount_%_2011.pkl:
	$(COUNTER) $(DATA_TREES_2011) $(subst shelves/cutAndCount_,,$(subst .pkl,,$@))

shelves/cutAndCount_%_METPD.pkl:
	$(COUNTER) $(DATA_TREES_METPD) $(subst shelves/cutAndCount_,,$(subst .pkl,,$@))

shelves/cutAndCount_%_SingleLepton.pkl:
	$(COUNTER) $(DATA_TREES_SingleLepton) $(subst shelves/cutAndCount_,,$(subst .pkl,,$@))

shelves/cutAndCount_%.pkl:
	$(COUNTER) $(DATA_TREES) $(subst shelves/cutAndCount_,,$(subst .pkl,,$@))

efficiencyCorrections: 
	wget http://lovedeep.web.cern.ch/lovedeep/work11/Jul20EleTnP2012/Tables/Tight/effiGsfIdTightMC.txt -O cfg/effiGsfIdLooseMC.txt
	$(CONVERT_EFFICIENCIES) electronTxt cfg/effiGsfIdLooseMC.txt
	wget http://lovedeep.web.cern.ch/lovedeep/work11/Jul20EleTnP2012/Tables/Tight/effiGsfIdTightMC.txt -O cfg/effiGsfIdLooseData.txt
	$(CONVERT_EFFICIENCIES) electronTxt cfg/effiGsfIdLooseData.txt

	echo "download https://twiki.cern.ch/twiki/pub/CMS/MuonReferenceEffs/MuonEfficiencies_11June2012_52X.pk yourself!"
	$(CONVERT_EFFICIENCIES) muonPkl cfg/MuonEfficiencies_11June2012_52X.pkl

fig/mll_Datadriven_%.pdf_NoSig:
	./mllDatadriven.py $(DATA_TREES) $(subst _, ,$(subst fig/mll_Datadriven_,,$(subst .pdf,,$@)))

fig/mll_Datadriven_%.pdf_Signal:
	./mllDatadriven.py $(DATA_TREES) $(subst _, ,$(subst fig/mll_Datadriven_,,$(subst .pdf,,$@)))	

fig/lumi_vs_%.pdf:
	./vsLumi.py $(DATA_TREES) $(subst _, ,$(subst fig/lumi_vs_,,$(subst .pdf,,$@)))

eventLists:
	./makeEventLists.py

SSPlots:
	$(SSPlotter) SignalHighMET
	$(SSPlotter) BarrelHighMET 	
	$(SSPlotter) SignalLowMET
	$(SSPlotter) SignalLowMETFullEta 	 
	$(SSPlotter) ControlBarrel
	$(SSPlotter) ControlInclusive
SSPlotsNonIso: 
	$(SSPlotter) SignalHighMET True
	$(SSPlotter) BarrelHighMET True 	
	$(SSPlotter) SignalLowMET True
	$(SSPlotter) SignalLowMETFullEta True	 
	$(SSPlotter) ControlBarrel True
	$(SSPlotter) ControlInclusive True 			
