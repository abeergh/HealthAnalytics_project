#!/usr/bin/env python
# coding: utf-8

# #  Setup and import libraries

# In[3]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from ipywidgets import AppLayout, Button, Layout


# # Load csv files 

# ### Different csv files are loaded and saved into data frames:
#      1. Mortality: csv file that inclues covid19 mortality from January 2019 to June 2021
#      2. Life expectancy: csv file that includes life expectancy years by country 
#      2. Covid data: csv file that includes data about total confirmed cases and deaths by country
#      3. Health System Ranking: csv file that includes the ranking of health system performance by country

# In[110]:


all_mortality = pd.read_csv("C:\\Users\\Abeer\\Documents\\2.MSBA Program\\MSBA385_HealthcareAnalytics\\Health_analytics_project\\covid_mortalities_by_time.csv")


# In[132]:


life_expectancy = pd.read_csv("C:\\Users\\Abeer\\Documents\\2.MSBA Program\\MSBA385_HealthcareAnalytics\\Health_analytics_project\\life_expectancy.csv")


# In[133]:


covid_mor = pd.read_csv('C:\\Users\\Abeer\\Documents\\2.MSBA Program\\MSBA385_HealthcareAnalytics\\Health_analytics_project\\WHO_covid_data.csv')


# In[134]:


healthsystem_rank = pd.read_csv('C:\\Users\\Abeer\\Documents\\2.MSBA Program\\MSBA385_HealthcareAnalytics\\Health_analytics_project\\WHO_healthsystem_rank.csv')


# In[4]:


pop_data = pd.read_csv("C:\\Users\\Abeer\\Documents\\2.MSBA Program\\MSBA385_HealthcareAnalytics\\Health_analytics_project\\IHME_population_age.csv")


# In[5]:


pop_data = pop_data.loc[(pop_data['age_group_name']!='Early Neonatal') | (pop_data['age_group_name']!='Late Neonatal')|(pop_data['age_group_name']!='Post Neonatal')]


# In[6]:


df = pop_data[['location_name', 'age_group_name', 'val']]


# In[135]:


#merge the life expectancy dataframe with the covid_data in one dataframe
df_merged = pd.merge(life_expectancy,covid_mor, on='Country')
df_merged2 = pd.merge(df_merged,healthsystem_rank,on='Country')


# In[123]:


all_mortality =all_mortality.loc[(all_mortality['location']=='World')]


# In[124]:


#extract month and year from date field in the mortality dataframe
all_mortality['date'] = pd.to_datetime(all_mortality['date'], errors='coerce')
all_mortality['Period'] = pd.to_datetime(all_mortality['date']).dt.to_period('M')
#group results by sum of total deaths
#df_fig0 =all_mortality.groupby(['month_year']).agg({'new_deaths':'sum'}).unstack(level=0)


# In[125]:


df_fig0 =all_mortality[['location','Period','total_deaths']]
df_fig0 = df_fig0.rename(columns={'total_deaths':'Total Deaths'})


# In[126]:


#convert month_year column from period type to datetime to use in line chart
df_fig0['Period'] =df_fig0.Period.values.astype('datetime64[M]')


# In[ ]:


#add title and information to the streamlit dashboard page
st.set_page_config(layout="wide")
st.markdown( "<div style='background-color:#EBF5FB;  font-size:30px; text-align: center; color: #2E86C1 ; width: 100%'>MSBA Program</div>",
    unsafe_allow_html=True)
st.markdown( "<div style='background-color:#EBF5FB; margin-bottom: 10px; font-size:25px; text-align: center; color: #2E86C1 ; width: 100%'>Health Analytics Course</div>",
    unsafe_allow_html=True)
st.title("Analyzing the Association between Covid19 Mortality,Health System and Life Expectancy")


# In[ ]:


#add side bar to streamlit page
#st.sidebar.title("Filtering")
#locations = list(set(
#    list(all_mortality['location']) +
#    list(df_merged2['Country']) +
#    list(healthsystem_rank['Country'])
#))
#locations.insert(0, 'World')
#location = st.sidebar.selectbox("Locations", locations)

#all_mortality = all_mortality.loc[(all_mortality['location'] == location)]


# In[ ]:


#create the first figure
fig0 = px.area(df_fig0,
               x='Period',
               y='Total Deaths',
               title='Total Covid19 deaths in the world from Jan 2020 to June 2021')
fig0.update_layout(margin=dict(b=0))
st.plotly_chart(fig0, use_container_width=True)
st.markdown(
    "<div style='margin-bottom: 11px; font-size:10px; text-align: center; color: gray; width: 100%'>Data Source: Covid data Worldmeter.info</div>",
    unsafe_allow_html=True
)

#divide streamlit page into columns to organize the layout of the graphs
row2_1, row2_2 = st.beta_columns((1, 1))

