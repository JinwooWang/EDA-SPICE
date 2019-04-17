__author__ = "JinoowW"
import re

def getFloat(inStr):
    if isfloat(inStr):
        return float(inStr)
    elif inStr[-3:] == "meg":
        return float(inStr[:-3]) * pow(10, 6)
    elif inStr[-2:] == "ns":
        return float(inStr[:-2])
    elif inStr[-2:] == "ps":
        return float(inStr[:-2]) * pow(10, -12)
    elif inStr[-2] == "e" and isfloat(inStr[-1]):
        return float(inStr[:-2]) * pow(10, float(inStr[-1]))
    elif inStr[-3] == "e" and isfloat(inStr[-2:]):
        return float(inStr[:-3]) * pow(10, float(inStr[-2:]))

def isfloat(input_string):
    try:
        float(input_string)
        return True
    except:
        return False

def func_pulse(v, line):
    if re.match(".*\((.*)\).*", line) != None:
        pulse_ele = re.match(".*\((.*)\).*", line).group(1).split()
    else:
        pulse_ele = matchedV[4:]

    #V1 V2 TD TR TF PW PER
    v["v1"] = float(pulse_ele[0])
    v["v2"] = float(pulse_ele[1])
    v["td"] = getFloat(pulse_ele[2])
    v["tr"] = getFloat(pulse_ele[3])
    v["tf"] = getFloat(pulse_ele[4])
    v["pw"] = getFloat(pulse_ele[5])
    v["per"] = getFloat(pulse_ele[6])

def func_sin(v, line):
    sin_ele = re.match(".*\((.*)\).*", line).group(1).split()
    #print "sin_ele: ", sin_ele
    #V0 VA FREQ TD THETA

    v["v0"] = float(sin_ele[0])
    v["va"] = float(sin_ele[1])
    v["freq"] = getFloat(sin_ele[2])
    v["td"] = 0.0
    v["theta"] = 0.0
    if len(sin_ele) > 3:
        v["td"] = getFloat(sin_ele[3])
        v["theta"] = getFloat(sin_ele[4])

def VltgMatch(VltgMatchObj, voltage, line):
    matchedV = VltgMatchObj.group().split()
    v = {}
    v["vname"] = matchedV[0]
    v["node1"] = matchedV[1]
    v["node2"] = matchedV[2]
    v["dc_val"] = 0.0
    v["func"] = None
    if len(matchedV) > 3:
        if matchedV[3] == "dc" and isfloat(matched[4]):
            v["dc_val"] = matchedV[4]
            if matchedV[5] == "ac":
                if isfloat(matchedV[6]):
                    v["ac_mag"] = float(matchedV[6])
                    if isfloat(matchedV[7]):
                        v["ac_phase"] = float(matchedV[7])
                    else:
                        if matchedV[7][0:5] == "pulse":
                            v["func"] = "pulse"
                            func_pulse(v, line)
                        elif matchedV[7][0:3] == "sin":
                            v["func"] = "sin"
                            func_sin(v, line)
            elif matchedV[5][0:5] == "pulse":
                v["func"] = "sin"
                func_pulse(v,line)
            elif matchedV[5][0:3] == "sin":
                v["func"] = "pulse"
                func_sin(v, line)
        elif matchedV[3][0:5] == "pulse":
            v["func"] = "pulse"
            func_pulse(v,line)
        elif matchedV[3][0:3] == "sin":
            v["func"] = "sin"
            func_sin(v, line)
        elif isfloat(matchedV[3]):
            v["dc_val"] = float(matchedV[3])

    if not voltage.has_key("%s"%matchedV[0]):
        voltage["%s"%matchedV[0]] = v
    else:
        print "REDEFINED %s in line %d"%(matchedV[0], lineNum)
    #return voltage

def CurrFlowMatch(CurrFlowMatchObj, current):
    matchedI = CurrFlowMatchObj.group().split()
    i = {}
    i["node1"] = matchedI[1]
    i["node2"] = matchedI[2]

    if matchedI[3] == "ac":
        i["mag"] = matchedI[4]
        i["phase"] = matchedI[5]
        i["std_form"] = matchedI[6]
    elif matchedI[3] == "dc":
        i["dc_val"] = matchedI[4]
        if matchedI[5] == "ac":
            i["mag"] = matchedI[6]
            i["phase"] = matchedI[7]
            i["std_form"] = matchedI[8]
    elif isfloat(matchedI[3]):
        i["dc_val"] = float(matchedI[3])
        if len(matchedI) > 4:
            if matchedI[4] == "ac":
                i["mag"] = matchedI[5]
                i["phase"] = matchedI[6]
                i["std_form"] = matchedI[7]
    if not current.has_key("%s"%matchedI[0]):
        current["%s"%matchedI[0]] = i
    else:
        print "REDEFINED %s in line %d"%(matchedI[0], lineNum)
    #return current

