#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import matplotlib.pyplot as plt


# In[2]:


data = pd.read_excel('../DE_Merge.xlsx')


# In[3]:


data.head()


# In[4]:


# Overall
data['day'] = [x.dayofyear for x in data.OrderDate]
temp_overall = data[data.ChannelCode=='SwodeEU'].groupby('day')['Code'].count().reset_index()
temp_overall.plot(x='day', y='Code', legend=False)

data['week'] = [x.weekofyear for x in data.OrderDate]
temp_overall = data[data.ChannelCode=='SwodeEU'].groupby('week')['Code'].count().reset_index()
temp_overall.plot(x='week', y='Code')

temp_30 = data[(data.ChannelCode=='id') & (data.week==30)].groupby('day')['Code'].count().reset_index()
temp_29 = data[(data.ChannelCode=='id') & (data.week==29)].groupby('day')['Code'].count().reset_index()
temp_28 = data[(data.ChannelCode=='id') & (data.week==28)].groupby('day')['Code'].count().reset_index()
temp_30.plot(x='day', y='Code')
temp_29.plot(x='day', y='Code')
temp_28.plot(x='day', y='Code')


# In[35]:


# change1: RULE 1002 SWOCH

data1 = data[(data.OrderDate < '2013-08-09') & (data.OrderDate >= '2013-08-02')]
data2 = data[(data.OrderDate >= '2013-08-09') & (data.OrderDate < '2013-08-16')]


# In[36]:


print(len(data1))
print(len(data2))
len(data2) / len(data1)


# In[37]:


# number of bookings 
# RULE 1002
sheet1 = data1.groupby('ChannelCode')['Code'].count().reset_index()
sheet2 = data2.groupby('ChannelCode')['Code'].count().reset_index()
temp = sheet1.merge(sheet2, on='ChannelCode', how='left').fillna(0)
temp['ratio'] = temp['Code_y'] / temp['Code_x']

temp = temp.sort_values(by='Code_x', ascending=False)[0:9]


fig, ax = plt.subplots()
xticklabels = temp['ChannelCode']
temp.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 45)
ax.legend(['before', 'after'])
for index, x in enumerate(ax.xaxis.get_ticklabels()):
    if index == 7:
        x.set_color('red')
        

# number of bookings changed as :
# after / expected
123/(108*0.67776)


# In[38]:


# margin 
# RULE 1002
print(data1.Marge.sum())
print(data2.Marge.sum())
print(data2.Marge.sum() / data1.Marge.sum())

sheet1_margin = data1.groupby('ChannelCode')['Marge'].sum().reset_index()
sheet2_margin = data2.groupby('ChannelCode')['Marge'].sum().reset_index()
temp_margin = sheet1_margin.merge(sheet2_margin, on='ChannelCode', how='left').fillna(0)
temp_margin['ratio'] = temp_margin['Marge_y'] / temp_margin['Marge_x']
temp_margin


temp_margin = temp_margin.sort_values(by='Marge_x', ascending=False)[0:9]


fig, ax = plt.subplots()
xticklabels = temp_margin['ChannelCode']
temp_margin.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 45)
ax.legend(['before', 'after'])
for index, x in enumerate(ax.xaxis.get_ticklabels()):
    if index == 4:
        x.set_color('red')


# In[39]:


# Average Margin per Order for swoch 
# RULE 1002
sheet1_avgMargin = data1.groupby('ChannelCode')['Marge'].mean().reset_index()
sheet2_avgMargin = data2.groupby('ChannelCode')['Marge'].mean().reset_index()

temp_avgMargin = sheet1_avgMargin.merge(sheet2_avgMargin, on='ChannelCode', how='left').fillna(0)
temp_avgMargin['ratio'] = temp_avgMargin['Marge_y'] / temp_avgMargin['Marge_x']
temp_avgMargin


# In[43]:


# ONLINE CM 1002
sheet1_margin_ = data1.groupby('ChannelCode')['Online.CM'].sum().reset_index()
sheet2_margin_ = data2.groupby('ChannelCode')['Online.CM'].sum().reset_index()
temp_margin_ = sheet1_margin_.merge(sheet2_margin_, on='ChannelCode', how='left').fillna(0)
temp_margin_['ratio'] = temp_margin_['Online.CM_y'] / temp_margin_['Online.CM_x']
temp_margin_


# In[45]:


temp_margin_[temp_margin_['ChannelCode']!='swoch'].sum()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[29]:


# RULE 1001
data1 = data[(data.OrderDate < '2013-08-28') & (data.OrderDate >= '2013-08-21')]
data2 = data[(data.OrderDate >= '2013-08-28') & (data.OrderDate < '2013-09-04')]

data1.loc[:,'compare'] = ['yes' if x else 'no' for x in (data1['DepWorldPart']=='Europe') & (data1['ArrWorldPart']=='Southeast Asia')]
data2.loc[:,'compare'] = ['yes' if x else 'no' for x in (data2['DepWorldPart']=='Europe') & (data2['ArrWorldPart']=='Southeast Asia')]


# In[30]:


# number of bookings 
# RULE 1001
sheet1 = data1.groupby('compare')['Code'].count().reset_index()
sheet2 = data2.groupby('compare')['Code'].count().reset_index()
temp = sheet1.merge(sheet2, on='compare', how='left').fillna(0)
temp['ratio'] = temp['Code_y'] / temp['Code_x']

temp = temp.sort_values(by='Code_x', ascending=False)[0:9]


fig, ax = plt.subplots()
xticklabels = ['other', 'EU-SEAsia']
temp.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 0)
ax.legend(['before', 'after'])
for index, x in enumerate(ax.xaxis.get_ticklabels()):
    if index == 7:
        x.set_color('red')
        
for i, h in enumerate(temp.Code_x):
    ax.text(i-0.25, h+25, str(h), color='black', fontweight='bold') 
for i, h in enumerate(temp.Code_y):
    ax.text(i-0.08, h+25, str(h), color='black', fontweight='bold') 

# number of bookings changed as :
# after / expected

1-434/(455*1.123417)


# In[31]:


# margin 
# RULE 1001
print(data1.Marge.sum())
print(data2.Marge.sum())
print(data2.Marge.sum() / data1.Marge.sum())

sheet1_margin = data1.groupby('compare')['Marge'].sum().reset_index()
sheet2_margin = data2.groupby('compare')['Marge'].sum().reset_index()
temp_margin = sheet1_margin.merge(sheet2_margin, on='compare', how='left').fillna(0)
temp_margin['ratio'] = temp_margin['Marge_y'] / temp_margin['Marge_x']
temp_margin


temp_margin = temp_margin.sort_values(by='Marge_x', ascending=False)


fig, ax = plt.subplots()
xticklabels = ['other', 'EU-SEAsia']
temp_margin.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 0)
ax.legend(['before', 'after'])
for index, x in enumerate(ax.xaxis.get_ticklabels()):
    if index == 4:
        x.set_color('red')
        
for i, h in enumerate(temp_margin.Marge_x):
    if i == 0:
        ax.text(i-0.25, h+25, '57.6k', color='black', fontweight='bold') 
    else:
        ax.text(i-0.25, h+1600, '15.4k', color='black', fontweight='bold') 

for i, h in enumerate(temp_margin.Marge_y):
    if i == 0:
        ax.text(i-0.08, h+25, '65.4k', color='black', fontweight='bold') 
    else:
        ax.text(i-0.08, h+25, '14.3k', color='black', fontweight='bold') 

        


# In[32]:


# Average Margin per Order 
# RULE 1001
sheet1_avgMargin = data1.groupby('compare')['Marge'].mean().reset_index()
sheet2_avgMargin = data2.groupby('compare')['Marge'].mean().reset_index()

temp_avgMargin = sheet1_avgMargin.merge(sheet2_avgMargin, on='compare', how='left').fillna(0)
temp_avgMargin['ratio'] = temp_avgMargin['Marge_y'] / temp_avgMargin['Marge_x']
temp_avgMargin


# In[34]:


# ONLINE CM 1001
sheet1_margin_ = data1.groupby('compare')['Online.CM'].sum().reset_index()
sheet2_margin_ = data2.groupby('compare')['Online.CM'].sum().reset_index()
temp_margin_ = sheet1_margin_.merge(sheet2_margin_, on='compare', how='left').fillna(0)
temp_margin_['ratio'] = temp_margin_['Online.CM_y'] / temp_margin_['Online.CM_x']
temp_margin_


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[18]:


# RULE 1003 "Published"


data1 = data[(data.OrderDate < '2013-09-04') & (data.OrderDate >= '2013-08-28')]
data2 = data[(data.OrderDate >= '2013-09-04') & (data.OrderDate < '2013-09-11')]


# In[19]:


data.Description


# In[20]:


# RULE 1003 'Published'

sheet1 = data1.groupby('Description')['Code'].count().reset_index()
sheet2 = data2.groupby('Description')['Code'].count().reset_index()
temp = sheet1.merge(sheet2, on='Description', how='left').fillna(0)
temp['ratio'] = temp['Code_y'] / temp['Code_x']

temp = temp.sort_values(by='Code_x', ascending=False)[0:2]


fig, ax = plt.subplots()
xticklabels = ['Published', 'Securates']
temp.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 0)
ax.legend(['before', 'after'])
        
for i, h in enumerate(temp.Code_x):
    ax.text(i-0.25, h+25, str(h), color='black', fontweight='bold') 
for i, h in enumerate(temp.Code_y):
    ax.text(i-0.08, h+25, str(h), color='black', fontweight='bold') 
# number of bookings changed as :
# after / expected

temp
1975/(1704*1.017595)


# In[21]:


# margin 
# RULE 1003
sheet1_margin = data1.groupby('Description')['Marge'].sum().reset_index()
sheet2_margin = data2.groupby('Description')['Marge'].sum().reset_index()
temp_margin = sheet1_margin.merge(sheet2_margin, on='Description', how='left').fillna(0)
temp_margin['ratio'] = temp_margin['Marge_y'] / temp_margin['Marge_x']
temp_margin


temp_margin = temp_margin.sort_values(by='Marge_x', ascending=False)[0:2]


fig, ax = plt.subplots()
xticklabels = ['Published', 'Securates']
temp_margin.plot(kind='bar', ax=ax)
ax.set_xticklabels(xticklabels, rotation = 0)
ax.legend(['before', 'after'])

for i, h in enumerate(temp_margin.Marge_x):
    if i == 0:
        ax.text(i-0.25, h+25, '52.9k', color='black', fontweight='bold') 
    else:
        ax.text(i-0.25, h+25, '26.0k', color='black', fontweight='bold') 

for i, h in enumerate(temp_margin.Marge_y):
    if i == 0:
        ax.text(i-0.08, h+25, '54.3k', color='black', fontweight='bold') 
    else:
        ax.text(i-0.08, h+25, '27.9k', color='black', fontweight='bold') 
        
temp_margin


# In[22]:


# Average Margin per Order 
# RULE 1003
sheet1_avgMargin = data1.groupby('Description')['Marge'].mean().reset_index()
sheet2_avgMargin = data2.groupby('Description')['Marge'].mean().reset_index()

temp_avgMargin = sheet1_avgMargin.merge(sheet2_avgMargin, on='Description', how='left').fillna(0)
temp_avgMargin['ratio'] = temp_avgMargin['Marge_y'] / temp_avgMargin['Marge_x']
temp_avgMargin


# In[23]:


1-0.8852


# In[24]:


data2.head()


# In[28]:


# ONLINE CM 1003
sheet1_margin_ = data1.groupby('Description')['Online.CM'].mean().reset_index()
sheet2_margin_ = data2.groupby('Description')['Online.CM'].mean().reset_index()
temp_margin_ = sheet1_margin_.merge(sheet2_margin_, on='Description', how='left').fillna(0)
temp_margin_['ratio'] = temp_margin_['Online.CM_y'] / temp_margin_['Online.CM_x']
temp_margin_


# In[ ]:





# In[ ]:




