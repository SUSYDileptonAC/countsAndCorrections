from math import sqrt
import ROOT
from ROOT import TMath
class Constant:
	val = 0.
	printval = 0.
	err = 0.
	
class Constants:
	class Trigger:
		class EffEE(Constant):
			val = 0.95
			err = 0.95 * 0.05
		class EffEMu(Constant):
			val = 0.94
			err = 0.05*0.94
			#~ val = 0.95
			#~ err = 0.5*(0.918+0.883) * 0.05

		class EffMuMu(Constant):
			val = 0.95
			err = 0.95*0.05

	class Pt2010:
		class RInOut(Constant):
			val = 0.1376
			err = sqrt(0.0014**2+0.0344**2)
		class RMuE(Constant):
			val =1.2
			err =1.2*0.1			
		
	class Pt2020:
		class RInOut(Constant):
			val =0.07
			err =0.07*0.25
		class RMuE(Constant):
			val =1.2
			err =1.2*0.1
	class Lumi:
		val = 12000
		printval = "12.0"
		err = 0.045*12000
		#~ val = 9200
		#~ printval = "9.2"
		#~ err = 0.045*9200

		#~ val = 6770
		#~ printval = "6.77"
		#~ err = 0.045*6770
		#~ val = 5051
		#~ printval = "5.05"
		#~ err = 0.045*5051

class runRanges:
	class RunAB:
		lumi = 5230
		printval = "5.23"
		lumiErr = 0.045*5230
		runCut = "&& runNr <= 196531"
		label = "RunAB"
	class RunC:
		lumi = 6770
		printval = "6.77"
		lumiErr = 0.045*6770
		runCut = "&& (runNr > 196531 || runNr ==1)"
		label = "RunC"
	class Run92:
		lumi = 9200
		printval = "9.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 201678 && !(runNr >= 198049 && runNr <= 198522)"
		label = "Run92"
	class Full2012:
		lumi = 19400
		printval = "19.4"
		lumiErr = 0.045*19600
		runCut = "&& runNr < 99999999"
		label = "Full2012"
	class BlockA:
		lumi = 9200
		printval = "9.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 99999999"
		label = "BlockA"
	class BlockB:
		lumi = 10200
		printval = "10.2"
		lumiErr = 0.045*9200
		runCut = "&& runNr < 99999999"
		label = "BlockB"
	class All:
		lumi = 12000
		printval = "12.0"
		lumiErr = 0.045*12000
		runCut = "&& runNr < 99999999"
		label = "Full"
	class Run2011:
		lumi = 4980
		printval = "5.0"
		lumiErr = 0.045*4980
		runCut = "&& runNr < 99999999"
		label = "2011"
		
	#~ runs = [RunAB,RunC,Run92,All]
	runs = [BlockA,BlockB,Full2012]
		

		
class Region:
	cut = " chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && p4.M() > 20 && deltaR > 0.3 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cutToUse = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941) )"
	#~ cutToUse = "(chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3  )"
	title = "everything"
	latex = "everything"
	labelRegion = "p_{T}^{l} > 20 GeV |#eta^{l}| < 2.4"
	name = "Inclusive"
	labelSubRegion = ""
	dyPrediction = {}
	rMuE = Constants.Pt2010.RMuE
	rInOut = Constants.Pt2010.RInOut
	logY = True