def ResMatch(ResMatchObj, resistence):
    matchedR = ResMatchObj.group().split()
    l = len(matchedR)
    r = {}
    r["node1"] = matchedR[1]
    r["node2"] = matchedR[2]

    if l == 4:
        if matchedR[3][-1] == "k":
            r["value"] = float(matchedR[3][:-1])*1000
        else:
            r["value"] = float(matchedR[3])

    elif l == 6:
        r["M_NAME"] = matchedR[3]
        _, r["length"] = matchedR[4].split("=")
        _, r["width"] = matchedR[5].split("=")

    if not resistence.has_key("%s"%matchedR[0]):
        resistence["%s"%matchedR[0]] = r
    else:
        print "REDEFINED %s in line %d"%(matchedR[0], lineNum)
    #return resistence

def CapMatch(CapMatchObj, capacitor):
    matchedC = CapMatchObj.group().split()
    l = len(matchedC)
    c = {}
    c["cname"] = matchedC[0]
    c["node1"] = matchedC[1]
    c["node2"] = matchedC[2]

    if l == 4:
        if matchedC[3][-1] == "p":
            c["value"] = float(matchedC[3][:-1]) * pow(10, -12)
        elif matchedC[3][-1] == "f":
            c["value"] = float(matchedC[3][:-1]) * pow(10, -15)
        elif matchedC[3][-1] == "a":
            c["value"] = float(matchedC[3][:-1]) * pow(10, -18)
        elif matchedC[3][-1] == "u":
            c["value"] = float(matchedC[3][:-1]) * pow(10, -6)
        elif matchedC[3][-1] == "m":
            c["value"] = float(matchedC[3][:-1]) * pow(10, -3)
        else:
            c["value"] = float(matchedC[3])
    else:
        c["mname"] = matchedC[3]
        _, c["l"] = matchedC[4].split("=")
        if l == 6:
            _, c["w"] = matchedC[5].split("=")
        else:
            c["w"] = "Default"
    if not capacitor.has_key("%s"%matchedC[0]):
        capacitor["%s"%matchedC[0]] = c
    else:
        print "REDEFINED %s in line %d"%(matchedC[0], lineNum)
    #return capacitor

def IndMatch(IndMatchObj, inductor):
    matchedL = IndMatchObj.group().split()
    l = {}
    l["lname"] = matchedL[0]
    l["node1"] = matchedL[1]
    l["node2"] = matchedL[2]

    if len(matchedL) == 4:
        if matchedL[3][-1] == "u":
            l["value"] = float(matchedL[3][:-1]) * pow(10, -6)
        elif matchedL[3][-1] == "m":
            l["value"] = float(matchedL[3][:-1]) * pow(10, -3)
        else:
            l["value"] = float(matchedL[3])

    if len(matchedL) == 5:
        _, l["IC"] = matchedL[4].split("=")
    if not inductor.has_key("%s"%matchedL[0]):
        inductor["%s"%matchedL[0]] = l
    else:
        print "REDEFINED %s in line %d"%(matchedL[0], lineNum)
    #return inductor

def DiodeMatch(DiodeMatchObj, diode):
    matchedD = DiodeMatchObj.group().split()
    d = {}
    d["node1"] = matchedD[1]
    d["node2"] = matchedD[2]
    d["mname"] = matchedD[3]
    if len(matchedD) > 4:
        if not bool(re.search("=", matchedM[4])):
            d["area"] = matchedD[4]
            if len(matchedD) > 5:
                if not bool(re.search("=", matchedM[5])):
                    d["off"] = matchedD[5]
                    if len(matchedD) > 6:
                        _, d["ic"] = matchedD[6].split("=")
                else:
                    _, d["ic"] = matchedD[5].split("=")
        else:
            _, d["ic"] = matchedD[4].split("=")
    if not diode.has_key("%s"%matchedD[0]):
        diode["%s"%matchedD[0]] = d
    else:
        print "REDEFINED %s in line %d"%(matchedD[0], lineNum)
    #return diode

def VCVSMatch(VCVSMatchObj, vcvs):
    matchedE = VCVSMatchObj.group().split()
    e = {}
    e["ename"] = matchedE[0]
    e["node1"] = matchedE[1]
    e["node2"] = matchedE[2]
    e["ctrNode1"] = matchedE[3]
    e["ctrNode2"] = matchedE[4]
    e["val"] = matchedE[5]
    if not vcvs.has_key("%s"%matchedE[0]):
        vcvs["%s"%matchedE[0]] = e
    else:
        print "REDEFINED %s in line %d"%(matchedE[0], lineNum)
    #return vcvs

def CCCSMatch(CCCSMatchObj, cccs):
    matchedF = CCCSMatchObj.group().split()
    f = {}
    f["node1"] = matchedF[1]
    f["node2"] = matchedF[2]
    f["vname"] = matchedF[3]
    f["val"] = matchedF[4]
    if not cccs.has_key("%s"%matchedF[0]):
        cccs["%s"%matchedF[0]] = f
    else:
        print "REDEFINED %s in line %d"%(matchedF[0], lineNum)
    #return cccs

def VCCSMatch(VCCSMatchObj, vccs):
    matchedG = VCCSMatchObj.group().split()
    g = {}
    g["node1"] = matchedG[1]
    g["node2"] = matchedG[2]
    g["ctrNode1"] = matchedG[3]
    g["ctrNode2"] = matchedG[4]
    g["val"] = matchedG[5]
    if not vccs.has_key("%s"%matchedG[0]):
        vccs["%s"%matchedG[0]] = g
    else:
        print "REDEFINED %s in line %d"%(matchedG[0], lineNum)
    #return vccs

def CCVSMatch(CCVSMatchObj, ccvs):
    matchedH = CCVSMatchObj.group().split()
    h = {}
    h["hname"] = matchedH[0]
    h["node1"] = matchedH[1]
    h["node2"] = matchedH[2]
    h["vname"] = matchedH[3]
    h["val"] = matchedH[4]
    if not ccvs.has_key("%s"%matchedH[0]):
        ccvs["%s"%matchedH[0]] = h
    else:
        print "REDEFINED %s in line %d"%(matchedH[0], lineNum)
    #return ccvs

def MOSFETMatch(MOSFETMatchObj, mosfet):
    matchedM = MOSFETMatchObj.group().split()
    l = len(matchedM)
    m = {}
    m["mosname"] = matchedM[0]
    m["nd"] = matchedM[1]
    m["ng"] = matchedM[2]
    m["ns"] = matchedM[3]
    m["nb"] = matchedM[4]
    m["mname"] = matchedM[5]
    for i in range(6, l):
        if bool(re.search("=", matchedM[i])):
            _key, _value = matchedM[i].split("=")
            if isfloat(_value):
                m[_key] = float(_value)
            else:
                m[_key] = float(_value[:-1])
                if _value[-1] == "u":
                    m[_key] *= 1e-6
                elif _value[-1] == "p":
                    m[_key] *= 1e-12
        else:
            m["off"] = matchedM[i]
    if not mosfet.has_key("%s"%matchedM[0]):
        mosfet["%s"%matchedM[0]] = m
    else:
        print "REDEFINED %s in line %d"%(matchedM[0], lineNum)
    #return mosfet

def DCMatch(DCMatchObj, dc):
    matchedDC = DCMatchObj.group().split()
    if len(matchedDC) != 5 and len(matchedDC) != 9:
        print "ERROR!"
    dc["flag"] = "dc"
    dc["src1"] = matchedDC[1]
    if dc["src1"][0] == "v":
        dc["iorv"] = "v"
    else:
        dc["iorv"] = "i"
    dc["start1"] = float(matchedDC[2])
    dc["stop1"] = float(matchedDC[3])
    dc["incr1"] = float(matchedDC[4])
    if len(matchedDC) == 9:
        dc["src2"] = matchedDC[5]
        dc["start2"] = float(matchedDC[6])
        dc["stop2"] = float(matchedDC[7])
        dc["incr2"] = float(matchedDC[8])

    #return dc

