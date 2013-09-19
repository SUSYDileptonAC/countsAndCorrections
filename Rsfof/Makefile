CALCULATOR = python Rsfof.py
TABLEMAKER = python makeRSFOFTables.py
CORRECTIONS = python fullCorrections.py
ANPATH = /home/jan/Doktorarbeit/Dilepton/projects/DileptonAN/tables

Data:
	$(CALCULATOR) Inclusive Data
	$(CALCULATOR) Barrel Data
	$(CALCULATOR) Endcap Data
MC:
	$(CALCULATOR) Inclusive MC
	$(CALCULATOR) Barrel MC
	$(CALCULATOR) Endcap MC
	
tables: 
	$(TABLEMAKER)

copyAN:
	cp tab/* $(ANPATH)
	
all: Data MC tables copyAN

calcCorrs:
	$(CORRECTIONS)
