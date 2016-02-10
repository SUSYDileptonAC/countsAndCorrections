#!/usr/bin/env python



def saveTable(table, name):
	tabFile = open("tab/table_%s_Run2015C.tex"%name, "w")
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

	dataPkls = loadPickles("shelves/rSFOF_Control_Run2015C.pkl")
	dataBarrelPkls = loadPickles("shelves/rSFOF_ControlCentral_Run2015C.pkl")
	dataEndcapPkls = loadPickles("shelves/rSFOF_ControlForward_Run2015C.pkl")
	mcPkls = loadPickles("shelves/rSFOF_Control_RunIITest_MC.pkl")
	mcBarrelPkls = loadPickles("shelves/rSFOF_ControlCentral_RunIITest_MC.pkl")
	mcEndcapPkls = loadPickles("shelves/rSFOF_ControlForward_RunIITest_MC.pkl")

	#~ print dataPkls
	
# Table for Inclusive

	tableTemplate =r"""
\begin{tabular}{c|c|c|c}     
  
 SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$\\    
\hline
 \multicolumn{4}{c}{MC} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline 
%s    
    \hline 
\multicolumn{4}{c}{Data} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline
%s    
\end{tabular}  
"""


	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataPkls["SF"],dataPkls["OF"],dataPkls["rSFOF"],dataPkls["rSFOFErr"])	

	tableMC += lineTemplate%(mcPkls["SF"],mcPkls["OF"],mcPkls["rSFOF"],mcPkls["rSFOFErr"],mcPkls["transfer"],mcPkls["transferErr"])	


	
	saveTable(tableTemplate%(tableMC,tableData), "Rsfof_Inclusive")

# Table with Barrel and Endcap seperated


	tableTemplate =r"""

\begin{tabular}{c|c|c|c|c|c|c|c}     
 SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$ &  SF & OF & $\Rsfof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$  \\    
\hline
 \multicolumn{8}{c}{MC} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ } \\
\hline 
%s    
    \hline 
\multicolumn{8}{c}{Data} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ }\\
\hline
%s 
  
\end{tabular}  

"""

	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f \\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataBarrelPkls["SF"],dataBarrelPkls["OF"],dataBarrelPkls["rSFOF"],dataBarrelPkls["rSFOFErr"],dataEndcapPkls["SF"],dataEndcapPkls["OF"],dataEndcapPkls["rSFOF"],dataEndcapPkls["rSFOFErr"])	

	tableMC += lineTemplate%(mcBarrelPkls["SF"],mcBarrelPkls["OF"],mcBarrelPkls["rSFOF"],mcBarrelPkls["rSFOFErr"],mcBarrelPkls["transfer"],mcBarrelPkls["transferErr"],mcEndcapPkls["SF"],mcEndcapPkls["OF"],mcEndcapPkls["rSFOF"],mcEndcapPkls["rSFOFErr"],mcEndcapPkls["transfer"],mcEndcapPkls["transferErr"])	


	saveTable(tableTemplate%(tableMC,tableData), "Rsfof_Seperated")
	
# Table for Inclusive

	tableTemplate =r"""
\begin{tabular}{c|c|c|c}     
 
 SF & OF & $\Reeof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$\\    
\hline
 \multicolumn{4}{c}{MC} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline 
%s    
    \hline 
\multicolumn{4}{c}{Data} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline
%s 
 
\end{tabular}  
"""


	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataPkls["EE"],dataPkls["OF"],dataPkls["rEEOF"],dataPkls["rEEOFErr"])	


	tableMC += lineTemplate%(mcPkls["EE"],mcPkls["OF"],mcPkls["rEEOF"],mcPkls["rEEOFErr"],mcPkls["transferEE"],mcPkls["transferEEErr"])	


	
	saveTable(tableTemplate%(tableMC,tableData), "Reeof_Inclusive")

