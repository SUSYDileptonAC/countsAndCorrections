#!/usr/bin/env python

def loadShapePickles(regionName, subcutName, shape = "GT", path = "../EdgeFitter/shelves"):
	import os
	import pickle
	from math import sqrt
	from src.defs import getRegion
	region = getRegion(regionName)
	print "test"
	if  "Run" in subcutName:
		regionName += "_"+ subcutName
	elif not subcutName == "default":
		regionName = regionName.replace("Signal", subcutName)
		regionName = regionName.replace("Barrel", subcutName+"Barrel")
		regionName = regionName.replace("Control", subcutName+"Control")
	picklePaths = {
		"nS":"edgefit-%s-%sSFOS-nS.pkl",
		"nSUncert":"edgefit-%s-%sSFOS-nSerror.pkl",
		"nB":"edgefit-%s-%sSFOS-nB.pkl",
		"nBUncert":"edgefit-%s-%sSFOS-nBerror.pkl",
		"nZ":"edgefit-%s-%sSFOS-nZ.pkl",
		"nZUncert":"edgefit-%s-%sSFOS-nZerror.pkl",
		"chi2":"edgefit-%s-%sSFOS-chi2.pkl",
		"nPar":"edgefit-%s-%sSFOS-nPar.pkl",
		}
	result = {}
	for varName, template in picklePaths.iteritems():
		pklPath = os.path.join(path, template%(regionName, shape))
		result[varName] = "--"
		if os.path.exists(pklPath):
			pklFile = open(pklPath, "r")
			result[varName] = pickle.load(pklFile)
			pklFile.close()
	if subcutName in region.dyPrediction:
		if region.dyPrediction[subcutName][0] > 0.:
			print subcutName
			print regionName
			result["nZ"] = region.dyPrediction[subcutName][0]
			result["nZSysUncert"] = region.dyPrediction[subcutName][1]
			result["nZStatUncert"] = region.dyPrediction[subcutName][2]
			result["nZUncert"] = sqrt(sum([i**2 for i in [result["nZStatUncert"], result["nZSysUncert"]]]))		
	if not result["nZ"] == "--":
		result["nCont"] = result["nZ"] * region.rInOut.val
		dyPredRelError = result["nZUncert"] * 1./result["nZ"]
#		if not region.dyPrediction == 0:
#			dyPredRelError = region.dyPredictionErr * 1./region.dyPrediction
#			result["nCont"] = region.dyPrediction * region.rInOut.val
		result["nContUncert"] = sqrt( (region.rInOut.err * 1./region.rInOut.val)**2 + (dyPredRelError)**2) * result["nCont"] 
		result["nCont"] = region.rInOut.val * result["nZ"]
		result["nContUncert"] = sqrt( (region.rInOut.err * 1./region.rInOut.val)**2 + (result["nZUncert"] * 1./result["nZ"] )**2) * result["nCont"] 
		if not result["nS"] == "--":
			result["nSStar"] = result["nS"] -result["nCont"]
			result["nSStarUncert"] = sqrt( result["nSUncert"]**2 + result["nContUncert"]**2)
	if shape == "GT":
	    	result["shape"] = "anal. shape"
	elif shape == "HistT":
		result["shape"] = "binned shape"
        elif shape == "KernelT":
                result["shape"] = "KDE"
	else:
		result["shape"] = shape
	result["title"] = ""

	return result

def extendBasics(pkl, region):
	from math import sqrt
	from src.defs import getOFScale
	n = {}
	n.update(pkl)

	ofScale = region.R_SFOF.val
	ofScaleRelError = region.R_SFOF.err
