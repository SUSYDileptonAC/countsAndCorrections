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
	class R_SFOF_A:
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
	class R_EEOF_A:
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
	class R_MMOF_A:
		class Inclusive(Constant):
			val = 0.54
			err = 0.05
		class Central(Constant):
			val = 0.54
			err = 0.04
		class Forward(Constant):
			val = 0.57
			err = 0.08
		class Control(Constant):
			val = 1.0
			err = 0.0
			
	class R_SFOF_B:
		class Inclusive(Constant):
			val = 1.00
			err = 0.05
		class Central(Constant):
			val = 1.00
			err = 0.05
		class Forward(Constant):
			val = 1.18
			err = 0.09
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_EEOF_B:
		class Inclusive(Constant):
			val = 0.43
			err = 0.03
		class Central(Constant):
			val = 0.43
			err = 0.03
		class Forward(Constant):
			val = 0.53
			err = 0.07
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_MMOF_B:
		class Inclusive(Constant):
			val = 0.56
			err = 0.04
		class Central(Constant):
			val = 0.56
			err = 0.04
		class Forward(Constant):
			val = 0.70
			err = 0.09
		class Control(Constant):
			val = 1.0
			err = 0.0
			
	class R_SFOF_AB:
		class Inclusive(Constant):
			val = 1.00
			err = 0.04
		class Central(Constant):
			val = 1.00
			err = 0.04
		class Forward(Constant):
			val = 1.13
			err = 0.08
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_EEOF_AB:
		class Inclusive(Constant):
			val = 0.45
			err = 0.03
		class Central(Constant):
			val = 0.45
			err = 0.03
		class Forward(Constant):
			val = 0.49
			err = 0.06
		class Control(Constant):
			val = 1.0
			err = 0.0
	class R_MMOF_AB:
		class Inclusive(Constant):
			val = 0.55
			err = 0.03
		class Central(Constant):
			val = 0.55
			err = 0.03
		class Forward(Constant):
			val = 0.63
			err = 0.07
		class Control(Constant):
			val = 1.0
			err = 0.0
			
			
class Constants2011(Constants):
	class Trigger:
		class EffEE(Constant):
			val = 1.0
			err = 0.02
			
		class EffEMu(Constant):
			val = 0.95
			err = 0.02

		class EffMuMu(Constant):
			val = 0.90
			err = 0.02
				#not actually used?
	class R_SFOF:
		class Inclusive(Constant):
							val = 1.0204
							err = 0.0319
		class Central(Constant):
							val = 1.0204
							err = 0.0319
		class Forward(Constant):
							val = 1.0241
							err = 0.0549	
	class R_EEOF:
		class Inclusive(Constant):
							val = 0.4192
							err = 0.0360
		class Central(Constant):
							val = 0.4192
							err = 0.0360
		class Forward(Constant):
							val = 0.3644
							err = 0.0639	
	class R_MMOF:
		class Inclusive(Constant):
							val = 0.6149
							err = 0.0507
		class Central(Constant):
							val = 0.6149
							err = 0.0507
		class Forward(Constant):
							val = 0.6349
							err = 0.1033	
	class Pt2020:
				#still 2012 numbers
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
				#just using inclusive numbers from SUS-11-011
		class RMuE:
			class Inclusive(Constant):
				val =1.11
				err =0.05
			class Central(Constant):
				val =1.11
				err =0.05
			class Forward(Constant):
				val =1.11
				err =0.05
			

