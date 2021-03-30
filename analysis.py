#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import readers
import pandas as pd
import csv
import matplotlib.pyplot as plt


# In[ ]:


zones = readers.read_zones('zones')
times, mass, totals = readers.dpm_reader('prueba.sum')


# ## Here we write our plotting code
# You access the data of the columns in dataframes by df['nameofcolumn'] where df is the name of your dataframe (times, zones, mass)
