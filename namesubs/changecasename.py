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
    instrlist = ['*'+sys.argv[1]+'*.sum','*'+sys.argv[1]+'*.zones','*'+sys.argv[1]+'*.dat']
    #outstr = r'*'+argv[2]+'*.sum'
    for instr in instrlist:
        print(instr)
        for old in glob.glob(instr):
            print('Input File', old)
            outstr = old.replace(sys.argv[1],sys.argv[2])
            print('Output File:', outstr)
            os.rename(old,outstr)
    return print('done')


# In[ ]:


if __name__ == "__main__":
    main()
else:
    print('import as module')