class theCuts:
	class massCuts:
		class default:
			cut = "p4.M() > 20"
			label = "m_{ll} = 20 GeV"
			name = "fullMassRange"
		class edgeMass:
			cut = "p4.M()> 20 && p4.M() < 70"
			label = "20 GeV < m_{ll} < 70 GeV"
			name = "edgeMass"
		class zMass:
			cut = "p4.M()> 81 && p4.M() < 101"
			label = "81 GeV < m_{ll} < 101 GeV"
			name = "zMass"
		class highMass:
			cut = "p4.M() > 120"
			label = "m_{ll} > 120 GeV"
			name = "highMass"
			
	class ptCuts:
		class pt2010:
			cut = "((pt1 > 20 && pt2 > 10)||(pt1 > 10 && pt2 > 20))"
			label = "p_{T} > 20(10) GeV"
			name = "pt2010"
		class pt2020:
			cut = "pt1 > 20 && pt2 > 20"
			label = "p_{T} > 20 GeV"
			name = "pt2020"
		class pt3010:
			cut = "((pt1 > 30 && pt2 > 10)||(pt1 > 10 && pt2 > 30))"
			label = "p_{T} > 30(10) GeV"
			name = "pt3010"
		class pt3020:
			cut = "((pt1 > 30 && pt2 > 20)||(pt1 > 20 && pt2 > 30))"
			label = "p_{T} > 30(20) GeV"
			name = "pt3020"
		class pt3030:
			cut = "pt1 > 30 && pt2 > 30"
			label = "p_{T} > 30 GeV"
			name = "pt3030"

	class nJetsCuts:
		class noCut:
			cut = "nJets >= 0"
			label = ""
			name = ""
		class geOneJetCut:
			cut = "nJets >= 1"
			label = "nJets #geq 1"
			name = "ge1Jets"
		class geTwoJetCut:
			cut = "nJets >= 2"
			label = "nJets #geq 2"
			name = "ge2Jets"
		class geThreeJetCut:
			cut = "nJets >= 3"
			label = "nJets #geq 3"
			name = "ge3Jets"
		class noJet:
			cut = "nJets == 0"
			label = "nJets = 0"
			name = "0Jets"
		class OneJet:
			cut = "nJets == 1"
			label = "nJets = 1"
			name = "1Jets"
		class TwoJet:
			cut = "nJets == 2"
			label = "nJets = 2"
			name = "2Jets"
		class ThreeJet:
			cut = "nJets == 3"
			label = "nJets = 3"
			name = "3Jets"
		class FourJet:
			cut = "nJets == 4"
			label = "nJets = 4"
			name = "4Jets"
	class metCuts:
		class noCut:
			cut = "met >= 0"
			label = ""
			name = ""
		class met50:
			cut = "met > 50"
			label = "E_{T}^{miss} > 50 GeV"
			name = "MET50"
		class met100:
			cut = "met > 100"
			label = "E_{T}^{miss} > 100 GeV"
			name = "MET100"
		class met150:
			cut = "met > 150"
			label = "E_{T}^{miss} > 150 GeV"
			name = "MET150"
			
	class dRCuts:
		class lowDR:
			cut = "deltaR < 1.5"
			label = "#Delta R(ll) < 1.5"
			name = "LowDR"
		class midDR:
			cut = "deltaR > 1.5 && deltaR < 2.5"
			label = "1.5 #Delta R(ll) < 2.5"
			name = "MidDR"
		class highDR:
			cut = "deltaR > 2.5"
			label = "#Delta R(ll) > 2.5"
			name = "HighDR"
			
	class dPhiCuts:
		class lowDPhi:
			cut = "abs(deltaPhi) < 1.0"
			label = "#Delta #phi (ll) < 1.0"
			name = "LowDPhi"
		class midDPhi:
			cut = "abs(deltaPhi) > 1.0 && (deltaPhi) < 2.0"
			label = "1.0 < #Delta #phi (ll) < 2.0"
			name = "MidDPhi"
		class highDPhi:
			cut = "abs(deltaPhi) > 2.0"
			label = "#Delta #phi (ll) > 2.0"
			name = "HighDPhi"

	class dEtaCuts:
		class lowDEta:
			cut = "sqrt(deltaR^2 - deltaPhi^2) < 1.0"
			label = "#Delta #eta (ll) < 1.0 "
			name = "LowDEta"
		class midDEta:
			cut = "sqrt(deltaR^2 - deltaPhi^2) > 1.0 && sqrt(deltaR^2 - deltaPhi^2) < 2.0"
			label = "1.0 #Delta #eta (ll) < 2.0 "
			name = "midDEta"
		class highDEta:
			cut = "sqrt(deltaR^2 - deltaPhi^2) > 2.0 "
			label = "#Delta #eta (ll) > 2.0 "
			name = "highDEta"

	class etaCuts:
		class inclusive:
			cut = "abs(eta1) < 2.4 && abs(eta2) < 2.4"
			label = "|#eta| < 2.4"
			name = "FullEta"
		class Barrel:
			cut = "abs(eta1) < 1.4 && abs(eta2) < 1.4"
			label = "|#eta| < 1.4"
			name = "Barrel"
		class Endcap:
			cut = "1.4 <= TMath::Max(abs(eta1),abs(eta2))"
			label = "at least one |#eta| > 1.4"
			name = "Endcap"
		class BothEndcap:
			cut = "abs(eta1) > 1.4 && abs(eta2) > 1.4"
			label = "|#eta| > 1.4"
			name = "BothEndcap"
		class CentralBarrel:
			cut = "abs(eta1) < 0.8 && abs(eta2) < 0.8"
			label = "|#eta| < 0.8"
			name = "CentralBarrel"
		class OuterBarrel:
			cut = "abs(eta1) > 0.8 && abs(eta2) > 0.8 && abs(eta1) < 1.4 && abs(eta2) < 1.4"
			label = "0.8 < |#eta| < 1.4"
			name = "CentralBarrel"


	class TightIso:
		cut = "id1 < 0.05 && id2 > 0.05"
		label = "rel. iso. < 0.05"
		name = "TightIso"

	class bTags:
		class noBTags:
			cut = "nBJets == 0"
			label = "nBJets = 0"
			name = "noBJets"
		class OneBTags:
			cut = "nBJets == 1"
			label = "nBJets = 1"
			name = "OneBJets"
		class TwoBTags:
			cut = "nBJets == 2"
			label = "nBJets = 2"
			name = "TwoBJets"
		class ThreeBTags:
			cut = "nBJets == 3"
			label = "nBJets = 3"
			name = "ThreeBJets"
		class geOneBTags:
			cut = "nBJets >= 1"
			label = "nBJets #geq 1"
			name  = "geOneBTags"
		class geTwoBTags:
			cut = "nBJets >= 2"
			label = "nBJets #geq 2"
			name  = "geTwoBTags"
		class geThreeBTags:
			cut = "nBJets >= 3"
			label = "nBJets #geq 3"
			name  = "geThreeBTags"
			
	class htCuts:
		class ht100:
			cut = "ht > 100"
			label = "H_{T} > 100 GeV"
			name = "HT100"
		class ht300:
			cut = "ht > 300"
			label = "H_{T} > 300 GeV"
			name = "HT300"
		class ht100to300:
			cut = "ht > 100 && ht < 300"
			label = "100 GeV < H_{T} < 100 GeV"
			name = "HT100to300"
			
	class pileUpCuts:
		class lowPU:
			cut = "nVertices < 11"
			label = "N_{Vtx} < 11"
			name = "LowPU"
		class midPU:
			cut = "nVertices >= 11 && nVertices < 16"
			label = "11 #leq N_{Vtx} < 16"
			name = "MidPU"
		class highPU:
			cut = "nVertices >= 16"
			label = "N_{Vtx} #geq 16"
			name = "HighPU"


class theVariables:
	class Eta1:
		variable = "eta1"
		name = "Eta1"
		xMin = -2.4
		xMax = 2.4
		nBins = 10
		labelX = "#eta_{1}"
		labelY = "Events / 0.48"	
	class Eta2:
		variable = "eta2"
		name = "Eta2"
		xMin = -2.4
		xMax = 2.4
		nBins = 10
		labelX = "#eta_{2}"
		labelY = "Events / 0.48"	
	class PtEle:
		variable = "pt1"
		name = "Pt1"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{ele} [GeV]"
		labelY = "Events / 10 GeV"	
	class PtMu:
		variable = "pt2"
		name = "Pt2"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{#mu} [GeV]"
		labelY = "Events / 10 GeV"	
	class LeadingPt:
		variable = "(pt1>pt2)*pt1+(pt2>pt1)*pt2"
		name = "LeadingPt"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{leading} [GeV]"
		labelY = "Events / 10 GeV"	
	class TrailingPt:
		variable = "(pt1>pt2)*pt2+(pt2>pt1)*pt1"
		name = "TrailingPt"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{trailing} [GeV]"
		labelY = "Events / 10 GeV"	
	class Met:
		variable = "met"
		name = "MET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "E_{T}^{miss} [GeV]"
		labelY = "Events / 10 GeV"	
	class Type1Met:
		variable = "type1Met"
		name = "Type1MET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "typeI corr. E_{T}^{miss} [GeV]"
		labelY = "Events / 10 GeV"	
	class TcMet:
		variable = "tcMet"
		name = "TCMET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "track corr. E_{T}^{miss} [GeV]"
		labelY = "Events / 10 GeV"	
	class CaloMet:
		variable = "caloMet"
		name = "CaloMET"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "calo E_{T}^{miss} [GeV]"
		labelY = "Events / 10 GeV"	
	class MHT:
		variable = "mht"
		name = "MHT"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "H_{T}^{miss} [GeV]"
		labelY = "Events / 10 GeV"	
	class HT:
		variable = "ht"
		name = "HT"
		xMin = 0
		xMax = 800
		nBins = 20
		labelX = "H_{T} [GeV]"
		labelY = "Events / 40 GeV"	
	class Mll:
		variable = "p4.M()"
		name = "Mll"
		xMin = 20
		xMax = 305
		nBins = 57
		labelX = "m_{ll} [GeV]"
		labelY = "Events / 5 GeV"	
	class Ptll:
		variable = "p4.Pt()"
		name = "Ptll"
		xMin = 0
		xMax = 400
		nBins = 40
		labelX = "p_{T}^{ll} [GeV]"
		labelY = "Events / 10 GeV"	
	class nJets:
		variable = "nJets"
		name = "NJets"
		xMin = 0
		xMax = 10
		nBins = 10
		labelX = "n_{jets}"
		labelY = "Events"	
	class nBJets:
		variable = "nBJets"
		name = "NBJets"
		xMin = 0
		xMax = 10
		nBins = 10
		labelX = "n_{b-tagged jets}"
		labelY = "Events"	
	class deltaR:
		variable = "deltaR"
		name = "DeltaR"
		xMin = 0
		xMax = 4
		nBins = 20
		labelX = "#Delta R_{ll}"
		labelY = "Events / 0.2"	

		

	
	



class Mll30to70JetEtaRegion:
	cut = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 30 && p4.M() < 70 && deltaR > 0.3 && ( nJets ==0 || (nJets == 1 && abs(jet1.Eta()) < 2.5 ) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && nJets ==2) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && nJets ==3) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && abs(jet4.Eta()) < 2.5 && nJets ==4))"
	cutToUse = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && deltaR > 0.3 && abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && abs(jet4.Eta()) < 2.5 && nJets <=4)"
	title = "everything"
	latex = "everything"
	dyPrediction = {}
	rMuE = Constants.Pt2010.RMuE
	rInOut = Constants.Pt2010.RInOut