def ACMatch(ACMatchObj, ac):
    matchedAC = ACMatchObj.group().split()
    if len(matchedAC) != 5:
        print "ERROR! in line %d", lineNum
    ac["flag"] = "ac"
    ac["type"] = matchedAC[1]
    ac["pointNum"] = matchedAC[2]
    if matchedAC[3][-1] == "k":
        ac["fstart"] = float(matchedAC[3][:-1]) * 1000
    elif matchedAC[3][-3:] == "meg":
        ac["fstart"] = float(matchedAC[3][:-3]) * 1000000
    else:
        ac["fstart"] = float(matchedAC[3])

    if matchedAC[4][-1] == "k":
        ac["fstop"] = float(matchedAC[4][:-1]) * 1000
    elif matchedAC[4][-3:] == "meg":
        ac["fstop"] = float(matchedAC[4][:-3]) * 1000000
    else:
        ac["fstop"] = float(matchedAC[4])

def TRANMatch(TRANMatchObj, tran):
    matchedTRAN = TRANMatchObj.group().split()
    l = len(matchedTRAN)

    for i in range(1, len(matchedTRAN)):
        if matchedTRAN[i][-2:] == "ns":
            matchedTRAN[i] = float(matchedTRAN[i][:-2])
            tran["unite"] = "ns"

    if l < 3 or l > 5:
        print "ERROR! in line %d", lineNum
    tran["flag"] = "tran"
    tran["tstep"] = matchedTRAN[1]
    tran["tstop"] = matchedTRAN[2]
    if l == 3:
        tran["tstart"] = 0
        tran["tmax"] = 0
    elif l == 4:
        tran["tstart"] = matchedTRAN[3]
        tran["tmax"] = 0
    else:
        tran["tstart"] = matchedTRAN[3]
        tran["tmax"] = matchedTRAN[4]
    #return tran

def PRTMatch(PRTMatchObj, prt):
    matchedPRT = PRTMatchObj.group().split()
    prt["type"] = matchedPRT[1]
    prt["ele"] = matchedPRT[2:]
    #return prt

def MODMatch(MODMatchObj, model, line):
    matchedMOD = MODMatchObj.group().split()
    mod = {}
    mod["mname"] = matchedMOD[1]
    mod["mtype"] = matchedMOD[2]
    if re.match(".*\((.*)\).*", line) != None:
        tmplist = re.match(".*\((.*)\).*", line).group(1).split()
    else:
        tmplist = matchedMOD[3:]
    for item in tmplist:
        _key, _value = item.split("=")
        mod[_key] = _value
    if not model.has_key("%s"%matchedMOD[0]):
        model["%s"%matchedMOD[1]] = mod
    else:
        print "REDEFINED %s in line %d"%(matchedM[0], lineNum)
    #return model

def OPMatch(OPMatchObj, option):
    matchedOP = OPMatchObj.group().split()
    for i in range(1, len(matchedOP)):
        if re.search("=", matchedOP[i]):
            _key, _value = matchedOP[i].split("=")
            option[_key] = _value
        else:
            option[matchedOP[i]] = "Default"
    #return option

def NODEMatch(NODEMatchObj, nodeset):
    matchedNODE = NODEMatchObj.group().split()
    for i in range(1, len(matchedNODE)):
        _key, _value = matchedNODE[i].split("=")
        nodeNum = re.match(".*\((.*)\).*", _key).group(1)
        nodeset["node%d"%i] = nodeNum
        nodeset["value_of_node%d"%i] = _value
    #return nodeset

def ICMatch(ICMatchObj, nodeset):
    matchedIC = ICMatchObj.group().split()
    for i in range(1, len(matchedIC)):
        _key, _value = matchedIC[i].split("=")
        nodeNum = re.match(".*\((.*)\).*", _key).group(1)
        nodeset["node%d"%i] = nodeNum
        nodeset["value_of_node%d"%i] = _value

    #return nodeset

def ENDMatch(ENDMatchObj, end):
    matchedEND = ENDMatchObj.group().split()
    if len(matchedEND) == 1:
        end["end"] = matchedEND[0][1:]
    else:
        print "ERROR! in line %d"%lineNum

    #return end

def CommentMatch(CommentMatchObj, comment, numCmt):
    numCmt += 1
    matchedCmt = CommentMatchObj.group()
    comment["cmt%d"%numCmt] = matchedCmt[1:]

    #return comment
