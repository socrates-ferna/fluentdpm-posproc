#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import pandas as pd
#import csv
#import os
from glob import glob
import re
from sys import argv


# In[ ]:


tecvars = ['Residence Time', 'X', 'Y', 'Z', 'U', 'V', 'W', 'Diameter', 'id', 'Current Time']


# In[ ]:


def main(casename):
    counter = 0
    paste = False
    digit = re.compile("\d")
    search = casename + '*'
    for name in glob(search):
        print('Input File: ', name)
        timestr = name.replace('.dat','').replace(casename,'') #here prefix will be casename in final version
        time = round(float(timestr),2)
        timestr = str(time)
        roundname = casename + timestr + '.dat'
        #print(roundname)
        with open('tec_' + roundname,'a') as fout:
            print('Output File: ', 'tec_' + roundname)
            fout.write('TITLE = "PARTICLE HISTORY"\n')
            fout.write('VARIABLES = ' + ','.join(['"' + x + '"' for x in tecvars]) + '\n')
            fout.write('ZONE T = "Particles",' + 'STRANDID = 50,' + 'SOLUTIONTIME = ' + timestr + ',DT = (' + ' '.join(['DOUBLE']*len(tecvars)) + ')\n')
            with open(name,'r') as fin:
                for line in fin:
                    #print(line+ str(counter))
                    #counter += 1
                    if not paste:
                        if digit.search(line[0]) :
                            paste = True
                            continue
                    else:
                        fout.write(line)
        paste = False
        print('done')


# In[ ]:


if __name__ == "__main__":
    main(argv[1])
else:
    print('import tecplot formatter')


# In[ ]:




