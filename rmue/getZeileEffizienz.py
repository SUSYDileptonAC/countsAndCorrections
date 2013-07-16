import ROOT
from src.messageLogger import messageLogger as log
from decimal import *

def getZeileEffizienz(zeilenbeschreibung, k, n,latexString = False , anzahlDezimalStellen = 4, level = 0.683 ):
    #k = Zaehler
    #n = Nenner
    #log.logDebug ("N = %f , k = %f , level %f "%(n,k,level))
    eff = k / n
    sigmaUpEff = ROOT.TEfficiency.ClopperPearson(int(n),int(k),level,True)-eff	#gibt CP Fehler aus
    sigmaDownEff = eff-ROOT.TEfficiency.ClopperPearson(int(n),int(k),level,False)
    bib = { "zeilenbeschreibung": zeilenbeschreibung , "k":int(k) , "n":int(n) , "eff":eff, "sigmaUpeff":sigmaUpEff , "sigmaDowneff":sigmaDownEff }
    if latexString == False:
        return bib
    elif latexString == True:
        string = "%(zeilenbeschreibung)s\t%(k).i\t%(n).i\t%(eff).4f^{+%(sigmaUpEff).4f}_{-%(sigmaDownEff).4f}\n" % bib
        #log.logDebug ("%s" % (string))
        return string
	
