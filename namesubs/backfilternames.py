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
    instr = 'tec_parts_toread_'+sys.argv[1]+'_*.dat'
    #outstr = r'*'+argv[2]+'*.sum'
    print(instr)
    for old in glob.glob(instr):
        print('Input File', old)
        outstr = old.replace('_'.join(['toread',sys.argv[1]]),sys.argv[1])
        print(outstr)
        print('Output File:', outstr)
        os.rename(old,outstr)
    return print('done')


# In[ ]:


if __name__ == "__main__":
    main()
else:
    print('import as module')

