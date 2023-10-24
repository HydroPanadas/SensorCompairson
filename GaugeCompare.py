from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
import pandas as pd
import numpy as np
from datetime import datetime
from pandas import read_csv
import matplotlib.pyplot as plt
from tktimepicker import constants, SpinTimePickerModern

def Dataplot(TG_df, WLO_df, meas, Cal_thr):

        fig, ax = plt.subplots()
        ax.plot(WLO_df.iloc[:,0],WLO_df.iloc[:,1], label = "00491: WLO (LASER)")

        T = TG_df.loc[TG_df.iloc[:,2] == meas]
        ax.plot(T.iloc[:,0], T.iloc[:,3], label = '49999: ' + meas )

        plt.legend()
        plt.title("Sensor: " + meas + ' Comparison Graph')
        plt.xlabel("Date and Time")
        plt.ylabel("Height")
        plt.savefig("Sensor_XXXXXX_" + meas + "_ObservationPlot.png")

        QC_df = pd.merge(WLO_df, T, how = "outer")
        QC_df['Diff'] = (QC_df.iloc[:,1] - QC_df['Value'])
        QC_df = QC_df[QC_df['Diff'].notna()]
        diffmean = round(QC_df['Diff'].mean(),3)
        diffstd = round(QC_df['Diff'].std(),3)
        diffmax = round(QC_df['Diff'].max(),3)
        diffmin = round(QC_df['Diff'].min(),3)

        QC_df['Within Allowable'] = np.where((QC_df.Diff <= Cal_thr) & (QC_df.Diff >= -Cal_thr), 'yes', 'no')
        Per = round(((len(QC_df[QC_df['Within Allowable'] == 'yes'])/len(QC_df)))*100,2)
        fig, ax = plt.subplots(nrows=2)
        Diffs = list(QC_df.loc[:,'Diff'])
        ax[0].hist(Diffs, weights=np.ones(len(Diffs)) / len(Diffs), alpha=0.5)
        ax[0].axvline(diffmax, 0, c='r', label = "MAX = " + str(diffmax) + 'm')
        ax[0].axvline(diffmean, 0, c='g', label = "MEAN = " + str(diffmean) + 'm')
        ax[0].axvline(diffmin, 0, c='c', label = "MIN = " + str(diffmin) + 'm')
        ax[0].axvline(Cal_thr, 0, c='b', label = "Cal Value +" + str(Cal_thr) + 'm')
        ax[0].axvline(-Cal_thr, 0, c='b', label = "Cal Value " + str(-Cal_thr) + 'm')
        ax[0].legend(loc='upper right')
        ax[0].set_title('Sensor: ' + meas + '\nAverage Difference ' + str(diffmean) + ' m')
        ax[0].set_xlabel('Differences (m)')
        ax[0].set_ylabel('Percentage (%)')
        colors = {'yes': 'green', 'no':'red'}
        ax[1].scatter(QC_df['DateTime'],QC_df['Diff'], c=QC_df['Within Allowable'].map(colors))
        ax[1].axhline(Cal_thr, c='b')
        ax[1].axhline(-Cal_thr, c='b')
        ax[1].set_title('Differences Scatterplot \n Red - Outside Allowable Green - Within Allowable(' + str(Per) + '%)')
        ax[1].set_xlabel('Date and Time')
        ax[1].set_ylabel('Difference (m)')
        plt.tight_layout()
        plt.savefig("Sensor_XXXXXX_" + meas + "_DifferencesPlot.png")


