import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt 
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
import json
import base64
from PIL import Image

st.set_page_config(page_title = 'Personal Finance Management' , layout= "wide" ,  page_icon = ':bar_chart:')
z1, z2, z3 = st.columns([2,4,1])
with z2:
    st.header("Personal Finance Management :bar_chart:")


selected = option_menu(menu_title=  None, 
                            options = ['Expense' , 'Income' , 'About'],
                            icons= ['graph-up' , 'reception-4', 'person-lines-fill'],
                            orientation= "horizontal", )

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_filter = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_sIYkst1pmD.json')   

lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")


@st.cache(allow_output_mutation=True)
def read_csv():
    data = pd.read_csv("Dataset/personal_transactions.csv")
    data.rename(columns={'Transaction Type': 'Transaction_Type', 'Account Name': 'Account_Name'}, inplace=True)
    return data

data = read_csv()

data['year'] = pd.to_datetime(data['Date']).dt.year
data['month'] = pd.to_datetime(data['Date']).dt.month_name()
data['day'] = pd.to_datetime(data['Date']).dt.day
data['month_year'] = pd.to_datetime(data['year'].astype(str) + '-' + data['month'].astype(str) , yearfirst= True)

if selected == 'Expense':
    with st.sidebar:
            st_lottie(
        lottie_filter,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=200,
        width=200,
        key=None,)
    category = st.sidebar.multiselect(
                'Select The Category : ',
                options= data['Category'].unique(),
                default= data['Category'].unique())

    month = st.sidebar.multiselect(
        'Select Months here : ',
        options= data['month'].unique(),
        default= data['month'].unique())

    year = st.sidebar.multiselect(
        'Select Year here : ',
        options= data['year'].unique(),
        default= data['year'].unique())

    data = data.query('Category == @category & month == @month & year == @year ')

    l1, l2, l3, l4 , l5 = st.columns([2,2,2,2,2])

    with l1:
        tot_spend = data[data["Transaction_Type"] == "debit"]
        tot_spend = tot_spend.groupby(["Transaction_Type"])["Amount"].sum().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_spend._get_value(0, 'Total')) , title= {'text' : 'Total Spend'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)


    with l2 :
        tot_inc = data[data["Transaction_Type"] == "credit"]
        tot_inc = tot_inc.groupby(["Transaction_Type"])["Amount"].sum().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_inc._get_value(0, 'Total')) , title= {'text' : 'Total Income'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)
        

    with l3:
        tot_avg = data[data["Transaction_Type"] == "debit"]
        tot_avg = tot_avg.groupby(["Transaction_Type"])["Amount"].mean().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_avg._get_value(0, 'Total')) , title= {'text' : 'Avarage Spend'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)

    with l4:
        tot_avg_in = data[data["Transaction_Type"] == "credit"]
        tot_avg_in = tot_avg_in.groupby(["Transaction_Type"])["Amount"].mean().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_avg_in._get_value(0, 'Total')) , title= {'text' : 'Average Income'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)

    with l5:
        total_savings = round(((tot_inc._get_value(0, 'Total')-(tot_spend._get_value(0 , 'Total')))),3)
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= total_savings , title= {'text' : 'Total Saving'}))
        fig1.update_layout( width = 350 , height  = 350)
        st.write(fig1)

    
    st.markdown(f'<h1 style = " text-align : center ; color: Red;font-size:35px;">{"Expense Analysis"}</h1>', unsafe_allow_html=True)
    col1 , col2 = st.columns(2)
    with st.container():
        with col1:
            exp_data = data.groupby(['Transaction_Type'])
            exp_data = exp_data.get_group('debit')
            fig = px.histogram(exp_data, x='Amount', y='Category', color_discrete_sequence= ['orange'] ,  barmode='group' , width= 800 )
            fig.update_xaxes(showgrid=False, zeroline=False)
            fig.update_yaxes(showgrid=False, zeroline=False)
            fig.update_layout(title_text= "Total Expenses" ,title_x =  0.5 , title_font_color = 'red')
            st.plotly_chart(fig , config = {'displayModeBar' : False})
            

    with st.container():
        with col2:
            debit_data = data.groupby(['Transaction_Type'])
            debit_data = debit_data.get_group('debit')
            fig2 = px.pie(debit_data, names='Account_Name', values='Amount')
            fig2.update_layout(title_text= "Mode of Payment" ,title_x =  0.33 , title_font_color = 'red' )
            st.plotly_chart(fig2 , config = {'displayModeBar' : False})
    

    c1, c2 = st.columns([2,2])
    with st.container():
        with c2:
            
            debit_data = data[data["Transaction_Type"] == "debit"]
            debit_avg = debit_data.groupby(["Category"])["Amount"].mean().reset_index(name='Avarage')
            fig8 = px.bar(data_frame=debit_avg, x=debit_avg['Category'], y= debit_avg['Avarage'] , width = 800 , height = 500)
            fig8.update_xaxes(showgrid=False)
            fig8.update_yaxes(showgrid=False)
            fig8.update_layout(title_text="Avarage spend on category", title_x=0.5, title_font_color='red')
            st.plotly_chart(fig8 , config = {'displayModeBar' : False})

    with st.container():
        with c1:

            debit_data = data[data["Transaction_Type"] == "debit"]
            debit_avg =debit_data.groupby(["month_year"])["Amount"].sum().reset_index(name='Total')
            fig8 = px.line(data_frame=debit_avg, x='month_year', y='Total' , color_discrete_sequence= ['red'])
            fig8.update_xaxes(showgrid=False)
            fig8.update_yaxes(showgrid=False)
            fig8.update_layout(title_text="Monthly Spend", title_x=0.5, title_font_color='red')
            st.plotly_chart(fig8 , config = {'displayModeBar' : False})



if selected == 'Income':


    with st.sidebar:
            st_lottie(
        lottie_filter,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=200,
        width=200,
        key=None,)
    category = st.sidebar.multiselect(
                'Select The Category : ',
                options= data['Category'].unique(),
                default= data['Category'].unique())

    month = st.sidebar.multiselect(
        'Select Months here : ',
        options= data['month'].unique(),
        default= data['month'].unique())

    year = st.sidebar.multiselect(
        'Select Year here : ',
        options= data['year'].unique(),
        default= data['year'].unique())

    data = data.query('Category == @category & month == @month & year == @year ')


    l1, l2, l3, l4 , l5 = st.columns([2,2,2,2,2])

    with l1:
        tot_spend = data[data["Transaction_Type"] == "debit"]
        tot_spend = tot_spend.groupby(["Transaction_Type"])["Amount"].sum().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_spend._get_value(0, 'Total')) , title= {'text' : 'Total Spend'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)


    with l2 :
        tot_inc = data[data["Transaction_Type"] == "credit"]
        tot_inc = tot_inc.groupby(["Transaction_Type"])["Amount"].sum().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_inc._get_value(0, 'Total')) , title= {'text' : 'Total Income'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)
        

    with l3:
        tot_avg = data[data["Transaction_Type"] == "debit"]
        tot_avg = tot_avg.groupby(["Transaction_Type"])["Amount"].mean().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_avg._get_value(0, 'Total')) , title= {'text' : 'Avarage Spend'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)

    with l4:
        tot_avg_in = data[data["Transaction_Type"] == "credit"]
        tot_avg_in = tot_avg_in.groupby(["Transaction_Type"])["Amount"].mean().reset_index(name='Total')
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= (tot_avg_in._get_value(0, 'Total')) , title= {'text' : 'Average Income'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)

    with l5:
        total_savings = round(((tot_inc._get_value(0, 'Total')-(tot_spend._get_value(0 , 'Total')))),3)
        fig1 = go.Figure(go.Indicator(mode = 'gauge + number' , value= total_savings , title= {'text' : 'Total Saving'}))
        fig1.update_layout( width = 350 , height = 350)
        st.write(fig1)


    st.markdown(f'<h1 style = " text-align : center ; color: green;font-size:35px;">{"Income Analysis"}</h1>', unsafe_allow_html=True)

    col1 , col2 = st.columns([6,4])
    with st.container():
        with col2:

            credit_data = data.groupby(['Transaction_Type'])
            credit_data = credit_data.get_group('credit')
            fig3 = px.pie(credit_data, names='Account_Name', values='Amount' , width= 600 )
            fig3.update_layout(title_text="Mode of Payment", title_x=0.3, title_font_color='green')
            st.plotly_chart(fig3 , config = {'displayModeBar' : False})
            
    with st.container():
        with col1:
            credit_data = data[data["Transaction_Type"] == "credit"]
            credit_avg = credit_data.groupby(["month_year"])["Amount"].sum().reset_index(name='Total')
            fig8 = px.bar(data_frame=credit_avg, x='month_year', y='Total' , color_discrete_sequence= ['lime'])
            fig8.update_xaxes(showgrid=False)
            fig8.update_yaxes(showgrid=False)
            fig8.update_layout(title_text="Total Income", title_x=0.5, title_font_color='green')
            st.plotly_chart(fig8 , config = {'displayModeBar' : False})
            

    c1 , c2  = st.columns([2,2])
    with st.container():
        with c2:
            mon_data = data.groupby(['month_year', 'Transaction_Type'])['Amount'].sum().reset_index(name='Total')
            fig4 = px.bar(mon_data, x='month_year', y='Total', color='Transaction_Type', barmode='group' , width= 800,
                         color_discrete_sequence =  ['lightgreen' , 'red'], height= 500 )

            fig4.update_xaxes(showgrid = False)
            fig4.update_yaxes(showgrid=False)
            fig4.update_layout(title_text="Income vs Expense", title_x=0.5, title_font_color='green')
            st.plotly_chart(fig4 , config = {'displayModeBar' : False})

        with c1:
            debit_data = data[data["Transaction_Type"] == "credit"]
            debit_avg =debit_data.groupby(["month_year"])["Amount"].mean().reset_index(name='Total')
            fig8 = px.line(data_frame=debit_avg, x='month_year', y='Total' , color_discrete_sequence= ['blue'])
            fig8.update_xaxes(showgrid=False)
            fig8.update_yaxes(showgrid=False)
            fig8.update_layout(title_text="Avarage Monthly Income", title_x=0.5, title_font_color='green')
            st.plotly_chart(fig8 , config = {'displayModeBar' : False})

if selected == 'About':
    with st.container():
        l1 , l2 = st.columns((3,2))
        with l1:
            st.markdown('##            ')
            st.markdown('#####            ')
            st.markdown("### Hello and Welcome to my Personal Finance Management")
            st.markdown("#### I am Roshan :wave:, A Data science student from R. J. College.")
            st.markdown("###### In this project i have analysed a persons personal transaction data over a period of time.\n ###### There is detailed visulization of " + f'<h style = " color: Red;font-size:20px;">{"Expense"}</h>'+ " , " + f'<h style = "color: green;font-size:20px;">{"Income"}</h>' + '  And  ' + f'<h style = "color: blue;font-size:20px;">{"Category"}</h>' ""+"\n ###### This project will help the user to understand and track there expense for better investments and savinges. \n ###### i have created a detailed guide below on how to use this dashboard. ", unsafe_allow_html=True)
    with st.container():
        with l2:
            st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=300,
        width=300,
        key=None,)
            
    st.write('---')

    st.markdown('### Guide for the Dashboard')
    with st.container():
        x1 , x2 , x3 = st.columns([2,1,4])
        with x1:
            image1 = Image.open('images/filter.png')
            st.image(image1 , width= 600)

        with x3:
            st.markdown('###')
            st.markdown('#### How can you filter the data in this dashboard...')
            st.markdown('##### When user open the dashbord there will be a sidebar with filters.')
            st.markdown('##### This page will open by default, user can click on cross button to close filter section.')
            st.markdown('##### User can filter the data based on Category, Month and year.')
            st.markdown("##### For more you can watch the video on how to filter data.. \n [watch video...]()")

    st.write('---')
    with st.container():
        x1 , x2 , x3 = st.columns([2,1,4])
        with x1:
            image1 = Image.open('images/expanes.png')
            st.image(image1 , width= 600)

        with x3:
            st.markdown('###')
            st.markdown('#### How to Track your Expense in this Dashboard...')
            st.markdown('##### There are some major KPI and some Visulization of expense over time')
            st.markdown('##### On the first bar chart total expanes over different categorty is ploted on the other side there is a pie chart on account type.')
            st.markdown('##### scroll down there is a line chart on month wise spend and a bar chart on avarage spend on category. For more you can watch the video on how to filter data.. \n [watch video...]()')
    st.write('---')
    
    with st.container():
        x1 , x2 , x3 = st.columns([2,1,4])
        with x1:
            image1 = Image.open('images/income.png')
            st.image(image1 , width= 600)

        with x3:
            st.markdown('###')
            st.markdown('#### How to Track your Income in this Dashboard...')
            st.markdown('##### There are some major KPI and some Visulization of expense over time')
            st.markdown('##### On the first bar chart total income for different months is ploted on the other side there is a pie chart on account type.')
            st.markdown('##### scroll down there is a line chart on avarage income for all months  and a bar chart for comparinsion of Expense and Income. For more you can watch the video on how to filter data.. \n [watch video...]()')
    st.write('---')
    contact_form = """
            <form action="https://formsubmit.co/roshan.tiwari.24.5.2001@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here"></textarea>
                <button type="submit">Send</button>
            </form>"""
    with st.container():
        
        st.markdown('#### Get In Touch With Me! :mailbox:')
        
        st.markdown('####')
        x1 , x2= st.columns((2,2))
        with x2:
            
            st.markdown(contact_form, unsafe_allow_html=True)
    

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    local_css("style/style.css")


    with x1:

        lottie_contact = load_lottieurl('https://assets9.lottiefiles.com/packages/lf20_px0ntw70.json')
        st_lottie(
        lottie_contact ,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        height=300,
        width=600,
        key=None,)
        



        







