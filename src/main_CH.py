#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import copy
import re
import matplotlib.pyplot as plt


# In[2]:


data_save = pd.read_excel('../CH_merge.xlsx', sheet_name='CH_sample')


# In[3]:


data = data_save.copy()


# In[4]:


data.head()


# In[5]:


def categorize(x):
    if re.match(pattern='[Ss]ky.*', string=x):
        return 'skyscanner'
    elif x=='direct':
        return 'direct'
    else:
        return 'meta'
    
data['ChannelCode'] = data['ChannelCode'].fillna('direct')
data['channel'] = [categorize(x) for x in data.ChannelCode]


# In[6]:


data['day'] = [x.dayofyear for x in data.OrderDate]


# In[7]:


data1 = data.groupby(['channel','day'])['Code'].count().reset_index()
data1['day'] = [(x + 365) if x < 100 else x for x in data1['day']]


# In[8]:


data1.sort_values(by='day').head()


# In[9]:


fig, ax = plt.subplots(figsize=(20,5))
data1.sort_values(by='day').groupby('channel').plot(x='day',y='Code', ax=ax)
ax.legend(['direct', 'meta', 'skyscanner'])
plt.title('Number of Orders per Day', fontsize=20)

labels = ['', '2013-12-06', '2013-12-26', '2014-01-15', '2014-02-04', '2014-02-24']
ax.set_xticklabels(labels)

plt.axvline(x=21+365, color='black')
plt.axvline(x=24+365, color='black')
plt.axvline(x=28+365, color='black')
plt.axvline(x=31+365, color='black')


# In[11]:


data1.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# payment fee change


# In[12]:


def minmax(minimum, maximum, x):
    if x < minimum:
        return minimum
    elif x > maximum:
        return maximum
    else:
        return x

def payment(date, channel, method, total):
    if (date < pd.to_datetime('2014-1-21')): # phase 1
        if method == 'VISADC':
            return 0
        
        if channel == 'direct':
            if method in ('VISA', 'MC', 'PAYPAL'):
                return 12.64
            elif method == 'AMEX':
                return 14.74
            
        else:
            temp = total * 0.025
            if channel == 'meta':
                if method in ('VISA', 'MC', 'PAYPAL'):
                        return minmax(9.48, 30.54, temp)
                else:
                    return minmax(11.58, 30.54, temp)
            else:
                return minmax(0, 21.06, temp)
            
    elif (date < pd.to_datetime('2014-1-31')): # phase 2-4
        if method == 'VISADC':
            return 0
        else:
            temp = total * 0.035
            return minmax(7.37, 36.83, temp)
    
    else: # phase 5
        if method == 'VISADC':
            return 0
        elif method in ('AMEX', 'PAYPAL'):
            temp = total * 0.04
        elif method in ('VISA', 'MC'):
            temp = total * 0.035
        elif method == 'Postfinance':
            temp = total * 0.03
        
        return minmax(7.37, 36.83, temp) 

def payment_cost(method, payment):
    if method in ('VISA', 'MC', 'MAESTRO', 'VISAEL', 'VISADC'):
        return payment * 0.008
    elif method in ('CB', 'BMC', 'ECB', 'EMAIL'):
        return 0
    elif method == 'PAYPAL':
        return 0.45 + payment * 0.013
    elif method == 'AMEX':
        return payment * 1.95
    elif method == 'SOFORT':
        return 3.53
    elif method == 'Postfinance':
        return 6.32
    else:
        return 0


# In[13]:


temp = []

for index, row in data.iterrows():
    if row['CreditCardTypeName'] in ('EMAIL', 'Invoice'):
        temp.append(0)
    else:
        temp.append(payment(row['OrderDate'], row['ChannelCode'], row['CreditCardTypeName'], row['Verkoop.Bedrag']))

data['payment'] = temp

temp_ = []

for index, row in data.iterrows():
    temp_.append(payment_cost(row['CreditCardTypeName'], row['payment']))

data['payment_cost'] = temp_


# In[14]:


daily_payment = data.groupby('day')['payment'].sum().reset_index()
daily_payment['day'] = [(x + 365) if x < 100 else x for x in daily_payment['day']]

daily_payment_ = data.groupby(['day', 'channel'])['payment'].sum().reset_index()
daily_payment_['day'] = [(x + 365) if x < 100 else x for x in daily_payment_['day']]


fig, ax = plt.subplots(figsize=(20,5))
daily_payment.sort_values(by='day').plot(x='day',y='payment', ax=ax)
daily_payment_.sort_values(by='day').groupby('channel').plot(x='day',y='payment', ax=ax)
ax.legend(['ALL', 'direct', 'meta', 'skyscanner'])
plt.title('Sum Payment per Day', fontsize=20)

labels = ['', '2013-12-06', '2013-12-26', '2014-01-15', '2014-02-04', '2014-02-24']
ax.set_xticklabels(labels)

plt.axvline(x=21+365, color='black')
plt.axvline(x=24+365, color='black')
plt.axvline(x=28+365, color='black')
plt.axvline(x=31+365, color='black')


# In[35]:


# proportion
daily_payment_combined = daily_payment_.merge(daily_payment, on = 'day', how='left')
daily_payment_combined['ratio'] = daily_payment_combined['payment_x'] / daily_payment_combined['payment_y']


# In[30]:


daily_payment_combined[:21].groupby('channel')['ratio'].mean()


# In[32]:


daily_payment_combined[-21:].groupby('channel')['ratio'].mean()


# In[41]:


# per order
temp = data1.groupby('day')['Code'].sum().reset_index()
temp

temp2 = daily_payment.merge(temp, on='day', how='left')
temp2['avg'] = temp2.payment / temp2.Code
temp2


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[15]:


# payment cost change


# In[16]:


daily_payment_cost = data.groupby('day')['payment_cost'].sum().reset_index()
daily_payment_cost['day'] = [(x + 365) if x < 100 else x for x in daily_payment_cost['day']]

daily_payment_cost_ = data.groupby(['day', 'channel'])['payment_cost'].sum().reset_index()
daily_payment_cost_['day'] = [(x + 365) if x < 100 else x for x in daily_payment_cost_['day']]


fig, ax = plt.subplots(figsize=(20,5))
daily_payment_cost.sort_values(by='day').plot(x='day',y='payment_cost', ax=ax)
daily_payment_cost_.sort_values(by='day').groupby('channel').plot(x='day',y='payment_cost', ax=ax)
ax.legend(['ALL', 'direct', 'meta', 'skyscanner'])
plt.title('Sum Payment Cost per Day', fontsize=20)

labels = ['', '2013-12-06', '2013-12-26', '2014-01-15', '2014-02-04', '2014-02-24']
ax.set_xticklabels(labels)

plt.axvline(x=21+365, color='black')
plt.axvline(x=24+365, color='black')
plt.axvline(x=28+365, color='black')
plt.axvline(x=31+365, color='black')


# In[42]:


daily_payment_combined = daily_payment_cost_.merge(daily_payment_cost, on = 'day', how='left')
daily_payment_combined['ratio'] = daily_payment_combined['payment_cost_x'] / daily_payment_combined['payment_cost_y']


# In[43]:


daily_payment_combined[:21].groupby('channel')['ratio'].mean()


# In[44]:


daily_payment_combined[-21:].groupby('channel')['ratio'].mean()


# In[46]:


# per order
temp2 = daily_payment_cost.merge(temp, on='day', how='left')
temp2['avg'] = temp2.payment_cost / temp2.Code
temp2


# In[47]:


temp2.avg[:14].mean()


# In[48]:


temp2.avg[-14:].mean()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[17]:


# online.CM change


# In[18]:


daily_online = data.groupby('day')['Online.CM'].sum().reset_index()
daily_online['day'] = [(x + 365) if x < 100 else x for x in daily_payment_cost['day']]

daily_online_ = data.groupby(['day', 'channel'])['Online.CM'].sum().reset_index()
daily_online_['day'] = [(x + 365) if x < 100 else x for x in daily_online_['day']]


fig, ax = plt.subplots(figsize=(20,5))
daily_online.sort_values(by='day').plot(x='day',y='Online.CM', ax=ax)
daily_online_.sort_values(by='day').groupby('channel').plot(x='day',y='Online.CM', ax=ax)
ax.legend(['ALL', 'direct', 'meta', 'skyscanner'])
plt.title('Sum Online.CM per Day', fontsize=20)

labels = ['', '2013-12-06', '2013-12-26', '2014-01-15', '2014-02-04', '2014-02-24']
ax.set_xticklabels(labels)

plt.axvline(x=21+365, color='black')
plt.axvline(x=24+365, color='black')
plt.axvline(x=28+365, color='black')
plt.axvline(x=31+365, color='black')


# In[49]:


# per order
temp2 = daily_online.merge(temp, on='day', how='left')
temp2['avg'] = temp2['Online.CM'] / temp2.Code
temp2


# In[59]:


temp2 = temp2.sort_values(by='day')

fig, ax = plt.subplots(figsize=(20,5))
temp2.plot(x='day',y='avg', ax=ax)
ax.legend(['ALL', 'direct', 'meta', 'skyscanner'])
plt.title('Online.CM per Order per Day', fontsize=20)

labels = ['', '2013-12-06', '2013-12-26', '2014-01-15', '2014-02-04', '2014-02-24']
ax.set_xticklabels(labels)

plt.axvline(x=21+365, color='black')
plt.axvline(x=24+365, color='black')
plt.axvline(x=28+365, color='black')
plt.axvline(x=31+365, color='black')


# In[ ]:





# In[ ]:




