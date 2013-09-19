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
	inputs["rMuEForwardErr"] = 0.178
	
	inputs["trigEECentral"] = 0.968
	inputs["trigEECentralErr"] = (0.05**2+0.006**2)**0.5 ## Add statistical uncertainty of trigger eff and 5% syst eff in quadrature
	inputs["trigMMCentral"] = 0.979
	inputs["trigMMCentralErr"] = (0.05**2+0.012**2)**0.5
	inputs["trigEMCentral"] = 0.963
	inputs["trigEMCentralErr"] = (0.05**2+0.021**2)**0.5
	
	inputs["trigEEForward"] = 0.967
	inputs["trigEEForwardErr"] = (0.05**2+0.012**2)**0.5
	inputs["trigMMForward"] = 0.950
	inputs["trigMMForwardErr"] = (0.05**2+0.032**2)**0.5
	inputs["trigEMForward"] = 0.932
	inputs["trigEMForwardErr"] = (0.05**2+0.062**2)**0.5

	inputs["RsfofCRCentral"] = 1.008*0.994 ## multiply factor from CR with transfer factor from MC 
	inputs["RsfofCRCentralErr"] = (0.072**2+0.015**2)**0.5 ## statistical uncertainty of R(SF/OF) from CR and stat. uncert. from transfer factor
	inputs["RsfofCRForward"] = 0.939*1.032
	inputs["RsfofCRForwardErr"] = (0.136**2+0.032**2)**0.5

	
	
	result = {}
	### error propagation deluxe! 
	result["fromRMuECentral"] = 0.5*(inputs["rMuECentral"]+1./inputs["rMuECentral"])
	result["fromRMuECentralErr"] = 0.5*(1. - (1./(inputs["rMuECentral"]**2)))*inputs["rMuECentralErr"]
	result["fromRMuEForward"] = 0.5*(inputs["rMuEForward"]+1./inputs["rMuEForward"])
	result["fromRMuEForwardErr"] = 0.5*(1. - (1./(inputs["rMuEForward"]**2)))*inputs["rMuEForwardErr"]
	
	result["fromTriggerCentral"] = (inputs["trigEECentral"]*inputs["trigMMCentral"])**0.5/inputs["trigEMCentral"]
	result["fromTriggerCentralErr"] = result["fromTriggerCentral"]*( (inputs["trigEECentralErr"]/(2*inputs["trigEECentral"]))**2 + (inputs["trigMMCentralErr"]/(2*inputs["trigMMCentral"]))**2 + (inputs["trigEMCentralErr"]/(inputs["trigEMCentral"]))**2 )**0.5
	result["fromTriggerForward"] = (inputs["trigEEForward"]*inputs["trigMMForward"])**0.5/inputs["trigEMForward"]
	result["fromTriggerForwardErr"] = result["fromTriggerForward"]*( (inputs["trigEEForwardErr"]/(2*inputs["trigEEForward"]))**2 + (inputs["trigMMForwardErr"]/(2*inputs["trigMMForward"]))**2 + (inputs["trigEMForwardErr"]/(inputs["trigEMForward"]))**2 )**0.5
	
	result["fromACCentral"] = result["fromRMuECentral"]*result["fromTriggerCentral"]
	result["fromACCentralErr"] = (result["fromRMuECentralErr"]**2 + result["fromTriggerCentralErr"]**2)**0.5
	result["fromACForward"] = result["fromRMuEForward"]*result["fromTriggerForward"]
	result["fromACForwardErr"] = (result["fromRMuEForwardErr"]**2 + result["fromTriggerForwardErr"]**2)**0.5


	result["fromETHCentral"] = inputs["RsfofCRCentral"]
	result["fromETHCentralErr"] = inputs["RsfofCRCentralErr"]
	result["fromETHForward"] = inputs["RsfofCRForward"]
	result["fromETHForwardErr"] = inputs["RsfofCRForwardErr"]
	
	
	
	### weighted average of both methods because Bob said so	
	result["combinationCentral"] = (result["fromACCentral"]/result["fromACCentralErr"]**2 + result["fromETHCentral"]/result["fromETHCentralErr"]**2) / (1./result["fromACCentralErr"]**2 + 1./result["fromETHCentralErr"]**2)
	result["combinationCentralErr"] = (1./(1./result["fromACCentralErr"]**2 + 1./result["fromETHCentralErr"]))**0.5
	
	result["combinationForward"] = (result["fromACForward"]/result["fromACForwardErr"]**2 + result["fromETHForward"]/result["fromETHForwardErr"]**2) / (1./result["fromACForwardErr"]**2 + 1./result["fromETHForwardErr"]**2)
	result["combinationForwardErr"] = (1./(1./result["fromACForwardErr"]**2 + 1./result["fromETHForwardErr"]))**0.5

	
	
	
	
	

	outFilePkl = open("shelves/FullCorrection.pkl","w")
	pickle.dump(result, outFilePkl)
	outFilePkl.close()	
	
	tableTemplate =r"""
\begin{tabular}{|l|c|c|}     \hline  
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
\hline     
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
	
	
	saveTable(tableTemplate%(tableAC,tableETH,tableComb), "correctionTable")