#	rmue = 1.20
#	trigger = {
#		"EE":93.0,
#		"EMu":92.5,
#		"MuMu":94.4
#		}
#	nllPredictionScale =  0.5* sqrt(trigger["EE"]*trigger["MuMu"])*1./trigger["EMu"] *(rmue+1./(rmue))
	
	n["nS"] = n["EE"]  + n["MuMu"] - n["EMu"]*ofScale
	n["nSSysUncert"] = n["EMu"]* ofScaleRelError
	n["nSStatUncert"] = sqrt(n["EMu"]+n["EE"]+n["MuMu"])
	#~ n["nSSysUncert"] = ((n["EMu"]* ofScaleRelError)**2 + (sqrt(n["EMu"])*ofScale)**2)**0.5
	#~ n["nSStatUncert"] = sqrt(n["EMu"])
	n["nSUncert"] = sqrt(n["nSStatUncert"]**2+n["nSSysUncert"]**2)

	n["nSF"] = n["EE"]  + n["MuMu"]
	
	n["nOF"] = n["EMu"]*ofScale
	n["nOFSysUncert"] = n["EMu"] * ofScaleRelError
	#~ n["nOFSysUncert"] =((n["EMu"]* ofScaleRelError)**2 + (sqrt(n["EMu"])*ofScale)**2)**0.5
	n["nOFStatUncert"] = sqrt(n["EMu"])
	n["nOFUncert"] = sqrt(n["nOFStatUncert"]**2+n["nOFSysUncert"]**2)
		
	n["nS-debug"] = "nS=%s + %s - %s = %s"%(n["EE"] , n["MuMu"], n["nOF"], n["nS"])
	if n["EE"] != 0:
		n["rmueSR"] = sqrt(n["MuMu"]*1./n["EE"]*1.) 
	else: 
        	n["rmueSR"] = 0.
	n["rmueSR-reldiff"] =  n["rmueSR"]*100./ofScale -100.
	if (n["EE"]+n["MuMu"]+n["EMu"] > 0):
		n["sig-debug"] = (n["EE"]+n["MuMu"]-n["EMu"])*1./sqrt(n["EE"]+n["MuMu"]+n["EMu"])  
	else:
		n["sig-debug"] = -1
	return n

