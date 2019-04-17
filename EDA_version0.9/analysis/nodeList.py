__author__ = "JinoowW"

def voltage_node(element, nodeList):
    voltage = element["voltage"]
    vList = voltage.values()
    for v in vList:
        nodeList.append(v["node1"])
        nodeList.append(v["node2"])
        nodeList.append(v["vname"])

def resistence_node(element, nodeList):
    resistence = element["resistence"]
    resList = resistence.values()
    for res in resList:
        nodeList.append(res["node1"])
        nodeList.append(res["node2"])

def capacitor_node(element, nodeList, label):
    capacitor = element["capacitor"]
    capList = capacitor.values()
    for cap in capList:
        nodeList.append(cap["node1"])
        nodeList.append(cap["node2"])
        if label == "tran":
            nodeList.append(cap["cname"])

def inductor_node(element, nodeList, label):
    inductor = element["inductor"]
    indList = inductor.values()
    for ind in indList:
        nodeList.append(ind["node1"])
        nodeList.append(ind["node2"])
        if label != "dc":
            nodeList.append(ind["lname"])

def vccs_node(element, nodeList):
    vccs = element["vccs"]
    GList = vccs.values()
    for g in GList:
        nodeList.append(g["node1"])
        nodeList.append(g["node2"])
        nodeList.append(g["ctrNode1"])
        nodeList.append(g["ctrNode2"])

def vcvs_node(element, nodeList):
    vcvs = element["vcvs"]
    EList = vcvs.values()
    for e in EList:
        nodeList.append(e["node1"])
        nodeList.append(e["node2"])
        nodeList.append(e["ename"])
        nodeList.append(e["ctrNode1"])
        nodeList.append(e["ctrNode2"])

def cccs_node(element, nodeList):
    cccs = element["cccs"]
    FList = cccs.values()
    for f in FList:
        nodeList.append(f["node1"])
        nodeList.append(f["node2"])

def ccvs_node(element, nodeList):
    ccvs = element["ccvs"]
    HList = ccvs.values()
    for h in HList:
        nodeList.append(h["hname"])
        nodeList.append(h["node1"])
        nodeList.append(h["node2"])

def diode_node(element, nodeList):
    diode = element["diode"]
    dList = diode.values()
    for d in dList:
        nodeList.append(d["node1"])
        nodeList.append(d["node2"])

def mosfet_node(element, nodeList):
    mosfet = element["mosfet"]
    mList = mosfet.values()
    for m in mList:
        nodeList.append(m["nd"])
        nodeList.append(m["ng"])
        nodeList.append(m["ns"])