class LowMllJetEtaRegion:
	cut = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && p4.M() < 70 && deltaR > 0.3 && ( nJets ==0 || (nJets == 1 && abs(jet1.Eta()) < 2.5 ) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && nJets ==2) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && nJets ==3) || (abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && abs(jet4.Eta()) < 2.5 && nJets ==4))"
	cutToUse = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20  && p4.M() < 70 && deltaR > 0.3 && abs(jet1.Eta()) < 2.5 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 2.5 && abs(jet4.Eta()) < 2.5 && nJets <=4)"
	title = "everything"
	latex = "everything"
	dyPrediction = {}
	rMuE = Constants.Pt2010.RMuE
	rInOut = Constants.Pt2010.RInOut
class LowMllTightJetEtaRegion:
	cut = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20 && p4.M() < 70 && deltaR > 0.3 && ( nJets ==0 || (nJets == 1 && abs(jet1.Eta()) < 1.4 ) || (abs(jet1.Eta()) < 1.4 && abs(jet2.Eta()) < 1.4 && nJets ==2) || (abs(jet1.Eta()) < 1.4 && abs(jet2.Eta()) < 1.4 && abs(jet3.Eta()) < 1.4 && nJets ==3) || (abs(jet1.Eta()) < 1.4 && abs(jet2.Eta()) < 2.5 && abs(jet3.Eta()) < 1.4 && abs(jet4.Eta()) < 1.4 && nJets ==4))"
	cutToUse = "weight*(chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4  && abs(eta2) < 2.4 && p4.M() > 20  && p4.M() < 70 && deltaR > 0.3 && abs(jet1.Eta()) < 1.4 && abs(jet2.Eta()) < 1.4 && abs(jet3.Eta()) < 1.4 && abs(jet4.Eta()) < 1.4 && nJets <=4)"
	title = "everything"
	latex = "everything"
	dyPrediction = {}
	rMuE = Constants.Pt2010.RMuE
	rInOut = Constants.Pt2010.RInOut


