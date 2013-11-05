from math import sqrt
import ROOT
from ROOT import TMath



	
class Signals:
	
	CMSSM_4610_202 = {
	"filename" : "/media/data/DATA/sw532v0470/sw532v0470.processed.SUSY_CMSSM_4610_202_Summer12.root",
	"crossSection" : 2.63,
	"nEvents" : 50000,
	"lineColour" : 628,
	"label"		: "CMSSM 4610/202",
	
	}

	
	theSignals = [CMSSM_4610_202]
		




class Constant:
	val = 0.
	err = 0.
	
class Constants:
	class Trigger:
		class EffEE(Constant):
			val = 0.970
			err = 0.970 * 0.05
		class EffEMu(Constant):
			val = 0.943
			err = 0.943 * 0.05

		class EffMuMu(Constant):
			val = 0.964
			err = 0.964 * 0.05
		class Correction:
			class Inclusive(Constant):
				val = 1.0141201251122918
				err = 0.067*1.0141201251122918
			class Central(Constant):
				val = 1.01
				err = 0.07
			class Forward(Constant):
				val = 1.04
				err = 0.10

	class Pt2010:## Wrong numbers, redo!
		class RInOut:
			class Inclusive(Constant):
				val =0.069
				err =0.069*0.25
			class Central(Constant):
				val =0.072
				err =0.072*0.25
			class Forward(Constant):
				val =0.063
				err =0.063*0.25
		class RMuE:
			class Inclusive(Constant):
				val =1.144
				err =1.144*0.1
			class Central(Constant):
				val =1.101
				err =1.101*0.1
			class Forward(Constant):
				val =1.209
				err =1.209*0.15		
		
	class Pt2020:
		class RInOut:
			class Inclusive(Constant):
				val =0.069
				err =0.069*0.25
			class Central(Constant):
				val =0.071
				err =0.071*0.25
			class Forward(Constant):
				val =0.066
				err =0.066*0.25
		class RMuE:
			class Inclusive(Constant):
				val =1.144
				err =1.144*0.1
			class Central(Constant):
				val =1.101
				err =1.101*0.1
			class Forward(Constant):
				val =1.209
				err =1.209*0.15
	class R_SFOF:
		class Inclusive(Constant):
			val = 1.02
			err = 0.07
		class Central(Constant):
			val = 1.01
			err = 0.05
		class Forward(Constant):
			val = 1.02
			err = 0.10
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_EEOF:
		class Inclusive(Constant):
			val = 0.47
			err = 0.03
		class Central(Constant):
			val = 0.47
			err = 0.03
		class Forward(Constant):
			val = 0.43
			err = 0.06
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_MMOF:
		class Inclusive(Constant):
			val = 0.54
			err = 0.05
		class Central(Constant):
			val = 0.54
			err = 0.04
		class Forward(Constant):
			val = 0.57
			err = 0.08
		class Control(
		Constant):
			val = 1.0
			err = 0.0
			
			

class Region:
	cut = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20  && !(runNr >= 198049 && runNr <= 198522) && runNr <= 201678 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cut2010 = "chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 15  && !(runNr >= 198049 && runNr <= 198522) && runNr < 201678 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cut3020 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 20 ) || (pt2 > 30 && pt1 > 20 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20  && !(runNr >= 198049 && runNr <= 198522) && runNr < 201678 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cut3010 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 10 ) || (pt2 > 30 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20  && !(runNr >= 198049 && runNr <= 198522) && runNr < 201678 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	cut3030 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 30 ) || (pt2 > 30 && pt1 > 30 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20  && !(runNr >= 198049 && runNr <= 198522) && runNr < 201678 && !(runNr == 195649 && lumiSec == 49 && eventNr == 75858433) && !(runNr == 195749 && lumiSec == 108 && eventNr == 216906941)"
	title = "everything"
	latex = "everything"
	dyPrediction = {}
	rMuE = Constants.Pt2020.RMuE
	rInOut = Constants.Pt2020.RInOut
	color = ROOT.kBlack
	@staticmethod
	def getPath(path): return path


