#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt


# In[2]:


import readers
#from functions import plotagainstparam, percentage, read_results
import pandas as pd
import numpy as np
import csv
from glob import glob


# In[3]:

def buildacrossdict(resultdict,col,filt,instant):
    ylist = []
    for param,df in resultdict.items():
        try:
            ylist.append(df[col].loc[df.Fate.str.contains(fr"{filt}",regex=True)].loc[instant].sum())
        except:
            ylist.append(0.0)
    return ylist

def barplot(resultdict,col,instant,fates):
    print('The function returns figure handle, ax.handles in a dict and bar lists in a dict with the passed fates as keys')
    print('Example: fig,ax,handles,bars = barplot(timesdict,"Particles %",60,["desk","in Fluid","Escaped","student"]')
    print('                                                                ^                      ^')
    print('                                                                |                      |')
    print('                                                               instant     list of fates/surfaces to search for')
    print('--------------------------------------------------------------------------------')
    labels = resultdict.keys()
    bars = {}
    handles = {}
    x = 1.5*np.arange(len(labels))
    width = 0.2
    i = 0.0
    n = len(fates)
    fig, ax = plt.subplots()
    for fate in fates:
        i += 1
        try:
            bars[fate] = buildacrossdict(resultdict,col,fate,instant)
            handles[fate] = ax.bar(x+width*(-n/2+i-0.5),bars[fate],width,label=fate)
        except:
            print('No fate found, skipping bar:', fate)
            continue
    #ax.set_xticks(x)
    #ax.set_xtickslabels(labels)
    #ax.legend()
    #ax.ylabel(col)
    print('Useful Commands:')
    print('ax.set_ylabel()')
    print('ax.set_title()')
    print('ax.set_xticks()')
    print('ax.set_xtickslabels')
    print('ax.legend()')
    print('ax.bar_label(handles[fate],padding=3)')
    print('plt.show()')
    return fig,ax,handles,bars


def plotagainstparam(resultdict,column,filterstring,instant,leg):
    """
    Plots the result of a percentage value across the studied parameter variation.
    Example: plotagainstparam(timesdict,'Particle %','student') will sum all % of particles
    trapped by students in each dataframe of times dict and will plot that agains the variation
    parameter (e.g. social distance in x-axis and % of particles in y-axis)
    """
    xlist = list(resultdict.keys())
    ylist = buildacrossdict(resultdict,column,filterstring,instant)
    plt.plot(xlist,ylist,label=leg)
    #plt.xlabel(xlab)
    #plt.ylabel(ylab)
    #plt.legend()


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


def read_results(casename):  #DEBER??A PODER PASARLE SOLO EL CASENAME
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
    print('Read zones: ' + casename + '.zones')
    zones = readers.read_zones(casename + '.zones')
    masslist = []
    timeslist = []
    #tdict = {}
    #mdict = {}
    #totalsdict = {}
    """
    Puedes aislar el par??metro en los nombres de la carpeta con paramlist
    Para ello tienes que explicarles que aqu?? s?? que deben separar el par??metro del nombre base
    Voy a dejar el loop fuera y hago un dict from keys
    Aqu?? dentro hago el tiempo solamente.
    casename entra y es el prefijo
    """
    globname = casename + '_*.sum'
    masscols = ['Fate','Initial','Final', 'Change','flowtime']
    timecols = ['Fate', 'Number', 'Min', 'Max', 'Avg', 'Stdev', 'injection','flowtime']
    totcols = ['Particles','Mass','flowtime']
    massts = pd.DataFrame(columns=masscols)
    timests = pd.DataFrame(columns=timecols)
    totalsts = pd.DataFrame(columns=totcols)
    print('Reading ' + casename + ' summaries')
    for file in glob(globname):
        #print(file)
        instant = file.replace('.sum','').replace(casename + '_','')
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
        #print(totals)
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
    print('start building...')
    for i in plist:
        print('building ',i)
        zonesdict[i],timesdict[i], massdict[i], totalsdict[i] = read_results(casename + '_' + str(i))
    return zonesdict, timesdict, massdict, totalsdict

def matchallnames(tdict,mdict,zns,parameter):
    for elem in parameter:
        tdict[elem],matchlist = readers.matchnames(zns[elem],tdict[elem])
        print('timesdict name substitution ' + str(elem))
        #print(matchlist)
        mdict[elem],matchlist = readers.matchnames(zns[elem],mdict[elem])
        print('massdict name substitution ' + str(elem))
        #print(matchlist)

