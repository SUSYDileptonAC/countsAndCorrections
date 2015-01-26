import ROOT
import numpy as np

from math import sqrt
attic = []


ROOT.gStyle.SetOptStat(0)




def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()
	
	
if (__name__ == "__main__"):

	import pickle
	inputs = {}
	
	inputs["rMuECentral"] = 1.089
	inputs["rMuECentralErr"] = 0.109
	inputs["rMuEForward"] = 1.188
	inputs["rMuEForwardErr"] = 0.238
	
	inputs["trigEECentral"] = 0.9687010954616588
	inputs["trigEECentralErr"] = ((0.05*0.9687010954616588)**2+0.00564**2)**0.5 ## Add statistical uncertainty of trigger eff and 5% syst eff in quadrature
	inputs["trigMMCentral"] = 0.9753086419753086
	inputs["trigMMCentralErr"] = ((0.05*0.9753086419753086)**2+0.01438**2)**0.5
	inputs["trigEMCentral"] = 0.9662921348314607
	inputs["trigEMCentralErr"] = ((0.05*0.9662921348314607)**2+0.03155**2)**0.5
	
	inputs["trigEEForward"] = 0.9739884393063584
	inputs["trigEEForwardErr"] = ((0.05*0.9739884393063584)**2+0.01159**2)**0.5
	inputs["trigMMForward"] = 0.9550561797752809
	inputs["trigMMForwardErr"] = ((0.05*0.9550561797752809)**2+0.03394**2)**0.5
	inputs["trigEMForward"] = 0.88
	inputs["trigEMForwardErr"] = ((0.05*0.88)**2+0.10264**2)**0.5

	inputs["RsfofCRCentral"] = 1.010##*0.994 ## don't multiply factor from CR with transfer factor from MC 
	inputs["RsfofCRCentralErr"] = (0.072**2+(0.02*inputs["RsfofCRCentral"])**2)**0.5 ## statistical uncertainty of R(SF/OF) from CR and stat. uncert. from transfer factor
	inputs["RsfofCRForward"] = 0.9484536082474226##*1.032
	inputs["RsfofCRForwardErr"] = (0.138**2+(0.03*inputs["RsfofCRForward"])**2)**0.5

	inputs["ReeofCRCentral"] = 0.472##*0.977 ## don't multiply factor from CR with transfer factor from MC 
	inputs["ReeofCRCentralErr"] = (0.042**2+(0.02*inputs["ReeofCRCentral"])**2)**0.5 ## statistical uncertainty of R(SF/OF) from CR and stat. uncert. from transfer factor
	inputs["ReeofCRForward"] = 0.412##*1.021
	inputs["ReeofCRForwardErr"] = (0.077**2+(0.04*inputs["ReeofCRForward"])**2)**0.5

	inputs["RmmofCRCentral"] = 0.538##*1.007 ## don't multiply factor from CR with transfer factor from MC 
	inputs["RmmofCRCentralErr"] = (0.046**2+(0.02*inputs["RmmofCRCentral"])**2)**0.5 ## statistical uncertainty of R(SF/OF) from CR and stat. uncert. from transfer factor
	inputs["RmmofCRForward"] = 0.5361##*1.039
	inputs["RmmofCRForwardErr"] = (0.0921**2+(0.04*inputs["RmmofCRForward"])**2)**0.5

	
	
	result = {}
	### error propagation deluxe! 
	result["fromRMuECentral"] = 0.5*(inputs["rMuECentral"]+1./inputs["rMuECentral"])
	result["fromRMuECentralErr"] = 0.5*(1. - (1./(inputs["rMuECentral"]**2)))*inputs["rMuECentralErr"]
	result["fromRMuEForward"] = 0.5*(inputs["rMuEForward"]+1./inputs["rMuEForward"])
	result["fromRMuEForwardErr"] = 0.5*(1. - (1./(inputs["rMuEForward"]**2)))*inputs["rMuEForwardErr"]
	result["fromRMuECentralMM"] = 0.5*(inputs["rMuECentral"])
	#~ result["fromRMuECentralMMErr"] = 0.5*(1.)*inputs["rMuECentralErr"]
	result["fromRMuECentralMMErr"] = inputs["rMuECentralErr"]
	result["fromRMuEForwardMM"] = 0.5*(inputs["rMuEForward"])
	#~ result["fromRMuEForwardMMErr"] = 0.5*(1.)*inputs["rMuEForwardErr"]
	result["fromRMuEForwardMMErr"] = inputs["rMuEForwardErr"]
	
	result["fromRMuECentralEE"] = 0.5*(1./inputs["rMuECentral"])
	#~ result["fromRMuECentralEEErr"] = 0.5*((1./(inputs["rMuECentral"]**2)))*inputs["rMuECentralErr"]
	result["fromRMuECentralEEErr"] = inputs["rMuECentralErr"]
	result["fromRMuEForwardEE"] = 0.5*(1./inputs["rMuEForward"])
	#~ result["fromRMuEForwardEEErr"] = 0.5*((1./(inputs["rMuEForward"]**2)))*inputs["rMuEForwardErr"]
	result["fromRMuEForwardEEErr"] = inputs["rMuEForwardErr"]
	
	result["fromTriggerCentral"] = (inputs["trigEECentral"]*inputs["trigMMCentral"])**0.5/inputs["trigEMCentral"]
	result["fromTriggerCentralErr"] = result["fromTriggerCentral"]*( (inputs["trigEECentralErr"]/(2*inputs["trigEECentral"]))**2 + (inputs["trigMMCentralErr"]/(2*inputs["trigMMCentral"]))**2 + (inputs["trigEMCentralErr"]/(inputs["trigEMCentral"]))**2 )**0.5
	result["fromTriggerForward"] = (inputs["trigEEForward"]*inputs["trigMMForward"])**0.5/inputs["trigEMForward"]
	result["fromTriggerForwardErr"] = result["fromTriggerForward"]*( (inputs["trigEEForwardErr"]/(2*inputs["trigEEForward"]))**2 + (inputs["trigMMForwardErr"]/(2*inputs["trigMMForward"]))**2 + (inputs["trigEMForwardErr"]/(inputs["trigEMForward"]))**2 )**0.5


	result["fromACCentral"] = result["fromRMuECentral"]*result["fromTriggerCentral"]
	result["fromACCentralErr"] = result["fromACCentral"]*((result["fromRMuECentralErr"]/result["fromRMuECentral"])**2 + (result["fromTriggerCentralErr"]/result["fromTriggerCentral"])**2)**0.5
	result["fromACForward"] = result["fromRMuEForward"]*result["fromTriggerForward"]
	result["fromACForwardErr"] = result["fromACForward"]*((result["fromRMuEForwardErr"]/result["fromRMuEForward"])**2 + (result["fromTriggerForwardErr"]/result["fromTriggerForward"])**2)**0.5
	
	result["fromACCentralMM"] = result["fromRMuECentralMM"]*result["fromTriggerCentral"]
	result["fromACCentralMMErr"] = result["fromACCentralMM"]*((result["fromRMuECentralMMErr"]/inputs["rMuECentral"])**2 + (result["fromTriggerCentralErr"]/result["fromTriggerCentral"])**2)**0.5
	result["fromACForwardMM"] = result["fromRMuEForwardMM"]*result["fromTriggerForward"]
	result["fromACForwardMMErr"] = result["fromACForwardMM"]*((result["fromRMuEForwardMMErr"]/inputs["rMuEForward"])**2 + (result["fromTriggerForwardErr"]/result["fromTriggerForward"])**2)**0.5
	
	result["fromACCentralEE"] = result["fromRMuECentralEE"]*result["fromTriggerCentral"]
	result["fromACCentralEEErr"] = result["fromACCentralEE"]*((result["fromRMuECentralEEErr"]/inputs["rMuECentral"])**2 + (result["fromTriggerCentralErr"]/result["fromTriggerCentral"])**2)**0.5
	result["fromACForwardEE"] = result["fromRMuEForwardEE"]*result["fromTriggerForward"]
	result["fromACForwardEEErr"] = result["fromACForwardEE"]*((result["fromRMuEForwardEEErr"]/inputs["rMuEForward"])**2 + (result["fromTriggerForwardErr"]/result["fromTriggerForward"])**2)**0.5


	result["fromETHCentral"] = inputs["RsfofCRCentral"]
	result["fromETHCentralErr"] = inputs["RsfofCRCentralErr"]
	result["fromETHForward"] = inputs["RsfofCRForward"]
	result["fromETHForwardErr"] = inputs["RsfofCRForwardErr"]

	result["fromETHCentralEE"] = inputs["ReeofCRCentral"]
	result["fromETHCentralEEErr"] = inputs["ReeofCRCentralErr"]
	result["fromETHForwardEE"] = inputs["ReeofCRForward"]
	result["fromETHForwardEEErr"] = inputs["ReeofCRForwardErr"]

	result["fromETHCentralMM"] = inputs["RmmofCRCentral"]
	result["fromETHCentralMMErr"] = inputs["RmmofCRCentralErr"]
	result["fromETHForwardMM"] = inputs["RmmofCRForward"]
	result["fromETHForwardMMErr"] = inputs["RmmofCRForwardErr"]
	
	
	
	### weighted average of both methods because Bob said so
	result["combinationCentral"] = (result["fromACCentral"]/result["fromACCentralErr"]**2 + result["fromETHCentral"]/result["fromETHCentralErr"]**2) / (1./result["fromACCentralErr"]**2 + 1./result["fromETHCentralErr"]**2)
	result["combinationCentralErr"] = (1./(1./result["fromACCentralErr"]**2 + 1./result["fromETHCentralErr"]**2))**0.5
	
	result["combinationForward"] = (result["fromACForward"]/result["fromACForwardErr"]**2 + result["fromETHForward"]/result["fromETHForwardErr"]**2) / (1./result["fromACForwardErr"]**2 + 1./result["fromETHForwardErr"]**2)
	result["combinationForwardErr"] = 1./((1./result["fromACForwardErr"]**2 + 1./result["fromETHForwardErr"]**2))**0.5

	result["combinationCentralMM"] = (result["fromACCentralMM"]/result["fromACCentralMMErr"]**2 + result["fromETHCentralMM"]/result["fromETHCentralMMErr"]**2) / (1./result["fromACCentralMMErr"]**2 + 1./result["fromETHCentralMMErr"]**2)
	result["combinationCentralMMErr"] = 1./((1./result["fromACCentralMMErr"]**2 + 1./result["fromETHCentralMMErr"]**2))**0.5
	
	result["combinationForwardMM"] = (result["fromACForwardMM"]/result["fromACForwardMMErr"]**2 + result["fromETHForwardMM"]/result["fromETHForwardMMErr"]**2) / (1./result["fromACForwardMMErr"]**2 + 1./result["fromETHForwardMMErr"]**2)
	result["combinationForwardMMErr"] = 1./((1./result["fromACForwardMMErr"]**2 + 1./result["fromETHForwardMMErr"]**2))**0.5

	result["combinationCentralEE"] = (result["fromACCentralEE"]/result["fromACCentralEEErr"]**2 + result["fromETHCentralEE"]/result["fromETHCentralEEErr"]**2) / (1./result["fromACCentralEEErr"]**2 + 1./result["fromETHCentralEEErr"]**2)
	result["combinationCentralEEErr"] = 1./((1./result["fromACCentralEEErr"]**2 + 1./result["fromETHCentralEEErr"]**2))**0.5
	
	result["combinationForwardEE"] = (result["fromACForwardEE"]/result["fromACForwardEEErr"]**2 + result["fromETHForwardEE"]/result["fromETHForwardEEErr"]**2) / (1./result["fromACForwardEEErr"]**2 + 1./result["fromETHForwardEEErr"]**2)
	result["combinationForwardEEErr"] = 1./((1./result["fromACForwardEEErr"]**2 + 1./result["fromETHForwardEEErr"]**2))**0.5

	
	
	
	
	

	outFilePkl = open("shelves/FullCorrection.pkl","w")
	pickle.dump(result, outFilePkl)
	outFilePkl.close()	
	
	tableTemplate =r"""
\begin{tabular}{l|c|c}       
$R_{SF/OF}$  & central  & forward   \\    
\hline
\hline  
%s    
\hline
\hline
%s
\hline
\hline
%s 
   
\end{tabular}
"""
	tableTemplateEE =r"""
\begin{tabular}{l|c|c}       
$R_{ee/OF}$  & central  & forward   \\    
\hline
\hline  
%s    
\hline
\hline
%s
\hline
\hline
%s 
 
\end{tabular}
"""
	tableTemplateMM =r"""
\begin{tabular}{l|c|c}     
$R_{\mu\mu/OF}$  & central  & forward   \\    
\hline
\hline  
%s    
\hline
\hline
%s
\hline
\hline
%s 
     
\end{tabular}
"""
	lineTemplate = r" %s & %.2f$\pm$%.2f & %.2f$\pm$%.2f\\"+"\n"

	tableAC = ""
	tableETH = ""
	tableComb = ""
	
	tableAC+= lineTemplate%("from $r_{\mu e}$",result["fromRMuECentral"],result["fromRMuECentralErr"],result["fromRMuEForward"],result["fromRMuEForwardErr"])
	tableAC+= lineTemplate%("from trigger efficiencies",result["fromTriggerCentral"],result["fromTriggerCentralErr"],result["fromTriggerForward"],result["fromTriggerForwardErr"])
	tableAC+= lineTemplate%("combination",result["fromACCentral"],result["fromACCentralErr"],result["fromACForward"],result["fromACForwardErr"])
	
	tableETH+= lineTemplate%("from Control Region",result["fromETHCentral"], result["fromETHCentralErr"], result["fromETHForward"], result["fromETHForwardErr"])
	
	tableComb = lineTemplate%("Weighted Average",result["combinationCentral"], result["combinationCentralErr"], result["combinationForward"], result["combinationForwardErr"])
	
	
	saveTable(tableTemplate%(tableAC,tableETH,tableComb), "correctionTableSF")

	tableAC = ""
	tableETH = ""
	tableComb = ""
	
	tableAC+= lineTemplate%("from $r_{\mu e}$",result["fromRMuECentralEE"],result["fromRMuECentralEEErr"],result["fromRMuEForwardEE"],result["fromRMuEForwardEEErr"])
	tableAC+= lineTemplate%("from trigger efficiencies",result["fromTriggerCentral"],result["fromTriggerCentralErr"],result["fromTriggerForward"],result["fromTriggerForwardErr"])
	tableAC+= lineTemplate%("combination",result["fromACCentralEE"],result["fromACCentralEEErr"],result["fromACForwardEE"],result["fromACForwardEEErr"])
	
	tableETH+= lineTemplate%("from Control Region",result["fromETHCentralEE"], result["fromETHCentralEEErr"], result["fromETHForwardEE"], result["fromETHForwardEEErr"])
	
	tableComb = lineTemplate%("Weighted Average",result["combinationCentralEE"], result["combinationCentralEEErr"], result["combinationForwardEE"], result["combinationForwardEEErr"])
	
	
	saveTable(tableTemplateEE%(tableAC,tableETH,tableComb), "correctionTableEE")

	tableAC = ""
	tableETH = ""
	tableComb = ""
	
	tableAC+= lineTemplate%("from $r_{\mu e}$",result["fromRMuECentralMM"],result["fromRMuECentralMMErr"],result["fromRMuEForwardMM"],result["fromRMuEForwardMMErr"])
	tableAC+= lineTemplate%("from trigger efficiencies",result["fromTriggerCentral"],result["fromTriggerCentralErr"],result["fromTriggerForward"],result["fromTriggerForwardErr"])
	tableAC+= lineTemplate%("combination",result["fromACCentralMM"],result["fromACCentralMMErr"],result["fromACForwardMM"],result["fromACForwardMMErr"])
	
	tableETH+= lineTemplate%("from Control Region",result["fromETHCentralMM"], result["fromETHCentralMMErr"], result["fromETHForwardMM"], result["fromETHForwardMMErr"])
	
	tableComb = lineTemplate%("Weighted Average",result["combinationCentralMM"], result["combinationCentralMMErr"], result["combinationForwardMM"], result["combinationForwardMMErr"])
	
	
	saveTable(tableTemplateMM%(tableAC,tableETH,tableComb), "correctionTableMM")
