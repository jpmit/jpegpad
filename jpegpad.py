import wx
from const import *
import os

class MainWindow(wx.Frame):
    """We simply derive a new class of Frame. """
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, size=(400,350))
        self.CreateInteriorWindowComponents()
        self.CreateExteriorWindowComponents()
        self.GetPadData()
        self.filename = None
        self.filesize = 0

    def CreateInteriorWindowComponents(self):
        text = wx.StaticText(self, label="Select file to pad:",
                             pos=(20, 30))
        self.editfile = wx.TextCtrl(self, value="", pos=(150,26),size=(100,-1))
        self.Bind(wx.EVT_TEXT, self.OnChangeFileName, self.editfile)
        self.button = wx.Button(self, label="Browse", pos=(250,26))
        self.Bind(wx.EVT_BUTTON, self.OnBrowse, self.button)

        # display currently selected file size
        text = wx.StaticText(self, label="File size",
                             pos=(20,80))
        self.sizetext = wx.StaticText(self, label="", pos=(150,80))
        
        # display box with number of bytes to pad
        text2 = wx.StaticText(self, label="Kilobytes to pad",
                              pos=(20,130))
        self.pad = wx.SpinCtrl(self, -1, '', (160, 126), (60, -1))
        self.pad.SetRange(0,1000)
        self.pad.SetValue(100)
        self.Bind(wx.EVT_SPINCTRL, self.OnChangePadSize, self.pad)
        self.Bind(wx.EVT_TEXT, self.OnChangePadSize, self.pad)        

        # display file size after padding
        text3 = wx.StaticText(self, label="File size after padding",
                              pos=(20,180))
        self.sizetext2 = wx.StaticText(self, label="", pos=(200,180))

        # save button
        self.sbutton = wx.Button(self, label="Pad!", pos=(180,230))
        self.Bind(wx.EVT_BUTTON, self.OnPad, self.sbutton)

    def OnChangeFileName(self,e):
        self.filename = self.editfile.GetValue()
        self.UpdateFileSize()
        self.UpdatePadSize()

    def CreateExteriorWindowComponents(self):
        self.CreateMenus()
        self.CreateStatusBar()
        self.SetTitle()

    def GetPadData(self):
        padstring = open('curio10.txt').read(self.pad.GetValue()*1024)
        return padstring

    def OnPad(self,e):
        if not self.filesize:
            # want to write something to the status bar here
            return
        self.dirname = ''
        dlg = wx.FileDialog(self, "Filename to size padded file",
                            self.dirname, "", "*.*", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.savename = dlg.GetPath()
            self.PadImage()

    def PadImage(self):
        # open the jpeg file
        indata = open(self.filename,'rb').read()
        fout = open(self.savename,'wb')
        # pad with zeros!
        paddata = self.GetPadData()
        fout.write(indata + paddata)

    def OnChangePadSize(self,e):
        self.UpdatePadSize()

    def CreateMenus(self):
        filemenu = self.CreateFileMenu()
        helpmenu = self.CreateHelpMenu()
        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        menubar.Append(helpmenu, '&Help')
        self.SetMenuBar(menubar)

    def CreateFileMenu(self):
        """Return wx.MenuBar object"""
        filemenu = wx.Menu()
        # exit the program
        ex = filemenu.Append(wx.ID_EXIT, 'E&xit', 'Terminate the program')
        self.Bind(wx.EVT_MENU, self.OnExit, ex)
        return filemenu
       
    def CreateHelpMenu(self):
        helpmenu = wx.Menu()
        # display about info
        ab = helpmenu.Append(wx.ID_ABOUT, '&About',
                             'Information about this program')
        self.Bind(wx.EVT_MENU, self.OnAbout, ab)
        return helpmenu

    def SetTitle(self):
        super(MainWindow, self).SetTitle('JPEGpad %s' %VERSION)

    def OnAbout(self,e):
        csymb = u'\u00A9'
        message = (u'JPEGpad version %s\nCopyright %s 2013\n'
                   'James Mithen\njamesmithen@gmail.com '%(VERSION,csymb))
        dlg = wx.MessageDialog( self, message, "About JPEGpad", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished

    def OnExit(self,e):
        self.Close(True) # Close the frame.

    def UpdateFileSize(self):
        textsize = ''
        self.filesize = 0
        # don't want to display size if a directory
        if os.path.isfile(self.filename):
            try:
                # file size in kb
                fsize = os.path.getsize(self.filename) / 1024.0
            except:
                pass
            else:
                self.filesize = fsize
                textsize = '%.1fKb' % fsize
        self.sizetext.SetLabel(textsize)

    def UpdatePadSize(self):
        textpad = ''
        if self.filesize:
            padsize = self.filesize + self.pad.GetValue()
            textpad =  '%.1fKb' % padsize
        self.sizetext2.SetLabel(textpad)

    def OnBrowse(self,e):
        """Select a file to Browse"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file",
                            self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.editfile.SetValue(self.filename)
        dlg.Destroy()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainWindow(None)
    frame.Show()
    app.MainLoop()
