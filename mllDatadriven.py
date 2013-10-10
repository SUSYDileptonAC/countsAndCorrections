#!/usr/bin/env python
from ROOT import TColor
def getDY(trees, cut, var = "inv"):
	from src.histos import getSFHisto
	from ROOT import kYellow, kBlack
	result = getSFHisto(trees, cut, var)
	result.SetLineColor(TColor.GetColor("#006600"))
	result.SetFillColor(TColor.GetColor("#006600"))
	result.SetFillStyle(3002)
	result.SetLineStyle(2)
	return result

def getOF(trees, cut, var = "inv"):
	from src.histos import  getHisto
	from ROOT import kAzure, kBlack
	result = getHisto(trees["EMu"], cut, var)
	#~ result.SetFillColor(kAzure-4)
	result.SetLineColor(TColor.GetColor("#cc0066"))
	result.SetFillStyle(1001)
	result.SetLineWidth(2)
	return result


	
def getOFSignal(trees, cut,lineColour = 0, var = "inv",name = "signal"):
	
	from src.histos import  getHisto
	from ROOT import kRed, kWhite
	result = getHisto(trees["EMu"], cut, var,name)
	result.SetFillColor(kWhite)
	#~ result.SetFillStyle(1001)
	result.SetLineColor(lineColour)
	return result

def getSF(trees, cut, var = "inv"):
	from src.histos import getSFHisto
	from ROOT import kBlack
	result = getSFHisto(trees, cut, var)
	result.SetLineColor(kBlack)
	result.SetLineWidth(2)
	result.SetMarkerColor(kBlack)
	result.SetMarkerStyle(8)
	result.SetMarkerSize(1)
	return result
	
def getDilepton(trees, cut,dilepton, var = "inv"):
	from src.histos import getHisto
	from ROOT import kBlack
	result = getHisto(trees[dilepton], cut, var)
	result.SetLineColor(kBlack)
	result.SetLineWidth(2)
	result.SetMarkerColor(kBlack)
	result.SetMarkerStyle(8)
	result.SetMarkerSize(1)
	return result
	
def getSFSignal(trees, cut ,lineColour=0, var = "inv",name = "signal"):
	
	from src.histos import getSFHisto
	from ROOT import kRed
	result = getSFHisto(trees, cut, var,name)
	result.SetLineColor(lineColour)
	result.SetLineWidth(2)
	result.SetMarkerColor(lineColour)
	result.SetMarkerStyle(8)
	result.SetMarkerSize(1)
	return result

def getSplitCorrection(rmue,rmueErr,dilepton):
	from src.defs import Constants
	result = 0.
	resultErr = 0.
	if dilepton == "EE":
		result = 1./(2*rmue)*(Constants.Trigger.EffEE.val/Constants.Trigger.EffEMu.val)
		resultErr = (2*(rmueErr/rmue)**2+(0.071)**2)**0.5
	elif dilepton == "MuMu":
		result =(1.*rmue/2)*(Constants.Trigger.EffMuMu.val/Constants.Trigger.EffEMu.val)
		resultErr = (2*(rmueErr/rmue)**2+(0.071**2))**0.5
	return result,resultErr

def getLines(yMin,yMax, xPos = [70.,81., 101]):
	from ROOT import TLine, kGray
	result = []
	for x in xPos:
		result.append(TLine(x, yMin, x,yMax))
		result[-1].SetLineWidth(1)
		result[-1].SetLineColor(kGray+2)
		result[-1].SetLineStyle(2)
	return result



