__author__ = "JinoowW"

import numpy as np
from const import constval
from math import exp

def currentRHS(element, RHSmat, nodeMap):
    iList = element["current"].values()
    for cs in iList:
        n_plus = nodeMap[cs["node1"]]
        n_minus = nodeMap[cs["node2"]]
        cs_value = cs["dc_val"]
        RHSmat[n_plus][0] += -1.0 * float(cs_value)
        RHSmat[n_minus][0] += float(cs_value)

def voltageRHS(element, RHSmat, nodeMap):
    vList = element["voltage"].values()
    for vs in vList:
        branch_k = nodeMap[vs["vname"]]
        vs_value = vs["dc_val"]
        RHSmat[branch_k][0] += float(vs_value)

def cccsRHS(element, RHSmat, nodeMap):
    fList = element["cccs"].values()
    for f in fList:
        branch_k = nodeMap[f["vname"]]
        v_value = element["voltage"][f["vname"]]["dc_value"]
        RHSmat[branch_k][0] += float(v_value)

def ccvsRHS(element, RHSmat, nodeMap):
    hList = element["ccvs"].values()
    for h in hList:
        branch_k = nodeMap[h["vname"]]
        v_value = element["voltage"][h["vname"]]["dc_value"]
        RHSmat[branch_k][0] += float(v_value)

def diodeRHS(element, x, RHSmat, nodeMap):
    dList = element["diode"].values()
    for d in dList:
        n_plus = nodeMap[d["node1"]]
        n_minus = nodeMap[d["node2"]]
        if(d["node1"] == "0"):
            u_n = -1.0 * x[n_minus][0]
        elif(d["node2"] == "0"):
            u_n = x[n_plus][0]
        else:
            u_n = x[n_plus][0] - x[n_minus][0]
        #print u_n
        i_n = exp(40*u_n) - 1.0
        gn = 40.0*exp(40.0*u_n)
        RHSmat[n_plus] += -1.0 * (i_n - u_n * gn)
        RHSmat[n_minus] += i_n - u_n * gn

def mosfetRHS(element, x, RHSmat, nodeMap, gList, modelList):
    mList = element["mosfet"].values()
    for m in mList:
        nd = nodeMap[m["nd"]]
        ng = nodeMap[m["ng"]]
        ns = nodeMap[m["ns"]]
        gm = gList[m["mosname"]]["gm"]
        gds = gList[m["mosname"]]["gds"]
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
        if modelList[m["mname"]]["mtype"] == "nmos":
            if 0 <= vds <= vgs - constval._VTN:
                Id = constval._KN_PRIME * m["w"] / m["l"] * ((vgs - constval._VTN) * vds - 0.5 * vds * vds) * (1.0 + constval._CLM_N * vds) - gds * vds - gm * vgs
            elif vds > vgs - constval._VTN:
                Id = constval._KN_PRIME * m["w"] / m["l"] / 2.0 * ((vgs - constval._VTN)**2) * (1.0 + constval._CLM_N * vds) - gds * vds - gm * vgs
            else:
                Id = constval._KN_PRIME * m["w"] / m["l"] * ((vgs-constval._VTN) * vds-1./2.*vds**2) - gds * vds - gm * vgs
        elif modelList[m["mname"]]["mtype"] == "pmos":
            if 0 >= vds >= (vgs - constval._VTP):
                Id = constval._KP_PRIME * m["w"] / m["l"] * ((vgs - constval._VTP) * vds - 0.5 * vds * vds) * (1.0 + constval._CLM_P * vds) - gds * vds - gm * vgs
            elif vds < (vgs - constval._VTP):
                Id = constval._KP_PRIME * m["w"] / m["l"] / 2.0 * ((vgs - constval._VTP) ** 2) * (1.0 + constval._CLM_P * vds) - gds * vds - gm * vgs
            else:
                Id = constval._KP_PRIME * m["w"] / m["l"] * ((vgs-constval._VTP) * vds-1./2.*vds**2) - gds * vds - gm * vgs

        RHSmat[nd] += -1.0 * Id
        RHSmat[ns] += Id

def capacitorRHS(element, x, RHSmat, nodeMap, step, option):
    cList = element["capacitor"].values()
    for c in cList:
        branch_k = nodeMap[c["cname"]]
        c_value = c["value"]
        inode = x[nodeMap[c["cname"]]][0]
        if option == "BE":
            if c["node1"] == "0":
                vnode2 = x[nodeMap[c["node2"]]][0]
                RHSmat[branch_k][0] += -1.0 * vnode2 * float(c_value) / float(step)
            elif c["node2"] == "0":
                vnode1 = x[nodeMap[c["node1"]]][0]
                RHSmat[branch_k][0] += vnode1 * float(c_value) / float(step)
            else:
                vnode1 = x[nodeMap[c["node1"]]][0]
                vnode2 = x[nodeMap[c["node2"]]][0]
                RHSmat[branch_k][0] += (vnode1 - vnode2) * float(c_value) / float(step)

        elif option == "TR":
            if c["node1"] == "0":
                vnode2 = x[nodeMap[c["node2"]]][0]
                RHSmat[branch_k][0] += -2.0 * vnode2 * float(c_value) / float(step) + inode
            elif c["node2"] == "0":
                vnode1 = x[nodeMap[c["node1"]]][0]
                RHSmat[branch_k][0] += 2.0 * vnode1 * float(c_value) / float(step) + inode
            else:
                vnode1 = x[nodeMap[c["node1"]]][0]
                vnode2 = x[nodeMap[c["node2"]]][0]
                RHSmat[branch_k][0] += 2.0 * (vnode1 - vnode2) * float(c_value) / float(step) + inode

def inductorRHS(element, x, RHSmat, nodeMap, step, option):
    lList = element["inductor"].values()
    for l in lList:
        branch_k = nodeMap[l["lname"]]
        l_value = l["value"]
        inode = x[branch_k][0]
        if option == "BE":
            RHSmat[branch_k][0] += -1.0 * inode * float(l_value) / float(step)
        elif option == "TR":
            if l["node1"] == "0":
                vnode2 = x[nodeMap[l["node2"]]][0]
                RHSmat[branch_k][0] += -2.0 * inode * float(l_value) / float(step) + vnode2
            elif l["node2"] == "0":
                vnode1 = x[nodeMap[l["node1"]]][0]
                RHSmat[branch_k][0] += -2.0 * inode * float(l_value) / float(step) - vnode1
            else:
                vnode1 = x[nodeMap[l["node1"]]][0]
                vnode2 = x[nodeMap[l["node2"]]][0]
                RHSmat[branch_k][0] += -2.0 * inode * float(l_value) / float(step) - vnode1 + vnode2

def RHS(element, nodeMap, label, x = 0, step = 1, option = "BE", command = {}, gList = {}):
    dimen = len(nodeMap)
    RHSmat =  np.zeros((dimen, 1))
    if command.has_key("model"):
        modelList = command["model"]
    else:
        modelList = {}
    currentRHS(element, RHSmat, nodeMap)
    voltageRHS(element, RHSmat, nodeMap)
    cccsRHS(element, RHSmat, nodeMap)
    ccvsRHS(element, RHSmat, nodeMap)
    diodeRHS(element, x, RHSmat, nodeMap)
    if modelList:
        mosfetRHS(element, x, RHSmat, nodeMap, gList, modelList)
    if label == "tran":
        capacitorRHS(element, x, RHSmat, nodeMap, step, option)
        inductorRHS(element, x, RHSmat, nodeMap, step, option)

    return RHSmat
