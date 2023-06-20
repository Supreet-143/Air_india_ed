#!/usr/bin/env python
# coding: utf-8

# # Analyzing Air India's Domestic and international monthly passenger traffic

# ## About Dataset
# This dataset is about airline operations and performance. The data is quantitative and numerical in nature. It can be analyzed and used to derive insights on the airline's performance, capacity utilization, revenue generation, and efficiency. This type of data is commonly used in the airline industry for performance analysis, benchmarking, and decision-making purposes.
# 
# 1. Month: This column refers to the month in which the data was recorded.
# 
# 2. DEPARTURES: The number of flights that departed during the month in question.
# 
# 3. HOURS: Hours flown by the airline during the month in question. This can be used to track the airline's utilization of its fleet.
# 
# 4. KILOMETRE(TH): Kilometers flown by the airline during the month, measured in thousands. This can be used to track the airline's overall operational performance.
# 
# 5. PASSENGERS CARRIED: Number of passengers carried by the airline during a given month.
# 
# 6. PASSENGER KMS.PERFORMED(TH): Passenger kilometers performed by the airline during the month, measured in thousands. This can be used to track the airline's revenue performance.
# 
# 7. AVAILABLE SEAT KILOMETRE(TH): Seat kilometers available on the airline's flights during the month, measured in thousands. This can be used to track the airline's capacity utilization.
# 
# 8. PAX.LOAD FACTOR (IN %): Percentage of available seats that were actually occupied by passengers during the month in question. This is a key metric for airlines, as it indicates how effectively they are filling their planes.

# 1. Install 'opendatasets' python module for downloading datasets from online aources like kaggle and google drive using simple python commands.
# 2. '!' before pip is not a part of the pip command itself, instead, it is a prefix used in some interactive environments or shells to indicate that the command should be executed in the underlying system shell, rather than within the programming language's runtime environment.  

# In[2]:


get_ipython().system('pip install opendatasets --upgrade')


# ## Import all the neccessary modules 

# In[3]:


import opendatasets as od
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
get_ipython().run_line_magic('matplotlib', 'inline')


# By default, when you create a plot using matplotlib in a Jupyter Notebook, the plot will be shown as a separate interactive window. However, using %matplotlib inline sets the backend to inline, which means that the plot will be rendered within the notebook itself as a static image.

# ### Download dataset from kaggle
# When you want to download dataset from kaggle you need to do the following!!
# 1. Get the url from kaggle and save it as a string in a variable
# 2. With the 'od' module download the data into current directory
# 3. Get Kaggle username and key from your kaggle profile
# 4. Go to your kaggle account--> click on settings-->Account-->API-->Create New Token-->Download the json file on your local machine-->open with notepad-->you will have your username and key here

# In[4]:


dataset_url = 'https://www.kaggle.com/datasets/nishantbhardwaj07/airindia-monthly-passenger-traffic'
od.download(dataset_url)


# In[5]:


os.listdir('./airindia-monthly-passenger-traffic')


# Here you can view the downloaded datasets which are 
# 1. Domestic 
# 2. International
# 
# Let's load the datasets into two dataframes, one for domestic and another for international

# In[6]:


domestic_df = pd.read_csv('./airindia-monthly-passenger-traffic/AirIndia (Domestic).csv')
international_df = pd.read_csv('./airindia-monthly-passenger-traffic/AirIndia (International).csv')


# Let's have a look at the domestic_df

# In[7]:


domestic_df


# 1. From the above dataframe its clear that the shape of the data frame is (120, 9)
# 2. We can see som 'Nan' values, let's have a look at them

# In[8]:


domestic_df.fillna(0, inplace=True)
domestic_df


# - Here you have replaced all the 'Nan' Values with 0
# - Let us take a look at the financial year of the data set
# - We want the months to be represented in integers rather than string

# In[9]:


domestic_df.Month.unique()


# - Copy the above list as it will help us replace these strings with appropriate integers

# In[10]:


domestic_df.Month.replace(to_replace=['APR', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
       'JAN', 'FEB', 'MAR'], value=[4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3], inplace=True)
domestic_df.head(13)


# - From the above table it it clear that the financial year is between from april of current year till march of next year
# - Now let us take a look at the correlation of flights departed between each months of all years given.

# In[11]:


pivot_table_df = domestic_df.pivot(index='Month', columns='FY', values='DEPARTURES\n')
pivot_table_df


# In[12]:


plt.figure(figsize=(12, 8))
sns.heatmap(data=pivot_table_df, cmap='Blues', annot=True);


# - As we can see here since Financial Year(FY) 2014 till 2020, the departures of the air india flights kept on increasing and dropped suddenly in the jan of 2021, and remained relatively low untill december of 2022

# In[13]:


domestic_df


# - Let us remane the column names and make it look a little bit pleasant 

# In[14]:


domestic_df.rename(columns={'DEPARTURES\n' : 'Departures', 'HOURS\n':'Hours', 
                           'KILOMETER\n(TH)': 'Kilometers (in 1000s)', 
                           'PASSENGERS CARRIED\n':'Passengers_carried', 
                        'PASSENGER KMS. PERFORMED\n(TH)':'Passengers_kms_performed(in 1000s)', 
                          'AVAILABLE SEAT KILOMETRE\n(TH)':'Available_seat_kms(in 1000s)', 
                           'PAX. LOAD FACTOR#\n(IN %)' : 'Pax_load_factor(in percent)'}, inplace=True)