# Table with Barrel and Endcap seperated


	tableTemplate =r"""

\begin{tabular}{c|c|c|c|c|c|c|c}     
 
 SF & OF & $\Reeof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$ &  SF & OF & $\Reeof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$  \\    
\hline
 \multicolumn{8}{c}{MC} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ } \\
\hline 
%s    
    \hline 
\multicolumn{8}{c}{Data} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ }\\
\hline
%s  
\end{tabular}  

"""

	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f \\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataBarrelPkls["EE"],dataBarrelPkls["OF"],dataBarrelPkls["rEEOF"],dataBarrelPkls["rEEOFErr"],dataEndcapPkls["EE"],dataEndcapPkls["OF"],dataEndcapPkls["rEEOF"],dataEndcapPkls["rEEOFErr"])	

	tableMC += lineTemplate%(mcBarrelPkls["EE"],mcBarrelPkls["OF"],mcBarrelPkls["rEEOF"],mcBarrelPkls["rEEOFErr"],mcBarrelPkls["transferEE"],mcBarrelPkls["transferEEErr"],mcEndcapPkls["EE"],mcEndcapPkls["OF"],mcEndcapPkls["rEEOF"],mcEndcapPkls["rEEOFErr"],mcEndcapPkls["transferEE"],mcEndcapPkls["transferEEErr"])	


	saveTable(tableTemplate%(tableMC,tableData), "Reeof_Seperated")
	
# Table for Inclusive

	tableTemplate =r"""
\begin{tabular}{c|c|c|c}     
 
 SF & OF & $\Rmmof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$\\    
\hline
 \multicolumn{4}{c}{MC} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline 
%s    
    \hline 
\multicolumn{4}{c}{Data} \\
\hline
 \multicolumn{4}{c}{$|\eta|<2.4$ } \\
\hline
%s   
\end{tabular}  
"""


	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f\\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataPkls["MM"],dataPkls["OF"],dataPkls["rMMOF"],dataPkls["rMMOFErr"])	


	tableMC += lineTemplate%(mcPkls["MM"],mcPkls["OF"],mcPkls["rMMOF"],mcPkls["rMMOFErr"],mcPkls["transferMM"],mcPkls["transferMMErr"])	


	
	saveTable(tableTemplate%(tableMC,tableData), "Rmmof_Inclusive")

# Table with Barrel and Endcap seperated


	tableTemplate =r"""

\begin{tabular}{c|c|c|c|c|c|c|c}     
\hline    
 SF & OF & $\Rmmof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$ &  SF & OF & $\Rmmof \pm \sigma_{stat}$ & Transfer $\pm \sigma_{stat}$  \\    
\hline
 \multicolumn{8}{c}{MC} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ } \\
\hline 
%s    
    \hline 
\multicolumn{8}{c}{Data} \\
\hline
  \multicolumn{4}{c|}{$|\eta|<1.4$ } & \multicolumn{4}{|c}{ at least 1 $|\eta| > 1.6$ }\\
\hline
%s     
\end{tabular}  

"""

	lineTemplate = r" %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f & %d & %d & %.3f$\pm$%.3f & %.3f$\pm$%.3f \\"+"\n"
	lineTemplateData = r" %d & %d & %.3f$\pm$%.3f & -- & %d & %d & %.3f$\pm$%.3f & -- \\"+"\n"


	tableMC =""
	tableData =""

	tableData += lineTemplateData%(dataBarrelPkls["MM"],dataBarrelPkls["OF"],dataBarrelPkls["rMMOF"],dataBarrelPkls["rMMOFErr"],dataEndcapPkls["MM"],dataEndcapPkls["OF"],dataEndcapPkls["rMMOF"],dataEndcapPkls["rMMOFErr"])	


	tableMC += lineTemplate%(mcBarrelPkls["MM"],mcBarrelPkls["OF"],mcBarrelPkls["rMMOF"],mcBarrelPkls["rMMOFErr"],mcBarrelPkls["transferMM"],mcBarrelPkls["transferMMErr"],mcEndcapPkls["MM"],mcEndcapPkls["OF"],mcEndcapPkls["rMMOF"],mcEndcapPkls["rMMOFErr"],mcEndcapPkls["transferMM"],mcEndcapPkls["transferMMErr"])	


	saveTable(tableTemplate%(tableMC,tableData), "Rmmof_Seperated")


main()
