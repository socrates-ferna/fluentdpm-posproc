#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import matplotlib.pyplot as plt
import readers


# In[ ]:


def plotagainstparam(resultdict,column,filterstring,xlab,ylab,leg):
    """
    Plots the result of a percentage value across the studied parameter variation.
    
    Example: plotagainstparam(timesdict,'Particle %','student','xlabel','ylabel','legend name') will sum all % of particles
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
    """
    Adds the percentage column with respect to the total passed.
    
    Usage: dataframe = percentage(dataframe, column,parameter,totalsdict)
    
    Example: timesdict[2] = percentage(timesdict[2],'Number',totalsdict[2])
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
            df[newname] = df[column] / totals[param] *100
        elif answer == 'n':
            print('not overwriting, returned df is the same')
        else:
            print('inappropriate answer, "no" is understood')
    else:
        df[newname] = df[column] / totals[param] *100
    return df

def read_results(casename,zonesfile,paramlist):
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

