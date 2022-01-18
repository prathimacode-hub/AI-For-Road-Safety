import datetime
import math
import folium
import geopandas as gpd
import geopy
import networkx as nx
import joblib
import osmnx as ox
import shapely.wkt
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import time
import base64
from branca.element import Figure
from folium.features import DivIcon
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from PIL import Image
from streamlit_folium import folium_static
from dateutil.relativedelta import relativedelta
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import geemap


st.set_page_config(
    page_title="AI For Road Safety In Hyderabad",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

st.sidebar.markdown('<h1 style="margin-left:8%; color:	#000080 ">AI For Road Safety In Hyderabad </h1>',
                    unsafe_allow_html=True)

add_selectbox = st.sidebar.radio(
    "",
    ("Home", "About", "Features", "Road Safety", "Visualizations", "Conclusion", "Team")
)

if add_selectbox == 'Home':
    
    LOGO_IMAGE = "omdena_india_logo.png"
    
    st.markdown(
          """
          <style>
          .container {
          display: flex;
        }
        .logo-text {
             font-weight:700 !important;
             font-size:50px !important;
             color: #f9a01b !important;
             padding-top: 75px !important;
        }
        .logo-img {
             float:right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
          f"""
          <div class="container">
               <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
          </div>
          """,
          unsafe_allow_html=True
    )
    
    st.subheader('PROBLEM STATEMENT')
    
    st.markdown('', 
         unsafe_allow_html=True)

    
elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)
    st.markdown('• ',unsafe_allow_html=True)


elif add_selectbox == 'Features':

    st.subheader('FEATURES INVOLVED')

    st.markdown('• ', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True)
    st.markdown('• ', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Road Safety':   
    
    st.subheader('ROAD SAFETY')    
    
        
elif add_selectbox == 'Output Visualizations':
    
    st.subheader('VISUALIZATIONS')

   
elif add_selectbox == 'Conclusion':

    st.subheader('TECH STACK')

    st.markdown('• Web Scraping - ', unsafe_allow_html=True)
    st.markdown('• Data Wrangling & Pre-Processing - ', unsafe_allow_html=True)
    st.markdown('• NLP Modelling - ', unsafe_allow_html=True) 
    st.markdown('• Image Classification & Computer Vision Modelling - ', unsafe_allow_html=True) 
    st.markdown('• Dashboard - Streamlit', unsafe_allow_html=True) 

    st.subheader('PROJECT SUMMARY')

    st.markdown('', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    st.markdown('• ', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Team':
    
    st.subheader('COLLABORATORS')

   
    st.markdown('• <a href="https://www.linkedin.com/in/nikhilshreshta/">Nikhil Shrestha</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/BhushanChougule/">Bhushan Choughule</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/tanisha-banik-04b511173/">Tanisha Banik</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/shreyachawla1998/">Shreya Chawla</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/vamsi-chittoor-331b80189/">Chittoor Vamsi</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/harshaljhirpara/">Harshal Hirpara</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/viveklalex/">Vivek L. Alex</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/goli-tarun/">Tarun Goli</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/pawani-morum-42788521/">Pawani Kumari Morum</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/hardik-tejani/">Hardik Tejani</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/jayra-gaile-ortiz/">Jayra Gaile Ortiz</a>',
                unsafe_allow_html=True)
    

    st.subheader('PROJECT MANAGER')

    st.markdown('• <a href="https://www.linkedin.com/in/shaik-muhammad-yahiya/">Muhammad Yahiya</a>', unsafe_allow_html=True)
                
