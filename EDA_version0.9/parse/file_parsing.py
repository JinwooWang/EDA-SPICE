__author__ = "JinoowW"

import re
from device_parse import *

def parsing(filename):
    comment = {}
    element = {}
    command = {}

    numCmt = 0
    lineNum = 1
    resistence = {}
    capacitor = {}
    inductor = {}
    diode = {}
    voltage = {}
    current = {}
    vcvs = {}
    cccs = {}
    vccs = {}
    ccvs = {}
    mosfet = {}

    option = {}
    model = {}
    dc = {"flag":None}
    ac = {"flag":None}
    tran = {"flag":None}
    prt = {}
    nodeset = {}
    end = {}


    openfile = open(filename, "r")
    lines = openfile.readlines()
    lines = lines[1:]
    for line in lines:
        lineNum += 1
        line = line.strip().lower()

        matchV = r"^v.*"
        matchI = r"^i.*"
        matchR = r"^r.*"
        matchC = r"^c.*"
        matchD = r"^d.*"
        matchL = r"^l.*"
        matchE = r"^e.*"
        matchF = r"^f.*"
        matchG = r"^g.*"
        matchH = r"^h.*"
        matchM = r"^m.*"

        matchDC = r"^\.dc.*"
        matchAC = r"^\.ac.*"
        matchTRAN = r"^\.tran.*"
        matchPRT = r"^\.print.*"
        matchMOD = r"^\.model.*"
        matchOP = r"^\.option.*"
        matchNODE = r"^\.nodeset.*"
        matchIC =  r"^\.ic.*"
        matchEND = r"^\.end.*"

        matchComment = r"^\*.+"


        ResMatchObj = re.match(matchR, line)
        CapMatchObj = re.match(matchC, line)
        IndMatchObj = re.match(matchL, line)
        DiodeMatchObj = re.match(matchD, line)
        VltgMatchObj = re.match(matchV, line)
        CurrFlowMatchObj = re.match(matchI, line)
        VCVSMatchObj = re.match(matchE, line)
        CCCSMatchObj = re.match(matchF, line)
        VCCSMatchObj = re.match(matchG, line)
        CCVSMatchObj = re.match(matchH, line)
        MOSFETMatchObj = re.match(matchM, line)

        ENDMatchObj = re.match(matchEND, line)
        DCMatchObj = re.match(matchDC, line)
        ACMatchObj = re.match(matchAC, line)
        TRANMatchObj = re.match(matchTRAN, line)
        PRTMatchObj = re.match(matchPRT, line)
        MODMatchObj = re.match(matchMOD, line)
        OPMatchObj =re.match(matchOP, line)
        NODEMatchObj = re.match(matchNODE, line)
        ICMatchObj = re.match(matchIC, line)

        CommentMatchObj = re.match(matchComment, line)

        if VltgMatchObj:
            VltgMatch(VltgMatchObj, voltage, line)
        elif CurrFlowMatchObj:
            CurrFlowMatch(CurrFlowMatchObj, current)
        elif ResMatchObj:
            ResMatch(ResMatchObj, resistence)
        elif CapMatchObj:
            CapMatch(CapMatchObj, capacitor)
        elif IndMatchObj:
            IndMatch(IndMatchObj, inductor)
        elif DiodeMatchObj:
            DiodeMatch(DiodeMatchObj, diode)
        elif VCVSMatchObj:
            VCVSMatch(VCVSMatchObj, vcvs)
        elif CCCSMatchObj:
            CCCSMatch(CCCSMatchObj, cccs)
        elif VCCSMatchObj:
            VCCSMatch(VCCSMatchObj, vccs)
        elif CCVSMatchObj:
            CCVSMatch(CCVSMatchObj, ccvs)
        elif MOSFETMatchObj:
            MOSFETMatch(MOSFETMatchObj, mosfet)
        elif DCMatchObj:
            DCMatch(DCMatchObj, dc)
        elif ACMatchObj:
            ACMatch(ACMatchObj, ac)
        elif TRANMatchObj:
            TRANMatch(TRANMatchObj, tran)
        elif PRTMatchObj:
            PRTMatch(PRTMatchObj, prt)
        elif MODMatchObj:
            MODMatch(MODMatchObj, model, line)
        elif OPMatchObj:
            OPMatch(OPMatchObj, option)
        elif NODEMatchObj:
            NODEMatch(NODEMatchObj, nodeset)
        elif ICMatchObj:
            ICMatch(ICMatchObj, nodeset)
        elif ENDMatchObj:
            ENDMatch(ENDMatchObj, end)
        elif CommentMatchObj:
            CommentMatch(CommentMatchObj, comment, numCmt)

        element["resistence"] = resistence
        element["capacitor"] = capacitor
        element["inductor"] = inductor
        element["diode"] = diode
        element["voltage"] = voltage
        element["current"] = current
        element["vcvs"] = vcvs
        element["cccs"] = cccs
        element["vccs"] = vccs
        element["ccvs"] = ccvs
        element["mosfet"] = mosfet
        command["dc"] = dc
        command["ac"] = ac
        command["tran"] = tran
        command["print"] = prt
        command["model"] = model
        command["option"] = option
        command["nodeset"] = nodeset
        command["end"] = end

    return element, comment, command

if "__main__" == __name__:
    filename = raw_input("input filename:")
    element, comment, command = parsing(filename)
    print "element: ", element
    print "comment: ", comment
    print "command: ", command