with row2_1:
    st.subheader('Health Systems Performance ranking in 2019 by Country')
    df_fig_2 = df_merged2[['Rank', 'Country', 'Deaths - cumulative total per 100000 population']]
    df_fig_2 = df_fig_2.sort_values('Rank', ascending=True)
    df_fig_2 = df_fig_2.groupby(['Rank', 'Country']).size().to_frame().head(50).reset_index()
    fig_2 = go.Figure(
        data=go.Table(
            header=dict(values=list(df_fig_2[['Rank', 'Country']].columns)),
            cells=dict(values=[df_fig_2.Rank, df_fig_2.Country])
        )
    )
    fig_2.update_layout(margin=dict(t=0,l=0, r=50, b=0),autosize=False,
    width=500,
    height=300
)
    st.write(fig_2, use_container_width=True)
    st.markdown(
        "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data Source: WHO, Measuring Overall Health System Performance for 191 Countries</div>",
        unsafe_allow_html=True
    )

with row2_2:
    st.subheader('Covid19 deaths (cumulative total per 100000 population) by country')
    df_fig_1 = df_merged2[['Country', 'Deaths - cumulative total per 100000 population']]
    df_fig_1 = df_fig_1.sort_values(
        'Deaths - cumulative total per 100000 population', ascending=False
    ).head(50)
    fig_1 = px.bar(
        df_fig_1,
        x='Deaths - cumulative total per 100000 population',
        y='Country',
        color='Country'
    )
    fig_1.update_layout(margin=dict(b=0),autosize=False,
    width=500,
    height=300)
    st.plotly_chart(fig_1, use_container_width=True)
    st.markdown(
        "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data source: WHO- Covid19 mortality data</div>",
        unsafe_allow_html=True
    )

row3_1, row3_2 = st.beta_columns((1, 1))
with row3_1:
    st.subheader('Total confirmed Covid19 deaths vs Health System ranking')
    df_fig_4 = df_merged2[['Deaths - cumulative total per 100000 population', 'Rank']]
    fig_4 = px.scatter(
        df_fig_4,
        x='Rank',
        y='Deaths - cumulative total per 100000 population'
    )
    fig_4.update_layout(margin=dict(b=0,t=0),autosize=False,
    width=500,
    height=300)
    st.plotly_chart(fig_4, use_container_width=True)
    st.markdown(
        "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data source:WHO, Measuring Overall Health System Performance for 191 Countries</div>",
        unsafe_allow_html=True
    )

with row3_2:
    st.subheader('Total confirmed Covid19 deaths vs life expectancy')
    df_fig_3 = df_merged[[
        'Deaths - cumulative total per 100000 population',
        'Life Expectancy'
    ]]
    fig_3 = px.scatter(
        df_fig_3,
        x='Life Expectancy',
        y='Deaths - cumulative total per 100000 population'
    )
    fig_3.update_layout(margin=dict(b=0,t=0),autosize=False,
    width=500,
    height=300)
    st.plotly_chart(fig_3, use_container_width=True)
    st.markdown(
        "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data source: WHO- life expectancy(years) by country in 2019</div>",
        unsafe_allow_html=True
    )

df = pop_data[['location_name', 'age_group_name', 'val']]
df_fig6 = df.groupby(['location_name', 'age_group_name']).agg({'val': 'sum'}).reset_index()
df_fig6 = df_fig6.loc[
    (df_fig6['location_name'] == 'France') & (df_fig6['age_group_name'] != 'All Ages')
    ]
df_fig6['%population'] = (df_fig6['val'] / df_fig6['val'].sum()) * 100

df_fig7 = df.groupby(['location_name', 'age_group_name']).agg({'val': 'sum'}).reset_index()
df_fig7 = df_fig7.loc[
    (df_fig7['location_name'] == 'Italy') & (df_fig7['age_group_name'] != 'All Ages')
    ]
df_fig7['%population'] = (df_fig7['val'] / df_fig7['val'].sum()) * 100
df_age_pop = pd.concat([df_fig6, df_fig7])

#df_fig8 = df.groupby(['location_name', 'age_group_name']).agg({'val': 'sum'}).reset_index()
#df_fig8 = df_fig8.loc[
#    (df_fig8['location_name'] == 'South Sudan') & (df_fig8['age_group_name'] != 'All Ages')
#    ]
#df_fig8['%population'] = (df_fig8['val'] / df_fig8['val'].sum()) * 100

row4_1, row4_2 = st.beta_columns((1, 1))
with row4_1:
    
    fig_5 = px.bar(
        df_fig6,
        x='%population',
        y='age_group_name',
        color='age_group_name'
)
    st.plotly_chart(fig_5, use_container_width=True)
    fig_5.update_layout(margin=dict(b=0,t=0))
    st.markdown(
    "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data Source: Institute for Health Metrics and Evaluation(IHME) population forcasting</div>",
    unsafe_allow_html=True
)
with row4_2:
    
    fig_7 = px.bar(
        df_fig7,
        x='%population',
        y='age_group_name',
        color='age_group_name'
)
    st.plotly_chart(fig_7, use_container_width=True)
    fig_7.update_layout(margin=dict(b=0,t=0))
    st.markdown(
    "<div style='margin-bottom: 11px; font-size:10px; text-align: left; color: gray; width: 100%'>Data Source: Institute for Health Metrics and Evaluation(IHME) population forcasting</div>",
    unsafe_allow_html=True
)