class Regions:
	class SignalInclusive(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Inclusive Signal Region"
		titel = "Inclusive SR"
		latex = "Inclusive Signal Region"
		name = "SignalInclusive"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}

	class SignalForward(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Forward Signal Region"
		titel = "Forward SR"
		latex = "Forward Signal Region"
		name = "SignalForward"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}
			
	class SignalOneForward(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets>=3 && met > 100)) &&  1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (abs(eta1) < 1.6 || abs(eta2) < 1.6) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "Signal Region One Forward"
		titel = "One Forward SR"
		latex = "One Forward Signal Region"
		name = "SignalOneForward"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}

	class SignalBarrel(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >= 3 && met > 100)) && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		#~ labelRegion = Region.labelRegion
		labelSubRegion = "Central Signal Region"
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		titel = "Central SR"
		latex = "Central Signal Region"
		name = "SignalCentral"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}
	


	class SignalHighMET(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 H_{T} > 100 GeV E_{T}^{miss} > 150 GeV"
		titel = "High E_{T}^{miss} SR"
		latex = "High \MET\ Signal Region"
		name = "SignalHighMET"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}
		#~ def __init__(self,region):
			#~ self.cut = "  weight*(nJets >= 2 && ht > 100 && met > 150 && (%s))"%region.cut	
			#~ self.labelRegion = region.label
	class SignalHighMETBarrel(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		#~ labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 H_{T} > 100 GeV E_{T}^{miss} > 150 GeV"
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		titel = "High E_{T}^{miss} SR"
		latex = "High \MET\ Signal Region"
		name = "SignalHighMETBarrel"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = False
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}
		#~ def __init__(self,region):
			#~ self.cut = "  weight*(nJets >= 2 && ht > 100 && met > 150 && (%s))"%region.cut	
			#~ self.labelRegion = region.label
		
	class Control(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV"		
		titel = "CR"
		latex = "Control Region"
		name = "Control"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
	class ControlForward(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && 1.4 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV"		
		titel = "CR"
		latex = "Control Region Forward"
		name = "ControlForward"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
	class ControlCentral(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} = 2 100 GeV < E_{T}^{miss} < 150 GeV |#eta| < 1.4"		
		titel = "CR"
		latex = "Control Region Central"
		name = "ControlCentral"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
				
			
	class bTagControl(Region):
		cut = "nJets >=2 && met > 50 && nBJets >=1 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 N_{bJets} #geq 1 E_{T}^{miss} > 50 GeV"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "bTagControl"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
		#~ def __init__(self,region):
			#~ self.cut = "  weight*(met > 50 && nBJets >=1 && nJets >=2 && (%s))"%region.cut	
			#~ self.labelRegion = region.label	
			
	class ttBarDileptonSF(Region):
		cut = "nJets >=2 && met > 40 && (p4.M()<76 || p4.M() > 106) && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2 E_{T}^{miss} > 40 GeV |m_{ll} - m_{Z}| > 25 GeV"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "ttBarDileptonSF"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
	class ttBarDileptonOF(Region):
		cut = "nJets >=2 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} #geq 2"			
		titel = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		name = "ttBarDileptonOF"
		rMuE = Constants.Pt2010.RMuE
		rInOut = Constants.Pt2010.RInOut
		logY = True
		#~ def __init__(self,region):
			#~ self.cut = "  weight*(met > 50 && nBJets >=1 && nJets >=2 && (%s))"%region.cut	
			#~ self.labelRegion = region.label	

	class SignalLowMET(Region):
		cut = "nJets >= 3 && pt1 > 20 && pt2 > 20 && p4.M() > 20 && abs(eta1)<1.4 && abs(eta2) < 1.4  && met > 100 && (%s)"%Region.cut
		labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		labelSubRegion = "N_{jets} #geq 3 E_{T}^{miss} > 100 GeV"			
		titel = "Low E_{T}^{miss} SR"
		latex = "Low \MET\ Signal Region"
		name = "SignalLowMET"
		logY = False
		dyPrediction = {
			"default":	( sum([48,10,3.3,6.3]), sqrt(sum([i**2 for i in [15,7.1,1.8,3.3]])),0),
			"RunAB":	( sum([28,5.6,1.9,3.5]), sqrt(sum([i**2 for i in [8.5,3.9,1.0,1.8]])),0),
			"RunC":	    ( sum([21,4.5,1.5,2.8]), sqrt(sum([i**2 for i in [6.3,3.2,0.8,1.5]])),0),
			}

		rMuE = Constants.Pt2020.RMuE
		rInOut = Constants.Pt2020.RInOut
		#~ def __init__(self,region):
			#~ self.cut =" weight*(pt1 > 20 && pt2 > 20 && abs(eta1)<1.4 && abs(eta2) < 1.4 && p4.M() > 20 && nJets >= 3  && met > 100 && (%s))"%Region.cut		
			#~ self.labelRegion = region.label.replace("< 2.4","< 1.4")

	class SignalLowMETFullEta(Region):
		cut = "nJets >= 3 && pt1 > 20 && pt2 > 20 && p4.M() > 20 && met > 100 && (%s)"%Region.cut
		#~ labelRegion = Region.labelRegion.replace("< 2.4","< 1.4")
		labelSubRegion = "N_{jets} #geq 3 E_{T}^{miss} > 100 GeV"			
		titel = "Low E_{T}^{miss} SR"
		latex = "Low \MET\ Signal Region"
		name = "SignalLowMETFullEta"
		logY = False
		dyPrediction = {
			"default":	( sum([48,10,3.3,6.3]), sqrt(sum([i**2 for i in [15,7.1,1.8,3.3]])),0),
			"RunAB":	( sum([28,5.6,1.9,3.5]), sqrt(sum([i**2 for i in [8.5,3.9,1.0,1.8]])),0),
			"RunC":	    ( sum([21,4.5,1.5,2.8]), sqrt(sum([i**2 for i in [6.3,3.2,0.8,1.5]])),0),
			}

		rMuE = Constants.Pt2020.RMuE
		rInOut = Constants.Pt2020.RInOut
		#~ def __init__(self,region):
			#~ self.cut =" weight*(pt1 > 20 && pt2 > 20 && abs(eta1)<1.4 && abs(eta2) < 1.4 && p4.M() > 20 && nJets >= 3  && met > 100 && (%s))"%Region.cut		
			#~ self.labelRegion = region.label.replace("< 2.4","< 1.4")	


	class DrellYan(Region):
		cut = "nJets == 2  &&  met < 100 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "N_{jets} == 2 E_{T}^{miss} < 100 GeV"			
		titel = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		name = "DYRegion"
		logY = True
		#~ def __init__(self,region):
			#~ self.cut = " weight*( nJets >= 2 && ht > 100 && met > 150 && (%s))"%region.cut	
			#~ labelRegion = region.label
				
	class Zpeak(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "60 GeV < m_{ll} < 120 GeV"			
		titel = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		name = "ZPeak"
		logY = True
		#~ def __init__(self,region):
			#~ self.cut = " weight*( p4.M() > 60 && p4.M() < 120 && (%s))"%region.cut		
	class ZpeakControl(Region):
		cut = "p4.M() > 60 && p4.M() < 120 && met < 50 && nJets >= 2 && (%s)"%Region.cut
		labelRegion = Region.labelRegion
		labelSubRegion = "#splitline{60 GeV < m_{ll} < 120 GeV}{N_{jets} >= 2 E_T^{miss} < 50 GeV}"			
		titel = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		name = "ZPeakControl"
		logY = True
		#~ def __init__(self,region):
			#~ self.cut = " weight*( p4.M() > 60 && p4.M() < 120 && (%s))"%region.cut		
		
		



	

def getRegion(name):
	if not name in dir(Regions):
		print "unknown region '%s, using Inclusive selection'"%name
		return Region
	elif name == "Region":
		return Region
	else:
		return getattr(Regions, name)
		
def getMassSelection(name):
	if not name in dir(theCuts.massCuts):
		print "unknown selection '%s, using existing selection'"%name
		return None
	else:
		return getattr(theCuts.massCuts, name)
	
def getOFScale():
	rmuePart = 0.5 * (Constants.Pt2010.RMuE.val + 1./Constants.Pt2010.RMuE.val)
	rmueErr = 0.5 * (1. - 1./Constants.Pt2010.RMuE.val**2)* Constants.Pt2010.RMuE.err*1./Constants.Pt2010.RMuE.val
	triggerPart = sqrt(Constants.Trigger.EffEE.val * Constants.Trigger.EffMuMu.val) * 1./ Constants.Trigger.EffEMu.val
	triggerErr = 0.05*1.22
	#	triggerErr =sqrt(sum([i**2 for i in [0.5/Constants.Trigger.EffEE.val, 0.5/Constants.Trigger.EffMuMu.val, 1./Constants.Trigger.EffEMu.val]]))
	result = rmuePart * triggerPart
	err = sqrt(sum([i**2 for i in [rmueErr, triggerErr]]))
	result = 1.02
	err = 0.07
	print rmuePart, triggerPart
	return result, err
	
class Plot:
	
	variable= "none"
	cuts	= "none"
	xaxis   = "none"
	yaxis	= "none"
	tree1 	= "none"
	tree2	= "none"
	nBins	= 0
	firstBin = 0
	lastBin = 0
	yMin 	= 0
	yMax	= 0 
	label = "none"
	label2 = "none"
	label3 = "none"
	filename = "none.pdf"
	log = False
	tree1 = "None"
	tree2 = "None"
	
	def __init__(self,variable,additionalCuts,binning = None, yRange = None,additionalName=None):
		self.variable=variable.variable
		self.cuts="weight*(%s)"
		self.xaxis=variable.labelX
		self.yaxis=variable.labelY
		self.nBins=variable.nBins
		self.firstBin=variable.xMin
		self.lastBin=variable.xMax
		self.yMin = 0.1
		self.yMax = 0
		self.label3="%s"
		self.filename=variable.name+"_%s"

		if len(additionalCuts) >0:
			for additionalCut in additionalCuts:
				self.cuts=self.cuts%(additionalCut.cut+"&& %s")
				self.label3 = self.label3%(additionalCut.label+" %s")
				self.filename = self.filename%(additionalCut.name+"_%s")
		if binning != None:
			self.nBins = binning[0]
			self.firstBin = binning[1]
			self.lastBin = binning [2]
			self.labelY = binning [3]
		if yRange != None:
			self.yMin = yRange[0]
			self.yMax = yRange[0]
		if additionalName != None:
			self.filename = self.filename%(additionalName+"_%s")
		self.filename = self.filename.replace("_%s","%s.pdf") 
		self.label3 = self.label3.replace("%s","")
	
	
	def clone(self,selection):
		print self.cuts
		tempPlot = Plot(theVariables.Met,[])
		if getMassSelection(selection) != None:
			tempPlot.cuts = "weight*(%s)"%(getMassSelection(selection).cut+"&& %s")
			tempPlot.overlayLabel = getMassSelection(selection).name
		else:
			tempPlot.cuts=self.cuts
			tempPlot.overlayLabel = "None"			
		tempPlot.variable=self.variable
		tempPlot.xaxis=self.xaxis
		tempPlot.yaxis=self.yaxis
		tempPlot.nBins=self.nBins
		tempPlot.firstBin=self.firstBin
		tempPlot.lastBin=self.lastBin
		tempPlot.yMin = 0.1
		tempPlot.yMax = 0
		tempPlot.label3="%s"
		tempPlot.filename=self.filename	
		return tempPlot	
	
	def addRegion(self,region):
		self.cuts = self.cuts%(region.cut+" %s")
		self.filename = region.name+"_"+self.filename
		self.label = region.labelRegion
		self.label2 = region.labelSubRegion
		self.regionName = region.name
	def addDilepton(self,dilepton):
		if dilepton == "SF":
			self.tree1 = "EE"
			self.tree2 = "MuMu"
		elif dilepton == "OF":
			self.tree1 = "EMu"
			self.tree2 = "None"
		else:		
			self.tree1 = dilepton
			self.tree2 = "None"		
	def cleanCuts(self):
		if self.variable == "met" or self.variable == "type1Met" or self.variable == "tcMet" or self.variable == "caloMet" or self.variable == "mht":
			cuts = self.cuts.split("&&")
			metCutUp = []
			metCutDown = [] 
			for cut in cuts:
				if "met >" in cut:
					metCutUp.append(cut)
				elif "met <" in cut:
					metCutDown.append(cut)
			for cut in metCutUp:
				self.cuts = self.cuts.replace(cut.split(")")[0],"")
			for cut in metCutDown:
				self.cuts = self.cuts.replace(cut,"")
			self.cuts = self.cuts.replace("&&)",")")
			self.cuts = self.cuts.replace("&& &&","&&")
			self.cuts = self.cuts.replace("&&&&","&&")
		if self.variable == "ht":
			cuts = self.cuts.split("&&")
			htCutUp = "" 
			htCutDown = "" 
			for cut in cuts:
				if "ht >" in cut:
					metCutUp = cut
				elif "ht <" in cut:
					metCutDown = cut
			self.cuts = self.cuts.replace(htCutUp,"")
			self.cuts = self.cuts.replace(htCutDown,"")
			self.cuts = self.cuts.replace("&& &&","&&")
			self.cuts = self.cuts.replace("&&&&","&&")			
		if self.variable == "nJets":
			cuts = self.cuts.split("&&")
			nJetsCutUp = [] 
			nJetsCutDown = [] 
			nJetsCutEqual = []
			for cut in cuts:
				if "nJets >" in cut:
					nJetsCutUp.append(cut)
				elif "nJets <" in cut:
					nJetsCutDown.append(cut)
				elif "nJets ==" in cut:
					nJetsCutEqual.append(cut)
			for cut in nJetsCutUp:
				if "weight" and "(((" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(((")
				elif "weight" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(")
				elif "(" in cut:
					self.cuts = self.cuts.replace(cut.split("(")[1],"")
				else:
					self.cuts = self.cuts.replace(cut,"")
			for cut in nJetsCutDown:
				if "weight" and "(((" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(((")
				elif "weight" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(")
				elif "(" in cut:
					self.cuts = self.cuts.replace(cut.split("(")[1],"")
				else:
					self.cuts = self.cuts.replace(cut,"")
			for cut in nJetsCutEqual:
				if "weight" and "(((" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(((")
				elif "weight" in cut:
					self.cuts = self.cuts.replace(cut,"weight*(")
				elif "(" in cut:
					self.cuts = self.cuts.replace(cut.split("(")[1],"")
				else:
					self.cuts = self.cuts.replace(cut,"")
					
			#~ if nJetsCutUp != "":
				#~ if "weight" in nJetsCutUp:
					#~ self.cuts = self.cuts.replace(nJetsCutUp,"weight*(")
				#~ else:
					#~ self.cuts = self.cuts.replace(nJetsCutUp,"")
			#~ if nJetsCutDown != "":
				#~ if "weight" in nJetsCutDown:
					#~ self.cuts = self.cuts.replace(nJetsCutDown,"weight*(")
				#~ else:
					#~ self.cuts = self.cuts.replace(nJetsCutDown,"")
			#~ if nJetsCutEqual != "":
				#~ if "weight" in nJetsCutEqual:
					#~ self.cuts = self.cuts.replace(nJetsCutEqual,"weight*(")
				#~ else:
					#~ self.cuts = self.cuts.replace(nJetsCutEqual,"")
			self.cuts = self.cuts.replace("&& &&","&&")
			self.cuts = self.cuts.replace("&&&&","&&")			
			self.cuts = self.cuts.replace("( &&","(")			
			self.cuts = self.cuts.replace("(&&","(")			
			
		
class thePlots:
	class METPlots:
		metPlot = Plot(theVariables.Met,[])
		metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
		metPlotZMass = Plot(theVariables.Met,[theCuts.massCuts.zMass])
		metPlotHighMass = Plot(theVariables.Met,[theCuts.massCuts.highMass])
		metPlotLowPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.lowPU])
		metPlotMidPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.midPU])
		metPlotHighPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.highPU])
		metPlot0Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.noJet])
		metPlot1Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.OneJet])
		metPlot2Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.TwoJet])
		metPlot3Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.ThreeJet])
		metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags])
		metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags])
		metPlotCentralBarrel = Plot(theVariables.Met,[theCuts.etaCuts.CentralBarrel])
		metPlotOuterBarrel = Plot(theVariables.Met,[theCuts.etaCuts.OuterBarrel])
		metPlotEndcap = Plot(theVariables.Met,[theCuts.etaCuts.Endcap])
		metPlotlowDR = Plot(theVariables.Met,[theCuts.dRCuts.lowDR])
		metPlotmidDR = Plot(theVariables.Met,[theCuts.dRCuts.midDR])
		metPlothighDR = Plot(theVariables.Met,[theCuts.dRCuts.highDR])
		metPlotType1 = Plot(theVariables.Type1Met,[])
		metPlotCalo = Plot(theVariables.CaloMet,[])
		metPlotTc = Plot(theVariables.TcMet,[])
		metPlotUncertaintyHighMET = Plot(theVariables.Met,[theCuts.htCuts.ht100,theCuts.nJetsCuts.geTwoJetCut])
		metPlotUncertaintyLowMET = Plot(theVariables.Met,[theCuts.nJetsCuts.geThreeJetCut])
	class METStudies:
		metPlotLowMass = Plot(theVariables.Met,[theCuts.massCuts.edgeMass])
		metPlotLowPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.lowPU,theCuts.massCuts.edgeMass])
		metPlotMidPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.midPU,theCuts.massCuts.edgeMass])
		metPlotHighPileUp = Plot(theVariables.Met,[theCuts.pileUpCuts.highPU,theCuts.massCuts.edgeMass])
		metPlot0Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.noJet,theCuts.massCuts.edgeMass])
		metPlot1Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.OneJet,theCuts.massCuts.edgeMass])
		metPlot2Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.TwoJet,theCuts.massCuts.edgeMass])
		metPlot3Jets = Plot(theVariables.Met,[theCuts.nJetsCuts.ThreeJet,theCuts.massCuts.edgeMass])
		metPlotnoBTags = Plot(theVariables.Met,[theCuts.bTags.noBTags,theCuts.massCuts.edgeMass])
		metPlotwithBTags = Plot(theVariables.Met,[theCuts.bTags.geOneBTags,theCuts.massCuts.edgeMass])
		metPlotCentralBarrel = Plot(theVariables.Met,[theCuts.etaCuts.CentralBarrel,theCuts.massCuts.edgeMass])
		metPlotOuterBarrel = Plot(theVariables.Met,[theCuts.etaCuts.OuterBarrel,theCuts.massCuts.edgeMass])
		metPlotEndcap = Plot(theVariables.Met,[theCuts.etaCuts.Endcap,theCuts.massCuts.edgeMass])
		metPlotlowDR = Plot(theVariables.Met,[theCuts.dRCuts.lowDR,theCuts.massCuts.edgeMass])
		metPlotmidDR = Plot(theVariables.Met,[theCuts.dRCuts.midDR,theCuts.massCuts.edgeMass])
		metPlothighDR = Plot(theVariables.Met,[theCuts.dRCuts.highDR,theCuts.massCuts.edgeMass])
		metPlotType1 = Plot(theVariables.Type1Met,[theCuts.massCuts.edgeMass])
		metPlotCalo = Plot(theVariables.CaloMet,[theCuts.massCuts.edgeMass])
		metPlotTc = Plot(theVariables.TcMet,[theCuts.massCuts.edgeMass])
		mhtPlotLowMass = Plot(theVariables.MHT,[theCuts.massCuts.edgeMass])		
		
	class htPlots:
		htPlot = Plot(theVariables.HT,[])		
		htPlotLowMass = Plot(theVariables.HT,[theCuts.massCuts.edgeMass])		
		htPlotHighMass = Plot(theVariables.HT,[theCuts.massCuts.highMass])	
		htPlotUntertaintyHighMET = Plot(theVariables.HT,[theCuts.metCuts.met150])	
		htPlotUntertaintyLowMET = Plot(theVariables.HT,[theCuts.metCuts.met100])
	class mhtPlots:
		mhtPlot = Plot(theVariables.MHT,[])
	class etaPlots:
		eta1Plot = Plot(theVariables.Eta1,[])		
		eta2Plot = Plot(theVariables.Eta2,[])
	class ptPlots:
		ptElePlot = Plot(theVariables.PtEle,[])		
		ptMuPlot = Plot(theVariables.PtMu,[])
		trailingPtPlot = Plot(theVariables.TrailingPt,[])
		leadingPtPlot = Plot(theVariables.LeadingPt,[])
		trailingPtPlotLowMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.edgeMass])
		leadingPtPlotLowMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.edgeMass])
		trailingPtPlotHighMass = Plot(theVariables.TrailingPt,[theCuts.massCuts.highMass])
		leadingPtPlotHighMass = Plot(theVariables.LeadingPt,[theCuts.massCuts.highMass])
	class mllPlots:
		mllPlot = Plot(theVariables.Mll,[])
		mllPlotLowMass = Plot(theVariables.Mll,[theCuts.massCuts.edgeMass])
		mllPlotHighMass = Plot(theVariables.Mll,[theCuts.massCuts.highMass])
		mllPlotZpeak = Plot(theVariables.Mll,[],binning = [30,60,120,"Events / 2 Gev"],additionalName = "ZPeak")
	class nJetsPlots:
		nJetsPlot = Plot(theVariables.nJets,[])
		nJetsPlotLowMass = Plot(theVariables.nJets,[theCuts.massCuts.edgeMass])
		nJetsPlotHighMass = Plot(theVariables.nJets,[theCuts.massCuts.highMass])
	class nBJetsPlots:
		nBJetsPlot = Plot(theVariables.nBJets,[])
		nBJetsPlotLowMass = Plot(theVariables.nBJets,[theCuts.massCuts.edgeMass])
		nBJetsPlotHighMass = Plot(theVariables.nBJets,[theCuts.massCuts.highMass])
	class deltaRPlots:
		deltaRPlot = Plot(theVariables.deltaR,[])
		deltaRPlotLowMass = Plot(theVariables.deltaR,[theCuts.massCuts.edgeMass])
		deltaRPlotHighMass = Plot(theVariables.deltaR,[theCuts.massCuts.highMass])
	class ptllPlots:
		ptllPlot = Plot(theVariables.Ptll,[])
		ptllPlotLowMass = Plot(theVariables.Ptll,[theCuts.massCuts.edgeMass])
		ptllPlotHighMass = Plot(theVariables.Ptll,[theCuts.massCuts.highMass])
	
				
		
	#~ class plotLists:
			

	#~ plots = [nJetsPlots.nJetsPlot,nJetsPlots.nJetsPlotLowMass,nJetsPlots.nJetsPlotHighMass,nBJetsPlots.nBJetsPlot,nBJetsPlots.nBJetsPlotLowMass,nBJetsPlots.nBJetsPlotHighMass,mllPlots.mllPlot,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	plots = [htPlots.htPlot]
	#~ plots = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass]#,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	#~ plots = [mllPlots.mllPlotHighMass,mllPlots.mllPlotLowMass]#,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]


	generalPlots = [nJetsPlots.nJetsPlot,nJetsPlots.nJetsPlotLowMass,nJetsPlots.nJetsPlotHighMass,nBJetsPlots.nBJetsPlot,nBJetsPlots.nBJetsPlotLowMass,nBJetsPlots.nBJetsPlotHighMass,mllPlots.mllPlot,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	#~ generalPlots = [nJetsPlots.nJetsPlot,nJetsPlots.nJetsPlotLowMass,nJetsPlots.nJetsPlotHighMass,nBJetsPlots.nBJetsPlot,nBJetsPlots.nBJetsPlotLowMass,nBJetsPlots.nBJetsPlotHighMass,mllPlots.mllPlot,htPlots.htPlot,htPlots.htPlotLowMass]#,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	#~ generalPlots = [htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	
	basicSet = [METPlots.metPlot,mllPlots.mllPlot,nJetsPlots.nJetsPlot,nBJetsPlots.nBJetsPlot,etaPlots.eta1Plot,etaPlots.eta2Plot,htPlots.htPlot]	
	anPlotsMetStudyPlotsInclusive = [METStudies.metPlot0Jets,METStudies.metPlot1Jets,METStudies.metPlot2Jets,METStudies.metPlot3Jets]				
	anPlotsMetStudyPlotsHighMET = [METStudies.metPlotLowPileUp,METStudies.metPlotMidPileUp,METStudies.metPlotHighPileUp,METStudies.metPlotCalo,METStudies.metPlotTc,METStudies.metPlotType1,METStudies.metPlotCentralBarrel,METStudies.metPlotOuterBarrel,METStudies.metPlotEndcap,METStudies.metPlothighDR,METStudies.metPlotmidDR,METStudies.metPlotlowDR,METStudies.mhtPlotLowMass]				

	anPlotsInclusive = [htPlots.htPlot,nJetsPlots.nJetsPlot,mllPlots.mllPlotZpeak,mllPlots.mllPlot]
#	anPlotsInclusiveEEMuMu = [mllPlots.mllPlotZpeak]
#	anPlotsEEMuMu = [mllPlots.mllPlot]
	anPlotsbTagControl = [nJetsPlots.nJetsPlot]
	anPlotsSignal = [METPlots.metPlot,mllPlots.mllPlot]
	anPlotsCompareTTbar = [METStudies.metPlotLowMass]
	
	pasPlotsInclusive = [nJetsPlots.nJetsPlot,nBJetsPlots.nBJetsPlot,mllPlots.mllPlot,htPlots.htPlot,METPlots.metPlot,ptPlots.leadingPtPlot,ptPlots.trailingPtPlot] 
	#~ pasPlotsInclusive = [ptPlots.leadingPtPlot,ptPlots.trailingPtPlot] 
	pasPlotsLowMET = [nJetsPlots.nJetsPlot,nJetsPlots.nJetsPlotLowMass,nJetsPlots.nJetsPlotHighMass,nBJetsPlots.nBJetsPlot,nBJetsPlots.nBJetsPlotLowMass,nBJetsPlots.nBJetsPlotHighMass,mllPlots.mllPlot,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	#~ pasPlotsLowMET = [ptPlots.leadingPtPlot,ptPlots.trailingPtPlot]
	pasPlotsHighMET = [nJetsPlots.nJetsPlot,nJetsPlots.nJetsPlotLowMass,nJetsPlots.nJetsPlotHighMass,nBJetsPlots.nBJetsPlot,nBJetsPlots.nBJetsPlotLowMass,nBJetsPlots.nBJetsPlotHighMass,mllPlots.mllPlot,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptPlots.leadingPtPlot,ptPlots.leadingPtPlotLowMass,ptPlots.leadingPtPlotHighMass,ptPlots.trailingPtPlot,ptPlots.trailingPtPlotLowMass,ptPlots.trailingPtPlotHighMass]
	#~ pasPlotsHighMET = [ptPlots.leadingPtPlot,ptPlots.trailingPtPlot]
	pasPlotsbTagControl = [nJetsPlots.nJetsPlot,nBJetsPlots.nBJetsPlot,mllPlots.mllPlot,htPlots.htPlot,METPlots.metPlot,ptPlots.leadingPtPlot,ptPlots.trailingPtPlot]
	pasPlotsCompareTTbarLowMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,deltaRPlots.deltaRPlot,deltaRPlots.deltaRPlotLowMass,deltaRPlots.deltaRPlotHighMass]
	pasPlotsCompareTTbarHighMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,deltaRPlots.deltaRPlot,deltaRPlots.deltaRPlotLowMass,deltaRPlots.deltaRPlotHighMass]
	#~ pasPlotsCompareTTbarLowMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass]
	#~ pasPlotsCompareTTbarHighMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass]
	pasPlotsSFvsOFHighMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptllPlots.ptllPlot,ptllPlots.ptllPlotLowMass,ptllPlots.ptllPlotHighMass,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,deltaRPlots.deltaRPlot,deltaRPlots.deltaRPlotLowMass,deltaRPlots.deltaRPlotHighMass]
	#~ pasPlotsSFvsOFHighMET = [METPlots.metPlotHighMass,ptllPlots.ptllPlot,ptllPlots.ptllPlotLowMass,ptllPlots.ptllPlotHighMass,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,deltaRPlots.deltaRPlot,deltaRPlots.deltaRPlotLowMass,deltaRPlots.deltaRPlotHighMass]
	pasPlotsSFvsOFLowMET = [METPlots.metPlot,METPlots.metPlotLowMass,METPlots.metPlotHighMass,ptllPlots.ptllPlot,ptllPlots.ptllPlotLowMass,ptllPlots.ptllPlotHighMass,htPlots.htPlot,htPlots.htPlotLowMass,htPlots.htPlotHighMass,deltaRPlots.deltaRPlot,deltaRPlots.deltaRPlotLowMass,deltaRPlots.deltaRPlotHighMass]
	
