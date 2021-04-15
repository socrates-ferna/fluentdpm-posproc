#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt


# In[2]:


import readers
#from functions import plotagainstparam, percentage, read_results
import pandas as pd
import csv
from glob import glob


# In[3]:


def plotagainstparam(resultdict,column,filterstring,instant,xlab,ylab,leg):
    """
    Plots the result of a percentage value across the studied parameter variation.
    Example: plotagainstparam(timesdict,'Particle %','student') will sum all % of particles
    trapped by students in each dataframe of times dict and will plot that agains the variation
    parameter (e.g. social distance in x-axis and % of particles in y-axis)
    """
    xlist = []
    ylist = []
    for param,df in resultdict.items():
        #we sum all particles trapped in a surface
        xlist.append(param)
        ylist.append(df[column].loc[df.Fate.str.contains(fr"{filterstring}",regex=True)].loc[instant].sum())
        
    plt.plot(xlist,ylist,label=leg)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()


# In[4]:


def percentage(df,column,param,totals):
    """
    Adds the percentage column with respect to the total passed.
    
    Usage: dataframe = percentage(dataframe, column,parameter,totalsdict)
    
    Example: timesdict[2] = percentage(timesdict[2],'Number', 'Particles', totalsdict[2])
    The example calculates the percentage of 'Number' of particles that represent each row 
    of the data frame corresponding to the parameter value '2' with respect to the total number of particles injected
    
    The added column is the string 'column %'
    """
    newname = param + ' %'
    if newname in df.columns:
        print(newname,' already exists overwrite?')
        #pending
        answer = input('y/n')
        if answer == 'y':
            df[newname] = 0.0
            for (flowtime,i), row in df.iterrows():
                #print(flowtime)
                #print(row)
                df.loc[flowtime,newname] = df.loc[flowtime,column].values / totals[param].loc[flowtime].values *100
                #timesdict['2m'].loc[(flowtime,i),'Percentage %'] = timesdict['2m'].loc[(flowtime,i),'Number'] / totalsdict['2m'].loc[flowtime,'Particles']
        elif answer == 'n':
            print('not overwriting, returned df is the same')
        else:
            print('inappropriate answer, "no" is understood')
    else:
        df[newname] = 0.0
        for (flowtime,i), row in df.iterrows():
            #print(flowtime)
            #print(row)
            df.loc[flowtime,newname] = df.loc[flowtime,column].values / totals[param].loc[flowtime].values *100
    return df


# In[83]:


def read_results(casename):  #DEBERÍA PODER PASARLE SOLO EL CASENAME
    """
    Reads a list of files named with the string 'casename' (the actual case name)
    and with the extension of the parameter list passed.
    
    Requires the name of the file in which you can find the list of zones corresponding to the case
    
    Example: zones, timesdict, massdict, totalsdict = read_results('distance_','zones',distanceslist)
    
    Returns the dataframe for zones. A dictionary for the time summary and another for the mass summary both with the form:
    dictname = {distanceslist[0]: dataframe_0,distanceslist[1]:dataframe_1, ... }
    
    So you access to the dataframe of the first element in the parameter list with dictname[distanceslist[0]], where
    distanceslist[0] can be substituted for the actual value. Let's say it is 2, then timesdict[2] will return
    the time summary for 2 metres between students
    
    """
    #casename = casename + '_'
    zones = readers.read_zones(casename + '.zones')
    masslist = []
    timeslist = []
    #tdict = {}
    #mdict = {}
    #totalsdict = {}
    """
    Puedes aislar el parámetro en los nombres de la carpeta con paramlist
    Para ello tienes que explicarles que aquí sí que deben separar el parámetro del nombre base
    Voy a dejar el loop fuera y hago un dict from keys
    Aquí dentro hago el tiempo solamente.
    casename entra y es el prefijo
    """
    globname = casename + '_*.sum'
    masscols = ['Fate','Initial','Final', 'Change','flowtime']
    timecols = ['Fate', 'Number', 'Min', 'Max', 'Avg', 'Stdev', 'injection','flowtime']
    totcols = ['Particles','Mass','flowtime']
    massts = pd.DataFrame(columns=masscols)
    timests = pd.DataFrame(columns=timecols)
    totalsts = pd.DataFrame(columns=totcols)
    for file in glob(globname):
        print(file)
        instant = file.removesuffix('.sum').removeprefix(casename + '_')
        #print(instant)
        instantfloat = round(float(instant),2)
        timesdf, massdf, totals = readers.dpm_reader(file)
        totals['flowtime'] = instantfloat
        timesdf['flowtime'] = instantfloat
        massdf['flowtime'] = instantfloat
        #print(timesdf)
        #print(massdf)
        timests = timests.append(timesdf,ignore_index=True)
        massts = massts.append(massdf,ignore_index=True)
        totalsts = totalsts.append(totals, ignore_index=True)
        print(totals)
        #break
        #print(timeseriestimes)
        #print(timeseriesmass)
        #print(zones)
    timests.set_index(['flowtime',timests.index],inplace=True)
    massts.set_index(['flowtime',massts.index],inplace=True)
    totalsts.set_index(['flowtime',totalsts.index],inplace=True)
    return zones, timests, massts, totalsts


# In[90]:


def build(casename,plist):
    timesdict = dict.fromkeys(plist)
    massdict = dict.fromkeys(plist)
    zonesdict = dict.fromkeys(plist)
    totalsdict = dict.fromkeys(plist)
    for i in plist:
        zonesdict[i],timesdict[i], massdict[i], totalsdict[i] = read_results(casename + '_' + str(i))
    return zonesdict, timesdict, massdict, totalsdict

