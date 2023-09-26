# import wxPython
import wx


class Window(wx.Frame):
    def __init__(self, title):
        super().__init__(parent=None, title=title)

        # Make Panel
        self.panel = wx.Panel(self)

        # Button set uo
        button = wx.Button(self.panel, label="Press Me", pos=(50, 50))
        # Button Linking
        button.Bind(wx.EVT_BUTTON, self.OnClick)

        # Displays Frame
        self.Show()

        # Displays the window in the centre
        self.Centre()

    def OnClick(self, e):
        # Gets the object event works with all widgets not just buttons
        widget = e.GetEventObject()
        # Prints what button was pressed
        print(widget.GetClassName())
        # Prints the label of the widget
        print(widget.GetLabel())
        # Set widget label
        widget.SetLabel("Pressed")

        # Now the button has become an exit button
        # self.Close()


# Begin wxApplication
app = wx.App()

window = Window("WxPython Tutorial")

# Infinite loop only breaks when we tell it to
app.MainLoop()
