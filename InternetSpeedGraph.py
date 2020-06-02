#!/usr/bin/env python
# coding: utf-8

# In[64]:


#get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
#import matplotlib.patches as mp
import csv
import matplotlib.ticker as mticker

time = []
dl = []
ul = []

dl5 = []
ul5 = []

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
            s = line[0]
            c = ' '
            x = ([pos for pos, char in enumerate(s) if char == c])
            if len(line) == 5:
                if line[4] == "RyanNetwork_5GHz_5GEXT":
                    time.insert(0,(line[0])[x[-1]+1:])
                    dlG.insert(0, float(line[1]))
                    ulG.insert(0, float(line[2]))
                elif line[4] == "RyanNetwork_5GHz":
                    time.insert(0,(line[0])[x[-1]:])
                    dl5.insert(0, float(line[1]))
                    ul5.insert(0, float(line[2]))
                elif line[4] == "RyanNetwork_2.4":
                    time.insert(0,(line[0])[x[-1]:])
                    dl.insert(0, float(line[1]))
                    ul.insert(0, float(line[2]))

print("time: ", time)

print("")
print("2.4: ")
print(dl)
print(ul)

print("")
print("5GHz: ")
print(dl5)
print(ul5)

print("")
print("5GEXT: ")
print(dlG)
print(ulG)



#5GEXT
if len(dlG)>0:
    plt.rcParams['figure.figsize'] = (20, 10)
    plt.plot(time, dlG, '.r-', label = "download")
    plt.plot(time, ulG, '.b-', label = "upload")
    
    plt.xlabel('Test Time')
    plt.ylabel('Speed (GHz)')
    plt.title("Internet Speed (5GEXT)")
    plt.xlim(xmin = 0.0)
    plt.ylim(ymin = 0.0)
    
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    loc = mticker.MultipleLocator(base=3) # this locator puts ticks at regular intervals
    plt.gca().xaxis.set_major_locator(loc)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.show()



#5GHZ
if len(dl5)>0:
    plt.plot(time, dl5, '.r-', label = "download")
    plt.plot(time, ul5, '.b-', label = "upload")
    
    plt.xlabel('Test Time')
    plt.ylabel('Speed (GHz)')
    plt.title("Internet Speed (5GHz)")
    plt.xlim(xmin = 0.0)
    plt.ylim(ymin = 0.0)
    
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    loc = mticker.MultipleLocator(base=3) # this locator puts ticks at regular intervals
    plt.gca().xaxis.set_major_locator(loc)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.show()
    
    
    
#2.4GHz
if len(dl)>0:
    plt.plot(time, dl, '.r-', label = "download")
    plt.plot(time, ul, '.b-', label = "upload")
    
    plt.xlabel('Test Time')
    plt.ylabel('Speed (GHz)')
    plt.title("Internet Speed (2.4GHz)")
    plt.xlim(xmin = 0.0)
    plt.ylim(ymin = 0.0)
    
    plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    loc = mticker.MultipleLocator(base=3) # this locator puts ticks at regular intervals
    plt.gca().xaxis.set_major_locator(loc)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.show()

