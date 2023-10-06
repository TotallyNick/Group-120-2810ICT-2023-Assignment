import wx
import wx.adv


class NewWindow(wx.Frame):
    def __init__(self, parent, title):
        super(NewWindow, self).__init__(parent, title=title, size=(1000, 750))


class NewProjectWindow(wx.Frame):
    def __init__(self, parent, title):
        super(NewProjectWindow, self).__init__(parent, title=title, size=(1000, 750))

        self.panel_1 = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridSizer(6, 3, 0, 0)

        self.create_empty_cell(grid_sizer)
        self.create_label(grid_sizer, "Start Date:")
        self.create_label(grid_sizer, "End Date:")
        self.create_label(grid_sizer, "Data Range:")
        self.datepicker_ctrl_1 = self.create_date_picker(grid_sizer)
        self.datepicker_ctrl_2 = self.create_date_picker(grid_sizer)
        self.create_label(grid_sizer, "Accident Type:")
        self.choice_1 = self.create_choice(grid_sizer, ["choice 1", "choice 2", "choice 3"])
        self.create_empty_cell(grid_sizer)
        self.create_label(grid_sizer, "Has Alcohol:")
        self.choice_2 = self.create_choice(grid_sizer, ["Yes", "No"])
        self.create_empty_cell(grid_sizer)
        self.create_empty_cell(grid_sizer)
        self.create_empty_cell(grid_sizer)
        self.create_empty_cell(grid_sizer)
        self.create_label(grid_sizer, "Confirm Selection:")
        self.create_empty_cell(grid_sizer)

        self.create_button(grid_sizer, "Apply Search")

        self.panel_1.SetSizer(grid_sizer)
        main_sizer.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetSizer(main_sizer)

    def create_label(self, sizer, text):
        label = wx.StaticText(self.panel_1, wx.ID_ANY, text)
        label.SetMinSize((150, 55))
        label.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        sizer.Add(label, 0, wx.ALIGN_CENTER, 0)

    def create_date_picker(self, sizer):
        datepicker_ctrl = wx.adv.DatePickerCtrl(self.panel_1, wx.ID_ANY)
        sizer.Add(datepicker_ctrl, 0, wx.ALIGN_CENTER, 0)
        return datepicker_ctrl

    def create_choice(self, sizer, choices):
        choice = wx.Choice(self.panel_1, wx.ID_ANY, choices=choices)
        choice.SetMinSize((150, 50))
        choice.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        choice.SetSelection(0)
        sizer.Add(choice, 0, wx.ALIGN_CENTER, 0)
        return choice

    def create_empty_cell(self, sizer):
        empty_cell = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        sizer.Add(empty_cell, 0, 0, 0)

    def create_button(self, sizer, label):
        button = wx.Button(self.panel_1, wx.ID_ANY, label)
        button.SetMinSize((200, 50))
        button.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Segoe UI"))
        sizer.Add(button, 0, wx.ALIGN_CENTER, 0)
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

    def on_button_click(self, event):
        # Create and show the new window
        Data_frame = NewWindow(self, title="Data Frame")
        
        # Get Data from Search filters
        
        # Add Jacks Code here, it produces an XSL and Pngs
        
        # Display the Pngs with references 

        Data_frame.Show()


class HelpWindow(wx.Frame):
    def __init__(self, parent, title):
        super(HelpWindow, self).__init__(parent, title=title, size=(400, 300))

        panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        help_text = wx.StaticText(panel, wx.ID_ANY, "This is the Help Window", style=wx.ALIGN_CENTER)
        sizer.Add(help_text, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        button_back = wx.Button(panel, wx.ID_ANY, "Back to Main")
        button_back.Bind(wx.EVT_BUTTON, self.on_back_button_click)
        sizer.Add(button_back, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(sizer)
        self.Layout()

    def on_back_button_click(self, event):
        self.Close()


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        super(MainFrame, self).__init__(*args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("VCS")

        self.panel = wx.Panel(self, wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        title = wx.StaticText(self.panel, wx.ID_ANY, "Victorian Crash Sight", style=wx.ALIGN_CENTER)
        sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        title.SetFont(font)

        NewProject = wx.Button(self.panel, wx.ID_ANY, "New Project")
        Help = wx.Button(self.panel, wx.ID_ANY, "Help")
        button_exit = wx.Button(self.panel, wx.ID_ANY, "Exit")

        NewProject.Bind(wx.EVT_BUTTON, self.ProjectWindow)
        Help.Bind(wx.EVT_BUTTON, self.HelpWindow)
        button_exit.Bind(wx.EVT_BUTTON, self.on_exit_button_click)

        sizer.Add(NewProject, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(Help, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(button_exit, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.panel.SetSizer(sizer)
        self.Layout()

    def ProjectWindow(self, event):
        new_project_window = NewProjectWindow(self, "New Project")
        new_project_window.Show()

    def HelpWindow(self, event):
        help_window = HelpWindow(self, "Help")
        help_window.Show()

    def on_exit_button_click(self, event):
        self.Close()

    def DataWindow(self, event):
        new_window = NewWindow(self, "Data")
        new_window.Show()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