def drawDiffPad(resPad, diffHisto, maxY) :
	from ROOT import TLine, kGray, kBlue
	#~ axHisto = resPad.DrawFrame(diffHisto.GetXaxis().GetXmin(), maxY[0], diffHisto.GetXaxis().GetXmax(), maxY[1])
	axHisto = resPad.DrawFrame(diffHisto.GetXaxis().GetXmin(), maxY[0], 305, maxY[1])
	zeroLine = TLine(diffHisto.GetXaxis().GetXmin(), 1., 305,1.)
	zeroLine.SetLineWidth(1)
	zeroLine.SetLineColor(kBlue)
	zeroLine.SetLineStyle(2)
	zeroLine.Draw()

	#~ axHisto.GetYaxis().SetNdivisions(7)#int(sum(maxY)), 0, 2)
	#~ axHisto.SetTitleOffset(0.4, "Y")
	#~ axHisto.SetTitleSize(0.05, "XY")
	#~ axHisto.SetTitleOffset(1.1, "Y")
	#~ axHisto.SetYTitle("data/pred")
	#~ axHisto.SetXTitle("m_{ll} [GeV]")
	#~ axHisto.GetXaxis().CenterTitle(True)
	#~ axHisto.GetXaxis().SetLabelOffset(0.007)
	#~ axHisto.GetYaxis().SetLabelOffset(0.007)

	axHisto.GetXaxis().SetTitle("m_{ll} [GeV]");
	axHisto.GetXaxis().CenterTitle(True);
	axHisto.GetXaxis().SetLabelFont(42);
	axHisto.GetXaxis().SetLabelOffset(0.007);
	axHisto.GetXaxis().SetLabelSize(0.1104);
	axHisto.GetXaxis().SetTitleSize(0.138);
	axHisto.GetXaxis().SetTitleFont(42);
	axHisto.GetYaxis().SetTitle("data/pred");
	axHisto.GetYaxis().CenterTitle(True);
	axHisto.GetYaxis().SetNdivisions(-502);
	axHisto.GetYaxis().SetLabelFont(42);
	axHisto.GetYaxis().SetLabelOffset(0.007);
	axHisto.GetYaxis().SetLabelSize(0.1104);
	axHisto.GetYaxis().SetTitleSize(0.138);
	axHisto.GetYaxis().SetTitleOffset(0.4);
	axHisto.GetYaxis().SetTitleFont(42);
	
	#~ axHisto.GetYaxis().SetLabelSize(0.15)

	return zeroLine, diffHisto

def setOverflowBin(histo,xMax,binWidth):	
	#~ print xMax
	from ROOT import TH1F
	#~ print histo.GetXaxis().GetXmax()
	overflow = histo.Integral()- histo.Integral(histo.FindBin(histo.GetXaxis().GetXmin()),histo.FindBin(xMax-1))
	#~ print histo.Integral(histo.FindBin(histo.GetXaxis().GetXmin()),histo.FindBin(histo.GetXaxis().GetXmax()))
	#~ print histo.GetEntries()
	#~ print histo.Integral(histo.FindBin(histo.GetXaxis().GetXmin()),histo.FindBin(xMax))
	#~ print overflow

	histo.SetBinContent(histo.FindBin(xMax-1),histo.GetBinContent(histo.FindBin(xMax-1))+overflow)
	


def getSysErrorGraph(hist, scale, errorList=None,additionalHist=None):
	from ROOT import TGraphErrors, kBlack
	from array import array
	from math import sqrt
	nBins = hist.GetXaxis().GetNbins()
	
	vals = []
	yVals = []
	errs = []
	widths = []
	for i in range(1, nBins+1):
		vals.append( hist.GetXaxis().GetBinCenter(i))
		if additionalHist==None: 
			yVals.append( hist.GetBinContent(i)) 
		else:
			yVals.append(hist.GetBinContent(i)+additionalHist.GetBinContent(i))
		errs.append( sqrt(hist.GetBinContent(i)*scale**2+hist.GetBinContent(i)))
		widths.append( hist.GetXaxis().GetBinWidth(i) * 0.5)
	if not errorList == None:
		assert len(errorList) == nBins, "errorList incopatible %s != %s"%(nBins, len(errorList))
		errs = [ sqrt(err**2+ errorList[i]**2) for i, err in enumerate(errs) ]
	result = TGraphErrors(nBins, array("f", vals), array("f",yVals), array("f", widths),array("f", errs) )
	#~ result.SetFillColor(hist.GetFillColor())
	#~ result.SetLineColor(hist.GetFillColor())
	result.SetFillColor(TColor.GetColor("#2E9AFE"))
	result.SetLineColor(kBlack)
	return result, errs
	
