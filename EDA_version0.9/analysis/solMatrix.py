__author__ = "JinoowW"

from nodeList import*
from stamp import*
from command import *
global gList
gList = {}


def getNodeList(element, label):
    nodeList = []
    voltage_node(element, nodeList)
    resistence_node(element, nodeList)
    capacitor_node(element, nodeList, label)
    inductor_node(element, nodeList, label)
    vccs_node(element, nodeList)
    vcvs_node(element, nodeList)
    cccs_node(element, nodeList)
    ccvs_node(element, nodeList)
    diode_node(element, nodeList)
    mosfet_node(element, nodeList)

    nodeList = list(set(nodeList))
    nodeMap = {}
    i = 0
    for item in nodeList:
        if item != "0":
            nodeMap[item] = i
            i += 1
        else:
            nodeMap[item] = len(nodeList) - 1

    verseMap = {}
    for key in nodeMap:
        verseMap[nodeMap[key]] = key

    return nodeMap, verseMap

def mergeStamps(element, label):
    nodeMap, verseMap = getNodeList(element,label)
    dimen = len(nodeMap) - 1
    stamp = np.zeros((dimen + 1, dimen + 1))
    resStamp(element, nodeMap, stamp)
    vltgStamp(element, nodeMap, stamp)
    vcvsStamp(element, nodeMap, stamp)
    cccsStamp(element, nodeMap, stamp)
    vccsStamp(element, nodeMap, stamp)
    ccvsStamp(element, nodeMap,stamp)

    return stamp, dimen, nodeMap, verseMap

def solMatEquv(element, command, option = "BE"):
    if command["dc"]["flag"] == "dc":
        A, dimen, nodeMap, verseMap = mergeStamps(element, "dc")
        voltagedic, currentdic, srcname, srclist = dc_sol(element, command, A, dimen, nodeMap, verseMap, gList)
        plot_dc(voltagedic, currentdic, srcname, srclist)
    if command["ac"]["flag"] == "ac":
        A, dimen, nodeMap, verseMap = mergeStamps(element, "ac")
        voltageModeDic, voltagePhaseDic, currentModeDic, currentPhaseDic, freqlist = ac_sol(element, command, A, dimen, nodeMap, verseMap)
        plot_ac(voltageModeDic, voltagePhaseDic, currentModeDic, currentPhaseDic, freqlist)
    if command["tran"]["flag"] == "tran":
        A, dimen, nodeMap, verseMap = mergeStamps(element, "tran")
        voltagedic, currentdic, timelist = tran_sol( element, command, A, dimen, nodeMap, verseMap, option, gList)
        #plot_tran(voltagedic, currentdic, timelist)
        #plt.title("node %s voltage"%item)
	"""
        plt.plot(timelist[1:],  voltagedic['1'][1:])
        plt.plot(timelist[1:],  voltagedic['2'][1:])
        plt.plot(timelist[1:],  voltagedic['3'][1:])
        plt.plot(timelist[1:],  voltagedic['4'][1:])
        plt.plot(timelist[1:],  voltagedic['5'][1:])
        plt.plot(timelist[1:],  voltagedic['6'][1:])
	"""

	"""
	plt.plot(timelist[1:],  voltagedic['9'][1:])
        plt.plot(timelist[1:],  voltagedic['7'][1:])
	plt.xlabel("time")
	plt.ylabel("V")
        plt.show()
	"""
	return voltagedic, currentdic, timelist
