__author__ = "JinoowW"

from RHS import RHS
import matplotlib.pyplot as plt
from stamp import *
from math import fabs
from math import exp
from math import sin
from math import pi
import scipy.sparse
import scipy.sparse.linalg

def pulse_func(v1, v2, td, tr, tf, pw, per, tick):
    if tick < td:
        return v1
    else:
        TScycle = (tick - td)%per
        if TScycle  < tr:
            return TScycle * (v2 - v1) / tr
        elif tr <= TScycle < (tr + pw):
            return v2
        elif (tr + pw) <= TScycle < (tr + pw + tf):
            return (v2 - v1) * (tr + pw + tf - TScycle) / tf
        else:
            return v1

def dc_sol(element, command, A, dimen, nodeMap, verseMap, gList):
    x = np.zeros((dimen, 1))
    voltagedic = {}
    currentdic = {}
    srclist = []
    for i in range(dimen):
        if verseMap[i][0] == "v" or verseMap[i][0] == "e" or verseMap[i] == "h":
            currentdic[verseMap[i]] = []
        else:
            voltagedic[verseMap[i]] = []
    if command["dc"]["iorv"] == "v":
        tmpStore = element["voltage"][command["dc"]["src1"]]["dc_val"]
    else:
        tmpStore = element["current"][command["dc"]["src1"]]["dc_val"]

    srcname = command["dc"]["src1"]
    src = command["dc"]["start1"]
    while(src <= command["dc"]["stop1"]):
        it1 = 0
        srclist.append(src)
        if command["dc"]["iorv"] == "v":
            element["voltage"][command["dc"]["src1"]]["dc_val"] = src
        else:
            element["current"][command["dc"]["src1"]]["dc_val"] = src

        if(element["diode"] or element["mosfet"]):
            tmpsave = []
            epsilon = []
            RHSsave = []
            for it in nodeMap:
                epsilon.append(0.0001)
                tmpsave.append([0])
                RHSsave.append(0)
            tmpsave = tmpsave[:-1]
            counter = 0
            initstate = 1
            while True:
                it1 += 1
                if it1 > 100:
                    break

                nonlinear = np.zeros((dimen+1, dimen+1))
                if (element["diode"]):
                    diodeStamp(element, nodeMap, tmpsave, nonlinear)
                if (element["mosfet"]):
                    mosfetStamp(element, nodeMap, tmpsave, command, initstate, nonlinear, gList)

                initstate = 0

                B = A + nonlinear
                b = RHS(element= element, nodeMap = nodeMap, label = "dc", x = tmpsave, command = command, gList = gList)
                lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(B[:dimen, :dimen]))
                x = lu.solve(b[:dimen])

                tmpx = []
                for i in range(len(x)):
                    tmpx.append(np.fabs(x[i][0] - tmpsave[i]))
                for i in range(dimen):
                    tmpsave[i] = x[i]
                    RHSsave[i] = b[i][0]
                innerflag = 0
                for (it1, it2) in zip(list(tmpx), epsilon):
                    if float(it1) < float(it2):
                        continue
                    else:
                        innerflag = 1
                        break
                if innerflag == 1:
                    continue
                else:
                    break


        else:
            b = RHS(element, nodeMap, "dc")
            lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(A[:dimen, :dimen]))
            x = lu.solve(b[:dimen])
        for i in range(dimen):
            if verseMap[i][0] == "v" or verseMap[i][0] == "e" or verseMap[i] == "h":
                currentdic[verseMap[i]].append(x[i][0])
            else:
                voltagedic[verseMap[i]].append(x[i][0])
        src += command["dc"]["incr1"]
    #W = W[:, 0:i]
    if command["dc"]["iorv"] == "v":
        element["voltage"][command["dc"]["src1"]]["dc_val"] = tmpStore
    else:
        element["current"][command["dc"]["src1"]]["dc_val"] = tmpStore
    """
    for i in range(len(srclist)):
        if (srclist[i] - float(1)) < 0.0001:
            print "v-node1: %fV"%(voltagedic['1'][i])
            print "v-node2: %fV"%(voltagedic['2'][i])
            print "v-node3: %fV"%(voltagedic["3"][i])
            print "c-v2: %fA"%(currentdic["v2"][i])
            print "c-v1: %fA"%(currentdic["v1"][i])
    """


    """
    if filename == "inverter.sp":
    #inverter vtc
        plt.plot(np.array(voltagedic['1']),  np.array(voltagedic['2']))
        plt.ylabel("vout")
        plt.xlabel("vin")
        plt.show()
    elif filename == "nmos.sp" or filename == "pmos.sp":
        #nmos or pmos i-v
        plt.plot(np.array(voltagedic['2']),  -1.0 * np.array(currentdic['v2']))
        plt.ylabel("Id")
        plt.xlabel("vds")
        plt.show()

    else:
        if filename == "diode1.sp":
            print "src: %f, node1: %f, node2: %f"%(srclist[0], voltagedic["1"][0], voltagedic["2"][0])
        for item in voltagedic:
            plt.title("node %s voltage dc_curve"%item)
            plt.ylabel("node %s"%item)
            plt.xlabel("%s"%srcname)
            plt.plot(srclist, voltagedic[item])
            plt.show()

        for item in currentdic:
            plt.title("node %s current dc_curve"%item)
            plt.ylabel("node %s"%item)
            plt.xlabel("%s"%srcname)
            plt.plot(srclist, currentdic[item])
            plt.show()
    """
    #plot_dc(voltagedic, currentdic, srcname, srclist)
    return voltagedic, currentdic, srcname, srclist