def instant_to_latex(resultdict,cols,instant,printdf=True):
    k = list(resultdict.keys())
    for key,df in resultdict.items(): 
        df[cols].loc[instant].to_latex(buf='_'.join([str(key),str(instant),'.tex']),index=False,float_format="{:0.2f}".format)
        if printdf:
            print(df[cols].loc[instant].to_markdown())

def dropfates(resultdict,searchlist):
    if isinstance(resultdict,dict):
        newdict = dict.fromkeys(resultdict.keys())
        for key,df in resultdict.items():
            newdf = df
            for match in searchlist:
                newdf = newdf[~newdf.Fate.str.contains(match,regex=True)]
            newdict[key] = newdf
    elif isinstance(resultdict,pd.DataFrame):
        if isinstance(resultdict.columns,pd.core.indexes.multi.MultiIndex):
            newdf = resultdict
            idx = pd.IndexSlice
            for match in searchlist:
                newdf = newdf.loc[~newdf.loc[:,idx[:,'Fate']].squeeze().str.contains(match,regex=True)]
            newdict = newdf
        elif isinstance(resultdict.columns,pd.core.indexes.base.Index):
            newdf = resultdict
            for match in searchlist:
                newdf = newdf[~newdf.Fate.str.contains(match,regex=True)]
            newdict = newdf
        else:
            print('I dont know the columns index type of resultdict. It must be either pandas.core.indexes.base.Index or pandas.core.indexes.multi.MultiIndex. Check it with type(resultdict.columns)')
    else:
        print('I only support dictionaries or DataFrames as first argument')
    return newdict

def plotagainsttime(resultdict,fatelist,column='Particles %',mix=False,savefig=True):
    if mix == False:
        for key,df in resultdict.items():
            plt.figure()
            for f in fatelist:
                filtsum = df[column].loc[df.Fate.str.contains(fr"{f}",regex=True)].sum(axis=0,level='flowtime').reset_index(level='flowtime')
                plt.plot('flowtime',column,data=filtsum,label=f)
            plt.title(str(key) + ' time evolution')
            plt.xlabel('flow time')
            plt.ylabel(column)
            plt.legend()
            if savefig:
                plt.savefig(str(key)+'_'+column.replace(' ','').replace('%','')+'.pdf', bbox_inches="tight" )
    elif mix == True:
        for key,df in resultdict.items():
            for f in fatelist:
                filtsum = df[column].loc[df.Fate.str.contains(fr"{f}",regex=True)].sum(axis=0,level='flowtime').reset_index(level='flowtime')
                plt.plot('flowtime',column,data=filtsum,label=' '.join([str(key),f]))
            plt.title('Time evolution of selected parameters')
            plt.xlabel('flow time')
            plt.ylabel(column)
            plt.legend()
            if savefig:
                plt.savefig('mixedtimeevo.pdf',bbox_inches="tight")
        
    else:
        print('mix is neither True nor False, please pass mix=True or mix=False')

def changekey(d,old,new):   #PENDING
    d[new] = d.pop(old)
    return d

def colacrossparam(resultdict,instant,col='Particles %'):
    fates = pd.Series(dtype='string')
    k = list(resultdict.keys())
    k.insert(0,'Fate')
    level = [col] * len(k)
    tuples = zip(level,k)
    index = pd.MultiIndex.from_tuples(tuples)
    resultdf = pd.DataFrame(columns=index)
    idx = pd.IndexSlice
    #print(resultdf)
    for key,df in resultdict.items():
        fates = fates.append(df.loc[instant,'Fate'],ignore_index=True)
        fates = fates.drop_duplicates()
    fates.reset_index(drop=True,inplace=True)
    #print(fates)
    for key,df in resultdict.items():
        dfinst = df.loc[instant]
        result = [dfinst[col].loc[dfinst.Fate == x].iloc[0] if (dfinst.Fate == x).any() else '-' for x in fates]
        resultdf.loc[:,idx[col,key]] = result
    resultdf.loc[:,idx[col,'Fate']] = fates
    return resultdf
#map(changekey,[timesmixdict,massmixdict,totalsmixdict],zonesmixdict)