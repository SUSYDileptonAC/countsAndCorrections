
# tool for finding overlap and differences between event lists

# fileName, institute, skipLines, column
ifca = "IFCAOvi_BaselinePlusFatJet.txt", "IFCA", 3, 4
#rwth = "eventList_RWTH_isoTrack.txt", "RWTH", 11, 4
rwth = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/countsAndCorrections/eventCounts_EMu_Data_Run2017D.txt", "RWTH", 4, 2
#rwth2 = "eventList_RWTH_isoTrackLargerSample2.txt", "RWTH", 8, 4
ucsd = "/home/home4/institut_1b/teroerde/Doktorand/SUSYFramework/countsAndCorrections/MuonElectron-eraD_emu.txt", "UCSD", 1, 3

def inFirstNotInSecond(l1, l2):
    return [l for l in l1 if l not in l2]

def compare(list1, list2):
    file1, name1, skip1, pos1 = list1
    file2, name2, skip2, pos2 = list2
    
    in1, in2 = [], []
    with open(file1, "r") as fi:
        for i in range(skip1):
            fi.readline()
        for line in fi:
            evNr = line.split("*")[pos1]
            if len(evNr) > 0:
                in1.append(int(evNr))
    with open(file2, "r") as fi:
        for i in range(skip2):
            fi.readline()
        for line in fi:
            evNr = line.split("*")[pos2]
            if len(evNr) > 0:
                in2.append(int(evNr))
    print len(in1)," events in ",name1," list"
    print len(in2)," events in ",name2," list"
    in1notin2 = inFirstNotInSecond(in1, in2)
    in2notin1 = inFirstNotInSecond(in2, in1)
    print "events in {} but not in {}: {}".format(name1, name2, len(in1notin2))
    print in1notin2
    print "events in {} but not in {}: {}".format(name2, name1, len(in2notin1))
    print in2notin1
#compare(rwth, rwth)
#compare(rwth, ifca)
#print
compare(rwth, ucsd)
#print 
#compare(ifca, ucsd)


#events in RWTH but not in UCSD: 1
#[55091568]
#events in UCSD but not in RWTH: 12
#[217091235, 166688353, 608398223, 92768134, 30736076, 295685617, 603596150, 102167358, 242623044, 416640000, 46599335, 219941964]