def ac_sol(element, command, A, dimen, nodeMap, verseMap):
    voltageModeDic = {}
    currentModeDic = {}
    voltagePhaseDic = {}
    currentPhaseDic = {}
    freqlist = []

    fstart = command["ac"]["fstart"]
    fstop = command["ac"]["fstop"]
    freq = fstart

    pointNumDec = float(command["ac"]["pointNum"])*(fstop - fstart)/10
    pointNumOct = float(command["ac"]["pointNum"])*(fstop - fstart)/8
    pointNumLin = float(command["ac"]["pointNum"])

    for i in range(dimen):
        if verseMap[i][0] == "v" or verseMap[i][0] == "l" or verseMap[i][0] == "e" or verseMap[i] == "h":
            currentModeDic[verseMap[i]] = []
            currentPhaseDic[verseMap[i]] = []
        else:
            voltageModeDic[verseMap[i]] = []
            voltagePhaseDic[verseMap[i]] = []
    if (command["ac"]["type"] == "dec"):
        pointNum = pointNumDec
    elif (command["ac"]["type"] == "ac"):
        pointNum = pointNumOct
    else:
        pointNum = pointNumLin
    interval = int((fstop - fstart)/pointNum)

    while (freq < command["ac"]["fstop"]):
        LC = np.zeros((dimen + 1, dimen + 1), dtype = complex)
        capStamp(element, nodeMap, omega = freq, stamp = LC)
        indStamp(element, nodeMap, omega = freq, stamp = LC)

        B = A +LC
        b = RHS(element, nodeMap, "ac")
        lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(B[:dimen, :dimen]))
        x = lu.solve(b[:dimen])

        for i in range(dimen):
            if verseMap[i][0] == "v" or verseMap[i][0] == "l" or verseMap[i][0] == "e" or verseMap[i] == "h":
                #if freq == 1000:
                    #print "i: %s: %r"%(verseMap[i], x[i][0])
                currentModeDic[verseMap[i]].append(abs(x[i][0]))
                currentPhaseDic[verseMap[i]].append(np.angle(x[i][0], deg = True))
            else:
                #if freq == 1000:
                    #print "v: %s: %r"%(verseMap[i], x[i][0])
                voltageModeDic[verseMap[i]].append(abs(x[i][0]))
                voltagePhaseDic[verseMap[i]].append(np.angle(x[i][0], deg = True))

        freqlist.append(freq)
        freq += interval

    #plot_ac(voltageModeDic, voltagePhaseDic, currentModeDic, currentPhaseDic, freqlist)
    return voltageModeDic, voltagePhaseDic, currentModeDic, currentPhaseDic, freqlist

def tran_sol( element, command, A, dimen, nodeMap, verseMap, option, gList):
    voltagedic = {}
    currentdic = {}
    timelist = []

    for i in range(dimen):
        if verseMap[i][0] == "v" or verseMap[i][0] == "l" or verseMap[i][0] == "c" or verseMap[i][0] == "e" or verseMap[i] == "h":
            currentdic[verseMap[i]] = []
        else:
            voltagedic[verseMap[i]] = []

    tstart = command["tran"]["tstart"]
    tstop = command["tran"]["tstop"]
    tstep = 0.02
    counter = 0
    tick = tstart
    x = np.zeros((dimen, 1))
    conStep = 0.2
    LC = np.zeros((dimen + 1, dimen + 1))
    if option == "BE":
        capStampTranBE(element, nodeMap, step = conStep, stamp = LC)
        indStampTranBE(element, nodeMap, step = conStep, stamp = LC)
    elif option == "TR":
        capStampTranTR(element, nodeMap, step = conStep, stamp = LC)
        indStampTranTR(element, nodeMap, step = conStep, stamp = LC)
    A = (A + LC)
    while tick < tstop:
        counter += 1
        timelist.append(tick)
        initstate = 1
        if element["diode"] or element["mosfet"]:
            diodeList = element["diode"].values()
            mosfetList = element["mosfet"].values()
            tmpsave = []
            epsilon = []
            for it in nodeMap:
                epsilon.append(0.00001)
                tmpsave.append([1])
            while True:
                print tick
                stamp = np.zeros((dimen + 1, dimen + 1))
                diodeStamp(element, nodeMap, tmpsave, stamp)
                mosfetStamp(element, nodeMap, tmpsave, command, initstate, stamp, gList)
                B = A + stamp

                if tick == tstart:
                    b = RHS(element, nodeMap, "dc", tmpsave)
                else:
                    b = RHS(element, nodeMap, "tran", tmpsave, step = conStep, option = option, gList = gList)
                    for v in element["voltage"].values():
                        if v["func"] == "sin":
                            branch_k = nodeMap[v["vname"]]
                            vs_value = v["v0"] + v["va"] * exp((v["td"] - tick - conStep) * v["theta"]) * sin(2*pi*v["freq"]*(tick - conStep - v["td"]))
                            #vs_value = sin(2 * pi * v["freq"] * tick)
                            b[branch_k][0] += float(vs_value)
                        if v["func"] == "pulse":
                            branch_k = nodeMap[v['vname']]
                            vs_value = pulse_func(v["v1"], v["v2"], v["td"], v["tr"], v["tf"], v["pw"], v["per"], tick)
                            b[branch_k][0] += float(vs_value)
                lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(B[:dimen, :dimen]))
                x = lu.solve(b[:dimen])
                print x
                tmpx = []
                for i in range(len(x)):
                    tmpx.append(np.fabs(x[i][0] - tmpsave[i][0]))
                for i in range(dimen):
                    tmpsave[i] = x[i]

                innerflag = 0
                for (it1, it2) in zip(list(tmpx), epsilon):
                    if float(it1) < float(it2):
                        continue
                    else:
                        innerflag = 1
                if innerflag == 1:
                    continue
                else:
                    break

        else:
            if tick == tstart:
                b = RHS(element, nodeMap, "dc")
            else:
                b = RHS(element, nodeMap, "tran", x, step = conStep, option = option)
                for v in element["voltage"].values():
                    if v["func"] == "sin":
                        branch_k = nodeMap[v["vname"]]
                        vs_value = v["v0"] + v["va"] * exp((v["td"] - tick - conStep) * v["theta"]) * sin(2*pi*v["freq"]*(tick - v["td"]))
                        #vs_value = sin(2 * pi * v["freq"] * tick)
                        b[branch_k][0] += float(vs_value)
                    if v["func"] == "pulse":
                        branch_k = nodeMap[v['vname']]
                        vs_value = pulse_func(v["v1"], v["v2"], v["td"], v["tr"], v["tf"], v["pw"], v["per"], tick)
                        b[branch_k][0] += float(vs_value)
            lu = scipy.sparse.linalg.splu(scipy.sparse.csc_matrix(A[:dimen, :dimen]))
            x = lu.solve(b[:dimen])

        for i in range(dimen):
            if verseMap[i][0] == "v" or verseMap[i][0] == "l" or verseMap[i][0] == "c" or verseMap[i][0] == "e" or verseMap[i] == "h":
                currentdic[verseMap[i]].append(x[i][0])
                if counter > 5:
                    if fabs(currentdic[verseMap[i]][counter - 1] - currentdic[verseMap[i]][counter - 2]) < 0.0000000001:
                        #conStep *= 2.0
                        pass
            else:
                voltagedic[verseMap[i]].append(x[i][0])
        tick += tstep

    #plot_tran(voltagedic, currentdic, timelist)
    return voltagedic, currentdic, timelist

def plot_dc(voltagedic, currentdic, srcname, srclist):
    for item in voltagedic:
        plt.title("node %s voltage dc_curve"%item)
        plt.ylabel("node %s"%item)
        plt.xlabel("%s"%srcname)
        plt.plot(srclist, voltagedic[item])
        plt.show()
    for item in currentdic:
        plt.title("node %s current dc_curve"%item)
        plt.ylabel("node %s"%item)
        plt.xlabel("%s"%srcname)
        plt.plot(srclist, currentdic[item])
        plt.show()

def plot_ac(voltageModeDic, voltagePhaseDic, currentModeDic, currentPhaseDic, freqlist):
    for item in voltageModeDic.keys():
        plt.title("node %s voltage magnitude"%item)
        plt.plot(freqlist, voltageModeDic[item])
        plt.show()

        plt.title("node %s voltage phase"%item)
        plt.plot(freqlist, voltagePhaseDic[item])
        plt.show()
    for item in currentModeDic.keys():
        plt.title("device %s current magnitude"%item)
        plt.plot(freqlist, currentModeDic[item])
        plt.show()

        plt.title("device %s current phase"%item)
        plt.plot(freqlist, currentPhaseDic[item])
        plt.show()

def plot_tran(voltagedic, currentdic, timelist):
    for item in voltagedic.keys():
        plt.title("node %s voltage"%item)
        plt.plot(timelist[1:],  voltagedic[item][1:])
        plt.show()

    for item in currentdic.keys():
        plt.title("device %s current"%item)
        plt.plot(timelist[1:], currentdic[item][1:])
        plt.show()
