binning = {
	"ht": (20,100, 800),
	"met": (30,50, 500),
	"tcMet": (30,50, 500),	
	"type1Met": (30,50, 500),	
	"caloMet": (30,50, 500),	
	"mht": (30,50, 500),	
	"jzb": (40,-300, 300),
	"inv": (996,20, 5000),
	#~ "inv": (56,20, 300),
	"invZoomed": (35,0, 70),
	"ptLead": (20,20,150),
	"ptTrail": (20,10,100),
	"isoLead":(15,0,0.15),
	"isoTrail":(15,0,0.15),
	"etaLead":(10,-2.5,2.5),
	"etaTrail":(10,-2.5,2.5),
	"absEtaLead":(10,0,2.5),
	"absEtaTrail":(10,0,2.5),
	"nJets":(8,-0.5,7.5),
	"nLightLeptons":(8,-0.5,7.5),
	"nBJets":(8,-0.5,7.5),
	"deltaR":(20, 0, 5 ),
	"deltaPhi":(15, 0, 4 ),
	"deltaPhiJetMET":(15, 0, 4.0 ),
	"deltaPhiSecondJetMET":(15, 0, 4.0 ),
	"deltaPhiLeptonMETHard":(15, 0, 4.0 ),		
	"deltaPhiLeptonMETSoft":(15, 0, 4.0 ),		
	"meanIP":(20, 0, 500),
	"nVertices":(38, -0.5, 37.5),
	"sqrts":(25, 100,1000)
	}

xTitle = {
	"ht": "H_{T} [GeV]",
	"met": "E^{miss}_{T} [GeV]",
	"tcMet": "track corr. E^{miss}_{T} [GeV]",	
	"caloMet": "calo based. E^{miss}_{T} [GeV]",	
	"type1Met": "type1 corr. E^{miss}_{T} [GeV]",	
	"mht": "H^{miss}_{T} [GeV]",	
	"jzb": "JZB [GeV]",
	"inv": "m_{ll} [GeV]",
	"invZoomed": "m_{ll} [GeV]",
	"ptLead": "p^{lead}_{T}  [GeV]",
	"ptTrail": "p^{trail}_{T} [GeV]",
	"isoLead": "rel. iso^{lead}",
	"isoTrail": "rel. iso^{trail}",
	"etaLead": "#eta^{lead}",
	"etaTrail": "#eta^{trail}",
	"absEtaLead": "|#eta^{lead}|",
	"absEtaTrail": "|#eta^{trail}|",
	"nJets":"n_{Jets}",
	"nLightLeptons":"n_{e, #mu}",
	"nBJets":"n_{b-Jets}",
	"deltaPhi":"|#Delta #phi (l_{1} l_{2})|",
	"deltaR":"|#Delta R (l_{1} l_{2})|",
	"deltaPhiJetMET":"|#Delta #phi (lead. jet E^{miss}_{T})|",
	"deltaPhiLeptonMETHard":"|#Delta #phi (lead. lepton E^{miss}_{T})|",
	"deltaPhiLeptonMETSoft":"|#Delta #phi (trail. lepont E^{miss}_{T})|",	
	"deltaPhiSecondJetMET":"|#Delta #phi (second. jet E^{miss}_{T})|",	
	"meanIP":"3D dist. to PV [#mum]",
	"nVertices":"n_{Vertices}",
	"sqrts":"#sqrt{s}^{(sub)}_{min}",
	"runNr": "Run Nr."
	}

def getHisto(tree,  cut, var,eventType = "", varBinning = None):
	from ROOT import TH1F

	name = "_".join([tree.GetName(), var, eventType])
	if varBinning is None:
		varBinning = binning[var]
	result = TH1F(name,";%s;"%xTitle[var], *(varBinning))
	result.Sumw2()
	changedVars = {
		"ptLead":"TMath::Max(pt1, pt2)",
		"ptTrail":"TMath::Min(pt1, pt2)",
		"absEtaLead":"((pt1>= pt2) * TMath::Abs(eta1) + (pt2> pt1) * TMath::Abs(eta2))",
		"absEtaTrail":"((pt1<= pt2) * abs(eta1) + (pt2< pt1) * abs(eta2))",
		"etaLead":"((pt1>= pt2) * eta1 + (pt2> pt1) * eta2)",
		"etaTrail":"((pt1<= pt2) * eta1 + (pt2< pt1) * eta2)",
		"isoLead":"((pt1>= pt2) * id1 + (pt2> pt1) * id2)",
		"isoTrail":"((pt1<= pt2) * id1 + (pt2< pt1) * id2)",
		"invZoomed":"p4.M()",
		"inv":"p4.M()",
		"deltaPhi":"abs(deltaPhi)",
		"deltaPhiJetMET":"abs(deltaPhiJetMET)",	
		"deltaPhiLeptonMETHard":"abs((pt1>pt2)*deltaPhiLeptonMET1+(pt2>pt1)*deltaPhiLeptonMET2)",	
		"deltaPhiLeptonMETSoft":"abs((pt1<pt2)*deltaPhiLeptonMET1+(pt2<pt1)*deltaPhiLeptonMET2)",						
		"deltaPhiSecondJetMET":"abs(deltaPhiSecondJetMET)",				
		"meanIP": "0.5*(abs(dB1)+abs(dB2))*10000",
		}

	for varName, changeTo in changedVars.iteritems():
		if var == varName:
			#raw_input( var+" -> "+changeTo)
			var = changeTo

	tree.Draw("%s>>%s"%(var, name), cut,"goff")
	

	return result

def getSFHisto(trees, cut, var, name="",varBinning = None):
	result = None
	for comb in ["EE", "MuMu"]:
		histo = getHisto(trees[comb], cut, var,name, varBinning)
		if result is None:
			result = histo.Clone(histo.GetName().replace(comb, "SF"))
		else:
			result.Add(histo)
	return result

def getBinWidth(var):
	bins = binning[var]
	return (bins[2]-bins[1])*1./bins[0]