def getSysErrorBand(hist, scale, errorList=None,DY=False,ofHist=None):
	from ROOT import TColor
	from ROOT import TGraphErrors
	from array import array
	from math import sqrt
	#~ nBins = hist.GetXaxis().GetNbins()
	nBins = hist.FindBin(305)
	
	vals = []
	errs = []
	widths = []
	xVals  = []
	print scale
	if DY==True:
		for i in range(0, nBins):
			vals.append( 1.)
			if i <=13 and ofHist.GetBinContent(i) > 0:  
				errs.append(scale[1]+scale[0]*hist.GetBinContent(i)/ofHist.GetBinContent(i))
			elif ofHist.GetBinContent(i) > 0:
				errs.append(scale[0]*hist.GetBinContent(i)/ofHist.GetBinContent(i))
			else:
				errs.append(0)
			widths.append( hist.GetXaxis().GetBinWidth(i) * 0.5)
			xVals.append(17.5+i*5)
	else:
		for i in range(0, nBins):
			vals.append( 1.) 
			errs.append(scale)
			widths.append( hist.GetXaxis().GetBinWidth(i) * 0.5)
			xVals.append(17.5+i*5)

	if not errorList == None:
		assert len(errorList) == nBins, "errorList incopatible %s != %s"%(nBins, len(errorList))
		errs = [ sqrt(err**2+ errorList[i]**2) for i, err in enumerate(errs) ]
	result = TGraphErrors(nBins, array("f",xVals), array("f", vals), array("f", widths),array("f", errs) )
	#~ result.SetFillColor(hist.GetFillColor())
	#~ result.SetLineColor(hist.GetFillColor())
	result.SetFillColor(TColor.GetColor("#ff9933"))
	result.SetLineColor(TColor.GetColor("#ff9933"))
	return result, errs


