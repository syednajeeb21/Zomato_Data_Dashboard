import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pickle
import plotly.express as px

df = pd.read_pickle(open("ZomatoDataDashboard.pkl", "rb"))
st.title('Zomato Data Dashboard')
country_list = list(df['Country'].unique())
country_list.insert(0, 'Overall')
selected_country = st.sidebar.selectbox('Select Country', country_list)
#st.header("Total number of Restaurants")
col1,col2,col3=st.columns(3, gap = 'large')
if selected_country == 'Overall':
    with col1:
        st.header("Total number of Restaurant {}".format(selected_country))
        count = df.shape[0]
        st.subheader(count)
    with col2:
        st.header("Total number of Expensive Restaurants")
        count = df['Expensive'].value_counts()[3]
        st.subheader(count)
    st.header("Expensive Pie Chart Ratio Overall")
    ch = df['Expensive'].value_counts().reset_index()
    fig = px.pie(ch, values = 'count', names = 'Expensive')
    st.plotly_chart(fig)
    with col3:
        st.subheader('Distribution of Restaurants as per their Ratings')
        fig, ax = plt.subplots()
        pie = df.groupby('Rating text')['Aggregate rating'].count()
        ax.pie(pie, autopct = '%1.1f%%', labels = df.groupby('Rating text')['Aggregate rating'].count().index)
        st.pyplot(fig)
    st.subheader("Distribution of Ratings")
    fig, ax = plt.subplots(figsize = (10,6))
    ax.hist(df['Aggregate rating'], bins = 10)
    st.pyplot(fig)

    st.subheader("Top Five Restaurants of the World")
    Table = df.groupby('Country', as_index=False)[['Restaurant Name', 'Votes']].max().sort_values(by='Votes',ascending=False).set_index('Restaurant Name').drop('Votes', axis = 1).head(5)
    st.table(Table)

else:
    xx = df[df['Country'] == selected_country][['Restaurant Name', 'Rating text', 'Votes']].sort_values(by = 'Votes', ascending = False).head(5)
    fig, ax = plt.subplots()
    ax.bar(xx['Restaurant Name'], xx['Votes'])
    #ax.set_xticklabels(ax.get_xticks(), rotation = 50)
    plt.xticks(rotation = 40)
    plt.title("Top Five Restaurants of {}".format(selected_country))
    st.pyplot(fig)

    st.header("Delivery Status of {}".format(selected_country))
    fig, ax = plt.subplots(figsize = (10,6))
    x = df[df['Country'] == selected_country]['Has Online delivery'].value_counts()
    plt.pie(x, autopct='%1.1f%%', colors=['blue', 'red'], labels=df[df['Country'] == selected_country]['Has Online delivery'].value_counts().index)
    plt.xticks(rotation=30)
    plt.title("Countries having Online Deliveries {}".format(selected_country))
    st.pyplot(fig)
