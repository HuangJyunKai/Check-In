#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 23:59:51 2019

@author: aaron-mb
"""


import pandas as pd 
item = ['staff','office_time']

df = pd.DataFrame(columns=item)

print(df)

df.to_csv("office_time.csv", sep=",", index=False)


"""
df = pd.read_csv("office_time.csv")
df = df.append({'staff' : 'Aaron' , 'office_time' : 'aaa'} ,ignore_index=True)
df.to_csv("office_time.csv", sep="," , index=False)
"""