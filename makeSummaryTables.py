#!/usr/bin/env python

#~ def getSplitCorrection(rmue,rmueErr,dilepton):
	#~ from src.defs import Constants
	#~ result = 0.
	#~ resultErr = 0.
	#~ if dilepton == "EE":
		#~ result = 1./(2*rmue)*(Constants.Trigger.EffEE.val/Constants.Trigger.EffEMu.val)
		#~ resultErr = (2*(rmueErr/rmue)**2+(0.071)**2)**0.5
	#~ elif dilepton == "MuMu":
		#~ result =(1.*rmue/2)*(Constants.Trigger.EffMuMu.val/Constants.Trigger.EffEMu.val)
		#~ resultErr = (2*(rmueErr/rmue)**2+(0.071**2))**0.5
	#~ return result,resultErr

def loadShapePickles(regionName, subcutName, shape = "GT", path = "../test/EdgeFitter/shelves"):
	import os
	import pickle
	from math import sqrt
	from src.defs import getRegion
	region = getRegion(regionName)
	if  "Run" in subcutName:
		regionName += "_"+ subcutName
	elif not subcutName == "default":
		regionName = regionName.replace("Signal", subcutName)
		regionName = regionName.replace("Barrel", subcutName+"Barrel")
		regionName = regionName.replace("Control", subcutName+"Control")
	#~ print regionName
	#~ picklePaths = {
		#~ "nS":"edgefit-%s-%s_FixedEdgeSFOS-nS.pkl",
		#~ "nSUncert":"edgefit-%s-%s_FixedEdgeSFOS-nSerror.pkl",
		#~ "nB":"edgefit-%s-%s_FixedEdgeSFOS-nB.pkl",
		#~ "nBUncert":"edgefit-%s-%s_FixedEdgeSFOS-nBerror.pkl",
		#~ "nZ":"edgefit-%s-%s_FixedEdgeSFOS-nZ.pkl",
		#~ "nZUncert":"edgefit-%s-%s_FixedEdgeSFOS-nZerror.pkl",
		#~ "chi2":"edgefit-%s-%s_FixedEdgeSFOS-chi2.pkl",
		#~ "nPar":"edgefit-%s-%s_FixedEdgeSFOS-nPar.pkl",
		#~ }
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
		#~ print pklPath
		result[varName] = "--"
		#~ print pklPath
		if os.path.exists(pklPath):
			pklFile = open(pklPath, "r")
			print pklFile
			result[varName] = pickle.load(pklFile)
			pklFile.close()
	if subcutName in region.dyPrediction:
		if region.dyPrediction[subcutName][0] > 0.:
			#~ print subcutName
			#~ print regionName
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
		#~ result["nCont"] = region.rInOut.val * result["nZ"]
		result["nCont"] = 0.
		#~ result["nContUncert"] = sqrt( (region.rInOut.err * 1./region.rInOut.val)**2 + (result["nZUncert"] * 1./result["nZ"] )**2) * result["nCont"] 
		result["nContUncert"] = 0.
		if not result["nS"] == "--":
			result["nSStar"] = result["nS"] -result["nCont"]
			result["nSStarUncert"] = sqrt( result["nSUncert"]**2 + result["nContUncert"]**2)
	if shape == "GT":
	    	result["shape"] = "anal. shape"
	elif shape == "HistT":
		result["shape"] = "binned shape"
	elif shape == "KernelT":
		result["shape"] = "KDE"
	elif shape == "MarcoAndreaT":
		result["shape"] = "anal. shape"
	elif shape == "PetarT":
		result["shape"] = "3 Gaussians"
	else:
		result["shape"] = shape
	result["title"] = ""

	return result

