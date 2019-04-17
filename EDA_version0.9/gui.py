import wx
from parse.file_parsing import parsing
from analysis.command import *
from analysis.solMatrix import *
import matplotlib.pyplot as plt

class GUI(wx.Frame):
    def __init__(self):
        self.filepath = []
        self.log = []
        self.dc_nodename = []
        self.ac_nodename = []
        self.tran_nodename = []
        self.element = {}
        self.command = {}
        wx.Frame.__init__(self, None, title="OSSPICE", size=(600,600))
        self.panel = wx.Panel(self, -1)

        loadButton = wx.Button(self.panel, label='Open')
        self.Bind(wx.EVT_BUTTON, self.OnOpen, loadButton)

        saveButton = wx.Button(self.panel, label='Save')
        self.Bind(wx.EVT_BUTTON, self.OnSave, saveButton)

        self.dc_namechoice = wx.ComboBox(self.panel, id = -1, choices = self.dc_nodename, style = wx.CB_READONLY)
        self.dc_namechoice.SetSelection(0)

        self.ac_namechoice = wx.ComboBox(self.panel, id = -1, choices = self.ac_nodename, style = wx.CB_READONLY)
        self.ac_namechoice.SetSelection(0)

        self.tran_namechoice = wx.ComboBox(self.panel, id = -1, choices = self.tran_nodename, style = wx.CB_READONLY)
        self.tran_namechoice.SetSelection(0)

        parseButton = wx.Button(self.panel, label = "Parse")
        self.Bind(wx.EVT_BUTTON, self.parse_file, parseButton)

        simulateButton = wx.Button(self.panel, label = "Simulation")
        self.Bind(wx.EVT_BUTTON, self.simulate_file, simulateButton)

        waveview = wx.Button(self.panel, label = "Waveview")
        self.Bind(wx.EVT_BUTTON, self.wave_file, waveview)

        self.filename = wx.TextCtrl(self.panel)

        self.contents = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.HSCROLL)

        self.proccess = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.proccess.SetForegroundColour("White")
        self.proccess.SetBackgroundColour('DIM GREY')

        self.dc_name = wx.StaticText(self.panel, wx.ID_ANY, "DC")
        self.ac_name = wx.StaticText(self.panel, wx.ID_ANY, "AC")
        self.tran_name = wx.StaticText(self.panel, wx.ID_ANY, "TRAN")

        hdcbox = wx.BoxSizer()
        hdcbox.Add(self.dc_name, proportion = 0, flag = wx.LEFT, border = 30)
        hdcbox.Add(self.dc_namechoice, proportion = 0, flag = wx.LEFT, border = 10)

        hacbox = wx.BoxSizer()
        hacbox.Add(self.ac_name, proportion = 0, flag = wx.LEFT, border = 30)
        hacbox.Add(self.ac_namechoice, proportion = 0, flag = wx.LEFT, border = 10)

        htranbox = wx.BoxSizer()
        htranbox.Add(self.tran_name, proportion = 0, flag = wx.LEFT, border = 10)
        htranbox.Add(self.tran_namechoice, proportion = 0, flag = wx.LEFT, border = 10)

        hbox = wx.BoxSizer()
        hbox.Add(self.filename, proportion=1, flag=wx.EXPAND)
        hbox.Add(loadButton, proportion=0, flag=wx.LEFT, border=10)
        hbox.Add(saveButton, proportion=0, flag=wx.LEFT, border=10)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(self.contents, proportion=2, flag=wx.EXPAND | wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        vbox.Add(self.proccess, proportion=1, flag=wx.EXPAND | wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(hdcbox, proportion = 0, flag =  wx.TOP|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)
        vbox2.Add(hacbox, proportion = 0, flag =  wx.TOP|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)
        vbox2.Add(htranbox, proportion = 0, flag =  wx.TOP|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)
        vbox2.Add(parseButton, proportion = 0, flag = wx.TOP|wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)
        vbox2.Add(simulateButton, proportion = 0, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)
        vbox2.Add(waveview, proportion = 0, flag = wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border = 10)


        hbox2 = wx.BoxSizer()
        hbox2.Add(vbox, proportion = 1, flag = wx.EXPAND, border = 20)
        hbox2.Add(vbox2, proportion = 0, flag = wx.ALL, border = 40)

        self.panel.SetSizer(hbox2)
    def OnOpen(self, event):
        self.filepath = []
        self.log = []
        self.dc_nodename = []
        self.ac_nodename = []
        self.tran_nodename = []
        self.element = {}
        self.command = {}
	self.dc_namechoice.SetItems([])
	self.ac_namechoice.SetItems([])
	self.tran_namechoice.SetItems([])
        dialog = wx.FileDialog(None,'spice file',style = wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.filename.SetValue(dialog.GetPath())
            file = open(dialog.GetPath())
            self.contents.SetValue(file.read())
            if self.filename.GetValue():
                self.filepath.append(self.filename.GetValue())
            file.close()
        dialog.Destroy()
    def OnSave(self, event):
        if self.filename.GetValue() == '':
            dialog = wx.FileDialog(None,'Notepad',style = wx.SAVE)
            if dialog.ShowModal() == wx.ID_OK:
                self.filename.SetValue(dialog.GetPath())
                file = open(dialog.GetPath(), 'w')
                file.write(self.contents.GetValue())
                file.close()
            dialog.Destory()
        else:
            file = open(self.filename.GetValue(), 'w')
            file.write(self.contents.GetValue())
            file.close()

    def parse_file(self, event):
        self.element, self.comment, self.command = parsing(self.filepath[-1])
        #print self.element
        self.log.append("parsing\n")
        self.proccess.AppendText(self.log[-1])

    def simulate_file(self, event):
	self.dc_namechoice.SetItems([])
	self.ac_namechoice.SetItems([])
	self.tran_namechoice.SetItems([])
	self.dc_nodename = []
	self.ac_nodename = []
	self.tran_nodename = []
        self.proccess.AppendText("simulating\n")
        if self.command["dc"]["flag"] == "dc":
            A, dimen, nodeMap, verseMap = mergeStamps(self.element, "dc")
            self.voltagedic_dc, self.currentdic_dc, self.srcname_dc, self.srclist_dc = dc_sol(self.element, self.command, A, dimen, nodeMap, verseMap, gList)
            for item in self.voltagedic_dc:
                self.dc_nodename.append(item)
            for item in self.currentdic_dc:
                self.dc_nodename.append(item)
            self.dc_namechoice.SetItems(self.dc_nodename)
            self.dc_namechoice.SetSelection(0)
        if self.command["ac"]["flag"] == "ac":
            A, dimen, nodeMap, verseMap = mergeStamps(self.element, "ac")
            self.voltageModeDic_ac, self.voltagePhaseDic_ac, self.currentModeDic_ac, self.currentPhaseDic_ac, self.freqlist_ac = ac_sol(self.element, self.command, A, dimen, nodeMap, verseMap)
            for item in self.voltageModeDic_ac:
                self.ac_nodename.append(item)
            for item in self.currentModeDic_ac:
                self.ac_nodename.append(item)
            self.ac_namechoice.SetItems(self.ac_nodename)
            self.ac_namechoice.SetSelection(0)
        if self.command["tran"]["flag"] == "tran":
            A, dimen, nodeMap, verseMap = mergeStamps(self.element, "tran")
            self.voltagedic_tran, self.currentdic_tran, self.timelist_tran = tran_sol(self.element, self.command, A, dimen, nodeMap, verseMap, "BE", gList)
            for item in self.voltagedic_tran:
                self.tran_nodename.append(item)
            for item in self.currentdic_tran:
                self.tran_nodename.append(item)
            self.tran_namechoice.SetItems(self.tran_nodename)
            self.tran_namechoice.SetSelection(0)
	    #plt.plot(self.timelist_tran[1:],  self.voltagedic_tran['7'][1:])
	    #plt.plot(self.timelist_tran[1:],  self.voltagedic_tran['9'][1:])
	    #plt.ylabel("V")
            #plt.xlabel("time")
	    #plt.show()
    def wave_file(self, event):
        if self.command["dc"]["flag"] == "dc":
            item = self.dc_namechoice.GetValue()
            if self.voltagedic_dc.has_key(item):
                plt.title("node %s voltage dc_curve"%item)
                plt.ylabel("V")
                plt.xlabel("%s"%self.srcname_dc)
                plt.plot(self.srclist_dc, self.voltagedic_dc[item])
                plt.show()
            if self.currentdic_dc.has_key(item):
                plt.title("node %s current dc_curve"%item)
                plt.ylabel("A")
                plt.xlabel("%s"%self.srcname_dc)
                plt.plot(self.srclist_dc, self.currentdic_dc[item])
                plt.show()
        if self.command["ac"]["flag"] == "ac":
            item = self.ac_namechoice.GetValue()
            if self.voltageModeDic_ac.has_key(item):
                plt.subplot(211)
                plt.title("node %s voltage magnitude"%item)
                plt.ylabel("mag")
                #plt.xlabel("frequence")
                plt.plot(self.freqlist_ac, self.voltageModeDic_ac[item])

                plt.subplot(212)
                plt.title("node %s voltage phase"%item)
                plt.ylabel("dB")
                plt.xlabel("frequence")
                plt.plot(self.freqlist_ac, self.voltagePhaseDic_ac[item])
                plt.show()
            if self.currentModeDic_ac.has_key(item):
                plt.subplot(211)
                plt.title("device %s current magnitude"%item)
                plt.ylabel("mag")
                #plt.xlabel("frequence")
                plt.plot(self.freqlist_ac, self.currentModeDic_ac[item])
                plt.subplot(212)
                plt.title("device %s current phase"%item)
                plt.ylabel("dB")
                plt.xlabel("frequence")
                plt.plot(self.freqlist_ac, self.currentPhaseDic_ac[item])
                plt.show()

        if self.command["tran"]["flag"] == "tran":
            item = self.tran_namechoice.GetValue()
            """
            l1, = plt.plot(self.timelist_tran, self.voltagedic_tran['9'], 'b')
            l2, = plt.plot(self.timelist_tran, self.voltagedic_tran['7'], 'r')
            plt.xlabel('time')
            plt.ylabel('V')
            #plt.ylim(min(volTR['1'][1:]) - 0.2, max(volTR['1'][1:]) + 0.2)
            plt.legend(handles=[l1, l2], labels = ['Vin', 'Vout'])
            plt.title('opamp')
            plt.show()	
            """
            if self.voltagedic_tran.has_key(item):
                plt.title("node %s voltage"%item)
                plt.ylabel("V")
                plt.xlabel("time")
		plt.ylim(min(self.voltagedic_tran[item][1:]) - 0.2, max(self.voltagedic_tran[item][1:]) + 0.2)
                plt.plot(self.timelist_tran[1:],  self.voltagedic_tran[item][1:])
                plt.show()
            if self.currentdic_tran.has_key(item):
                plt.title("device %s current"%item)
                plt.ylabel("A")
                plt.xlabel("time")
		plt.ylim(min(self.currentdic_tran[item][1:]) - 0.2, max(self.currentdic_tran[item][1:]) + 0.2)
                plt.plot(self.timelist_tran[1:], self.currentdic_tran[item][1:])
                plt.show()


if __name__ == "__main__":
    app = wx.App()
    win = GUI()
    win.Show()
    app.MainLoop()
