#!/usr/bin/env python
# coding: utf-8

# In[7]:


import os
#import re
import glob
import sys


# In[18]:


def main():
    #argv = ['dummy','full_room_distance','base_back']
    print('------------SCRIPT USAGE-----------')
    print('python changecasename.py "existingcasename" "targetcasename"')
    print('EXAMPLE:  python changecasename.py "base_back" "npeople_front+teach"')
    print('-----------------------------------')
    instr = 'tec_parts_'+sys.argv[1]+'_*.dat'
    #outstr = r'*'+argv[2]+'*.sum'
    print(instr)
    for old in glob.glob(instr):
        flowtime = old.replace('tec_parts_'+sys.argv[1]+'_','').replace('.dat','')
        flowtime = float(flowtime)
        floor = int(flowtime)
        substract = flowtime-floor
        if substract == 0:
            outstr = old.replace(sys.argv[1],'_'.join(['toread',sys.argv[1]]))
            #print(outstr)
            print('Output File:', outstr)
            os.rename(old,outstr)
    return print('done')


# In[ ]:


if __name__ == "__main__":
    main()
else:
    print('import as module')