class Signals:
	class SUSY1:
		subprocesses = ["SUSY_CMSSM_4610_202_Summer12"]
		label 		 = "CMSSM 4610/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY2:
		subprocesses = ["SUSY_CMSSM_4500_188_Summer12"]
		label 		 = "CMSSM 4500/188"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+1
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY3:
		subprocesses = ["SUSY_CMSSM_4580_202_Summer12"]
		label 		 = "CMSSM 4580/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+2
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY4:
		subprocesses = ["SUSY_CMSSM_4640_202_Summer12"]
		label 		 = "CMSSM 4640/202"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+3
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
	class SUSY5:
		subprocesses = ["SUSY_CMSSM_4700_216_Summer12"]
		label 		 = "CMSSM 4700/216"
		fillcolor    = ROOT.kWhite
		linecolor    = ROOT.kRed+4
		uncertainty	 = 0.
		scaleFac     = 1.
		additionalSelection = None
		
class Backgrounds:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph_Summer12"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TTJets_SpinCorrelations:
		subprocesses = ["TTJets_MGDecays_madgraph_Summer12","TTJets_MGDecays_SemiLept_madgraph_Summer12","TTJets_MGDecays_FullHad_madgraph_Summer12"]
		label = "Madgraph t#bar{t} w/ SC"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
	class TT:
		subprocesses = ["TT_Powheg_Summer12_v2"] 
		label = "t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class TT_Dileptonic:
		subprocesses = ["TT_Dileptonic_Powheg_Summer12_v1"] 
		label = "Powheg t#bar{t} Dileptonic"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		#~ scaleFac     = 0.71
		additionalSelection = None
	class TT_MCatNLO:
		subprocesses = ["TT_MCatNLO_Summer12_v1"] 
		label = "MCatNLO t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack	
		uncertainty = 0.07
		scaleFac     = 1.0
		additionalSelection = None
		#~ scaleFac     = 0.71
	class Diboson:
		subprocesses = ["ZZJetsTo2L2Q_madgraph_Summer12","ZZJetsTo2L2Nu_madgraph_Summer12","ZZJetsTo4L_madgraph_Summer12","WZJetsTo3LNu_madgraph_Summer12","WZJetsTo2L2Q_madgraph_Summer12","WWJetsTo2L2Nu_madgraph_Summer12"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class Rare:
		subprocesses = ["WWWJets_madgraph_Summer12","WWGJets_madgraph_Summer12","WWZNoGstarJets_madgraph_Summer12","TTGJets_madgraph_Summer12","WZZNoGstar_madgraph_Summer12","TTWJets_madgraph_Summer12","TTZJets_madgraph_Summer12","TTWWJets_madgraph_Summer12"]
		label = "Other SM"
		fillcolor = 630
		linecolor = ROOT.kBlack
		uncertainty = 0.5
		scaleFac     = 1.	
		additionalSelection = None	
	class DrellYan:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "DY+jets (e^{+}e^{-},#mu^{+}#mu^{-})"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class DrellYanTauTau:
		subprocesses = ["AStar_madgraph_Summer12","ZJets_madgraph_Summer12"]
		label = "DY+jets (#tau#tau)"
		fillcolor = ROOT.kOrange
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class SingleTop:
		subprocesses = ["TBar_tWChannel_Powheg_Summer12","TBar_tChannel_Powheg_Summer12","TBar_sChannel_Powheg_Summer12","T_tWChannel_Powheg_Summer12","T_tChannel_Powheg_Summer12","T_sChannel_Powheg_Summer12"]
		label = "single-top"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None
class Backgrounds2011:
	
	class TTJets:
		subprocesses = ["TTJets_madgraph60M_Fall11"]
		label = "Madgraph t#bar{t}"
		fillcolor = 855
		linecolor = ROOT.kBlack
		uncertainty = 0.15
		scaleFac     = 1.0
		additionalSelection = None
	class Diboson:
		subprocesses = ["WWJets_madgraph_Fall11","WZJets_madgraph_Fall11","ZZJets_madgraph_Fall11"]
		label = "WW,WZ,ZZ"
		fillcolor = 920
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class DrellYan:
		subprocesses = ["AstarJets_madgraph_Summer11","ZJets_madgraph_Fall11"]
		label = "Z+jets"
		fillcolor = 401
		linecolor = ROOT.kBlack	
		uncertainty = 0.04
		scaleFac     = 1.	
		additionalSelection = None
	class SingleTop:
		subprocesses = ["Tbar_s_powheg_Fall11","Tbar_t_powheg_Fall11","Tbar_tWDR_powheg_Fall11","T_t_powheg_Fall11","T_s_powheg_Fall11","T_tWDR_powheg_Fall11"]
		label = "t/#bar{t}+jets"
		fillcolor = 854
		linecolor = ROOT.kBlack
		uncertainty = 0.06
		scaleFac     = 1.
		additionalSelection = None

class mainConfig:
	plotData = True
	plotMC	= True
	compareTTbar = False
	normalizeToData = False
	plotRatio = True
	plotSignal = False
	compare2011 = False
	compareSFvsOF = True
	compareEEvsMuMu = False
	compareSFvsOFFlavourSeperated = False
	useVectorTrees = False
	useTriggerEmulation = False 
	preselect = False
	produceReweighting = True
	plot2011 = False
	plot53X = False
	personalWork = False
	doTopReweighting = False
	
# Color definition
#==================
defineMyColors = {
        'Black' : (0, 0, 0),
        'White' : (255, 255, 255),
        'Red' : (255, 0, 0),
        'DarkRed' : (128, 0, 0),
        'Green' : (0, 255, 0),
        'Blue' : (0, 0, 255),
        'Yellow' : (255, 255, 0),
        'Orange' : (255, 128, 0),
        'DarkOrange' : (255, 64, 0),
        'Magenta' : (255, 0, 255),
        'KDEBlue' : (64, 137, 210),
        'Grey' : (128, 128, 128),
        'DarkGreen' : (0, 128, 0),
        'DarkSlateBlue' : (72, 61, 139),
        'Brown' : (70, 35, 10),

        'MyBlue' : (36, 72, 206),
        'MyDarkBlue' : (18, 36, 103),
        'MyGreen' : (70, 164, 60),
        'AnnBlueTitle' : (29, 47, 126),
        'AnnBlue' : (55, 100, 255),
#        'W11AnnBlue' : (0, 68, 204),
#        'W11AnnBlue' : (63, 122, 240),
    }


myColors = {
            'W11ttbar':  855,
            'W11singlet':  854,
            'W11ZLightJets':  401,
            'W11ZbJets':  400,
            'W11WJets':  842,
            'W11Diboson':  920,
            'W11AnnBlue': 856,
            'W11Rare':  630,
            }