def extendPickle( name, pkl):
	from math import sqrt
	from src.defs import getRegion
	result = {}
	for subcut, nSub in pkl.iteritems():
		region = getRegion(name)
		result[subcut] = {}
		for mllcut, n in nSub.iteritems():
			result[subcut][mllcut] =  extendBasics(n, region)

		result[subcut]["shapeGT"] = loadShapePickles(name, subcut, shape = "GT")
		result[subcut]["shapeHistT"] = loadShapePickles(name, subcut, shape = "HistT")
                result[subcut]["shapeKernelT"] = loadShapePickles(name, subcut, shape = "KernelT")
		result[subcut]["nBEdge"] = result[subcut]["edgeMass"]["nOF"]
		result[subcut]["nBEdgeSysUncert"] = result[subcut]["edgeMass"]["nOFSysUncert"]
		result[subcut]["nBEdgeStatUncert"] = result[subcut]["edgeMass"]["nOFStatUncert"]
		result[subcut]["nBEdgeUncert"] = result[subcut]["edgeMass"]["nOFUncert"]

		result[subcut]["nB"] = result[subcut]["default"]["nOF"]
		result[subcut]["nBSysUncert"] = result[subcut]["default"]["nOFSysUncert"]
		result[subcut]["nBStatUncert"] = result[subcut]["default"]["nOFStatUncert"]
		result[subcut]["nBUncert"] = result[subcut]["default"]["nOFUncert"]

		if not subcut in region.dyPrediction:
			result[subcut]["nZ"] = result[subcut]["onShellMass"]["nS"]
			result[subcut]["nZSysUncert"] = result[subcut]["onShellMass"]["nSSysUncert"]
			result[subcut]["nZStatUncert"] = result[subcut]["onShellMass"]["nSStatUncert"]
			result[subcut]["nZUncert"] = result[subcut]["onShellMass"]["nSUncert"]
		else:
			result[subcut]["nZ"] = region.dyPrediction[subcut][0]
			result[subcut]["nZSysUncert"] = region.dyPrediction[subcut][1]
			result[subcut]["nZStatUncert"] = region.dyPrediction[subcut][2]
			result[subcut]["nZUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nZStatUncert"], result[subcut]["nZSysUncert"]]]))
		result[subcut]["nCont"] = result[subcut]["nZ"] * region.rInOut.val
		result[subcut]["nContSysUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nCont"] * region.rInOut.err * 1./region.rInOut.val, result[subcut]["nZSysUncert"]* region.rInOut.val ]]))
		result[subcut]["nContStatUncert"] = result[subcut]["nZStatUncert"] * region.rInOut.val
		result[subcut]["nContUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nContStatUncert"], result[subcut]["nContSysUncert"]]]))

		for i in ["nS", "nSUncert", "nSSysUncert", "nSStatUncert"]:
			result[subcut][i] = result[subcut]["edgeMass"][i]
		
		result[subcut]["nSStar"] = result[subcut]["edgeMass"]["nS"] - result[subcut]["nCont"]
		result[subcut]["nSStarSysUncert"] = sqrt( result[subcut]["edgeMass"]["nSSysUncert"]**2 + result[subcut]["nContUncert"]**2)
		result[subcut]["nSStarStatUncert"] = result[subcut]["edgeMass"]["nSStatUncert"]
		result[subcut]["nSStarUncert"] = sqrt(result[subcut]["nSStarStatUncert"]**2 + result[subcut]["nSStarSysUncert"]**2)
		result[subcut]["nSStar-debug"] = "%.4f - %.4f = %.4f (Uncert sqrt(sum(i**2 for i in [%.4f, %.4f, %.4f] ) = %.4f"%(result[subcut]["edgeMass"]["nS"], result[subcut]["nCont"], result[subcut]["nSStar"], result[subcut]["edgeMass"]["nSSysUncert"], result[subcut]["nContUncert"], result[subcut]["edgeMass"]["nSStatUncert"], result[subcut]["nSStarUncert"])
	return result

def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

	print table
	