def extendBasics(pkl, region):
	from math import sqrt
	from src.defs import getOFScale
	n = {}
	n.update(pkl)
	print region.title
	print region.R_SFOF.val
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
	n["nSStatUncert"] = sqrt((sqrt(n["EMu"])*ofScale)**2+n["EE"]+n["MuMu"])
	#~ n["nSSysUncert"] = ((n["EMu"]* ofScaleRelError)**2 + (sqrt(n["EMu"])*ofScale)**2)**0.5
	#~ n["nSStatUncert"] = sqrt(n["EMu"])
	n["nSUncert"] = sqrt(n["nSStatUncert"]**2+n["nSSysUncert"]**2)

	n["nSF"] = n["EE"]  + n["MuMu"]
	
	n["nOF"] = n["EMu"]*ofScale
	n["nOFSysUncert"] = n["EMu"] * ofScaleRelError * ofScale
	#~ n["nOFSysUncert"] =((n["EMu"]* ofScaleRelError)**2 + (sqrt(n["EMu"])*ofScale)**2)**0.5
	n["nOFStatUncert"] = sqrt(n["EMu"])
	n["nOFUncert"] = sqrt(n["nOFStatUncert"]**2+n["nOFSysUncert"]**2)


	eeScale = region.R_EEOF.val
	eeScaleError = region.R_EEOF.err
	mmScale = region.R_MMOF.val
	mmScaleError = region.R_MMOF.err

	n["nBEE"] = n["EMu"]*eeScale
	n["nBEEStatUncert"] = sqrt(n["EMu"])*eeScale
	n["nBEESysUncert"] = sqrt( (n["EMu"] * eeScale * eeScaleError )**2 + (sqrt(n["EMu"])* eeScale)**2)
	n["nBEEUncert"] = sqrt(n["nBEEStatUncert"]**2 + n["nBEESysUncert"]**2)
	n["nSEE"] = n["EE"] - n["EMu"]*eeScale
	#~ n["nSEESysUncert"] = n["EMu"] * eeScale * eeScaleError
	#~ n["nSEEStatUncert"] = sqrt((sqrt(n["EMu"])* eeScale)**2+n["EE"]) 
	n["nSEESysUncert"] = sqrt((n["EMu"] * eeScale * eeScaleError)**2 + (sqrt(n["EMu"])* eeScale)**2) 
	n["nSEEStatUncert"] = sqrt(n["EE"]) 
	n["nSEEUncert"] = sqrt(n["nSEEStatUncert"]**2+n["nSEESysUncert"]**2)	
	
	n["nBMuMu"] = n["EMu"]*mmScale
	n["nBMuMuStatUncert"] = sqrt(n["EMu"])*mmScale
	n["nBMuMuSysUncert"] = sqrt( (n["EMu"] * mmScale * mmScaleError )**2 + (sqrt(n["EMu"]) * mmScale)**2)
	n["nBMuMuUncert"] = sqrt(n["nBMuMuStatUncert"]**2 + n["nBMuMuSysUncert"]**2)
	n["nSMuMu"] = n["MuMu"] - n["EMu"]*mmScale
	#~ n["nSMuMuSysUncert"] = n["EMu"] * mmScale * mmScaleError
	#~ n["nSMuMuStatUncert"] = sqrt((sqrt(n["EMu"])** mmScale)+n["MuMu"]) 
	n["nSMuMuSysUncert"] = sqrt((n["EMu"] * mmScale * mmScaleError)**2 + (sqrt(n["EMu"])* mmScale)**2) 
	n["nSMuMuStatUncert"] = sqrt(n["MuMu"])  
	n["nSMuMuUncert"] = sqrt(n["nSMuMuStatUncert"]**2+n["nSMuMuSysUncert"]**2)	
		
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
		result[subcut]["shapeMarcoAndreaT"] = loadShapePickles(name, subcut, shape = "MarcoAndreaT")
		result[subcut]["shapePetarT"] = loadShapePickles(name, subcut, shape = "PetarT")
		result[subcut]["nBEdge"] = result[subcut]["edgeMass"]["nOF"]
		#~ print subcut, result[subcut]["nBEdge"]
		result[subcut]["nBEdgeSysUncert"] = result[subcut]["edgeMass"]["nOFSysUncert"]
		result[subcut]["nBEdgeStatUncert"] = result[subcut]["edgeMass"]["nOFStatUncert"]
		result[subcut]["nBEdgeUncert"] = result[subcut]["edgeMass"]["nOFUncert"]
		
		result[subcut]["nB"] = result[subcut]["default"]["nOF"]
		#~ print subcut, result[subcut]["nB"] 
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
		#~ print subcut
		if not subcut in region.rarePrediction:
			result[subcut]["nRare"] = 0.
			result[subcut]["nRareUncert"] = 0.
		else:
			result[subcut]["nRare"] = region.rarePrediction[subcut][0]
			result[subcut]["nRareUncert"] = region.rarePrediction[subcut][1]		
		result[subcut]["nCont"] = result[subcut]["nZ"] * region.rInOut.val
		result[subcut]["nContSysUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nCont"] * region.rInOut.err * 1./region.rInOut.val, result[subcut]["nZSysUncert"]* region.rInOut.val ]]))
		result[subcut]["nContStatUncert"] = result[subcut]["nZStatUncert"] * region.rInOut.val
		result[subcut]["nContUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nContStatUncert"], result[subcut]["nContSysUncert"]]]))

		for i in ["nS", "nSUncert", "nSSysUncert", "nSStatUncert"]:
			result[subcut][i] = result[subcut]["edgeMass"][i]
		
		result[subcut]["nSStar"] = result[subcut]["edgeMass"]["nS"] - result[subcut]["nCont"] - result[subcut]["nRare"]
		result[subcut]["nSStarSysUncert"] = sqrt( result[subcut]["edgeMass"]["nSSysUncert"]**2 + result[subcut]["nContUncert"]**2 + result[subcut]["nRareUncert"]**2)
		result[subcut]["nSStarStatUncert"] = result[subcut]["edgeMass"]["nSStatUncert"]
		result[subcut]["nSStarUncert"] = sqrt(result[subcut]["nSStarStatUncert"]**2 + result[subcut]["nSStarSysUncert"]**2)
		result[subcut]["nSStar-debug"] = "%.4f - %.4f = %.4f (Uncert sqrt(sum(i**2 for i in [%.4f, %.4f, %.4f] ) = %.4f"%(result[subcut]["edgeMass"]["nS"], result[subcut]["nCont"], result[subcut]["nSStar"], result[subcut]["edgeMass"]["nSSysUncert"], result[subcut]["nContUncert"], result[subcut]["edgeMass"]["nSStatUncert"], result[subcut]["nSStarUncert"])
	return result
	
def extendPickleSeparated( name, pkl,dilepton):
	from math import sqrt
	from src.defs import getRegion
	result = {}
	for subcut, nSub in pkl.iteritems():
		region = getRegion(name)
		result[subcut] = {}
		for mllcut, n in nSub.iteritems():
			result[subcut][mllcut] =  extendBasics(n, region)


		#~ scale, scaleError = getSplitCorrection(region.rMuE.val,region.rMuE.err,dilepton)
		if dilepton == "MuMu":
			scale = region.R_MMOF.val
			scaleError = region.R_MMOF.err
		else:	
			scale = region.R_EEOF.val
			scaleError = region.R_EEOF.err
		result[subcut]["nBEdge"] = result[subcut]["edgeMass"]["nB%s"%dilepton]
		#~ print subcut, result[subcut]["nBEdge"] 
		result[subcut]["nBEdgeSysUncert"] = result[subcut]["edgeMass"]["nB%sSysUncert"%dilepton]
		result[subcut]["nBEdgeStatUncert"] = result[subcut]["edgeMass"]["nB%sStatUncert"%dilepton]
		result[subcut]["nBEdgeUncert"] = result[subcut]["edgeMass"]["nB%sUncert"%dilepton]

		result[subcut]["nB"] = result[subcut]["default"]["nB%s"%dilepton]
		result[subcut]["nBSysUncert"] = result[subcut]["default"]["nB%sSysUncert"%dilepton]
		result[subcut]["nBStatUncert"] = result[subcut]["default"]["nB%sStatUncert"%dilepton]
		result[subcut]["nBUncert"] = result[subcut]["default"]["nB%sUncert"%dilepton]

		if not subcut in region.dyPrediction:
			result[subcut]["nZ"] = result[subcut]["onShellMass"]["nS%s"%dilepton]
			result[subcut]["nZSysUncert"] = result[subcut]["onShellMass"]["nS%sSysUncert"%dilepton]
			result[subcut]["nZStatUncert"] = result[subcut]["onShellMass"]["nS%sStatUncert"%dilepton]
			result[subcut]["nZUncert"] = result[subcut]["onShellMass"]["nS%sUncert"%dilepton]
		else:
			result[subcut]["nZ"] = region.dyPrediction[subcut][0]*scale
			result[subcut]["nZSysUncert"] = ((region.dyPrediction[subcut][1]*scale)**2 + (region.dyPrediction[subcut][1]*scale*scaleError)**2)**0.5
			result[subcut]["nZStatUncert"] = ((region.dyPrediction[subcut][2]*scale)**2 + (region.dyPrediction[subcut][2]*scale*scaleError)**2)**0.5
			result[subcut]["nZUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nZStatUncert"], result[subcut]["nZSysUncert"]]]))
		if not subcut == "default":
			result[subcut]["nRare"] = 0.
			result[subcut]["nRareUncert"] = 0.
                elif  not dilepton in region.rarePrediction:
                        print "WARNING: Ignoring rare for '%s'"%(region.title)
			result[subcut]["nRare"] = 0.
			result[subcut]["nRareUncert"] = 0.
		else:
			result[subcut]["nRare"] = region.rarePrediction[dilepton][0]
			result[subcut]["nRareUncert"] = region.rarePrediction[dilepton][1]

		
		result[subcut]["nCont"] = result[subcut]["nZ"] * region.rInOut.val
		result[subcut]["nContSysUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nCont"] * region.rInOut.err * 1./region.rInOut.val, result[subcut]["nZSysUncert"]* region.rInOut.val ]]))
		result[subcut]["nContStatUncert"] = result[subcut]["nZStatUncert"] * region.rInOut.val
		result[subcut]["nContUncert"] = sqrt(sum([i**2 for i in [result[subcut]["nContStatUncert"], result[subcut]["nContSysUncert"]]]))

		for i in ["nS", "nSUncert", "nSSysUncert", "nSStatUncert"]:
			result[subcut][i] = result[subcut]["edgeMass"][i]
		
		result[subcut]["nS"] = result[subcut]["edgeMass"]["nS%s"%dilepton]
		result[subcut]["nSStatUncert"] = result[subcut]["edgeMass"]["nS%sStatUncert"%dilepton]
		result[subcut]["nSSysUncert"] = result[subcut]["edgeMass"]["nS%sSysUncert"%dilepton]
		result[subcut]["nSUncert"] = result[subcut]["edgeMass"]["nS%sUncert"%dilepton]
		
		result[subcut]["nSStar"] = result[subcut]["edgeMass"]["nS%s"%dilepton] - result[subcut]["nCont"] - result[subcut]["nRare"]
		result[subcut]["nSStarSysUncert"] = sqrt( result[subcut]["edgeMass"]["nS%sSysUncert"%dilepton]**2 + result[subcut]["nContUncert"]**2 + result[subcut]["nRareUncert"]**2)
		result[subcut]["nSStarStatUncert"] = result[subcut]["edgeMass"]["nS%sStatUncert"%dilepton]
		result[subcut]["nSStarUncert"] = sqrt(result[subcut]["nSStarStatUncert"]**2 + result[subcut]["nSStarSysUncert"]**2)
		result[subcut]["nSStar-debug"] = "%.4f - %.4f = %.4f (Uncert sqrt(sum(i**2 for i in [%.4f, %.4f, %.4f] ) = %.4f"%(result[subcut]["edgeMass"]["nS"], result[subcut]["nCont"], result[subcut]["nSStar"], result[subcut]["edgeMass"]["nSSysUncert"], result[subcut]["nContUncert"], result[subcut]["edgeMass"]["nSStatUncert"], result[subcut]["nSStarUncert"])
	return result

