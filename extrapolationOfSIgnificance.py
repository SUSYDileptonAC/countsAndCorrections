#!/usr/bin/env python

def uncertExtrapolation(fullUncert, relUncert, lumiFactor):
	from math import sqrt
	massRegionRatioABC =  341.1 * 1./ 949.2
	backgroundABC = 932.5
	systUncert = massRegionRatioABC * backgroundABC * 0.06
	assert systUncert < fullUncert, "%.1f %.1f"%(systUncert, fullUncert)

	statUncert= sqrt( fullUncert**2 - systUncert**2)
	return sqrt((lumiFactor * systUncert * relUncert * 1./0.06)**2 + (sqrt(lumiFactor) * statUncert)**2)


def main():
	from math import sqrt
	fitABC = [81.3, 24.5]
	fitAB = [43.7, 18.5]

	cncABC = [84.5, 27.6, 20.8]
	cncAB = [42.5, 21.0, 12.3]



	lumiFactor = 20 * 1./9.2

	print "lumi         | cut & count |    fit"
	print "5.1 fbi      | %8.1f sigma | %8.1f sigma "%(cncAB[0] * 1./ sqrt(cncAB[1]**2 + cncAB[2]**2), 
		fitAB[0] * 1./ fitAB[1])
	print "9.2 fbi      | %8.1f sigma | %8.1f sigma "%(cncABC[0] * 1./ sqrt( cncABC[1]**2 + cncABC[2]**2),
		fitABC[0] * 1./ fitABC[1])
	print "20  fbi (6%%) | %8.1f sigma | %8.1f sigma "%(  cncABC[0] * 1./ sqrt( cncABC[1]**2 + 1./lumiFactor *cncABC[2]**2),
	 fitABC[0]*lumiFactor * 1./ uncertExtrapolation(fitABC[1], 0.06, lumiFactor))
	print "20  fbi (5%%) | %8.1f sigma | %8.1f sigma "%(  cncABC[0] * 1./ sqrt( (0.05 * 1./0.06 * cncABC[1])**2 + 1./lumiFactor *cncABC[2]**2),
		fitABC[0]*lumiFactor * 1./ uncertExtrapolation(fitABC[1], 0.05, lumiFactor))

main()