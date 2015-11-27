def readTreeFromFile(path, dileptonCombination, preselection = "nJets >= 2",SingleLepton=False,use532=False):
	"""
	helper function
	path: path to .root file containing simulated events
	dileptonCombination: EE, EMu, or MuMu for electron-electron, electron-muon, or muon-muon events

	returns: tree containing events for on sample and dileptonCombination
	"""
	from ROOT import TChain
	chain = TChain()
#	chain.Add("%s/ETH2AachenNtuples/%sDileptonTree"%(path, dileptonCombination))
	if SingleLepton:
		chain.Add("%s/cutsV22DileptonFinalTriggerTrees/%sDileptonTree"%(path, dileptonCombination))
	elif use532:	
		chain.Add("%s/cutsV22DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	else:	
		chain.Add("%s/cutsV23DileptonFinalTrees/%sDileptonTree"%(path, dileptonCombination))
	result = chain.CopyTree(preselection)
#	result = chain
	return result

	return chain

def loadPickles(path):
	from glob import glob
	import pickle
	result = {}
	for pklPath in glob(path):
		pklFile = open(pklPath, "r")
		#~ result.update(pickle.load(pklFile))
		result[pklPath] = pickle.load(pklFile)
	return result


