
# coding: utf-8

# In[1]:

get_ipython().magic('pylab inline')
import glob


# In[2]:

def readVoltagesCurrents_Channel(filename, channel):
    lines = tuple(open(filename, 'r'))
    counter=0
    columnStarter=3+2*channel
    voltages=empty((0))
    voltageMesured=""
    currents=empty((0))
    currentMesured=""
    times=empty((0))
    for line in lines:
        if(line!='\n'):         
            line = line.replace('\n', '')
            strings=line.split(";")
            if(strings[columnStarter].startswith( 'Vmeasure' )):
                voltageMesured=strings[columnStarter]
                currentMesured=strings[columnStarter+1]
            else:
                voltages=append(voltages, float(strings[columnStarter].replace(',','')))
                currents=append(currents,float(strings[columnStarter+1]))
                time=strings[1].split(":")
                times=append(times, float(time[0])*3600.0+float(time[1])*60.0+float(time[2]))
                counter+=1
    #Getting the time (ms) from the start of the mesurement
    firstTime=times[0]
    timesFromStart=times-firstTime
    #The current in microamps
    microcurrents=currents*1000000
    return voltages,microcurrents,timesFromStart


# In[3]:

def readVoltagesCurrentsTimes_All(filename):
    my_file=open(filename)
    num_lines = sum(1 for line in my_file) -2 #because of 2 extra lines
    if(num_lines>5000):
        num_lines=num_lines+1
    if(my_file.readline()!=""):
        num_lines=num_lines+1
    voltages=zeros((8,num_lines))
    microcurrents=zeros((8,num_lines))
    for channel in range (8):
        voltages[channel],microcurrents[channel],times=readVoltagesCurrents_Channel(filename, channel)
    return voltages,microcurrents,times


# In[4]:

#For everychannel. It's not efficient but it doesn't matter here.
fileset = glob.glob('06_17_2015/*.csv')
counter=0
for nfile in fileset:
    voltages, microcurrents,times=readVoltagesCurrentsTimes_All(nfile)
    figure(num=counter, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    title("Voltages of file: "+nfile)
    for i in range(8):
        plot(times,voltages[i], label='Channel '+str(i))
        xlabel("time(s)")
        ylabel("Voltage (V)")
    legend()
    counter+=1
    figure(num=counter, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    title("Currents of file: "+nfile)
    for i in range(8):
        plot(times,microcurrents[i], label='Channel '+str(i))
        xlabel("time(s)")
        ylabel("Current ( micro A )")
    legend()
    counter+=1


# In[ ]:



