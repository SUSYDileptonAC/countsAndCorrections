#!/usr/bin/env python



def saveTable(table, name):
	tabFile = open("tab/table_%s.tex"%name, "w")
	tabFile.write(table)
	tabFile.close()

	#~ print table
	
def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		result.update(pickle.load(pklFile))
	return result

				  


def main():
	from sys import argv
	#~ allPkls = loadPickles("shelves/*.pkl")

	dataPkls = loadPickles("shelves/rSFOF_Data_Inclusive.pkl")
	dataBarrelPkls = loadPickles("shelves/rSFOF_Data_Barrel.pkl")
	dataEndcapPkls = loadPickles("shelves/rSFOF_Data_Endcap.pkl")
	mcPkls = loadPickles("shelves/rSFOF_MC_Inclusive.pkl")
	mcBarrelPkls = loadPickles("shelves/rSFOF_MC_Barrel.pkl")
	mcEndcapPkls = loadPickles("shelves/rSFOF_MC_Endcap.pkl")

	#~ print dataPkls
	
# Table for Inclusive

	tableTemplate =r"""
\begin{tabular}{|c|c|c|c|}     
\hline    
 SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$\\    
\hline\hline
 \multicolumn{4}{|c|}{MC} \\
\hline
 \multicolumn{4}{|c|}{$|\eta|<2.4$ } \\
\hline 
%s    
    \hline 
\multicolumn{4}{|c|}{Data} \\
\hline
 \multicolumn{4}{|c|}{$|\eta|<2.4$ } \\
\hline
%s 
 \hline     
\end{tabular}  
"""


	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""
	name = "default"
	run = "Run92"

	tableData += lineTemplateData%(dataPkls["SF"],dataPkls["OF"],dataPkls["rSFOF"],dataPkls["rSFOFErr"])	


	run = "Simulation"

	tableMC += lineTemplate%(mcPkls["SF"],mcPkls["OF"],mcPkls["rSFOF"],mcPkls["rSFOFErr"],mcPkls["transfer"],mcPkls["transferErr"])	


	
	saveTable(tableTemplate%(tableMC,tableData), "Rsfof_Inclusive")

# Table with Barrel and Endcap seperated


	tableTemplate =r"""

\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|}     
\hline    
 SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$ &  SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$  \\    
\hline\hline
 \multicolumn{8}{|c|}{MC} \\
\hline
  \multicolumn{4}{|c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c|}{ at least 1 $|\eta| > 1.6$ } \\
\hline 
%s    
    \hline 
\multicolumn{8}{|c|}{Data} \\
\hline
  \multicolumn{4}{|c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c|}{ at least 1 $|\eta| > 1.6$ }\\
\hline
%s 
 \hline     
\end{tabular}  

"""

	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f \\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""
	name = "default"
	run = "Run92"

	tableData += lineTemplateData%(dataBarrelPkls["SF"],dataBarrelPkls["OF"],dataBarrelPkls["rSFOF"],dataBarrelPkls["rSFOFErr"],dataEndcapPkls["SF"],dataEndcapPkls["OF"],dataEndcapPkls["rSFOF"],dataEndcapPkls["rSFOFErr"])	

	run = "Simulation"

	tableMC += lineTemplate%(mcBarrelPkls["SF"],mcBarrelPkls["OF"],mcBarrelPkls["rSFOF"],mcBarrelPkls["rSFOFErr"],mcBarrelPkls["transfer"],mcBarrelPkls["transferErr"],mcEndcapPkls["SF"],mcEndcapPkls["OF"],mcEndcapPkls["rSFOF"],mcEndcapPkls["rSFOFErr"],mcEndcapPkls["transfer"],mcEndcapPkls["transferErr"])	


	saveTable(tableTemplate%(tableMC,tableData), "Rsfof_Seperated")


main()