def makeSummaryTable(data, subcuts, regionName, name):
	tableTemplate =r"""
%s
\begin{tabular}{ll|ccc|cc}
selection & approach & $N_S$ & $N_B$ ( low \mll ) & $N_Z$ & $N_{\text{Continuum}}$ & \nsstar\\
\hline
\hline
%s
\end{tabular}
"""

	titles = {
		"default": "2012 A+B+C",
		"LowPU": r"$\nvert < 11$",
		"MidPU": r"$11 \le \nvert < 16$",
		"HighPU": r"$ \nvert \ge 16$",
		"0BTag":r"$n_{\text{b-tagged}} = 0$",
		"1BTag":r"$n_{\text{b-tagged}} = 1$",
		"Ge2BTag":r"$n_{\text{b-tagged}} \ge 2$",
		"Barrel":r"$\eta^{\ell} < 1.4$",
		"LowHT": r"$100 < \HT < 300$ GeV",
		"HighHT": r"$\HT > 300$ GeV",
		"TightIso":r"rel. iso $< 0.05$",
		"Pt2020":r"$p_{T}^{\ell} > 20$ GeV",
		"Pt2010":r"$p_{T}^{\ell} > 20(10)$ GeV",
		"Pt3010":r"$p_{T}^{\ell} > 30(10)$ GeV",
		"Pt3020":r"$p_{T}^{\ell} > 30(20)$ GeV",
		"Pt3030":r"$p_{T}^{\ell} > 30$ GeV",
		"CountCuts":r"$\mll > 20$ GeV, $p_T^{\ell}>20$ GeV ",
		"CatA": "$p_{T} > 20$ GeV, $|\eta| < 1.4$",
		"CatB": "$p_{T} > 20$ GeV, not $|\eta| < 1.4$",
		"CatC": "not $p_{T} > 20$ GeV, $|\eta| < 1.4$",
		"CatD": "not $p_{T} > 20$ GeV, not $|\eta| < 1.4$",
		"RunAB": "2012 A+B",
		"RunC":"2012 C",
		"MET100Ge2Jets":"E_{T}^{miss} > 100 Gev",
		"MET50Ge2Jets":"E_{T}^{miss} > 50 Gev",
		"Barrel":"$|\eta|<$ 1.4",
		"Endcap":"$|\eta_{1}|>$  1.4 $||$ $|\eta_{2}|>$  1.4 ",
		"Type1":" type1 $E_T^{miss}>$  150 GeV ",
		"Tc":" tc $E_T^{miss}>$  150 GeV ",
		"Calo":" calo $E_T^{miss}>$  150 GeV ",
		"MHT":"  $H_T^{miss}>$  150 GeV ",
		}
	notesTemplate = "%% %(nS-debug)s\n%% %(cut)s \n"
	notesLine2Template = r"%% %(nSStar-debug)s"+"\n"
	lineCountTemplate = r"%(title)50s &    count    & $%(nS)3.1f \pm %(nSUncert)3.1f$ & $%(nB)3.1f \pm %(nBUncert)3.1f$  ($%(nBEdge)3.1f \pm %(nBEdgeStatUncert)3.1f \pm %(nBEdgeSysUncert)3.1f$) & $%(nZ)3.1f \pm %(nZUncert)3.1f$  & $%(nCont)3.1f \pm %(nContUncert)3.1f$ & $%(nSStar)3.1f \pm %(nSStarStatUncert)3.1f \pm %(nSStarSysUncert)3.1f$ \\"+"\n"
	lineShapeTemplate = r"%(title)50s & %(shape)10s & $%(nS)3.1f \pm %(nSUncert)3.1f$ & $%(nB)3.1f \pm %(nBUncert)3.1f$                  & $%(nZ)3.1f \pm %(nZUncert)3.1f$  & $%(nCont)3.1f \pm %(nContUncert)3.1f$ & $%(nSStar)3.1f \pm %(nSStarUncert)3.1f$\\"+"\n"
	

	table = ""
	notes = ""
	for subcutName in subcuts:
		print name
		print regionName
		print subcutName
		print titles[subcutName]
		data[subcutName]["title"] = titles[subcutName]
		notes += notesTemplate%data[subcutName]["edgeMass"]
		notes += notesLine2Template%data[subcutName]
		table += lineCountTemplate%data[subcutName]
		if not data[subcutName]["shapeKernelT"]["nS"] == "--":
			table += lineShapeTemplate%data[subcutName]["shapeKernelT"]
		if not data[subcutName]["shapeHistT"]["nS"] == "--":
			table += lineShapeTemplate%data[subcutName]["shapeHistT"]
                #~ if not data[subcutName]["shapeKernelT"]["nS"] == "--":
			#~ table += lineShapeTemplate%data[subcutName]["shapeKernelT"]
		table += "\\hline\n"
	
	saveTable(tableTemplate%(notes, table), "summary_%s_%s"%(regionName,name))
				  