class Application(Frame):
    """Intialize Query Application"""

    def __init__(self, master):
        """Initialize the Frames for Querys"""
        Frame.__init__(self, master)
        self.grid()
        self.app_widgets()

    def Search_wlofile(self):
        
        self.wloF = filedialog.askopenfilename(initialdir = "/", title = "Select Test Sensor CSV",
                                   filetypes = (("CSV","*.CSV"),("all files","*.*")))
        self.wloFILE.set(self.wloF)

    def Search_8310logfile(self):
        
        self.SSPf = filedialog.askopenfilename(initialdir = "/", title = "Select Test Sensor CSV",
                                   filetypes = (("CSV","*.CSV"),("all files","*.*")))
        self.SSPFILE.set(self.SSPf)


    def app_widgets(self):
        """Creates Widgets for user GUI"""

        SDT = LabelFrame(self, text="Data Start Date and Time", foreground="blue")
        SDT.grid(row=1, column=0, padx=1, sticky=W+N)

        EDT = LabelFrame(self, text="Data End Date and Time", foreground="blue")
        EDT.grid(row=2, column=0, padx=1, sticky=W+N)

        WLO = LabelFrame(self, text="wlo Log", foreground="blue")
        WLO.grid(row=3, column=0, padx=1, sticky=W+N)

        logger_f = LabelFrame(self, text="Test Sensor Log", foreground="blue")
        logger_f.grid(row=4, column=0, padx=1, sticky=W+N)

        Meas = LabelFrame(self, text="Test Sensor Measurments", foreground="blue")
        Meas.grid(row=5, column=0, padx=1, sticky=W+N)

        self.StartDate = DateEntry(SDT, width=15, background= "magenta3", foreground= "white", bd=2)
        self.STD_text = Label(SDT, text="Start Date")
        self.STD_text.grid(row=0, column=0, sticky=W)
        self.StartDate.grid(row=0, column=1, sticky=W, padx=2)
        self.STD_text2 = Label(SDT, text="UTC")
        self.STD_text2.grid(row=0, column=3, sticky=W)

        self.STP = SpinTimePickerModern(SDT)
        self.STP.addAll(constants.HOURS24)
        self.STP.grid(row=0, column=2, sticky=W, padx=2)

        self.EndDate = DateEntry(EDT, width=15, background= "magenta3", foreground= "white", bd=2)
        self.ENDD_text = Label(EDT, text="End Date")
        self.ENDD_text.grid(row=0, column=0, sticky=W)
        self.EndDate.grid(row=0, column=1, sticky=W, padx=2)
        self.ENDD_text2 = Label(EDT, text="UTC")
        self.ENDD_text2.grid(row=0, column=3, sticky=W)

        self.EDP = SpinTimePickerModern(EDT)
        self.EDP.addAll(constants.HOURS24)
        self.EDP.grid(row=0, column=2, sticky=W, padx=2)

        self.wloFILE = StringVar()
        self.wloFile = Entry(WLO, width=15, textvariable=self.wloFILE)
        self.wloFile_text = Label(WLO, text="WLO File")
        self.wloFile_text.grid(row=2, column=0, sticky=W)
        self.wloFile.grid(row=2, column=1, sticky=W)
        self.Button1 = Button(WLO, text="...", height=0,
                              command=self.Search_wlofile)
        self.Button1.grid(row=2, column=3, sticky=W, padx=2)

        self.SSPFILE = StringVar()
        self.SSPFile = Entry(logger_f, width=15, textvariable=self.SSPFILE)
        self.SSPFile_text = Label(logger_f, text="8310 Log File")
        self.SSPFile_text.grid(row=3, column=0, sticky=W)
        self.SSPFile.grid(row=3, column=1, sticky=W)
        self.Button1 = Button(logger_f, text="...", height=0,
                              command=self.Search_8310logfile)
        self.Button1.grid(row=3, column=3, sticky=W, padx=2)

        self.TIDE = IntVar()
        self.TIDE_ = Checkbutton(Meas, variable=self.TIDE, text= "TIDE",
                                     state='active')
        self.TIDE_.grid(row=4, column=0, sticky=W)

        self.TIDE1 = IntVar()
        self.TIDE_1 = Checkbutton(Meas, variable=self.TIDE1, text= "TIDE1",
                                     state='active')
        self.TIDE_1.grid(row=4, column=1, sticky=W)

        self.TIDE2 = IntVar()
        self.TIDE_2 = Checkbutton(Meas, variable=self.TIDE2, text= "TIDE2",
                                     state='active')
        self.TIDE_2.grid(row=4, column=2, sticky=W)

        self.TIDE3 = IntVar()
        self.TIDE_3 = Checkbutton(Meas, variable=self.TIDE3, text= "TIDE3",
                                     state='active')
        self.TIDE_3.grid(row=4, column=3, sticky=W)

        self.CAL_Value = DoubleVar()
        Cal_thr = Scale(self, variable = self.CAL_Value, from_=0.001, to=0.030, digits=2, resolution=0.005, orient=HORIZONTAL)
        Cal_thr.set(0.030)
        cal_text = Label(self, text="Calibration Threshold Value (m)")
        cal_text.grid(row=6, column=0, sticky=W)
        Cal_thr.grid(row=7, column=0)

        self.Button_Q = Button(self, text="Run", height=0,
                               command=self.Calibartion_Analysis)
        self.Button_Q.grid(row=8, column=0, sticky=W, padx=2)


    def Calibartion_Analysis(self):

        ## Get Calibration Threshold
        Cal_thr = self.CAL_Value.get()


        ## Formatting the Start and End Date and Times for Comparison
        EndTime = self.EndDate.get() + " " + str(self.EDP.time()[0]) + ":" + str(self.EDP.time()[1]) + ":00"
        StartTime = self.StartDate.get() + " " + str(self.STP.time()[0]) + ":" + str(self.STP.time()[1]) + ":00"
        EndTime = datetime.strptime(EndTime, '%m/%d/%y %H:%M:%S')
        StartTime = datetime.strptime(StartTime, '%m/%d/%y %H:%M:%S')

        ## Test Gauge File
        TG = self.SSPFILE.get()
        TG_df = pd.read_csv(TG, skipfooter=1, skiprows=2, header=None, engine='python')
        TG_df.iloc[:,0] = pd.to_datetime(TG_df.iloc[:,0].astype(str) + ' ' + TG_df.iloc[:,1].astype(str))

        ## WLO (Laser)
        WLO = self.wloFILE.get()
        WLO_df = pd.read_csv(WLO, header=0)
        WLO_df.iloc[:,0] = pd.to_datetime(WLO_df.iloc[:,0].astype(str))

        ## Extracting Data within the Date and Time Extents
        mask = (TG_df[0] >= StartTime) & (TG_df[0] <= EndTime)
        TG_df = TG_df.loc[mask]
        mask = (WLO_df.iloc[:,0] >= StartTime) & (WLO_df.iloc[:,0] <= EndTime)
        WLO_df = WLO_df.loc[mask]
        TG_df.columns = ['DateTime', 'Time', 'Measurement', 'Value', 'units', 'Flag']
        WLO_df.rename(columns = {'Date / Time (UTC+00:00)':'DateTime'}, inplace = True)
        WLO_df = WLO_df[WLO_df.iloc[:,1].notna()]
        TG_df = TG_df[TG_df['Value'].notna()]

        ## Plotting Data
        if self.TIDE.get() == 1:
            Dataplot(TG_df, WLO_df, "TIDE", Cal_thr)
        if self.TIDE1.get() == 1:
            Dataplot(TG_df, WLO_df, "TIDE1", Cal_thr)
        if self.TIDE2.get() == 1:
            Dataplot(TG_df, WLO_df, "TIDE2", Cal_thr)
        if self.TIDE3.get() == 1:
            Dataplot(TG_df, WLO_df, "TIDE3", Cal_thr)
        


root = Tk()
root.title("Compare Sensors")
root.geometry("400x350")
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu)
submenu2 = Menu(menu)
app = Application(root)
root.mainloop()