class Region(object):
	cut = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20  "
	cut2010 = "chargeProduct < 0 && ((pt1 > 20 && pt2 > 10 ) || (pt2 > 20 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 15 "
	cut3020 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 20 ) || (pt2 > 30 && pt1 > 20 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20"
	cut3010 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 10 ) || (pt2 > 30 && pt1 > 10 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20"
	cut3030 = "chargeProduct < 0 && ((pt1 > 30 && pt2 > 30 ) || (pt2 > 30 && pt1 > 30 )) && abs(eta1)<2.4  && abs(eta2) < 2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && deltaR > 0.3 && p4.M() > 20"
	cut2011 = "chargeProduct < 0 && pt1 > 20 && pt2 > 20 && abs(eta1)<2.4 && ((abs(eta1) < 1.4 || abs(eta1) > 1.6) && (abs(eta2) < 1.4 || abs(eta2) > 1.6)) && abs(eta2) < 2.4 && deltaR > 0.3 && p4.M() > 20 && jet1pt > 40 && jet2pt > 40"
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive	
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central			
		dyPrediction = {
			"BlockA":	( 49.7, 11.1 ,0,0),
			"BlockB":	( 61, 18.96 ,0,0),
			"default":	( 110.7, 22 ,0,0),			
			"SingleLetpon":	(80,0,0),
			"EEBlockA": (28.6,6.2,0),
			"MuMuBlockA": (23.6,6.1,0),			
			"EEBlockB": (29.38,11.2475,0),
			"MuMuBlockB": (30.96,12.236265430269155,0),			
			"EEdefault": (48,13,0),
			"MuMudefault": (45,14,0),			
			"BTaggedBlockA": (6,3.5,0),
			"BVetoBlockA": (32,8,0),			
			"BTaggedBlockB": (22,12.1655,4.01123), 
			"BVetoBlockB": (38,10.3923,6.33719),	
			"BTaggeddefault": (28,13,0),
			"BVetodefault": (70,14,0)			
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
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_SFOF_A = Constants.R_SFOF_A.Forward
		R_EEOF_A = Constants.R_EEOF_A.Forward
		R_MMOF_A = Constants.R_MMOF_A.Forward		
		R_SFOF_B = Constants.R_SFOF_B.Forward
		R_EEOF_B = Constants.R_EEOF_B.Forward
		R_MMOF_B = Constants.R_MMOF_B.Forward		
		R_SFOF_AB = Constants.R_SFOF_AB.Forward
		R_EEOF_AB = Constants.R_EEOF_AB.Forward
		R_MMOF_AB = Constants.R_MMOF_AB.Forward		
		dyPrediction = {
			"BlockA":	( 22.3, 5.4 ,0,0),
			"BlockB":	(-4.16, 7.434793095238091 ,0,0),
			"default":	(18.1, 9.2 ,0,0),
			"SingleLetpon":	(20,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"EEBlockA": ( 11.5,2.7,0),
			"MuMuBlockA": (12.5,3.3,0),			
			"EEBlockB": (-0.36,4.410488656827042,0),
			"MuMuBlockB": (-4.4,4.658410892707941,0),			
			"EEdefault": (11.1,5.2,0),
			"MuMudefault": (8.1,5.7,0)						
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central			
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
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_SFOF_A = Constants.R_SFOF_A.Forward
		R_EEOF_A = Constants.R_EEOF_A.Forward
		R_MMOF_A = Constants.R_MMOF_A.Forward		
		R_SFOF_B = Constants.R_SFOF_B.Forward
		R_EEOF_B = Constants.R_EEOF_B.Forward
		R_MMOF_B = Constants.R_MMOF_B.Forward		
		R_SFOF_AB = Constants.R_SFOF_AB.Forward
		R_EEOF_AB = Constants.R_EEOF_AB.Forward
		R_MMOF_AB = Constants.R_MMOF_AB.Forward		
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central		
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
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_SFOF_A = Constants.R_SFOF_A.Forward
		R_EEOF_A = Constants.R_EEOF_A.Forward
		R_MMOF_A = Constants.R_MMOF_A.Forward		
		R_SFOF_B = Constants.R_SFOF_B.Forward
		R_EEOF_B = Constants.R_EEOF_B.Forward
		R_MMOF_B = Constants.R_MMOF_B.Forward		
		R_SFOF_AB = Constants.R_SFOF_AB.Forward
		R_EEOF_AB = Constants.R_EEOF_AB.Forward
		R_MMOF_AB = Constants.R_MMOF_AB.Forward		
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central		
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
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_SFOF_A = Constants.R_SFOF_A.Forward
		R_EEOF_A = Constants.R_EEOF_A.Forward
		R_MMOF_A = Constants.R_MMOF_A.Forward		
		R_SFOF_B = Constants.R_SFOF_B.Forward
		R_EEOF_B = Constants.R_EEOF_B.Forward
		R_MMOF_B = Constants.R_MMOF_B.Forward		
		R_SFOF_AB = Constants.R_SFOF_AB.Forward
		R_EEOF_AB = Constants.R_EEOF_AB.Forward
		R_MMOF_AB = Constants.R_MMOF_AB.Forward		
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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


#	class SignalControl2011(Region):
#		cut = " nJets >= 2 && ht > 100 && ht <= 300 && met > 150 && (%s)"%Region.cut
#		title = "High E_{T}^{miss} SR"
#		latex = "High \MET\ 2011 Controll Region"
#		rMuE = Constants.Pt2020.RMuE.Inclusive
#		rInOut = Constants.Pt2020.RInOut.Inclusive
#		R_SFOF = Constants.R_SFOF.Inclusive
#		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
#		R_EEOF = Constants.R_EEOF.Inclusive
#		R_MMOF = Constants.R_MMOF.Inclusive		
#		dyPrediction = {
#	
#			}
#		rarePrediction = {
#			"default":	( 0, 0,0),
#			"SingleLetpon":	(0,0,0),
#			"RunAB": (0,0,0),
#			"RunC": (0,0,0),
#			"MuMu": (0,0,0),
#			"EE": (0,0,0)			
#			}				
#		color = ROOT.kAzure-4
#	class SignalHighMET2011(Region):
#		cut = " nJets >= 2 && ht > 300 && ht < 300 && met > 150 && (%s)"%Region.cut
#		title = "High E_{T}^{miss} SR"
#		latex = "High \MET\ 2011 Signal Region"
#		rMuE = Constants.Pt2020.RMuE.Inclusive
#		rInOut = Constants.Pt2020.RInOut.Inclusive
#		R_SFOF = Constants.R_SFOF.Inclusive
#		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
#		R_EEOF = Constants.R_EEOF.Inclusive
#		R_MMOF = Constants.R_MMOF.Inclusive		
#		dyPrediction = {
#
#			}
#		rarePrediction = {
#			"default":	( 0, 0,0),
#			"SingleLetpon":	(0,0,0),
#			"RunAB": (0,0,0),
#			"RunC": (0,0,0),
#			"MuMu": (0,0,0),
#			"EE": (0,0,0)			
#			}				
#		color = ROOT.kAzure-4
		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Control
		R_EEOF_A = Constants.R_EEOF_A.Control
		R_MMOF_A = Constants.R_MMOF_A.Control		
		R_SFOF_B = Constants.R_SFOF_B.Control
		R_EEOF_B = Constants.R_EEOF_B.Control
		R_MMOF_B = Constants.R_MMOF_B.Control		
		R_SFOF_AB = Constants.R_SFOF_AB.Control
		R_EEOF_AB = Constants.R_EEOF_AB.Control
		R_MMOF_AB = Constants.R_MMOF_AB.Control		
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
		R_SFOFTrig = Constants.Trigger.Correction.Forward
		R_SFOF_A = Constants.R_SFOF_A.Control
		R_EEOF_A = Constants.R_EEOF_A.Control
		R_MMOF_A = Constants.R_MMOF_A.Control		
		R_SFOF_B = Constants.R_SFOF_B.Control
		R_EEOF_B = Constants.R_EEOF_B.Control
		R_MMOF_B = Constants.R_MMOF_B.Control		
		R_SFOF_AB = Constants.R_SFOF_AB.Control
		R_EEOF_AB = Constants.R_EEOF_AB.Control
		R_MMOF_AB = Constants.R_MMOF_AB.Control			
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Control
		R_EEOF_A = Constants.R_EEOF_A.Control
		R_MMOF_A = Constants.R_MMOF_A.Control		
		R_SFOF_B = Constants.R_SFOF_B.Control
		R_EEOF_B = Constants.R_EEOF_B.Control
		R_MMOF_B = Constants.R_MMOF_B.Control		
		R_SFOF_AB = Constants.R_SFOF_AB.Control
		R_EEOF_AB = Constants.R_EEOF_AB.Control
		R_MMOF_AB = Constants.R_MMOF_AB.Control		
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

	class SignalNonRectInclusive_2011(SignalNonRectInclusive):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100 && jet3pt > 40)) && (%s)"%Region.cut2011
		title = "Inclusive SR (2011)"
		latex = "Inclusive Signal Region (2011)"
#		R_SFOFTrig = Constants2011.Trigger.Correction.Inclusive
		R_SFOF = Constants2011.R_SFOF.Inclusive
		R_EEOF = Constants2011.R_EEOF.Inclusive
		R_MMOF = Constants2011.R_MMOF.Inclusive
		dyPrediction = {}
		rarePrediction = {"default":	( 0, 0,0),}
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")
	class SignalNonRectCentral_2011(SignalNonRectCentral):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100 && jet3pt > 40)) && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut2011
		title = "Central SR (2011)"
		latex = "Central Signal Region (2011)"
		R_SFOF = Constants2011.R_SFOF.Central
		R_EEOF = Constants2011.R_EEOF.Central
		R_MMOF = Constants2011.R_MMOF.Central
		dyPrediction = {}
		rarePrediction = {"default":	( 0, 0,0),}
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")
	class SignalNonRectForward_2011(SignalNonRectForward):
		cut = "((nJets >= 2 && met > 150) || (nJets >=3 && met > 100 && jet3pt > 40)) && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut2011
		title = "Forward SR (2011)"
		latex = "Forward Signal Region (2011)"
		R_SFOF = Constants2011.R_SFOF.Forward
		R_EEOF = Constants2011.R_EEOF.Forward
		R_MMOF = Constants2011.R_MMOF.Forward
		dyPrediction = {}
		rarePrediction = {"default":	( 0, 0,0),}
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")
	class ControlInclusive_2011(ControlInclusive):
		cut = "nJets == 2  && 100 <  met && met < 150 && (%s)"%Region.cut2011
		title = "Inclusive CR (2011)"
		latex = "Inclusive Control Region (2011)"
		R_SFOF = Constants2011.R_SFOF.Inclusive
		R_EEOF = Constants2011.R_EEOF.Inclusive
		R_MMOF = Constants2011.R_MMOF.Inclusive
		dyPrediction = {}
		rarePrediction = {"default":	( 0, 0,0),}
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")
	class ControlCentral_2011(ControlCentral):
		cut = "nJets == 2  && 100 <  met && met < 150 && abs(eta1)< 1.4 && abs(eta2) < 1.4 && (%s)"%Region.cut2011
		R_SFOF = Constants2011.R_SFOF.Central
		R_EEOF = Constants2011.R_EEOF.Central
		R_MMOF = Constants2011.R_EEOF.Central
		dyPrediction = {}
		rarePrediction = {"default":	( 0, 0,0),}
		title = "Central CR (2011)"
		latex = "Central Control Region (2011)"
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")
	class ControlForward_2011(ControlForward):
		cut = "nJets == 2  && 100 <  met && met < 150 && 1.6 <= TMath::Max(abs(eta1),abs(eta2)) && (%s)"%Region.cut2011
		title = "Forward CR (2011)"
		latex = "Forward Control Region (2011)"
		R_SFOF = Constants2011.R_SFOF.Forward
		R_EEOF = Constants2011.R_EEOF.Forward
		R_MMOF = Constants2011.R_EEOF.Forward
		dyPrediction = {}
		rarePrediction = {}
		color = ROOT.kAzure-2
		@staticmethod
		def getPath(path): return path.replace(".root", "_2011.root").replace("sw532v0474", "sw532v0471")

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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central		
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
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOFTrig = Constants.Trigger.Correction.Inclusive
		R_SFOF_A = Constants.R_SFOF_A.Inclusive
		R_EEOF_A = Constants.R_EEOF_A.Inclusive
		R_MMOF_A = Constants.R_MMOF_A.Inclusive		
		R_SFOF_B = Constants.R_SFOF_B.Inclusive
		R_EEOF_B = Constants.R_EEOF_B.Inclusive
		R_MMOF_B = Constants.R_MMOF_B.Inclusive		
		R_SFOF_AB = Constants.R_SFOF_AB.Inclusive
		R_EEOF_AB = Constants.R_EEOF_AB.Inclusive
		R_MMOF_AB = Constants.R_MMOF_AB.Inclusive		
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
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Control
		R_EEOF_A = Constants.R_EEOF_A.Control
		R_MMOF_A = Constants.R_MMOF_A.Control		
		R_SFOF_B = Constants.R_SFOF_B.Control
		R_EEOF_B = Constants.R_EEOF_B.Control
		R_MMOF_B = Constants.R_MMOF_B.Control		
		R_SFOF_AB = Constants.R_SFOF_AB.Control
		R_EEOF_AB = Constants.R_EEOF_AB.Control
		R_MMOF_AB = Constants.R_MMOF_AB.Control	
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
		rMuE = Constants.Pt2020.RMuE.Central
		rInOut = Constants.Pt2020.RInOut.Central
		R_SFOFTrig = Constants.Trigger.Correction.Central
		R_SFOF_A = Constants.R_SFOF_A.Central
		R_EEOF_A = Constants.R_EEOF_A.Central
		R_MMOF_A = Constants.R_MMOF_A.Central		
		R_SFOF_B = Constants.R_SFOF_B.Central
		R_EEOF_B = Constants.R_EEOF_B.Central
		R_MMOF_B = Constants.R_MMOF_B.Central		
		R_SFOF_AB = Constants.R_SFOF_AB.Central
		R_EEOF_AB = Constants.R_EEOF_AB.Central
		R_MMOF_AB = Constants.R_MMOF_AB.Central		
		rarePrediction = {
			"default":	( 0, 0,0),
			"SingleLetpon":	(0,0,0),
			"RunAB": (0,0,0),
			"RunC": (0,0,0),
			"MuMu": (0,0,0),
			"EE": (0,0,0)			
			}	
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
	