def DrawPlot(sfLeptons,ofLeptons,dyLineShape,ofErrors,binWidth,regionName,subcutName,maxY,plotSignal,relDYError,relDYErrorPeak,relDYErrorLowMass,ofScaleError,lumi,dilepton=""):

	from src.Styles import tdrStyle
	from ROOT import TLegend, TCanvas, THStack, TLatex, TPad, kBlue

	leg = TLegend(0.52, 0.51, 0.89, 0.89,"","brNDC")
	leg.SetFillColor(10)
	leg.SetLineColor(10)
	leg.SetShadowColor(0)
	leg.SetBorderSize(1)
	from ROOT import TH1F,kWhite
	legendHistDing = TH1F()
	legendHistDing.SetFillColor(kWhite)
	if regionName =="SignalNonRectInclusive":
		leg.AddEntry(legendHistDing,"Signal Inclusive Signal Region %s"%dilepton,"h")
	elif regionName =="SignalNonRectCentral":
		leg.AddEntry(legendHistDing,"Signal Central Signal Region %s"%dilepton,"h")
	elif regionName =="SignalNonRectForward":
		leg.AddEntry(legendHistDing,"Forward Signal Region %s"%dilepton,"h")
	leg.AddEntry(sfLeptons,"Data","PL")
	leg.AddEntry(ofLeptons, "Total Backgrounds","l")
	leg.AddEntry(dyLineShape,"DY (data-driven)", "f")
	leg.AddEntry(ofErrors,"Total uncert.", "f")
	

	if plotSignal:
		for signal in theSignals:
			signalTrees={
				"MuMu": readTreeFromFile(signal["filename"], "MuMu", preselection),
				"EMu": readTreeFromFile(signal["filename"], "EMu", preselection),
				"EE": readTreeFromFile(signal["filename"], "EE", preselection),		
			}
			print signal["lineColour"]
			print signal["crossSection"]
			print signal["nEvents"]
	
			ofSignalLeptons = getOFSignal(signalTrees, cuts["default"],signal["lineColour"])	
			ofSignalLeptons.Scale(ofScale)
			ofSignalLeptons.Scale(lumi[subcutName]*signal["crossSection"]/signal["nEvents"])
			ofSignalLeptons.SetTitle(signal["label"])
			sfSignalLeptons = getSFSignal(signalTrees, cuts["default"],signal["lineColour"])
			sfSignalLeptons.Scale(lumi[subcutName]*signal["crossSection"]/signal["nEvents"])	
			sfSignalLeptons.SetTitle(signal["label"])
			print lumi[subcutName]*signal["crossSection"]/signal["nEvents"]
			sfSignalLeptons.Add(ofSignalLeptons.Clone(),-1)
			print sfSignalLeptons.Integral(sfSignalLeptons.FindBin(20),sfSignalLeptons.FindBin(70))	
			sfSignalLeptons.Add(ofLeptons.Clone())
			sfSignalLeptons.Add(dyLineShape.Clone())
			leg.AddEntry(sfSignalLeptons.Clone(),signal["label"],"l")
			signalhistsSF.append(sfSignalLeptons.Clone())
			diffhistsSF.append(sfSignalLeptons.Clone())
			signalhistsOF.append(ofSignalLeptons.Clone())				
	
	
	style = tdrStyle()
	
	#~ canv = TCanvas("canv", "",800,int(800*1.25))
	canv = TCanvas("canv", "",0,0,600,750)
	canv.SetTopMargin(0.08)
	canv.SetBottomMargin(0.013)
	canv.SetLeftMargin(0.013)
	canv.SetRightMargin(0.05)
	pad = TPad("main", "main", 0.0, 0.289, 1, 1)

	pad.SetNumber(1)
	pad.Draw()
	#~ pad.UseCurrentStyle()
	pad.SetBottomMargin(0.02)
	canv.cd()
	resPad = TPad("residual", "residual", 0, 0.0, 1, 0.289)
	resPad.SetNumber(2)

	resPad.Draw()
	
	#~ resPad.UseCurrentStyle()
	resPad.SetBottomMargin(0.3)	
	
	labelPad = TPad("label", "label", 0.0, 0.0, 1, 1)
	#~ labelPad.UseCurrentStyle()
	labelPad.SetNumber(3)
	#~ labelPad.Draw()
	labelPad.UseCurrentStyle()			
	pad.cd()
	
	frame = pad.DrawFrame(20,0,305,maxY,";;events / %d GeV"%binWidth)
	frame.GetYaxis().CenterTitle(True)
	predictions = THStack("predictions","predictions")
	predictions.Add(dyLineShape, "hist")
	predictions.Add(ofLeptons, "hist")
	#~ predictions.SetLineWidth(2)

	predictionSum = dyLineShape.Clone("predictionSum")
	predictionSum.Add(ofLeptons)
	ofErrors.Draw("2,SAME")
	predictions.Draw("SAMEhist")
	lines = getLines(0, maxY)
	for line in lines:
		line.Draw()
	sfLeptons.Draw("P SAME")
	if plotSignal:
		for sigHist in signalhistsSF:			
			sigHist.Draw("histSAME")
	


	leg.Draw()

	#~ latex = TLatex()
	#~ latex.SetTextSize(0.042)
	#~ latex.SetTextFont(42)
	#~ latex.SetNDC(True)
	#~ latex.DrawLatex(0.13, 0.95, "CMS Preliminary,    #sqrt{s} = 8 TeV,     #scale[0.6]{#int}Ldt = %.1f fb^{-1}"%(lumi[subcutName]*0.001))

	text2 =TLatex(0.973,0.02,"High E_{T}^{miss} selection")
	text2.SetNDC()
	text2.SetTextAlign(32)
	text2.SetTextColor(14)
	text2.SetTextFont(42)
	text2.SetTextSize(0.03)
	text2.SetTextAngle(270)
	#~ text2.Draw()		
	
	pad.cd()
	pad.RedrawAxis()

	#residuals = RatioGraph(sfLeptons, predictionSum,title="Data / Pred.")
	#residuals.addErrorBySize(ofScaleError, ofScaleError, add=False, color = kBlue-9 )
	#residuals.draw(resPad, yMin = 0., yMax = 2., addChi2=False)
	resPad.cd()
	maxDiff = [0., 2.]
	difference = sfLeptons.Clone("difference")
	
	difference.Divide(predictionSum)
	
	zeroline, diffPadThings = drawDiffPad(resPad, difference, maxDiff)

	dyErrorsBand, errorListBand = getSysErrorBand(dyLineShape, [relDYErrorPeak,relDYErrorLowMass],DY=True,ofHist=ofLeptons)
	ofErrorsBand, errorListBand = getSysErrorBand(ofLeptons, ofScaleError,errorListBand)
	
	ofErrorsBand.Draw("2,SAME")
	#~ dyErrorsBand.Draw("2 SAME")
	
	zeroline.Draw("SAME")
	difference.Draw("SAME0")
	leg2 = TLegend(0.52, 0.55, 0.89, 0.89, "")
	leg2.SetFillColor(10)
	leg2.SetLineColor(10)
	leg2.SetShadowColor(0)
	leg2.SetBorderSize(1)

	import ROOT
	if plotSignal:
		for sigHist in diffhistsSF:
					
			sigHist.Add(predictionSum,-1.)
			sigHist.Draw("SAMEhist")
			leg2.AddEntry(sigHist,"%s OF Subtracted"%(sigHist.GetTitle(),),"l")
	
	#~ leg2.Draw()
	resLines = getLines(maxDiff[0], maxDiff[1])
	for line in resLines:
		line.Draw()
	canv.cd()
	from ROOT import TPaveText,TText

	pt = TPaveText(0.23,0.95,0.77,1,"blNDC")
	pt.SetBorderSize(0)
	pt.SetFillColor(0)
	pt.SetFillStyle(4000)
	pt.SetTextFont(42)
	pt.SetTextSize(0.042)
	text = TText()
	text = pt.AddText("CMS Preliminary, #sqrt{s} = 8 TeV, #scale[0.6]{#int}Ldt = %.1f fb^{-1}"%(lumi[subcutName]*0.001))
	pt.Draw()
	
	#~ print regionName
	#~ print subcutName
	#~ print canv.GetWh(), canv.GetWw()
	canv.SetWindowSize(600,750)
	#~ print canv.GetWh(), canv.GetWw()
	if dilepton != "":
		canv.Print("fig/mll_Datadriven_%s_%s_%s.pdf"%(regionName, subcutName,dilepton))
	else:	
		canv.Print("fig/mll_Datadriven_%s_%s.pdf"%(regionName, subcutName))
	pad.Delete()
	resPad.Delete()