class Regions:
	class SignalHighMET(Region):
		cut = " nJets >= 2 && ht > 100 && met > 150 && (%s)"%Region.cut
		title = "High E_{T}^{miss} SR"
		latex = "High \MET\ Signal Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( 49.7, 11.1 ,0,0),
			"SingleLetpon":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalNonRectInclusive(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100)) && (%s)"%Region.cut
		title = "NonRect  SR"
		latex = "NonRect Signal Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( 100, 0,0),
			"SingleLetpon":	(100,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalNonRectCentral(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100)) && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "NonRect  SR Barrel"
		latex = "NonRect Signal Region Barrel"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central		
		dyPrediction = {
			"default":	( 49.7, 11.1 ,0,0),
			"SingleLetpon":	(80,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"EE": (28.6,6.2,0),
			"MuMu": (23.6,6.1,0)			
			}
		rarePrediction = {
			"default":	( 1.2, 0.7,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0.7,0.4,0),
			"EE": (0.6,0.3,0)			
			}
		color = ROOT.kAzure-4
	class SignalNonRectForward(Region):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		title = "NonRect  SR Forward"
		latex = "NonRect Signal Region Forward"
		rMuE = Constants.Pt2020.RMuE.Forward
		rInOut = Constants.Pt2020.RInOut.Forward
		R_SFOF = Constants.R_SFOF.Forward
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 22.3, 5.4 ,0,0),
			"SingleLetpon":	(20,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"EE": ( 11.5,2.7,0),
			"MuMu": (12.5,3.3,0)			
			}
		rarePrediction = {
			"default":	( 0.3, 0.2,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0.2,0.1,0),
			"EE": (0.1,0.1,0)			
			}			
		color = ROOT.kAzure-4
	class SignalHighMETLowNJetsCentral(Region):
		cut = "nJets == 2 && met > 150  && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "HighMETLowNJets  SR Barrel"
		latex = "HighMETLowNJets Region Barrel"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalHighMETLowNJetsForward(Region):
		cut = "nJets == 2 && met > 150  && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		title = "HighMETLowNJets  SR Forward"
		latex = "HighMETLowNJets Signal Region Forward"
		rMuE = Constants.Pt2020.RMuE.Forward
		rInOut = Constants.Pt2020.RInOut.Forward
		R_SFOF = Constants.R_SFOF.Forward
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalHighMETHighNJetsCentral(Region):
		cut = "nJets >= 3 && met > 150  && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "HighMETHighNJets  SR Barrel"
		latex = "HighMETHighNJets Region Barrel"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalHighMETHighNJetsForward(Region):
		cut = "nJets >= 3 && met > 150  && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		title = "HighMETHighNJets  SR Forward"
		latex = "HighMETHighNJets Signal Region Forward"
		rMuE = Constants.Pt2020.RMuE.Forward
		rInOut = Constants.Pt2020.RInOut.Forward
		R_SFOF = Constants.R_SFOF.Forward
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalLowMETHighNJetsCentral(Region):
		cut = "nJets >= 3 &&  met > 100 && met < 150  && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "LowMETHighNJets  SR Barrel"
		latex = "LowMETHighNJets Region Barrel"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalLowMETHighNJetsForward(Region):
		cut = "nJets >= 3 && met > 100 &&  met < 150  && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		title = "LowMETHighNJets  SR Forward"
		latex = "LowMETHighNJets Signal Region Forward"
		rMuE = Constants.Pt2020.RMuE.Forward
		rInOut = Constants.Pt2020.RInOut.Forward
		R_SFOF = Constants.R_SFOF.Forward
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 30, 0,0),
			"SingleLetpon":	(30,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class BarrelHighMET(Region):
		cut = " nJets >= 2 && ht > 100 && met > 150 && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "High E_{T}^{miss} SR"
		latex = "High \MET\ Signal Region"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central		
		dyPrediction = {
			"default":	( 28.91, 6.72,0),
			"SingleLetpon":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4		
	class Pt2010HighMET(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 &&  (%s)"%Region.cut2010
		title = "High E_{T}^{miss} SR p_{T} > 20(10) GeV"
		latex = "High \MET\ Signal Region p_{T} > 20(10) GeV"
		rMuE = Constants.Pt2010.RMuE.Inclusive
		rInOut = Constants.Pt2010.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( sum([32, 16, 7.7, 5.1]), sqrt(sum([i**2 for i in [10, 11, 4.1, 2.8]])),0),
			"RunAB":	( sum([14, 8.9, 4.3, 2.8]), sqrt(sum([i**2 for i in [4.2, 6.3, 2.3, 1.5]])),0),
			"RunC":	( sum([18, 7.1, 3.4, 2.3]), sqrt(sum([i**2 for i in [6.0, 5.1, 1.8, 1.2]])),0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class Pt3010HighMET(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 &&  (%s)"%Region.cut3010
		title = "High E_{T}^{miss} SR p_{T} > 30(10) GeV"
		latex = "High \MET\ Signal Region p_{T} > 30(10) GeV"
		rMuE = Constants.Pt2010.RMuE.Inclusive
		rInOut = Constants.Pt2010.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( 0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
		
	class Pt3020HighMET(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 &&  (%s)"%Region.cut3020
		title = "High E_{T}^{miss} SR p_{T} > 30(20) GeV"
		latex = "High \MET\ Signal Region p_{T} > 30(20) GeV"
		rMuE = Constants.Pt2010.RMuE.Inclusive
		rInOut = Constants.Pt2010.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( 0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
		
	class Pt3030HighMET(Region):
		cut = "nJets >= 2 && ht > 100 && met > 150 &&  (%s)"%Region.cut3030
		title = "High E_{T}^{miss} SR p_{T} > 30 GeV"
		latex = "High \MET\ Signal Region p_{T} > 30 GeV"
		rMuE = Constants.Pt2010.RMuE.Inclusive
		rInOut = Constants.Pt2010.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
			"default":	( 0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4


	class SignalHighMETControl2011(Region):
		cut = " nJets >= 2 && ht > 100 && ht <= 300 && met > 150 && (%s)"%Region.cut
		title = "High E_{T}^{miss} SR"
		latex = "High \MET\ 2011 Controll Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {
	
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
	class SignalHighMET2011(Region):
		cut = " nJets >= 2 && ht > 300 && ht < 300 && met > 150 && (%s)"%Region.cut
		title = "High E_{T}^{miss} SR"
		latex = "High \MET\ 2011 Signal Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {

			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kAzure-4
		
	class SignalNonRectInclusive_METPD(SignalNonRectInclusive):
		title = "High E_{T}^{miss} SR (MET PD)"
		latex = "High \MET\ Signal Region (MET PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
	class SignalNonRectCentral_METPD(SignalNonRectCentral):
		title = "High E_{T}^{miss} SR (MET PD)"
		latex = "High \MET\ Signal Region (MET PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
	class SignalNonRectForward_METPD(SignalNonRectForward):
		title = "High E_{T}^{miss} SR (MET PD)"
		latex = "High \MET\ Signal Region (MET PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
		
	class SignalHighMET_METPD(SignalHighMET):
		title = "High E_{T}^{miss} SR (MET PD)"
		latex = "High \MET\ Signal Region (MET PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
	class BarrelHighMET_METPD(BarrelHighMET):
		title = "Central High E_{T}^{miss} SR (MET PD)"
		latex = "Central High \MET\ Signal Region (MET PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
		
	class SignalHighMET_SingleLepton(SignalHighMET):
		title = "High E_{T}^{miss} SR (Single Lepton PD)"
		latex = "High \MET\ Signal Region (SingleLepton PD)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_SingleLepton.root")
	
	class ControlHighMET(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && (%s)"%Region.cut
		title = "High E_{T}^{miss} CR"
		latex = "High \MET\ Control Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {

			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kGray
		
	class ControlCentral(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "Central CR"
		latex = "Central Control Region"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Control
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central
		dyPrediction = {
			"default":	( 0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kGray
		
	class ControlForward(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut
		title = "Forward CR"
		latex = "Forward Control Region"
		rMuE = Constants.Pt2020.RMuE.Forward
		rInOut = Constants.Pt2020.RInOut.Forward
		R_SFOF = Constants.R_SFOF.Control
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_EEOF = Constants.R_EEOF.Forward
		R_MMOF = Constants.R_MMOF.Forward		
		dyPrediction = {
			"default":	( 0,0,0),
			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kGray
		
	class ControlInclusive(Region):
		cut = "nJets == 2  && 100 <  met && met < 150 && (%s)"%Region.cut
		title = "Inclusive CR"
		latex = "Inclusive Control Region"
		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Control
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		dyPrediction = {

			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				
		color = ROOT.kGray

	class SignalLowMET(Region):
		cut = "pt1 > 20 && pt2 > 20 && p4.M() > 20 && nJets >= 3  && met > 100 && abs(eta1) < 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut
		title = "Low E_{T}^{miss} SR"
		latex = "Low \MET\ Signal Region"
		#~ dyPrediction = {
			#~ "default":	( sum([48,10,3.3,6.3]), sqrt(sum([i**2 for i in [15,7.1,1.8,3.3]])),0),
			#~ "RunAB":	( sum([28,5.6,1.9,3.5]), sqrt(sum([i**2 for i in [8.5,3.9,1.0,1.8]])),0),
			#~ "RunC":	    ( sum([21,4.5,1.5,2.8]), sqrt(sum([i**2 for i in [6.3,3.2,0.8,1.5]])),0),
			#~ }
		dyPrediction = {
			"default":	( 37.52, 7.79,0),


			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				

		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central		
		color = ROOT.kRed-2
		
	class SignalLowMETFullEta(Region):
		cut = "pt1 > 20 && pt2 > 20 && p4.M() > 20 && nJets >= 3  && met > 100 && abs(eta1) < 2.4 && abs(eta2) < 2.4 && (%s)"%Region.cut
		title = "Low E_{T}^{miss} SR"
		latex = "Low \MET\ Signal Region"
		#~ dyPrediction = {
			#~ "default":	( sum([48,10,3.3,6.3]), sqrt(sum([i**2 for i in [15,7.1,1.8,3.3]])),0),
			#~ "RunAB":	( sum([28,5.6,1.9,3.5]), sqrt(sum([i**2 for i in [8.5,3.9,1.0,1.8]])),0),
			#~ "RunC":	    ( sum([21,4.5,1.5,2.8]), sqrt(sum([i**2 for i in [6.3,3.2,0.8,1.5]])),0),
			#~ }
		dyPrediction = {
			"default":	( 53.33, 10.39,0),

			}
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}				

		rMuE = Constants.Pt2020.RMuE.Inclusive
		rInOut = Constants.Pt2020.RInOut.Inclusive
		R_SFOF = Constants.R_SFOF.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_EEOF = Constants.R_EEOF.Inclusive
		R_MMOF = Constants.R_MMOF.Inclusive		
		color = ROOT.kRed-2		

	class SignalLowMET_METPD(SignalLowMET):
		title = "Low E_{T}^{miss} SR (MET PD)"
		latex = "Low \MET\ Signal Region (MET PD)"
		color = ROOT.kRed-1
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
	class SignalLowMETFullEta_METPD(SignalLowMETFullEta):
		title = "Low E_{T}^{miss} Inclusive SR (MET PD)"
		latex = "Low \MET\ Signal Inclusive Region (MET PD)"
		color = ROOT.kRed-1
		@staticmethod
		def getPath(path): return path.replace(".root", "_METPD.root")
		
	class SignalLowMET_SingleLepton(SignalLowMET):
		title = "Low E_{T}^{miss} SR (SingleLepton PD)"
		latex = "Low \MET\ Signal Region (SingleLepton PD)"
		color = ROOT.kRed-1
		@staticmethod
		def getPath(path): return path.replace(".root", "_SingleLepton.root")
		
	class ControlLowMET(Region):
		cut = "nJets <= 2  && 100 <  met && met < 150 && (%s)"%Region.cut
		title = "Low E_{T}^{miss} CR"
		latex = "Low \MET\ Control Region"
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOF = Constants.R_SFOF.Control
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_EEOF = Constants.R_EEOF.Central
		R_MMOF = Constants.R_MMOF.Central
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}			

	class DrellYan(Region):
		cut = "nJets == 2  &&  met < 100 && (%s)"%Region.cut
		title = "Drell-Yan Enhanced"
		latex = "Drell-Yan Enhanced"
		
	class TwoJets(Region):
		cut = "nJets >= 2  && (%s)"%Region.cut
		title = "More than 2 Jets"
		latex = "More than 2 Jets"
	

def getRegion(name):
	if not name in dir(Regions):
		print "unknown region '%s, using SignalHighMET'"%name
		return Regions.SignalHighMET
	return getattr(Regions, name)
	
def getOFScale(region):
	rmuePart = 0.5 * (region.rMuE.val + 1./region.rMuE.val)
	rmueErr = 0.5 * (1. - 1./region.rMuE.val**2)* region.rMuE.err*1./region.rMuE.val
	triggerPart = sqrt(Constants.Trigger.EffEE.val * Constants.Trigger.EffMuMu.val) * 1./ Constants.Trigger.EffEMu.val
	triggerErr = 0.05*1.23 #error propagation gives relative error * sqrt(1/4+1/4+1)
		#	triggerErr =sqrt(sum([i**2 for i in [0.5/Constants.Trigger.EffEE.val, 0.5/Constants.Trigger.EffMuMu.val, 1./Constants.Trigger.EffEMu.val]]))
	#~ result = rmuePart * triggerPart
	result = 1.02 #Common scale factor with ETH guys
	#~ print result
	
	#~ err = sqrt(sum([i**2 for i in [rmueErr, triggerErr]]))
	err = 0.07 #Common uncertainty with ETH guys 
	#~ print err
	return result, err
	
