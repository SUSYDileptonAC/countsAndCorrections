#!/usr/bin/env python

def makeDC(anaDict):
    print anaDict
    txt = """# Simple counting experiment, with one signal and one background process
imax 1  number of channels
jmax 3  number of backgrounds 
kmax *  number of nuisance parameters (sources of systematical uncertainties)
------------
# we have just one channel, in which we observe 0 events
bin         1
observation %(nObs).0f
------------
# now we list the expected events for signal and all backgrounds in that bin
# the second 'process' line must have a positive number for backgrounds, and 0 for signal
# then we list the independent sources of uncertainties, and give their effect (syst. error)
# on each process and bin
bin                 1           1           1           
process             Sig         EMu         DY       
process             0           1           2           
rate                1           %(nEM).3f          %(nDY).3f 
------------
deltaS  lnN         1.          -           -               -
uncertEMu  lnN      -     %(uncertEM).3f        -           -
EmuStat  gmN        %(nEM)      -       1.00    -           -
uncertDY  lnN       -           -       %(uncertDY).2f      -
""" %anaDict
    return txt

def main():
	from sys import argv
	import pickle

	subcutName = argv[2]
	pklFile = open(argv[1], "r")
	data = pickle.load(pklFile)
	pklFile.close

	regionName =  data.keys()[0]
	n = data[regionName][subcutName]

	rinout = 0.1188
	if subcutName == "CountCuts":
		rinout = 0.0644
	theDict = {
		"nObs": n["edgeMass"]["EE"]+ n["edgeMass"]["MuMu"],
		"nEM":n["edgeMass"]["EMu"] * 0.5*(1.2+1./1.2)*1.025 ,
		"uncertEM":1.05,"uncertFake":1.5,
		"nDY": (n["onShellMass"]["EE"]+ n["onShellMass"]["MuMu"] - n["onShellMass"]["EMu"] * 0.5*(1.2+1./1.2)) * rinout,
		"uncertDY":1.1
		}
	theDict["nFake"] = (theDict["nObs"] - theDict["nEM"]) * 0.05
	print n["edgeMass"]
	#theDict = {"nObs":203,"nEM":137.,"uncertEM":1.05,"nFake":4.,"uncertFake":1.5,"nDY":5.3,"uncertDY":1.5}
	result = makeDC(theDict)
	outFile = open("dataCards/%s_%s.dataCard"%(regionName, subcutName), "w")
	outFile.write(result)
	outFile.close()

main()
