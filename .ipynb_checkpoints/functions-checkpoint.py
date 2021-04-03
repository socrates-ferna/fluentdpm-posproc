#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import readers


# In[ ]:


def plotagainstparam(resultdict,column,filterstring,xlab,ylab,leg):
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
        xlist.append(float(param))
        ylist.append(df[column].loc[df.Fate.str.contains(fr"{filterstring}",regex=True)].sum())
        
    plt.plot(xlist,ylist,label=leg)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()


# In[ ]:


def percentage(df,column,param,totals):
    newname = param + ' %'
    if newname in df.columns:
        print(newname,' already exists overwrite?')
        #pending
        input('y/n')
        if input == 'y':
            df[newname] = df[column] / totals[param] *100
        elif input == 'n':
            print('not overwriting, returned df is the same')
        else:
            print('inappropriate answer, "no" is understood')
    else:
        df[newname] = df[column] / totals[param] *100
    return df

def read_results(casename,zonesfile,paramlist):
    zones = readers.read_zones(zonesfile)
    masslist = []
    timeslist = []
    tdict = {}
    mdict = {}
    totalsdict = {}
    for i in paramlist:
        timesdf, massdf, totals = readers.dpm_reader(casename + str(i) + '.sum')
        masslist.append(massdf)
        timeslist.append(timesdf)
        totalsdict[i] = totals
    tdict = dict(zip(paramlist,timeslist))
    mdict = dict(zip(paramlist,masslist))
    return zones, tdict, mdict, totalsdict

