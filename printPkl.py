#!/usr/bin/env python

def main():
	import pickle
	from pprint import pprint
	from sys import argv

	pkl = open(argv[1], "r")
	pprint(pickle.load(pkl))
	pkl.close()

main()