def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

	#~ print table
	
def makeSummaryTable(data, subcuts, regionName, name,dilepton=""):
	tableTemplate =r"""
%s
\begin{tabular}{ll|cc|ccc}
selection & approach & $N_S$ & $N_B$ ( low \mll ) & $N_{\text{Continuum}}$ & $N_{Rare}$ & \nsstar\\
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
		"LowHT": r"$\HT < 300$ GeV",
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
		"Type1MET":" type1 $E_T^{miss}$",
		"TcMET":" tc $E_T^{miss}$",
		"CaloMET":" calo $E_T^{miss}$",
		"MHTMET":"  $H_T^{miss}$",
		}
	notesTemplate = "%% %(nS-debug)s\n%% %(cut)s \n"
	notesLine2Template = r"%% %(nSStar-debug)s"+"\n"
	lineCountTemplate = r"%(title)50s &    count    & $%(nS)3.1f \pm %(nSUncert)3.1f$ & $%(nB)3.1f \pm %(nBUncert)3.1f$  ($%(nBEdge)3.1f \pm %(nBEdgeStatUncert)3.1f \pm %(nBEdgeSysUncert)3.1f$)  & $%(nCont)3.1f \pm %(nContUncert)3.1f$ & $%(nRare)3.1f \pm %(nRareUncert)3.1f$ & $%(nSStar)3.1f \pm %(nSStarStatUncert)3.1f \pm %(nSStarSysUncert)3.1f$ \\"+"\n"
	lineShapeTemplate = r"%(title)50s & %(shape)10s & $%(nS)3.1f \pm %(nSUncert)3.1f$ & $%(nB)3.1f \pm %(nBUncert)3.1f$                    & -- & -- & $%(nSStar)3.1f \pm %(nSStarUncert)3.1f$\\"+"\n"
	

	table = ""
	notes = ""
	for subcutName in subcuts:
		
		#~ print name
		#~ print regionName
		#~ print subcutName
		#~ print titles[subcutName]
		data[subcutName]["title"] = titles[subcutName]
		notes += notesTemplate%data[subcutName]["edgeMass"]
		notes += notesLine2Template%data[subcutName]
		table += lineCountTemplate%data[subcutName]
		if not dilepton != "":
			if not data[subcutName]["shapeMarcoAndreaT"]["nS"] == "--":
				table += lineShapeTemplate%data[subcutName]["shapeMarcoAndreaT"]
			if not data[subcutName]["shapeKernelT"]["nS"] == "--":
				table += lineShapeTemplate%data[subcutName]["shapeKernelT"]
			if not data[subcutName]["shapeHistT"]["nS"] == "--":
				table += lineShapeTemplate%data[subcutName]["shapeHistT"]
			if not data[subcutName]["shapePetarT"]["nS"] == "--":
				table += lineShapeTemplate%data[subcutName]["shapePetarT"]
                #~ if not data[subcutName]["shapeKernelT"]["nS"] == "--":
			#~ table += lineShapeTemplate%data[subcutName]["shapeKernelT"]
		table += "\\hline\n"
	if not dilepton == "":	
		saveTable(tableTemplate%(notes, table), "summary_%s_%s_%s"%(regionName,name,dilepton))
	else:
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
		"LowHT": r"$\HT < 300$ GeV",
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
		"Type1MET":r"$E_T^{miss}$ corr. for jet corrections",		
		"TcMET":r"track corr. $E_T^{miss}$",		
		"CaloMET":r"calo based $E_T^{miss}$",		
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
		tempData[subcutName]["shapeMarcoAndreaT"]["title"] = titles[subcutName]
		notes += notesTemplate%tempData[subcutName]["edgeMass"]
		notes += notesLine2Template%tempData[subcutName]
		if not tempData[subcutName]["shapeMarcoAndreaT"]["nS"] == "--":
			table += lineShapeTemplate%tempData[subcutName]["shapeMarcoAndreaT"]


		if subcutName == "default" or subcutName =="Ge2BTag" or subcutName =="Endcap" or subcutName =="Pt3030" or subcutName =="HighPU" or subcutName =="MuMu" or subcutName =="HighHT" or subcutName =="RunC" or subcutName =="TightIso" or subcutName =="CaloMET": 
			#~ print subcutName
			table += "\\hline\n"
	#~ tempDataMET100["default"]["shapeKernelT"]["title"] = "MET triggers and diff. PD"	
	#~ table += lineShapeTemplate%tempDataMETPD["default"]["shapeKernelT"]
	tempDataMETPD["default"]["shapeMarcoAndreaT"]["title"] = "MET triggers and diff. PD"
	#~ print tempDataMETPD["default"]["shapeKernelT"]	
	table += lineShapeTemplate%tempDataMETPD["default"]["shapeMarcoAndreaT"]
	table += "\\hline\n"
	#~ table += r"Simultaneous fit of \Rinout &  &   & \\"+"\n"
	table += "\\hline\n"
	tempData["default"]["shapeHistT"]["title"] = "Backgd. param. histogram"	
	table += lineShapeTemplate%tempData["default"]["shapeHistT"]
	table += "\\hline\n"
	saveTable(tableTemplate%(notes, table), name)
				  

def makeRegionTables(data, name,dilepton=""):
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
	if dilepton != "":
		saveTable(tableTemplate%(notes, table), "region_%s_%s"%(name,dilepton))
	else:
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
	allPklsEE = loadPickles("shelves/cutAndCount_*.pkl")
	allPklsMuMu = loadPickles("shelves/cutAndCount_*.pkl")
	#~ makeFitTable(allPkls, ["default","RunAB", "RunC","LowPU", "MidPU", "HighPU","LowHT", "HighHT","0BTag", "1BTag", "Ge2BTag","TightIso","Barrel"], "FitTable")
	#~ makeFitTable(allPkls,"SignalHighMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","MHT","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableHighMET")
	#~ makeFitTable(allPkls,"BarrelHighMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableBarrelHighMET")
	#~ makeFitTable(allPkls,"SignalLowMET", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableLowMET")
	#~ makeFitTable(allPkls,"SignalLowMETFullEta", ["default","0BTag",
        #"1BTag", "Ge2BTag","Pt2010","Pt2020",
        #"Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1","Tc","Calo","LowPU",
        #"MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",],
        #"FitTableLowMETFullEta")
	#~ makeFitTable(allPkls,"SignalNonRectCentral", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1MET","TcMET","CaloMET","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableSignalNonRectCentral")
	#~ makeFitTable(allPkls,"SignalNonRectForward", ["default","0BTag", "1BTag", "Ge2BTag","Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030","Barrel","Endcap","Type1MET","TcMET","CaloMET","LowPU", "MidPU", "HighPU","LowHT", "HighHT","RunAB", "RunC","TightIso",], "FitTableSignalNonRectForward")
	for regionName in allPkls:
		allPkls[regionName] = extendPickle(regionName, allPkls[regionName])		
		makeRegionTables(allPkls[regionName]["default"], regionName)
		makeRegionTables(allPkls[regionName]["RunAB"], regionName+"_RunAB")
		makeRegionTables(allPkls[regionName]["RunC"], regionName+"_RunC")
		

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
		makeSummaryTable(allPkls[regionName], ["default","Type1MET","TcMET","CaloMET","MHTMET"], regionName, "METFlavours")
		
		allPklsEE[regionName] = extendPickleSeparated(regionName, allPklsEE[regionName],"EE")		
		makeRegionTables(allPklsEE[regionName]["default"], regionName,"EE")
		makeRegionTables(allPklsEE[regionName]["RunAB"], regionName+"_RunAB","EE")
		makeRegionTables(allPklsEE[regionName]["RunC"], regionName+"_RunC","EE")
		

		makeSummaryTable(allPklsEE[regionName], ["default","RunAB", "RunC"], regionName, "Results","EE")
		makeSummaryTable(allPklsEE[regionName], ["Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030"], regionName, "PtCuts","EE")
		makeSummaryTable(allPklsEE[regionName], ["LowPU", "MidPU", "HighPU"], regionName, "PileUp","EE")
		makeSummaryTable(allPklsEE[regionName], ["LowHT", "HighHT"], regionName, "HT","EE")
		makeSummaryTable(allPklsEE[regionName], ["0BTag", "1BTag", "Ge2BTag"], regionName, "BTagging","EE")
		makeSummaryTable(allPklsEE[regionName], ["default"], regionName, "Pt2010","EE")
		makeSummaryTable(allPklsEE[regionName], ["default","TightIso"], regionName, "Iso","EE")
		makeSummaryTable(allPklsEE[regionName], ["default","Barrel","Endcap"], regionName, "Eta","EE")
		makeSummaryTable(allPklsEE[regionName], ["default","MET100Ge2Jets","MET50Ge2Jets"], regionName, "MET","EE")
		makeSummaryTable(allPklsEE[regionName], ["default","CatA","CatB","CatC","CatD"], regionName, "Categories","EE")
		makeSummaryTable(allPklsEE[regionName], ["default","Type1MET","TcMET","CaloMET","MHTMET"], regionName, "METFlavours","EE")
		
		
		allPklsMuMu[regionName] = extendPickleSeparated(regionName, allPklsMuMu[regionName],"MuMu")		
		makeRegionTables(allPklsMuMu[regionName]["default"], regionName,"MuMu")
		makeRegionTables(allPklsMuMu[regionName]["RunAB"], regionName+"_RunAB","MuMu")
		makeRegionTables(allPklsMuMu[regionName]["RunC"], regionName+"_RunC","MuMu")
		

		makeSummaryTable(allPklsMuMu[regionName], ["default","RunAB", "RunC"], regionName, "Results","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["Pt2010","Pt2020", "Pt3010","Pt3020","Pt3030"], regionName, "PtCuts","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["LowPU", "MidPU", "HighPU"], regionName, "PileUp","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["LowHT", "HighHT"], regionName, "HT","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["0BTag", "1BTag", "Ge2BTag"], regionName, "BTagging","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default"], regionName, "Pt2010","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default","TightIso"], regionName, "Iso","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default","Barrel","Endcap"], regionName, "Eta","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default","MET100Ge2Jets","MET50Ge2Jets"], regionName, "MET","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default","CatA","CatB","CatC","CatD"], regionName, "Categories","MuMu")
		makeSummaryTable(allPklsMuMu[regionName], ["default","Type1MET","TcMET","CaloMET","MHTMET"], regionName, "METFlavours","MuMu")
		
	makePASTable(allPkls, "default")
	#~ makePASTable(allPkls, "RunAB")
	#~ makePASTable(allPkls, "RunC")
	makePASTable2(allPkls, "default")
	#~ makePASTable2(allPkls, "RunAB")
	#~ makePASTable2(allPkls, "RunC")

main()