def makeFitTable(data,region, subcuts, name):
	tableTemplate =r"""
%s
\begin{tabular}{l|rrr}
\hline
 & background & on-shell $Z$ & signal \\
 Scenario & event yield & event yield & event yield \\ \hline \hline

%s
\end{tabular}
"""	


	titles = {
		"default": "nominal",
		"LowPU": r"low pileup $\nvert < 11$",
		"MidPU": r"medium pileup $11 \le \nvert < 16$",
		"HighPU": r"high pileup $ \nvert \ge 16$",
		"0BTag":r"$n_{\text{b-tagged}} = 0$",
		"1BTag":r"$n_{\text{b-tagged}} = 1$",
		"Ge2BTag":r"$n_{\text{b-tagged}} \ge 2$",
		"Barrel":r"Only Barrel $|\eta^{\ell}| < 1.4$",
		"Endcap":r"Only Forward, at least one $|\eta^{\ell}| > 1.4$",
		"LowHT": r"$100 < \HT < 300$ GeV",
		"HighHT": r"$\HT > 300$ GeV",
		"TightIso":r"Tight isolated leptopns",
		"Pt2020":r"$p_{T}^{\ell} > 20$ GeV",
		"CountCuts":r"$\mll > 20$ GeV, $p_T^{\ell}>20$ GeV ",
		"CatA": "$p_{T} > 20$ GeV, $|\eta| < 1.4$",
		"CatB": "$p_{T} > 20$ GeV, not $|\eta| < 1.4$",
		"CatC": "not $p_{T} > 20$ GeV, $|\eta| < 1.4$",
		"CatD": "not $p_{T} > 20$ GeV, not $|\eta| < 1.4$",
		"RunAB": "only Runs A,B $5.1$~fb$^{-1}$",
		"RunC":"only Runs C $4.1$~fb$^{-1}$",
		"MET100Ge2Jets": "$MET>100$~GeV",
		"Pt2020":r"$p_{T}^{\ell} > 20$ GeV",
		"Pt2010":r"$p_{T}^{\ell} > 20(10)$ GeV",
		"Pt3010":r"$p_{T}^{\ell} > 30(10)$ GeV",
		"Pt3020":r"$p_{T}^{\ell} > 30(20)$ GeV",
		"Pt3030":r"$p_{T}^{\ell} > 30$ GeV",		
		"Type1":r"$E_T^{miss}$ corr. for jet corrections",		
		"Tc":r"track corr. $E_T^{miss}$",		
		"Calo":r"calo based $E_T^{miss}$",		
		}
		
	notesTemplate = "%% %(nS-debug)s\n%% %(cut)s \n"
	notesLine2Template = r"%% %(nSStar-debug)s"+"\n"
	lineCountTemplate = r"%(title)50s &    count    & $%(nS)3.1f \pm %(nSUncert)3.1f$ & $%(nB)3.1f \pm %(nBUncert)3.1f$  ($%(nBEdge)3.1f \pm %(nBEdgeStatUncert)3.1f \pm %(nBEdgeSysUncert)3.1f$) & $%(nZ)3.1f \pm %(nZUncert)3.1f$  & $%(nCont)3.1f \pm %(nContUncert)3.1f$ & $%(nSStar)3.1f \pm %(nSStarStatUncert)3.1f \pm %(nSStarSysUncert)3.1f$ \\"+"\n"
	lineShapeTemplate = r"%(title)50s & $%(nB)3.1f \pm %(nBUncert)3.1f$  & $%(nZ)3.1f \pm %(nZUncert)3.1f$  & $%(nS)3.1f \pm %(nSUncert)3.1f$ \\"+"\n"
	
	tempData = extendPickle(region, data[region])
	tempDataMETPD = extendPickle(region+"_METPD", data[region+"_METPD"])
	#~ tempDataMET100 = extendPickle("MET100Ge2Jets", data["MET100Ge2Jets"])

	table = ""
	notes = ""
	for subcutName in subcuts:
		tempData[subcutName]["shapeKernelT"]["title"] = titles[subcutName]
		notes += notesTemplate%tempData[subcutName]["edgeMass"]
		notes += notesLine2Template%tempData[subcutName]
		if not tempData[subcutName]["shapeKernelT"]["nS"] == "--":
			table += lineShapeTemplate%tempData[subcutName]["shapeKernelT"]


		if subcutName == "default" or subcutName =="Ge2BTag" or subcutName =="Endcap" or subcutName =="Pt3030" or subcutName =="HighPU" or subcutName =="MuMu" or subcutName =="HighHT" or subcutName =="RunC" or subcutName =="TightIso" or subcutName =="Calo": 
			print subcutName
			table += "\\hline\n"
	#~ tempDataMET100["default"]["shapeKernelT"]["title"] = "MET triggers and diff. PD"	
	#~ table += lineShapeTemplate%tempDataMETPD["default"]["shapeKernelT"]
	tempDataMETPD["default"]["shapeKernelT"]["title"] = "MET triggers and diff. PD"	
	table += lineShapeTemplate%tempDataMETPD["default"]["shapeKernelT"]
	table += "\\hline\n"
	#~ table += r"Simultaneous fit of \Rinout &  &   & \\"+"\n"
	table += "\\hline\n"
	tempData["default"]["shapeHistT"]["title"] = "Backgd. param. histogram"	
	table += lineShapeTemplate%tempData["default"]["shapeHistT"]
	table += "\\hline\n"
	saveTable(tableTemplate%(notes, table), name)
				  

def makeRegionTables(data, name):
	tableTemplate =r"""
%s
\begin{tabular}{l|ccc|c}
selection & $ee$ & $\mu\mu$ & $e\mu$ & measured $N_{S}$\\
\hline
\hline
%s
\end{tabular}
"""



	lineTemplate = r"%(title)50s & %(EE)4i & %(MuMu)4i & %(EMu)4i & $%(nS)3.1f \pm %(nSUncert)3.1f$ \\"+"\n"
	notesTemplate = r"%% %(nS-debug)s, %(cut)s"+"\n"
	finaleNoteTemplate = r"%% %(sig-debug)s"+"\n"
	titles = {
		"default": "$\mll > 20$~GeV",
		"edgeMass":        "$20 < \mll <70~\GeV$",
		"onShellMass": "$81 < \mll <101~\GeV$",
		"highMass": "$\mll >110~\GeV$",
		}
	notes =""
	table =""
	
	for subcutName in ["edgeMass", "onShellMass","highMass", "default"]:
		data[subcutName]["title"] = titles[subcutName]
		if subcutName == "default":
			table += "\\hline \n"
		table += lineTemplate%data[subcutName]
		table += finaleNoteTemplate %data[subcutName]
		notes += notesTemplate%data[subcutName]

	saveTable(tableTemplate%(notes, table), "region_%s"%name)
	
	


def makePASTable(data, subcutName):
	tableTemplate = r"""
	  \hline
                                &  Low-\MET         & High-\MET          \\
    \hline
             SF                 &  $%(nSF_SignalLowMET)s$ & $%(nSF_SignalHighMET)s$ \\
    \hline
             OF                 & $%(nOF_SignalLowMET)s$ & $%(nOF_SignalHighMET)s$ \\
             DY                 & $%(nDY_SignalLowMET)s$ & $%(nDY_SignalHighMET)s$ \\
             Non-prompt leptons & ($-1\pm1\pm4$)    & ($< 2.4$) \\
             Rare bkgds         & $0.6\pm0.1\pm1.3$ &  $0.5\pm3.2$\\
    \hline
	"""
	def withError(n, name):
		val = n[name]
		sys = n["%sSysUncert"%name]
		stat = n["%sStatUncert"%name]
		return r"%.1f \pm %.1f \pm %.1f"%(val, sys, stat)
	repMap = {}
	for regionName in ["SignalLowMET","SignalHighMET"]:
		repMap["nSF_%s"%regionName] = data[regionName][subcutName]["edgeMass"]["nSF"]
		repMap["nOF_%s"%regionName] = withError(data[regionName][subcutName] ,"nBEdge")
		repMap["nDY_%s"%regionName] = withError(data[regionName][subcutName] ,"nCont")
	saveTable(tableTemplate%repMap, "pasTable2_%s"%subcutName)
	return 
		
def makePASTable2(data, subcutName):
	tableTemplate = r"""
	  \hline
                                &  Low-\MET         & High-\MET          \\
    \hline
             SF                 &  $%(nSF_SignalLowMETFullEta)s$ & $%(nSF_BarrelHighMET)s$ \\
    \hline
             OF                 & $%(nOF_SignalLowMETFullEta)s$ & $%(nOF_BarrelHighMET)s$ \\
             DY                 & $%(nDY_SignalLowMETFullEta)s$ & $%(nDY_BarrelHighMET)s$ \\
             Non-prompt leptons & ($-1\pm1\pm4$)    & ($< 2.4$) \\
             Rare bkgds         & $0.6\pm0.1\pm1.3$ &  $0.5\pm3.2$\\
    \hline
	"""
	def withError(n, name):
		val = n[name]
		sys = n["%sSysUncert"%name]
		stat = n["%sStatUncert"%name]
		return r"%.1f \pm %.1f \pm %.1f"%(val, sys, stat)
	repMap = {}
	for regionName in ["SignalLowMETFullEta","BarrelHighMET"]:
		repMap["nSF_%s"%regionName] = data[regionName][subcutName]["edgeMass"]["nSF"]
		repMap["nOF_%s"%regionName] = withError(data[regionName][subcutName] ,"nBEdge")
		repMap["nDY_%s"%regionName] = withError(data[regionName][subcutName] ,"nCont")
	saveTable(tableTemplate%repMap, "pasTable_%s"%subcutName)
	return 

def main():
	from sys import argv
	from src.datasets import loadPickles
	allPkls = loadPickles("shelves/cutAndCount_*.pkl")
	#~ makeFitTable(allPkls, ["default","RunAB", "RunC","LowPU", "MidPU", "HighPU","LowHT", "HighHT","0BTag", "1BTag", "Ge2BTag","TightIso","Barrel"], "FitTable")
	#~ makeFitTable(allPkls,"SignalHighMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableHighMET")
	#~ makeFitTable(allPkls,"BarrelHighMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableBarrelHighMET")
	#~ makeFitTable(allPkls,"SignalLowMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableLowMET")
	#~ makeFitTable(allPkls,"SignalLowMETFullEta", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableLowMETFullEta")
	for regionName in allPkls:
		allPkls[regionName] = extendPickle(regionName, allPkls[regionName])		
		makeRegionTables(allPkls[regionName]["default"], regionName)
		#~ makeRegionTables(allPkls[regionName]["RunAB"], regionName+"_RunAB")
		#~ makeRegionTables(allPkls[regionName]["RunC"], regionName+"_RunC")
		

		makeSummaryTable(allPkls[regionName], ["default","RunAB", "RunC"], regionName, "Results")
		makeSummaryTable(allPkls[regionName], ["Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030"], regionName, "PtCuts")
		makeSummaryTable(allPkls[regionName], ["LowPU", "MidPU", "HighPU"], regionName, "PileUp")
		makeSummaryTable(allPkls[regionName], ["LowHT", "HighHT"], regionName, "HT")
		makeSummaryTable(allPkls[regionName], ["0BTag", "1BTag", "Ge2BTag"], regionName, "BTagging")
		makeSummaryTable(allPkls[regionName], ["default"], regionName, "Pt2010")
		makeSummaryTable(allPkls[regionName], ["default","TightIso"], regionName, "Iso")
		makeSummaryTable(allPkls[regionName], ["default","Barrel","Endcap"], regionName, "Eta")
		makeSummaryTable(allPkls[regionName], ["default","MET100Ge2Jets","MET50Ge2Jets"], regionName, "MET")
		makeSummaryTable(allPkls[regionName], ["default","CatA","CatB","CatC","CatD"], regionName, "Categories")
		makeSummaryTable(allPkls[regionName], ["default","Type1","Tc","Calo","MHT"], regionName, "METFlavours")

	makePASTable(allPkls, "default")
	#~ makePASTable(allPkls, "RunAB")
	#~ makePASTable(allPkls, "RunC")
	makePASTable2(allPkls, "default")
	#~ makePASTable2(allPkls, "RunAB")
	#~ makePASTable2(allPkls, "RunC")

main()
