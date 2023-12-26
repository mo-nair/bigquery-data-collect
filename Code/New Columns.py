#!/usr/bin/env python
# coding: utf-8

# In[101]:


import pandas as pd
import datetime

import chart_studio.plotly as py
import plotly.tools as tls
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import math
from datetime import timedelta, date
from __future__ import division  ## important: for float division 


# In[1]:


folder=r'/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023'


# In[2]:


stats_folder=r'/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023/Descriptive Stats by Year'


# In[4]:


merged_folder=r'/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023/Merged Datasets'


# In[5]:


file_list=os.listdir(folder)


# In[6]:


sorted(file_list)


# In[17]:


# data_file_list=filter(lambda name: 'Data' in name and len(name)==12, file_list)
# 


# In[18]:


# list(sorted(data_file_list))


# In[68]:


## Merge all DataYYYMM files together
data_file_list=filter(lambda name: 'Data' in name and len(name)==12, file_list)
data_file_list2=list(sorted(data_file_list))

merged_data_frames=pd.DataFrame()

for i in range(0,len(data_file_list2)):
    df_stats=pd.read_csv(folder+"/"+data_file_list2[i])
    yearr=data_file_list2[i][4:8]
    df_stats['Year']=int(yearr)
    df_stats["date1"]=pd.to_datetime(df_stats['date1']).dt.strftime('%Y-%m-%d')
    print(df_stats["date1"].iloc[100])
    merged_data_frames=merged_data_frames.append(df_stats)


# In[69]:


len(merged_data_frames)
merged_data_frames.head()


# In[70]:


# merged_data_frames['GhRepo'].iloc[-1].split("/",1)[1]
merged_data_frames['GhRepo_2']=merged_data_frames['GhRepo'].str.split(pat="/",expand=False).apply(lambda k: k[-1])
# merged_data_frames['GhRepo'].split("/",1)[1]


# In[71]:


merged_data_frames.head()


# In[72]:


cols = list(merged_data_frames)
# move the column to head of list using index, pop and insert
cols.insert(0, cols.pop(cols.index('GhRepo_2')))

cols


# In[73]:


merged_data_frames = merged_data_frames.loc[:, cols]


# In[74]:


merged_data_frames.to_csv(folder+"/"+'Data_AllYears_Merged.csv', index=False)


# In[59]:


print(folder+"/"+'Data_AllYears_Merged.csv')


# In[61]:


# data=pd.read_csv('/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023/Data_AllYears_Merged.csv')


# In[75]:


merged_data_frames[merged_data_frames['date1'].isna()]


# In[76]:


merged_data_frames.groupby(["date1"])['num_activities'].sum().sort_values(ascending=False)


# In[34]:


merged_data_frames.groupby(["GhRepo"])['num_activities'].sum().sort_values(ascending=False)


# In[77]:


folder


# In[84]:


year=20132014

df1=pd.read_csv(folder+"/"+'Data'+str(year)+'.csv')
df1.drop_duplicates(inplace=True)
df2=pd.read_csv(folder+"/"+'Data'+str(year)+'CoreUser.csv')
df2.drop_duplicates(inplace=True)

df1['date1']=pd.to_datetime(df1['date1']).dt.strftime('%Y-%m-%d')
df2_sub=df2[['GhRepo','date1','actor_id','is_core_developer','is_user_bot']]
fmerged=df1.merge(df2_sub,left_on=['GhRepo','date1','actor_id'], right_on=['GhRepo','date1','actor_id'],suffixes=('_left', '_right') )


# fmerged.to_csv(merged_folder+"/"+'Data'+str(year)+'Merged.csv', index=False)

# fmerged['num_activities_core_developer']=fmerged['num_activities']*fmerged['is_core_developer']
# fmerged['num_activities_periferal_developer']=fmerged['num_activities']-fmerged['num_activities_core_developer']
# fmerged['num_activities_bot']=fmerged['num_activities']*fmerged['is_user_bot']
# fmerged['num_activities_not_bot']=fmerged['num_activities']-fmerged['num_activities_bot']
# fmerged['num_actors_peripheral']=fmerged['num_actors_allevents']-fmerged['is_core_developer']
# fmerged['num_actors_not_bot']=fmerged['num_actors_allevents']-fmerged['is_user_bot']

# describe=fmerged.describe().transpose()
# describe.to_csv(stats_folder+"/"+'Data'+str(year)+'DescriptiveStats.csv', index=True)


# In[82]:


folder1='/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2013'


# In[86]:


year=20132014

df1=pd.read_csv(folder1+"/"+'Data'+str(year)+'.csv')
df1.drop_duplicates(inplace=True)
df2=pd.read_csv(folder1+"/"+'Data'+str(year)+'CoreUser.csv')
df2.drop_duplicates(inplace=True)

df1['date1']=pd.to_datetime(df1['date1']).dt.strftime('%Y-%m-%d')
df2_sub=df2[['GhRepo','date1','actor_login','is_core_developer','is_user_bot']]
fmerged=df1.merge(df2_sub,left_on=['GhRepo','date1','actor_login'], right_on=['GhRepo','date1','actor_login'],suffixes=('_left', '_right') )


fmerged.to_csv(merged_folder+"/"+'Data'+str(year)+'Merged.csv', index=False)

fmerged['num_activities_core_developer']=fmerged['num_activities']*fmerged['is_core_developer']
fmerged['num_activities_periferal_developer']=fmerged['num_activities']-fmerged['num_activities_core_developer']
fmerged['num_activities_bot']=fmerged['num_activities']*fmerged['is_user_bot']
fmerged['num_activities_not_bot']=fmerged['num_activities']-fmerged['num_activities_bot']
fmerged['num_actors_peripheral']=fmerged['num_actors_allevents']-fmerged['is_core_developer']
fmerged['num_actors_not_bot']=fmerged['num_actors_allevents']-fmerged['is_user_bot']

describe=fmerged.describe().transpose()
describe.to_csv(stats_folder+"/"+'Data'+str(year)+'DescriptiveStats.csv', index=True)


# In[312]:


# df1['date1']=pd.to_datetime(df1['date1']).dt.strftime('%Y-%m-%d')


# In[313]:


# df2_sub=df2[['GhRepo','date1','actor_id','is_core_developer','is_user_bot']]


# In[314]:


# fmerged=df1.merge(df2_sub,left_on=['GhRepo','date1','actor_id'], right_on=['GhRepo','date1','actor_id'],suffixes=('_left', '_right') )


# In[315]:


# fmerged.to_csv(folder+"/"+'Data'+str(year)+'Merged.csv', index=False)


# In[372]:


# fmerged['num_activities_core_developer']=fmerged['num_activities']*fmerged['is_core_developer']
# fmerged['num_activities_periferal_developer']=fmerged['num_activities']-fmerged['num_activities_core_developer']
# fmerged['num_activities_bot']=fmerged['num_activities']*fmerged['is_user_bot']
# fmerged['num_activities_not_bot']=fmerged['num_activities']-fmerged['num_activities_bot']
# fmerged['num_actors_peripheral']=fmerged['num_actors_allevents']-fmerged['is_core_developer']
# fmerged['num_actors_not_bot']=fmerged['num_actors_allevents']-fmerged['is_user_bot']


# In[373]:


# describe=fmerged.describe().transpose()


# In[374]:


# describe.to_csv(folder+"/"+'Data'+str(year)+'DescriptiveStats.csv', index=True)


# In[375]:


# describe


# In[87]:


stats_folder=r'/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023/Descriptive Stats by Year'


# In[88]:


file_list_stats=os.listdir(stats_folder)


# In[89]:


sorted(file_list_stats)


# In[90]:


frames=pd.DataFrame()


# In[91]:


for i in range(0,len(file_list_stats)):
    df_stats=pd.read_csv(stats_folder+"/"+file_list_stats[i])
    yearr=file_list_stats[i][4:8]
    df_stats['Year']=int(yearr)
    frames=frames.append(df_stats)


# In[92]:


frames.to_csv(folder+"/"+'DescriptiveStats_2015_2023.csv', index=False)


# In[ ]:


## Box plot


# In[93]:


merged_folder=r'/Users/mariiapetryk/Dropbox (UFL)/Prj Ethereum project/02_Data/Data 2014-2023/Merged Datasets'
merged_list=os.listdir(merged_folder)
sorted(merged_list)


# In[94]:


frames2=pd.DataFrame()
for i in range(0,len(merged_list)):
    df_stats=pd.read_csv(merged_folder+"/"+merged_list[i])
    yearr=merged_list[i][4:8]
    df_stats['Year']=int(yearr)
    frames2=frames2.append(df_stats)


# In[95]:


frames2['date1']=pd.to_datetime(frames2['date1'])
frames2['YYWW']=frames2['date1'].dt.year*100+frames2['date1'].dt.week
frames2['YYMM']=frames2['date1'].dt.year*100+frames2['date1'].dt.month


# In[96]:


frames2['num_activities_core_developer']=frames2['num_activities']*frames2['is_core_developer']
frames2['num_activities_periferal_developer']=frames2['num_activities']-frames2['num_activities_core_developer']
frames2['num_activities_bot']=frames2['num_activities']*frames2['is_user_bot']
frames2['num_activities_not_bot']=frames2['num_activities']-frames2['num_activities_bot']
# frames2['num_activities_bot']=frames2['num_activities']*frames2['is_user_bot']
frames2['num_actors_peripheral']=frames2['num_actors_allevents']-frames2['is_core_developer']
frames2['num_actors_not_bot']=frames2['num_actors_allevents']-frames2['is_user_bot']


# In[97]:


frames2_bymonth=frames2.loc[:, frames2.columns!='actor_id'].groupby(["GhRepo",'date1']).sum()


# In[98]:


frames2_bymonth.reset_index(level=['GhRepo', 'date1'],inplace=True)


# In[99]:


frames2_bymonth['Year']=frames2_bymonth['date1'].dt.year


# In[100]:



frames2_bymonth.to_csv(folder+"/"+'Data_by_Day_2015_2023.csv', index=True)


# In[401]:


frames2_bymonth.head()


# In[407]:


boxplot = frames2.boxplot(column=['num_activities_core_developer','num_activities_periferal_developer','num_activities_bot','num_activities_not_bot'])  


# In[403]:


describe_by_month=frames2_bymonth.groupby(['Year']).describe().unstack('Year')


# In[404]:


describe_by_month.index.names=['first','second','Year']


# In[405]:


descr_stats_by_month=pd.DataFrame(describe_by_month).reset_index().pivot(index=['first','Year'], columns="second")


# In[406]:


descr_stats_by_month.to_csv(folder+"/"+'DescriptiveStats_by_Day_2015_2023.csv', index=True)