# In[15]:


domestic_df


# - Here for some reason 'PAX.LOAD FACTOR' is not renamed. let us have a closer look

# In[16]:


domestic_df.columns


# - As you can see there is a blank space behind the letter 'P', we need to account for that as well!!

# In[17]:


domestic_df.rename(columns={' PAX. LOAD FACTOR#\n(IN %)' : 
                            'Pax_load_factor(%)'}, inplace=True)
domestic_df


# - let us have a look at monthly average accross all the years!!

# groupby_month_df = domestic_df.groupby('Month').mean()
# groupby_month_df

# - Turn index column into column, which will be helpful in plotting the graphs.

# In[19]:


groupby_month_df.reset_index(inplace=True)
groupby_month_df


# - Let us plot a barplot to examine average departures in each month across all years!

# In[27]:


sns.barplot(x='Month', y='Departures', data=groupby_month_df);


# - Now let us have a look at yearwise average!!

# In[30]:


groupby_year_df = domestic_df.groupby('FY').mean()
groupby_year_df


# - Now let us examine how the trends have been year on year for each of the columns through some bar charts
# - Here we can drop the month column because it returns the average of all months which doesn't make sense

# In[31]:


groupby_year_df.drop('Month', axis=1, inplace=True)
groupby_year_df


# In[39]:


fig, axes = plt.subplots(nrows=len(groupby_year_df.columns), ncols=1, figsize=(10, 30))
for i in range(len(groupby_year_df.columns)):
    axes[i].bar(x=groupby_year_df.index, height=groupby_year_df.columns[i], color='blue', data=groupby_year_df)
    axes[i].set_title(groupby_year_df.columns[i], fontsize=10)
    axes[i].set_ylabel(groupby_year_df.columns[i], fontsize=10)
    axes[i].set_xlabel('FY', fontsize=10)
plt.tight_layout();


# - we see the increasing trend from FY14 till FY22 and there was a sudden drop in the growth of all other parameters.
# - Let's have a closer look at FY21

# In[42]:


fy_21_df = domestic_df[domestic_df['FY'] == 'FY21'].sort_values('Month')
fy_21_df


# In[44]:


monthwise_fy_21_df = fy_21_df.groupby('Month').sum()
monthwise_fy_21_df


# - Let's plot for all the variables monthwise and analyze

# In[57]:


sns.set_style("darkgrid")


# In[58]:


for i in range(len(monthwise_fy_21_df.columns)):
    sns.barplot(x=monthwise_fy_21_df.index, y=monthwise_fy_21_df.columns[i], data=monthwise_fy_21_df, errorbar="sd")
    plt.show();


# - As it is evident from the above plots that there have been 0 values in the month of april, and subsequent slow rise in the following month indicates covid lockdown!!

# ## Question 1
# - What is the total passenger carrying capacity of the airlines each month?

# In[59]:


domestic_df


# - we have passengers carried info and also occupancy percentage, so total passenger carrying capacity would be passengers_carried * 100/occupancy_percent
# 

# In[65]:


domestic_df['Total_passenger_capacity'] = domestic_df['Passengers_carried'] * (100/domestic_df['Pax_load_factor(%)'])
domestic_df


# In[66]:


passenger_monthly_agg_df = domestic_df.groupby('FY').sum()
passenger_monthly_agg_df


# In[68]:


plt.title('Total passenger capacity over the years')
sns.barplot(data=passenger_monthly_agg_df, x=passenger_monthly_agg_df.index, y=passenger_monthly_agg_df.Total_occupancy);


# ## Question 2
# - How has the trend of distance travelled per passenger been over the years?

# In[73]:


domestic_df['distance_per_passenger(in kms)'] = domestic_df['Passengers_kms_performed(in 1000s)'] * 1000 / domestic_df['Passengers_carried']
domestic_df


# In[75]:


fy_mean_df = domestic_df.groupby('FY').mean()


# In[80]:


plt.title('Distance per passenger over the years')
sns.lineplot(data=fy_mean_df, x=fy_mean_df.index, y=fy_mean_df['distance_per_passenger(in kms)']);


# - This line plot shows that despite the initial slowdown from FY14 till FY17 people are travelling more distances year on year.

# ## Question 3
# - What is the average distance covered by passengers in all years?

# In[71]:


np.mean(domestic_df['Passengers_kms_performed(in 1000s)'] * 1000 / domestic_df['Passengers_carried'])


# - Average distance travelled by each passenger in all these years is 997.13 kms

# ## Question 4
# - Show the total number of passengers carried over the years

# In[81]:


plt.title('Total number of passengers carried over the years')
sns.lineplot(data=fy_mean_df, x=fy_mean_df.index, y=fy_mean_df['Passengers_carried']);


# - Here we can see in the initial years from FY14 till FY20, there was a steady rise in the passenger traffic, follwed by a sudden dip in 2021 due to covid and again slowly the passenger carried by the airlines is slowly increasing!!

# ## Question 5
# - Anylyze the fleet utilization of the airlines!!

# In[82]:


plt.title('Number of hours air india flew its airlines over the years')
sns.lineplot(data=fy_mean_df, x=fy_mean_df.index, y=fy_mean_df['Hours']);


# In[ ]:




