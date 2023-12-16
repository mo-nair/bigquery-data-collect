#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime
import os
from os import listdir
from os.path import isfile, join
from datetime import timedelta, date


# In[2]:


## Full address to the folder where the data files from 2013-2014 are located
folder=r'Folder address'


# In[3]:


file_list=os.listdir(folder)


# In[5]:


sorted(file_list)
sorted(filter(lambda x: x.startswith('Data'), file_list))


# In[10]:


filtered_file_list=list(filter(lambda x: x.startswith('Data'), file_list))


# In[309]:


## Append all fragments into one dataframe - for ease of work 
frames=pd.DataFrame()
nn=0

for i in filtered_file_list:
    df1=pd.read_csv(folder+"/"+i)
    print(len(df1)) ## to control the size of the files read
    nn=nn+len(df1)
    frames=pd.concat([frames, df1])


# In[311]:


## Convert to datetime format
frames['date1']=pd.to_datetime(frames['created_at'])


# In[312]:


## Generate the index for each record
frames.reset_index(inplace=True)
frames['activity_id']=frames.index+1


# In[314]:


frames.drop(['index'], axis=1, inplace=True)


# In[316]:


import json


# In[317]:


### Extract repo name from repo
frames["repo_flat"]=frames['repo'].apply(json.loads).apply(pd.Series)
frames["repo_name"] = [d.get('name') for d in frames["repo_flat"]]


# In[318]:


### Extract actor login and id from actor

frames["actor_flat"]=frames['actor'].apply(json.loads).apply(pd.Series)
frames["actor_login"]= [d.get('login') for d in frames["actor_flat"]]


# In[319]:


### Extract payload action from payload

# frames["payload_flat"]=frames['payload'].apply(pd.Series)
frames["payload_flat"]=frames['payload'].apply(json.dumps).replace('\"','\'').apply(json.loads).apply(pd.Series)

# frames["payload_action"]= [d.get('action') for d in frames["payload"]]
# frames["payload_action"]= [d.get('action') for d in frames["payload_flat"]]


# In[321]:


# move the column to head of list using index, pop and insert
cols = list(frames)
cols.insert(0, cols.pop(cols.index('activity_id')))
cols.insert(len(cols), cols.pop(cols.index('payload')))


# In[322]:


frames = frames.loc[:, cols]


# In[323]:


## Remove unnecessary columns
frames.drop(['actor_flat','repo_flat','payload_flat'], axis=1, inplace=True)


# In[324]:


## Expost data to csv
frames.to_csv(folder+"/"+'Data_2013_2014_Merged.csv', index=False, sep=",")

