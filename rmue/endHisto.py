import ROOT
from src.messageLogger import messageLogger as log
from src.processes import SubProcesses7TeV, SubProcesses8TeV, Processes7TeV, Processes8TeV, TreePaths, Trees
from src.defs import Cuts, Colors, Titles, Constants, UnderLegendAnnotation, Lumi8TeVAnnotation1, Lumi8TeVAnnotation2, Lumi8TeVAnnotation3
from src.treeTools import getEntriesFromTree, getHistoFromProcess, getEntriesFromProcesses
from src.plotTools import histoStack, save, legende, setPalette, makeAnnotation
import src.Styles as Styles

class p4M():
    variable = "p4.M()"
    filename = "Vergleichsplot"
    nBins=30
    xMin=0
    xMax=300
    yMin=0.5
    yMax=650
    xaxis=Titles.p4M


def Histo(plot, isinput=False): # Vergleichhistogramm

    log.outputLevel=5
    rootContainer = []
    style=Styles.tdrStyle()
    style.SetPadRightMargin(0.1)
    style.SetTitleYOffset(0.9)
    setPalette()
    c1= ROOT.TCanvas("c1","c1",800,800)
    #c1.SetLogy()
    cut="chargeProduct==-1 && (pt1 > 20 && pt2 > 10 || pt1 > 10 && pt2 > 20)"

    SubProcesses8TeV.dataPath = "../Daten/"
    SubProcesses7TeV.dataPath = "../Daten/"
    
    #Histos einlesen
    histoTT_ee = getHistoFromProcess(Processes8TeV.TTJets, plot.variable, cut, Trees.ee, plot.nBins, plot.xMin, plot.xMax,False, False)
    histoTT_mumu = getHistoFromProcess(Processes8TeV.TTJets, plot.variable, cut, Trees.mumu, plot.nBins, plot.xMin, plot.xMax,False, False)
    histoTT_emu = getHistoFromProcess(Processes8TeV.TTJets, plot.variable, cut, Trees.emu, plot.nBins, plot.xMin, plot.xMax, False, False)
    histoTT_ee.Add(histoTT_mumu)

    histoTT_ee.SetFillColor(Colors.ttJets)
    histoTT_emu.SetFillColor(Colors.weiss)

    histos=[histoTT_ee, histoTT_emu]
    names=["t#bar{t}: ee+\mu\mu", "t#bar{t}: e\mu"]

    stack=histoStack(histos)

    frame=c1.DrawFrame(plot.xMin,plot.yMin,plot.xMax,plot.yMax,"; %s ; Events / 10.0 GeV" %plot.xaxis)
    frame.GetYaxis().SetTitleOffset(1.2) 
    stack.Draw("hist SAME NOSTACK")
 
    stack.SetTitle("; %s ; Entries" %plot.xaxis)
    
    #Legende
    leg=legende(histos, names, "f")
    

    #Annotations

    #anno=makeAnnotation(UnderLegendAnnotation, plot.cut)
    lumianno1=makeAnnotation(Lumi8TeVAnnotation1)
    lumianno2=makeAnnotation(Lumi8TeVAnnotation2)
    lumianno3=makeAnnotation(Lumi8TeVAnnotation3)
    lumianno1.Draw("same")
    lumianno2.Draw("same")
    lumianno3.Draw("same")
    #anno.Draw("same")
        
    c1.RedrawAxis()
    leg.Draw()
    c1.Update()
    plotpath="Plots/Histos/8TeV/neueDaten/"
    save(c1, plotpath, "%s" %plot.filename)

    #__________________________________________Ratio aus ttbar in SR_________________________________#

    log.logHighlighted(cut)
 
    effmumu=Constants.eff8TeVData_mumu
    effee=Constants.eff8TeVData_ee
    sigma_effmumu_p=Constants.sigma8TeVData_mumu_p
    sigma_effmumu_m=Constants.sigma8TeVData_mumu_m
    sigma_effee_p=Constants.sigma8TeVData_ee_p
    sigma_effee_m=Constants.sigma8TeVData_ee_m

    anz_mumu, sigma_mumu= getEntriesFromProcesses(Processes8TeV.TTJets, plot.variable, cut, Trees.mumu)
    log.logHighlighted ("Anzahl mumu=%s /pm %s"%(anz_mumu, sigma_mumu)) #mit cut

    anz_ee, sigma_ee=getEntriesFromProcesses(Processes8TeV.TTJets, plot.variable, cut, Trees.ee)
    log.logHighlighted ("Anzahl ee = %s /pm %s"%(anz_ee, sigma_ee)) #mit cut
    r=pow(anz_mumu/anz_ee,0.5)

    sigma_r_stat= r/2*pow( pow(sigma_mumu/anz_mumu,2) + pow(sigma_ee/anz_ee,2), 0.5)

    log.logHighlighted("anz_mumu= %f und anz_ee=%f" %(anz_mumu, anz_ee))

    log.logError("\t Das Verhaeltnis mit %s \n ist %s \pm %s" %(cut, r, sigma_r_stat)) # =1,128109 (2011) =1,124820 (2012)

    return anz_mumu, anz_ee, r, sigma_r_stat

    if isinput==True:
        raw_input("Press Enter to continue")

def main():
    Constants.setLumi(Constants.lumi8TeV)
    Histo(p4M)

if __name__ == "__main__":
        main()
