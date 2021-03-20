# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 21:19:16 2020

@author: Admin
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import csv
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from matplotlib.ticker import FuncFormatter
import numpy as np
import matplotlib.mlab as mlab
import mplfinance as mpf

import tkinter as tk
from tkinter import ttk


LARGE_FONT= ("Verdana", 12)

time = []
dl = []
ul = []

time5 = []
dl5 = []
ul5 = []

timeG = []
dlG = []
ulG = []

num_lines = 0;
with open('InternetSpeedTest.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    num_lines = sum(1 for line in readCSV)
    
with open('InternetSpeedTest.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for i, line in enumerate(reversed(list(readCSV))):
        if i < num_lines-1:
            #print(line)
            a = line[0]
            #print(s)
            c = ' '
            if len(line) == 5:
                if line[4] == "RyanNetwork_5GHz_5GEXT":
                    #a = (line[0])[x[0]+1:]
                    #a = datetime.strptime(a, '%m/%d/%Y %H:%M')
                    #print(a)
                    timeG.insert(0,a)
                    dlG.insert(0, float(line[1]))
                    ulG.insert(0, float(line[2]))
                elif line[4] == "RyanNetwork_5GHz":
                   # a = (line[0])[x[0]+1:]
                    #a = datetime.strptime(a, '%m/%d/%Y %H:%M')
                    time5.insert(0,a)
                    dl5.insert(0, float(line[1]))
                    ul5.insert(0, float(line[2]))
                elif line[4] == "RyanNetwork_2.4":
                    #a = (line[0])[x[0]+1:]
                    #a = datetime.strptime(a, '%m/%d/%Y %H:%M')
                    time.insert(0,a)
                    dl.insert(0, float(line[1]))
                    ul.insert(0, float(line[2]))

df = pd.read_csv('InternetSpeedTest.csv', names=["DateTime", "DownloadSpeed", "UploadSpeed", "PacketLoss", "SSID"])
print(df.head())

df.index = pd.to_datetime(df["DateTime"], format="%m/%d/%Y %H:%M")
df = df.drop(columns = ["DateTime"])
df.index.name = "Date"

print(df.head())
mpf.plot(df)
f = Figure(figsize = (20,10), dpi = 100)
d = df.plot()
myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
d.xaxis.set_major_formatter(myfmt)


print("2.4: ")
print("time: ", time)
print(dl)
print(ul)

print("")
print("5GHz: ")
print("time: ", time5)
print(dl5)
print(ul5)

print("")
print("5GEXT: ")
print("time: ", timeG)
print(dlG)
print(ulG)

'''

for a in time:
    a = datetime.strptime(a, '%m-%d-%Y %H:%M')
for a in timeG:
    a = datetime.strptime(a, '%m/%d/%Y %H:%M')
for a in time5:
    a = datetime.strptime(a, '%m/%d/%Y %H:%M')
''' 
#print(timeG)

if len(dl)>0:
    sum2 = round(sum(dl)/len(dl), 2)
else:
    sum2 = 'n/a'
if len(dl5)>0:
    sum5 = round(sum(dl5)/len(dl5),2)
else:
    sum5 = 'n/a'
if len(dlG)>0:
    sumG = round(sum(dlG)/len(dlG), 2)
else:
    sumG = 'n/a'

def equidate_ax(fig, ax, dates, fmt="%Y-%m-%d", label="Test Time"):
    """
    Sets all relevant parameters for an equidistant date-x-axis.
    Tick Locators are not affected (set automatically)

    Args:
        fig: pyplot.figure instance
        ax: pyplot.axis instance (target axis)
        dates: iterable of datetime.date or datetime.datetime instances
        fmt: Display format of dates
        label: x-axis label
    Returns:
        None

    """    
    N = len(dates)
    def format_date(index, pos):
        index = np.clip(int(index + 0.5), 0, N - 1)
        return dates[index].strftime(fmt)
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_xlabel(label)
    fig.autofmt_xdate()

class Capp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="speed.ico")
        tk.Tk.wm_title(self, "Internet Speed Graph")
        
        tk.Tk.geometry(self, "1600x900")
        container = tk.Frame(self, width=1600, height=900, relief='raised', borderwidth=0)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (home, gext, two, five, combined):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(home)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class home(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Internet Speed Graphs", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
     
        
        button1 = ttk.Button(self, text="View 5GEXT Graph",
                            command=lambda: controller.show_frame(gext))
        button1.pack()
        
        button2 = ttk.Button(self, text="View 5GHz Graph",
                            command=lambda: controller.show_frame(five))
        button2.pack()
        
        button3 = ttk.Button(self, text="View 2.4GHz Graph",
                            command=lambda: controller.show_frame(two))
        button3.pack()
        
        button4 = ttk.Button(self, text="View Combined Graph",
                            command=lambda: controller.show_frame(combined))
        button4.pack()


        label2 = tk.Label(self, text="5GEXT avg download speed: "+str(sumG)+" mbps", font=LARGE_FONT)
        label2.pack(pady=15,padx=15)
        
        label3 = tk.Label(self, text="5GHz avg download speed: "+str(sum5)+" mbps", font=LARGE_FONT)
        label3.pack(pady=15,padx=15)
        
        label4 = tk.Label(self, text="2.4GHz avg download speed: "+str(sum2)+" mbps", font=LARGE_FONT)
        label4.pack(pady=15,padx=15)



class combined(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Combined Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(home))
        button1.pack()
        
        summ = 0
        count = 0
        if sumG!= 'n/a':
            summ+=sumG
            count+=1
        if sum5 != 'n/a':
            summ+=sum5
            count+=1
        if sum2 !='n/a':
            summ+=sum2
            count+=1
            
            
        label2 = tk.Label(self, text="Combined avg download speed: "+str(round(summ/count, 2))+" mbps", font=LARGE_FONT)
        label2.pack(pady=15,padx=15)
        
        
        f = Figure(figsize = (20,10), dpi = 100)
        d = f.add_subplot(111)
        
    
        if len(dlG)>0:
            
            #plt.rcParams['figure.figsize'] = (20, 10)
            d.plot(timeG, dlG, 'r-', label = "GEXT down")
            d.plot(timeG, ulG, '.r-', label = "GEXT up")
            
            d.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            #myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
            #d.xaxis.set_major_formatter(myfmt)
            d.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
        
        if len(dl5)>0:
            
            #plt.rcParams['figure.figsize'] = (20, 10)
            d.plot(time5, dl5, 'b-', label = "5GHz down")
            d.plot(time5, ul5, '.b-', label = "5GHz up")
            
            d.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            #myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
            #d.xaxis.set_major_formatter(myfmt)
            d.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
         
        if len(dl)>0:
            
            #plt.rcParams['figure.figsize'] = (20, 10)
            d.plot(time, dl, '.g-', label = "2.4GHz down")
            d.plot(time, ul, 'xg-', label = "2.4GHz up")

            d.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            #myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
            #d.xaxis.set_major_formatter(myfmt)
            d.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
        
        d.set_xlabel('Test Time')
        d.set_ylabel('Speed (GHz)')
        d.set_title("Internet Speed (All)")
        d.set_ylim(ymin = 0.0)
        
        if len(timeG)+len(time5)+len(time)>150:
             loc = mticker.MultipleLocator(base=7) 
             d.set_xlim(0, 75)
        elif len(timeG)+len(time5)+len(time)>50:
            loc = mticker.MultipleLocator(base=5) 
            d.set_xlim(0, 50)
        else:
            loc = mticker.MultipleLocator(base=2)
            d.set_xlim(0)
            
        d.xaxis.set_major_locator(loc)
        d.set_xticklabels(timeG, rotation=25, horizontalalignment='right')
        myfmt = mdates.DateFormatter('%m/%d/%Y %H:%M')
        #d.xaxis.set_major_formatter(myfmt)
        d.tick_params(axis='x', which='major', labelsize=7)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)
        
        
        
        
class gext(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="5GEXT Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(home))
        button1.pack()
        
        label2 = tk.Label(self, text="5GEXT avg download speed: "+str(sumG)+" mbps", font=LARGE_FONT)
        label2.pack(pady=15,padx=15)
        
        
        f = Figure(figsize = (20,10), dpi = 100)
        a = f.add_subplot(111)
        
        if len(dlG)>0:
            
            #plt.rcParams['figure.figsize'] = (20, 10)
            a.set_xticklabels(timeG, rotation=25, horizontalalignment='right')
            a.plot(timeG, dlG, '.r-', label = "download")
            a.plot(timeG, ulG, '.b-', label = "upload")
            
            a.set_xlabel('Test Time')
            a.set_ylabel('Speed (GHz)')
            a.set_title("Internet Speed (5GEXT)") 

            a.set_ylim(ymin = 0.0)
            
            a.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            
            if len(timeG)>150:
                loc = mticker.MultipleLocator(base=10) 
                #a.set_xlim(0, 75)
            elif len(timeG)>50:
                loc = mticker.MultipleLocator(base=5) 
               # a.set_xlim(0, 50)
            else:
                loc = mticker.MultipleLocator(base=2)
            
            a.set_xlim(xmin =0.0)
                
            a.xaxis.set_major_locator(loc)
            
            myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
            #a.xaxis.set_major_formatter(myfmt)
            a.tick_params(axis='x', which='major', labelsize=7)
            a.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)
        
        
class two(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="2.4GHz Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(home))
        button1.pack()
        
        label4 = tk.Label(self, text="2.4GHz avg download speed: "+str(sum2)+" mbps", font=LARGE_FONT)
        label4.pack(pady=15,padx=15)
       
        f = Figure(figsize = (20,10), dpi = 100)
        a = f.add_subplot(111)
        
        if len(dl)>0:
           
           
            #plt.rcParams['figure.figsize'] = (20, 10)
            a.xticks(rotation=45)
            a.plot(time, dl, '.r-', label = "download")
            a.plot(time, ul, '.b-', label = "upload")
            
            a.set_xlabel('Test Time')
            a.set_ylabel('Speed (GHz)')
            a.set_title("Internet Speed (2.4GHz)")
            
            a.set_ylim(ymin = 0.0)
            
            a.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            
            if len(time)>150:
                loc = mticker.MultipleLocator(base=7) 
                a.set_xlim(0.0, 125)
            elif len(time)>50:
                loc = mticker.MultipleLocator(base=5) 
                a.set_xlim(0.0, 75)
            else:
                loc = mticker.MultipleLocator(base=2)
                a.set_xlim(xmin = 0.0)
                
            a.xaxis.set_major_locator(loc)
            
            myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
            a.xaxis.set_major_formatter(myfmt)
            a.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)
        
        
class five(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="5GHz Graph", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(home))
        button1.pack()

        label3 = tk.Label(self, text="5GHz avg download speed: "+str(sum5)+" mbps", font=LARGE_FONT)
        label3.pack(pady=15,padx=15)

        f = Figure(figsize = (20,10), dpi = 100)
        a = f.add_subplot(111)
        
        if len(dl5)>0:
            
            #plt.rcParams['figure.figsize'] = (20, 10)
            
            a.plot(time5, dl5, '.r-', label = "download")
            a.plot(time5, ul5, '.b-', label = "upload")
            a.set_xticklabels(time5, rotation=25, ha="right")
            a.set_xlabel('Test Time')
            a.set_ylabel('Speed (GHz)')
            a.set_title("Internet Speed (5GHz)")

            a.set_ylim(ymin = 0.0)
            
            a.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
            
            if len(time5)>150:
                loc = mticker.MultipleLocator(base=7) 
                a.set_xlim(0, 75)
            elif len(time5)>50:
                loc = mticker.MultipleLocator(base=5) 
                a.set_xlim(0, 50)
            else:
                loc = mticker.MultipleLocator(base=2)
                a.set_xlim(xmin = 0)
                
            a.xaxis.set_major_locator(loc)
            
            myfmt = mdates.DateFormatter('%Y/%m/%d %H:%M:%S')
           # a.xaxis.set_major_formatter(myfmt)
            a.tick_params(axis='x', which='major', labelsize=7)
            a.legend(bbox_to_anchor=(1.025, 1), loc='upper left', borderaxespad=0.)
        
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand = True)

        

app = Capp()
app.mainloop()