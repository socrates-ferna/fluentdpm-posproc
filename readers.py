# coding: utf-8

# PENDING:
# - FIXED Net row is added in mass pandas, fix
# - FIXED The matchnames only accepts one-digit zones
# - FIXED totals are strings

import pandas as pd
import csv

def clean_row(row):
    row = [x for x in row[:] if x]
    return row
#def addfate(row):  


# In[97]:


def read_zones(filepath):
    """
    Reads zones of simulation in report file and returns a DataFrame with the info
    """
    readzones = False
    with open(filepath,'r') as zf:
        reader = csv.reader(zf,delimiter=' ')
        for item in reader:
            if 'id' and 'name' in item:
                header = clean_row(item)
                zones = pd.DataFrame(columns=header)
                readzones = True
                continue

            if readzones:
                line = clean_row(item)
                if len(line) == 0 or line[0] == '>':
                    readzones = False
                    break
                if '-' in line[0]:
                    continue
                if len(line) != 5:
                    line.insert(3,'dummy')
                print(line)
                zones.loc[len(zones.index)+1] = line
    return zones


# In[247]:


def dpm_reader(filepath):
    """
    Reads the report file generated with the TUI command /report/dpm-extended-summary
    
    Input: filepath
    Output: residence time summary (df), mass deposition summary (df), total particles and mass injected (dict)
    
    """
    counter = 0
    dashcounter = 0
    readmass = False
    totals = {}
    with open(filepath,'r') as summary:
        reader = csv.reader(summary,delimiter=' ')
        for line in reader:
            #print(line)
            if counter == 0:
                if 'Max' and 'Min' in line:
                    cols = [x for x in line[:] if x]
                    cols = ['Fate', 'Number'] + cols
                    cols.remove('Dev')
                    cols = ['Stdev' if x == 'Std' else x for x in cols[:]]
                    cols.insert(6,'injection')
                    cols.insert(8,'injection')
                    times = pd.DataFrame(columns=cols)
                    counter = 1
                    continue
            elif counter == 1:
                row = clean_row(line)
                if len(line) > 0 and '-' in line[0]:
                    continue
                if 'Fluid' in row:
                    fate = row[0] + row[1]
                    row.pop(0)
                    row.pop(0)
                    row.insert(0,fate)
                    times.loc[len(times.index)+1] = row
                elif 'Trapped' in row:
                    fate = ' '.join(row[0:4])
                    row = row[4:]
                    row.insert(0,fate)
                    #print(row)
                    times.loc[len(times.index)+1] = row
                elif 'Injected' in row:
                    totals['Particles'] = int(row[1])
                    #totals.append(row[1])
                    counter += 1
                    print('COUNTER IS',counter)
                    continue
                else:
                    try:
                        times.loc[len(times.index)+1] = row
                    except:
                        print('Unconsidered Fate:',row[0:3])
                        continue
            elif counter == 2:
                row = clean_row(line)
                #print('enter')
                #print(row)
                if 'Initial' and 'Change' in row:
                    mcols = ['Fate','Initial','Final', 'Change']
                    mass = pd.DataFrame(columns=mcols)
                    readmass = True
                    #print(mass)
                    continue
                elif len(row) > 0 and '-' in row[0]:
                    if readmass:
                        dashcounter += 1
                    if dashcounter >=2:
                        readmass = False
                    continue
                elif 'Fluid' in row:
                    fate = row[0] + row[1]
                    row.pop(0)
                    row.pop(0)
                    row.insert(0,fate)
                    mass.loc[len(mass.index)+1] = row
                elif 'Trapped' in row:
                    fate = ' '.join(row[0:4])
                    row = row[4:]
                    row.insert(0,fate)
                    #print(row)
                    mass.loc[len(mass.index)+1] = row
                elif 'Injected' in row:
                    totals['Mass'] = float(row[1])
                    #print('toiaqui')
                    #totals.append(row[1])
                    counter += 1
                else:
                    try:
                        if readmass:
                            mass.loc[len(mass.index)+1] = row
                        else:
                            print('ignore line',row)
                            continue
                    except:
                        print('Unconsidered Fate:',row[0:3])
                        continue
            else:
                print('finished reading')
                break
    
    mass[['Initial', 'Final', 'Change']] = mass[['Initial', 'Final', 'Change']].apply(pd.to_numeric)
    times = times.loc[:,~times.columns.duplicated()]
    times[['Min', 'Max', 'Avg', 'Stdev', 'Number']] = times[['Min', 'Max', 'Avg', 'Stdev', 'Number']].apply(pd.to_numeric)
    mass['Fate'] = mass['Fate'].replace(to_replace='Trapped - Zone (\d{1,2})',value=r'\1',regex=True)
    times['Fate'] = times['Fate'].replace(to_replace='Trapped - Zone (\d{1,2})',value=r'\1',regex=True)
    #print(mass)
    #print(times)
    return times,mass,totals


# In[237]:


def matchnames(zones,df):
    """
    Matches the names in the zones dataframe with the reported ids in the dpm-extended-summary,
    then, it replaces the ids with the names to facilitate the labeling in plots
    """
    trapids = df['Fate'].loc[df['Fate'].str.contains(r'\d{1,2}',regex=True)].to_list()
    #print(trapids)
    matchlist = zones.id.isin(trapids)
    #print(matchlist)
    df['Fate'] = df.Fate.replace(to_replace=trapids, value=zones.name.loc[matchlist])
    #print(df)
    return df, matchlist

