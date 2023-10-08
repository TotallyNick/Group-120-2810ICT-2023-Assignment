import wx
import wx.adv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class TableData:
    def __init__(self, fileName):
        # reads the chosen file into a dataframe
        self.data = pd.read_csv(fileName)

    def getData(self):
        # returns dataframe when called
        return self.data

    def getSelectedDateData(self, startDate, endDate):
        # --- for a user selected period, display the information of all accidents that happened in the period ---

        # define the date range
        searchStart = pd.to_datetime(startDate, format='%d/%m/%Y')  # format the data into d/m/y because americans
        searchEnd = pd.to_datetime(endDate, format='%d/%m/%Y')

        # convert to timestamp format
        self.data['ACCIDENT_DATE'] = pd.to_datetime(self.data['ACCIDENT_DATE'], format='%d/%m/%Y')

        # selected data is between start and end data
        selectedData = self.data[
            (self.data['ACCIDENT_DATE'] >= searchStart) & (self.data['ACCIDENT_DATE'] <= searchEnd)]

        return selectedData

    def getAccidentPerHour(self, accidentType):
        # --- For a user selected period, produce a chart to show the number of accidents in each hour of the day ---

        self.data = self.getSelectedDateData(startDate, endDate)  # dataframe is the filtered time period

        self.data = self.getSelectedType(accidentType)

        hourCount = {}  # create a dictionary for the counted accidents

        # print(hourCount)

        for accidentTime in self.data['ACCIDENT_TIME']:
            hour = accidentTime.split('.')[0]  # data formatted as HH.MM.SS so split at '.'

            if hour in hourCount:
                hourCount[hour] += 1  # if the current hour is in the dictionary, add 1 to it
            else:
                hourCount[hour] = 1  # otherwise give it a value of 1

        # print(hourCount)
        sortedHourCount = dict(sorted(hourCount.items()))

        # print(sortedHourCount)

        return sortedHourCount

    def getSelectedType(self, accidentType):
        # --- for a user selected period, retrieve all accidents caused by a type containing a keyword ---

        # make the searched data the filtered time dataframe
        self.data = self.getSelectedDateData(startDate, endDate)

        if accidentType == "All":
            return self.data

        # selected data looks for 'Yes' or 'No' in any casings
        searchType = self.data[self.data['ACCIDENT_TYPE'].str.lower() == accidentType.lower()]

        # print(searchType)

        return searchType

    def getAlcoholInvolved(self, hasAlcohol):  # get data where alcohol was involved in the accident
        searchAlcohol = self.data[self.data['ALCOHOLTIME'].str.lower().str.contains(hasAlcohol.lower())]

        return searchAlcohol


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
        self.choice_1 = self.create_choice(grid_sizer, ["Struck Pedestrian", "Collision With Vehicle",
                                                        "Collision with fixed object",
                                                        "No Collision and no object struck", "Struck Animals",
                                                        "Vehicle overturned(No Collision)",
                                                        "Collision with some other object",
                                                        "Fall from or in moving vehicle", "Other Accident",
                                                        "All"])
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
        startDate = self.datepicker_ctrl_1.GetValue()
        endDate = self.datepicker_ctrl_2.GetValue()
        accidentType = self.choice_1.GetSelection()
        hasAlcohol = self.choice_2.GetSelection()

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
        Data_frame = NewWindow(self, title="Data Frame")
        startDateUNFORM = self.datepicker_ctrl_1.GetValue()
        global startDate
        startDate = startDateUNFORM.GetDateOnly().Format("%d/%m/%Y")
        endDateUNFORM = self.datepicker_ctrl_2.GetValue()
        global endDate
        endDate = endDateUNFORM.GetDateOnly().Format("%d/%m/%Y")
        select_index1 = self.choice_1.GetSelection()
        if select_index1 != wx.NOT_FOUND:
            accidentType = self.choice_1.GetString(select_index1)
        select_index2 = self.choice_2.GetSelection()
        if select_index2 != wx.NOT_FOUND:
            hasAlcohol = self.choice_2.GetString(select_index2)

        table = TableData('Stats.csv')
        print(table.data)
        table.getSelectedDateData(startDate, endDate)
        print(table.data)
        # print(table.data)
        # print(accidentType)
        table.getSelectedType(accidentType)
        print(table.data)
        hour_count = table.getAccidentPerHour(accidentType)
        print(table.data)
        # print(hour_count)
        plt.figure(figsize=(10, 6))
        hours = list(hour_count.keys())
        counts = list(hour_count.values())
        plt.bar(hours, counts, color='b')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Number of Accidents')
        plt.title('Accidents per Hour')
        plt.xticks(np.arange(0, 24, step=1))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig("data1.png")

        Data1 = NewWindow(self, 'DataImages-AccidentsPerHour')
        image = wx.Image("data1.png")
        bitmap = wx.Bitmap(image)
        wx.StaticBitmap(Data1, -1, bitmap, (10, 10))
        Data1.Show()
        if hasAlcohol == "Yes":
            Data2 = NewWindow(self, 'DataImages-Alcohol')
            Data2.SetTitle("Alcohol-Related Accidents")
            plt.figure(figsize=(10, 6))
            hours = list(hour_count.keys())
            counts = list(hour_count.values())
            plt.bar(hours, counts, color='g')
            plt.xlabel('Hour of the Day')
            plt.ylabel('Number of Alcohol-Related Accidents')
            plt.title('Alcohol-Related Accidents per Hour')
            plt.xticks(np.arange(0, 24, step=1))
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.savefig("data2.png")

            Data2 = NewWindow(self, 'DataImages-Alcohol')
            image = wx.Image("data2.png")
            bitmap = wx.Bitmap(image)
            wx.StaticBitmap(Data2, -1, bitmap, (10, 10))
            Data2.SetTitle("Alcohol-Related Accidents")
            Data2.Show()


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
