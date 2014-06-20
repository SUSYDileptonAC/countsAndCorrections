from messageLogger import messageLogger as log

def tabular(inhaltDictList,keyListList,anzahlDezimalStellenDict={},horizontalStrichRange = set([0,"1"]),prozentDarstellungList=[]):
	#Bsp.:
	"""horizontalStrichRange = set([0,"1",len(ueberschriftKeyList)])
	tabelleTriggereffizienz = latexTabelle("Triggereffizienz","Triggereffizienz", (ueberschriftDict,eEDict,eMuDict,muMuDict),(ueberschriftKeyList,eEList,eMuList,muMuList),horizontalStrichRange,nachKommaStellen)"""
	#horizontalStrichRange ist die Menge aller Zeilennummern, vor die ein Strich soll ( als String, wenn DoppelStrich)
	#anzahlDezimalStellen ist eine Liste mit Nachkommastellen zu jeder Spalte, die kein int oder str ist. fuer int und str muessen der uebersicht halber trotzdem Werte uebergeben werden. wurschtbrot, welche ! sigmaUp und sigmaDown werden ignoriert, also dafuer keine stellen angeben
	strichZeilen = set([])
	doppelStrichZeilen = set([])
	for i in horizontalStrichRange:
		if type(i) == str:
			i=int(i)
			doppelStrichZeilen.add(i)
		elif type(i) == int:
			strichZeilen.add(i)
		else:
			log.logError("Falsche Formatierung des sets horizontalStrichRange")



	if len(inhaltDictList) != len(keyListList):
		log.logError("Anzahl Zeilen nicht gleich in keyListList und inhaltDictList")

	#########################Zusammenfuegen der Tabelleninhalte###############################
	nZeilen = len(inhaltDictList)
	nSpalten = len(inhaltDictList[0])
	inhalt = "    "
	if 0 in strichZeilen:
		inhalt +="\\hline    "
	elif 0 in doppelStrichZeilen:
		inhalt +="\\hline\\hline    "
	for zeilenNr in range (0,nZeilen): #Zeilendurchlauf
		inhaltDict = inhaltDictList[zeilenNr] #Hole i-tes Dict
		keyList = keyListList[zeilenNr] #Hole i-te Keyliste
		nDict = len(inhaltDict)
		nKey = len(keyList)
		if nKey > nDict:
			log.logError("zu viele Keys - Zeile %i" % (zeilenNr+1))
		spaltenNr = 0
		for key in keyList: #Spaltendurchlauf
			if (key in inhaltDict) == None:
				log.logError("falscher Key Namens %s" % key)
			fehler = False
			fehlerUp = False
			fehlerDown = False
			prozentDarstellung = False
			spaltenNr +=1
			zelle = inhaltDict[key]
			if type(zelle) == float:
				faktor = 1
				for subKey in anzahlDezimalStellenDict:
					if key.endswith(subKey):
						schluessel = subKey
						if key.startswith("sigmaUp"):
							fehlerUp=True
						elif key.startswith("sigmaDown"):
							fehlerDown=True
						elif key.startswith("sigma") and not fehlerUp and not fehlerDown:
							fehler=True
						for prozentKey in prozentDarstellungList:
							if subKey.endswith("%s" % prozentKey):
								faktor = 100
								prozentDarstellung = True
				if key in anzahlDezimalStellenDict or fehler or fehlerUp or fehlerDown:
					zelle = zelle * faktor
					zelle = "%15%%d.%df" % (0, anzahlDezimalStellenDict[schluessel]) % zelle
					
				else:
					zelle = "%15%%d.%df" % (0, 2) % zelle
			elif type(zelle) == int:
				zelle = str(zelle)
				
			if ( spaltenNr == 1):
				inhalt = inhalt + "$" + str(zelle)
				
			if spaltenNr != 1:
				if not (fehler or fehlerUp or fehlerDown):
					inhalt = inhalt + "$" + " & " + "$" + zelle
				elif fehler: #Fehlernamen muessen mit "sigma" anfangen und in der keyListList hinter ihren Groessen stehen - z.B. sigma(Up/Down)Messgroesse
					inhalt = inhalt + "\\pm " + zelle
				elif fehlerUp: #Fuer asymmetrische Fehler fuege Up oder Down hinzu
					inhalt = inhalt + "^{+%s}" % (zelle)	
				elif fehlerDown:
					inhalt = inhalt + "_{-%s}" % (zelle)
				else:
					log.logError("Wie konnte das passieren 1???")
				if prozentDarstellung and (fehler or fehlerDown):
					inhalt = inhalt + "\\%"

			if not zeilenNr + 1 in strichZeilen | doppelStrichZeilen: 
				if ( spaltenNr == nKey) and (zeilenNr < nZeilen):
					inhalt = inhalt + "$" + "    \\\\ \n    "
				elif ( spaltenNr == nKey) and (zeilenNr == nZeilen)and not zeilenNr + 1 in strichZeilen:
					inhalt = inhalt + "$"
			elif zeilenNr + 1 in strichZeilen:
				if ( spaltenNr == nKey) and (zeilenNr < nZeilen) and zeilenNr + 1 in strichZeilen:
					inhalt = inhalt + "$" + "    \\\\  " + "  \\hline    "
				elif ( spaltenNr == nKey) and (zeilenNr == nZeilen)and zeilenNr + 1 in strichZeilen:
					inhalt = inhalt + "$" + "    \\hline    "
			elif zeilenNr + 1 in doppelStrichZeilen:
				if ( spaltenNr == nKey) and (zeilenNr < nZeilen) and zeilenNr + 1 in doppelStrichZeilen:
					inhalt = inhalt + "$" + "    \\\\  " + "  \\hline\\hline \n    "
				elif ( spaltenNr == nKey) and (zeilenNr == nZeilen)and zeilenNr + 1 in doppelStrichZeilen:
					inhalt = inhalt + "$" + "    \\hline\\hline    "
	format = "|l|"+ (nSpalten - 1)*"c|"
	tabular = "\\begin{tabular}{%s} %s \\end{tabular} " % (format, inhalt)				
	return tabular

def tableEnvironment(tabular,beschriftung,verweis):
	verweis="tab:" + verweis
	platzierung = "hbp"
	arraystretch = 1.2
	latexTabelle = "\\begin{table}[%s] \\caption{%s} \\centering \\renewcommand{\\arraystretch}{%s} %s \\label{%s}\\end{table}" % (platzierung,beschriftung,arraystretch,tabular,verweis)
	return latexTabelle


def main():
	Test=0.123456789
	Dict1={"1":Test,"2":Test,"3":Test}
	a=0.09
	b=0.0925363333
	sigmab=0.00355555252525
	sigmaUpb=0.0020320320530
	sigmaDownb=0.00032050
	c=Test
	Dict2={"a":int(a),"b":b,"sigmab":sigmab, "sigmaUpb":sigmaUpb,"sigmaDownb":sigmaDownb,"c":c}
	DictList=(Dict1,Dict2)
	keyListList=(("1","2","3"),("a","b","sigmab","sigmaUpb","sigmaDownb","c"))
	anzahlDezimalStellenDict = {"b":4,"1":7} #Fehlerbehaftete Groessen MUESSEN in diese Tabelle eingetragen werden. es genuegt der Wert. Fehler muessen nicht angegeben werden.
	prozendarstellunglist=["b"]
	print latexTabelle("Tst",Test,DictList,keyListList,anzahlDezimalStellenDict,prozentDarstellungList=prozendarstellunglist)

if __name__ == "__main__":
	main()
	