def main():
	
	from sys import argv
	from src.defs import getRegion, getOFScale, Signals
	from src.datasets import readTreeFromFile
	from src.histos import getBinWidth
	from src.Styles import tdrStyle
	from src.ratios import RatioGraph
	from math import sqrt

	from ROOT import TLegend, TCanvas, THStack, TLatex, TPad, kBlue
	plotSignal = False
	theSignals = []
	diffhistsSF = []
	signalhistsSF = []
	signalhistsOF = []
	if argv[4] == "Signal":
		plotSignal = True
		theSignals = Signals.theSignals 
		print "Plotting Signals!"
		

	regionName = argv[2]
	subcutName =  argv[3]
	lumi = { "default": 9200,
			 "RunAB": 5230,
			 "RunC": 4100
		}

 	
	maxY = 90
	
	if regionName == "SignalNonRectInclusive":
		maxY = 180.
	if regionName == "SignalNonRectCentral":
		maxY = 150.
	if regionName == "SignalNonRectForward":
		maxY = 120.
		#~ maxDiff = [-30, 50.]
	#~ if regionName == "SignalHighMET_SingleLepton":
		#~ maxY = 80.
		#~ maxDiff = [-30, 50.]
	#~ if regionName == "SignalHighMETpt2010":
		#~ maxY = 110.
		#~ maxDiff = [-30, 50.]
	#~ if regionName == "SignalLowMET":
		#~ maxY = 120.
		#~ maxDiff = [-30, 50.]


	
	region = getRegion(regionName)
	dyRegion = getRegion("DrellYan")
	
	cuts = {"default": region.cut,
			"RunAB": "%s && runNr <= 196531"%region.cut,
			"RunC":"%s && runNr > 196531 && (runNr < 198049 || runNr > 198522) &&  runNr < 201678"%region.cut,
			"SingleLepton": region.cut,
		}

	print cuts[subcutName]
	if "SingleLepton" in regionName  or "METPD" in regionName:
		path = region.getPath(argv[1])
	else:
		path = argv[1]
		
	print path
	preselection = "nJets >= 2"
	if regionName =="SignalHighMET_SingleLepton":
		trees = {
			"MuMu": readTreeFromFile(path, "MuMu", preselection,SingleLepton=True),
			"EMu": readTreeFromFile(path, "EMu", preselection,SingleLepton=True),
			"EE": readTreeFromFile(path, "EE", preselection,SingleLepton=True),
			}
	else:
		trees = {
			"MuMu": readTreeFromFile(path, "MuMu", preselection),
			"EMu": readTreeFromFile(path, "EMu", preselection),
			"EE": readTreeFromFile(path, "EE", preselection),
			}
	binWidth = getBinWidth("inv")	

	ofLeptons = getOF(trees, cuts[subcutName])
	
	ofScale = region.R_SFOF.val
	ofScaleError = region.R_SFOF.err
	
	ofLeptonsEE = ofLeptons.Clone("ofLeptonsEE")
	ofLeptonsMuMu = ofLeptons.Clone("ofLeptonsMuMu")
	
	print ofScale, ofScaleError
	
	ofLeptons.Scale(ofScale)
	setOverflowBin(ofLeptons,305,binWidth)
	
		

	dyLineShape = getDY(trees, dyRegion.cut)
	dyLineShape.Scale(region.dyPrediction[subcutName][0]*1./dyLineShape.Integral(0, dyLineShape.GetXaxis().GetNbins()+1))
	setOverflowBin(dyLineShape,305,binWidth)
	sfLeptons = getSF(trees, cuts[subcutName])
	setOverflowBin(sfLeptons,305,binWidth)
	
	eeLeptons = getDilepton(trees,cuts[subcutName],"EE")
	setOverflowBin(eeLeptons,305,binWidth)
	print region.rMuE.val,region.rMuE.err,region.R_SFOFTrig.val,region.R_SFOFTrig.err	
	eeScale = region.R_EEOF.val
	eeScaleError = region.R_EEOF.err/region.R_EEOF.val 
	ofLeptonsEE.Scale(eeScale)
	setOverflowBin(ofLeptonsEE,305,binWidth)	
	
	mmLeptons = getDilepton(trees,cuts[subcutName],"MuMu")
	setOverflowBin(mmLeptons,305,binWidth)	
	mmScale = region.R_MMOF.val
	mmScaleError = region.R_MMOF.err/region.R_MMOF.val
	ofLeptonsMuMu.Scale(mmScale)
	setOverflowBin(ofLeptonsMuMu,305,binWidth)	
	
	
	Rinout =  region.rInOut.val
	if region.dyPrediction[subcutName][0] > 0:
		relDYError = sqrt(region.dyPrediction[subcutName][1]**2 + region.dyPrediction[subcutName][2]**2) * 1./ region.dyPrediction[subcutName][0]
		relDYErrorPeak = sqrt(region.dyPrediction[subcutName][1]**2 + region.dyPrediction[subcutName][2]**2) * 1./region.dyPrediction[subcutName][0]
		relDYErrorLowMass = sqrt((sqrt(region.dyPrediction[subcutName][1]**2 + region.dyPrediction[subcutName][2]**2)*Rinout+(0.25*Rinout*region.dyPrediction[subcutName][0])**2)) * (region.dyPrediction[subcutName][0]*Rinout/ofLeptons.Integral(ofLeptons.FindBin(15),ofLeptons.FindBin(70)))
	else:
		relDYError = 0
		relDYErrorPeak = 0
		relDYErrorLowMass = 0
	if regionName == "SignalNonRectCentral" or regionName == "SignalNonRectForward":
		relDYErrorEE = sqrt(region.dyPrediction["EE"][1]**2 + region.dyPrediction["EE"][2]**2) * 1./ region.dyPrediction["EE"][0]
		relDYErrorPeakEE = sqrt(region.dyPrediction["EE"][1]**2 + region.dyPrediction["EE"][2]**2) * 1./region.dyPrediction["EE"][0]
		relDYErrorLowMassEE = sqrt((sqrt(region.dyPrediction["EE"][1]**2 + region.dyPrediction["EE"][2]**2)*Rinout+(0.25*Rinout*region.dyPrediction["EE"][0])**2)) * (region.dyPrediction["EE"][0]*Rinout/ofLeptons.Integral(ofLeptons.FindBin(15),ofLeptons.FindBin(70)))		
		relDYErrorMM = sqrt(region.dyPrediction["MM"][1]**2 + region.dyPrediction["MM"][2]**2) * 1./ region.dyPrediction["MM"][0]
		relDYErrorPeakMM = sqrt(region.dyPrediction["MM"][1]**2 + region.dyPrediction["MM"][2]**2) * 1./region.dyPrediction["MM"][0]
		relDYErrorLowMassMM = sqrt((sqrt(region.dyPrediction["MM"][1]**2 + region.dyPrediction["MM"][2]**2)*Rinout+(0.25*Rinout*region.dyPrediction["MM"][0])**2)) * (region.dyPrediction["MM"][0]*Rinout/ofLeptons.Integral(ofLeptons.FindBin(15),ofLeptons.FindBin(70)))		
	
	else:
		relDYErrorEE = relDYError
		relDYErrorPeakEE = relDYErrorPeak
		relDYErrorLowMassEE = relDYErrorLowMass		
		relDYErrorMM = relDYError
		relDYErrorPeakMM = relDYErrorPeak
		relDYErrorLowMassMM = relDYErrorLowMass		
	dyErrors, errorList = getSysErrorGraph(dyLineShape, relDYError)
	dyErrorsEE, errorListEE = getSysErrorGraph(dyLineShape, relDYErrorEE)
	dyErrorsMM, errorListMM = getSysErrorGraph(dyLineShape, relDYErrorMM)
	print ofScaleError, eeScaleError, mmScaleError
	ofErrors, errorListOF = getSysErrorGraph(ofLeptons, ofScaleError, errorList,dyLineShape)
	ofErrorsEE, errorListEE = getSysErrorGraph(ofLeptonsEE, eeScaleError, errorListEE,dyLineShape)
	ofErrorsMM, errorListMM = getSysErrorGraph(ofLeptonsMuMu, mmScaleError, errorListMM,dyLineShape)


	DrawPlot(sfLeptons,ofLeptons,dyLineShape,ofErrors,binWidth,regionName,subcutName,maxY,plotSignal,relDYError,relDYErrorPeak,relDYErrorLowMass,ofScaleError,lumi)
	DrawPlot(eeLeptons,ofLeptonsEE,dyLineShape,ofErrorsEE,binWidth,regionName,subcutName,maxY,plotSignal,relDYErrorEE,relDYErrorPeakEE,relDYErrorLowMassEE,eeScaleError,lumi,dilepton="EE")
	DrawPlot(mmLeptons,ofLeptonsMuMu,dyLineShape,ofErrorsMM,binWidth,regionName,subcutName,maxY,plotSignal,relDYErrorMM,relDYErrorPeakMM,relDYErrorLowMassMM,mmScaleError,lumi,dilepton="MuMu")
	

main()
