__author__ = "JinoowW"

import numpy as np
from const import constval
from math import exp

def resStamp(element, nodeMap, stamp):
    resList = element["resistence"].values()
    for res in resList:
        n_plus = nodeMap[res["node1"]]
        n_minus = nodeMap[res["node2"]]
        r_value = res["value"]
        stamp[n_plus][n_plus] += 1.0/(r_value)
        stamp[n_plus][n_minus] += -1.0/(r_value)
        stamp[n_minus][n_plus] += -1.0/(r_value)
        stamp[n_minus][n_minus] += 1.0/(r_value)

def capStamp(element, nodeMap, omega, stamp):
    capList = element["capacitor"].values()

    for cap in capList:
        n_plus = nodeMap[cap["node1"]]
        n_minus = nodeMap[cap["node2"]]
        c_value = cap["value"]
        stamp[n_plus][n_plus] += 1j * omega * c_value
        stamp[n_plus][n_minus] += -1j * omega * c_value
        stamp[n_minus][n_plus] += -1j * omega * c_value
        stamp[n_minus][n_minus] += 1j * omega * c_value

def capStampTranBE(element, nodeMap, step, stamp):
    capList = element["capacitor"].values()

    for cap in capList:
        n_plus = nodeMap[cap["node1"]]
        n_minus = nodeMap[cap["node2"]]
        c_value = cap["value"]
        branch_k = nodeMap[cap["cname"]]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += float(c_value) / float(step)
        stamp[branch_k][n_minus] += -1.0 * float(c_value) / float(step)
        stamp[branch_k][branch_k] += -1.0

def capStampTranTR(element, nodeMap, step, stamp):
    capList = element["capacitor"].values()

    for cap in capList:
        n_plus = nodeMap[cap["node1"]]
        n_minus = nodeMap[cap["node2"]]
        c_value = cap["value"]
        branch_k = nodeMap[cap["cname"]]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += 2.0 * float(c_value) / float(step)
        stamp[branch_k][n_minus] += -2.0 * float(c_value) / float(step)
        stamp[branch_k][branch_k] += -1.0

def indStamp(element, nodeMap, omega, stamp):
    indList = element["inductor"].values()

    for ind in indList:
        n_plus = nodeMap[ind["node1"]]
        n_minus = nodeMap[ind["node2"]]
        branch_k = nodeMap[ind["lname"]]
        l_value = ind["value"]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0
        stamp[branch_k][branch_k] += -1j * omega * l_value

def indStampTranBE(element, nodeMap, step, stamp):
    indList = element["inductor"].values()

    for ind in indList:
        n_plus = nodeMap[ind["node1"]]
        n_minus = nodeMap[ind["node2"]]
        branch_k = nodeMap[ind["lname"]]
        l_value = ind["value"]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][branch_k] += -1.0 * float(l_value) / float(step)
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0

def indStampTranTR(element, nodeMap, step, stamp):
    indList = element["inductor"].values()

    for ind in indList:
        n_plus = nodeMap[ind["node1"]]
        n_minus = nodeMap[ind["node2"]]
        branch_k = nodeMap[ind["lname"]]
        l_value = ind["value"]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][branch_k] += -2.0 * float(l_value) / float(step)
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0

def vltgStamp(element, nodeMap, stamp):
    vList = element["voltage"].values()

    for v in vList:
        n_plus = nodeMap[v["node1"]]
        n_minus = nodeMap[v["node2"]]
        branch_k = nodeMap[v["vname"]]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0

def vcvsStamp(element, nodeMap, stamp):
    vcvsList = element["vcvs"].values()

    for e in vcvsList:
        n_plus = nodeMap[e["node1"]]
        n_minus = nodeMap[e["node2"]]
        ctrn_plus = nodeMap[e["ctrNode1"]]
        ctrn_minus = nodeMap[e["ctrNode2"]]
        branch_k = nodeMap[e["ename"]]
        e_value = e["val"]
        stamp[n_plus][branch_k] += 1.0
        stamp[n_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0
        stamp[branch_k][ctrn_plus] += -1.0 * float(e_value)
        stamp[branch_k][ctrn_minus] += float(e_value)

def cccsStamp(element, nodeMap, stamp):
    cccsList = element["cccs"].values()

    for f in cccsList:
        n_plus = nodeMap[f["node1"]]
        n_minus = nodeMap[f["node2"]]
        ctrn_plus = nodeMap[element["voltage"][f["vname"]]["node1"]]
        ctrn_minus = nodeMap[element["voltage"][f["vname"]]["node2"]]
        f_value = f["val"]
        branch_k = nodeMap[f["vanme"]]
        stamp[n_plus][branch_k] += float(f_val)
        stamp[n_minus][branch_k] += -1.0 * float(f_val)
        stamp[ctrn_plus][branch_k] += 1.0
        stamp[ctrn_minus][branch_k] += -1.0
        stamp[branch_k][n_plus] += 1.0
        stamp[branch_k][n_minus] += -1.0

def vccsStamp(element, nodeMap, stamp):
    vccsList = element["vccs"].values()

    for g in vccsList:
        n_plus = nodeMap[g["node1"]]
        n_minus = nodeMap[g["node2"]]
        ctrn_plus = nodeMap[g["ctrNode1"]]
        ctrn_minus = nodeMap[g["ctrNode2"]]
        g_value = g["val"]
        stamp[n_plus][ctrn_plus] += float(g_value)
        stamp[n_plus][ctrn_minus] += -1.0 * float(g_value)
        stamp[n_minus][ctrn_plus] += -1.0 * float(g_value)
        stamp[n_minus][ctrn_minus] += float(g_value)

def ccvsStamp(element, nodeMap, stamp):
    ccvsList = element["ccvs"].values()

    for h in ccvsList:
        n_plus = nodeMap[h["node1"]]
        n_minus = nodeMap[h["node2"]]
        ctrn_plus = nodeMap[element["voltage"][h["vname"]]["node1"]]
        ctrn_minus = nodeMap[element["voltage"][h["vname"]]["node2"]]
        h_value = h["val"]
        branch_k1 = nodeMap[h["hname"]]
        branch_k2 = nodeMap[h["vname"]]
        stamp[n_plus][branch_k1] += 1.0
        stamp[n_minus][branch_k1] += -1.0
        stamp[ctrn_plus][branch_k2] += 1.0
        stamp[ctrn_minus][branch_k2] += -1.0
        stamp[branch_k1][n_plus] += 1.0
        stamp[branch_k1][n_minus] += -1.0
        stamp[branch_k1][branch_k2] += -1.0 * float(h_value)
        stamp[branch_k2][ctrn_plus] += 1.0
        stamp[branch_k2][ctrn_minus] += -1.0

def diodeStamp(element, nodeMap, x, stamp):
    diodeList = element["diode"].values()

    for d in diodeList:
        n_plus = nodeMap[d["node1"]]
        n_minus = nodeMap[d["node2"]]
        if(d["node1"] == "0"):
            u_before = -1.0 * x[n_minus][0]
        elif(d["node2"] == "0"):
            u_before = x[n_plus][0]
        else:
            u_before = x[n_plus][0] - x[n_minus][0]
        gn = 40.0*exp(40.0*u_before)
        stamp[n_plus][n_plus] += gn
        stamp[n_plus][n_minus] += -1.0 * gn
        stamp[n_minus][n_plus] += -1.0 * gn
        stamp[n_minus][n_minus] += gn

def mosfetStamp(element, nodeMap, x, command, initstate, stamp, gList):
    mosfetList = element["mosfet"].values()
    modelList = command["model"]
    for m in mosfetList:
        m1 = {}
        nd = nodeMap[m["nd"]]
        ng = nodeMap[m["ng"]]
        ns = nodeMap[m["ns"]]
        if(m["nd"] == "0"):
            if(m["ng"] == "0"):
                if(m["ns"] == "0"):
                    vgs = 0
                    vds = 0
                else:
                    vgs = -1.0 * x[ns][0]
                    vds = -1.0 * x[ns][0]
            else:#ng != 0
                if(m["ns"] == "0"):
                    vgs = x[ng][0]
                    vds = 0
                else:#ng != 0, ns != 0
                    vgs = x[ng][0] - x[ns][0]
                    vds = -1.0 * x[ns][0]
        else:
            if(m["ng"] == "0"):
                if(m["ns"] == "0"):
                    vgs = 0
                    vds = x[nd][0]
                else:
                    vgs = -1.0 * x[ns][0]
                    vds = x[nd][0] - x[ns][0]
            else:#ng != 0
                if(m["ns"] == "0"):
                    vgs = x[ng][0]
                    vds = x[nd][0]
                else:#ng != 0, ns != 0
                    vgs = x[ng][0] - x[ns][0]
                    vds = x[nd][0] - x[ns][0]
        aspectRatio = m["w"] / m["l"]

        if (initstate):
            gm = 0.00001
            gds = 0.00001
        else:
            if modelList[m["mname"]]["mtype"] == "nmos":
                if vds > (vgs - constval._VTN):
                    gm = constval._KN_PRIME * aspectRatio * (vgs - constval._VTN) * (1.0 + constval._CLM_N * vds)
                    gds = constval._KN_PRIME / 2.0 *constval._CLM_N * aspectRatio * ((vgs - constval._VTN) ** 2)
                elif 0 <= vds <= (vgs - constval._VTN):
                    gm = constval._KN_PRIME * aspectRatio * vds * (1 + constval._CLM_N * vds)
                    gds = constval._KN_PRIME * aspectRatio * (vgs - constval._VTN + 2 * constval._CLM_N * (vgs - constval._VTN) * vds - vds - 1.5 * constval._CLM_N * vds * vds)
                else:
                    gm = constval._KN_PRIME * aspectRatio * vds
                    gds =  constval._KN_PRIME * aspectRatio * (vgs - constval._VTN - vds)
            elif modelList[m["mname"]]["mtype"] == "pmos":
                if vds < vgs - constval._VTP:
                    gm =  constval._KP_PRIME * aspectRatio * (vgs - constval._VTP) * (1.0 + constval._CLM_P * vds)
                    gds = constval._KP_PRIME / 2.0 *constval._CLM_P * aspectRatio * ((vgs - constval._VTP) ** 2)
                elif vds >= vgs - constval._VTP:
                    gm = constval._KP_PRIME * aspectRatio * vds * (1 + constval._CLM_P * vds)
                    gds = constval._KP_PRIME * aspectRatio * (vgs - constval._VTP + 2 * constval._CLM_P * (vgs - constval._VTP) * vds - vds - 1.5 * constval._CLM_P * vds * vds)
                else:
                    gm = constval._KP_PRIME * aspectRatio * vds
                    gds =  constval._KP_PRIME * aspectRatio * (vgs - constval._VTP - vds)

        m1["gm"] = gm
        m1["gds"] = gds
        gList[m["mosname"]] = m1
        stamp[nd][nd] += gds
        stamp[nd][ns] += -1.0 * gds - gm
        stamp[nd][ng] += gm
        stamp[ns][nd] += -1.0 * gds
        stamp[ns][ns] += gds + gm
        stamp[ns][ng] += -1.0 * gm
