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
from predict_label import final_prep_prop


import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('words')
from predict_label import regex_cleaning, lemmatization, final_prep_prop

#Importing libraries for Gaze detection and head pose estimation
import cv2
import mediapipe as mp
import numpy as np
import math
import pyttsx3
import pygame 
from pygame import mixer

#Initializing variables for head pose estimation and Gaze detection
mixer.init()
voice_left = mixer.Sound('left.wav')
voice_right = mixer.Sound('Right.wav')
voice_down = mixer.Sound('down.wav')
eyes_blink= mixer.Sound('eyes_blink.wav')
yawn = mixer.Sound('Yawning.wav')

counter_right=0
counter_down=0
counter_left=0
FONTS =cv2.FONT_HERSHEY_COMPLEX

RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (255,0,0)
RED = (0,0,255)
CYAN = (255,255,0)
YELLOW =(0,255,255)
MAGENTA = (255,0,255)
GRAY = (128,128,128)
GREEN = (0,255,0)
PURPLE = (128,0,128)
ORANGE = (0,165,255)
PINK = (147,20,255)


#defining functions for head pose estimation and gaze detection 

def landmarksDetection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw :
        [cv2.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]
    return mesh_coord

def euclaideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

def blinkRatio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]
    # draw lines on right eyes 
    # cv.line(img, rh_right, rh_left, utils.GREEN, 2)
    # cv.line(img, rv_top, rv_bottom, utils.WHITE, 2)

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]

    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    rhDistance = euclaideanDistance(rh_right, rh_left)
    rvDistance = euclaideanDistance(rv_top, rv_bottom)

    lvDistance = euclaideanDistance(lv_top, lv_bottom)
    lhDistance = euclaideanDistance(lh_right, lh_left)

    reRatio = rhDistance/rvDistance
    leRatio = lhDistance/lvDistance

    ratio = (reRatio+leRatio)/2
    return ratio 


def MouthRatio(img, landmarks, top_indices, bottom_indices):

    lip_right = landmarks[bottom_indices[0]]
    lip_left = landmarks[bottom_indices[10]]

    lip_top = landmarks[top_indices[4]]
    lip_bottom = landmarks[bottom_indices[5]]

    MouthDistance = euclaideanDistance(lip_right, lip_left)
    lipDistance = euclaideanDistance(lip_top, lip_bottom)

    ratio = MouthDistance/lipDistance
    return ratio 


def colorBackgroundText(img, text, font, fontScale, textPos, textThickness=1,textColor=(0,255,0), bgColor=(0,0,0), pad_x=3, pad_y=3):
  
    (t_w, t_h), _= cv2.getTextSize(text, font, fontScale, textThickness) # getting the text size
    x, y = textPos
    cv2.rectangle(img, (x-pad_x, y+ pad_y), (x+t_w+pad_x, y-t_h-pad_y), bgColor,-1) # draw rectangle 
    cv2.putText(img,text, textPos,font, fontScale, textColor,textThickness ) # draw in text

    return img

Threshold_Frame = [200,500]
counter = 0
counter_eye = 0
counter_mouth = 0 
Counter_right=0
Counter_down=0
Counter_left=0
counter_left=0
counter_right=0
counter_down=0


#text = "#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850"

text = "@ndtv In India, most of the ambulances enter NO ENTRY roads and sometimes accidents occur - putting other road users to great risk."

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
    ("Home", "About", "Features", "Natural Language Processing", "Visualizations", "Conclusion", "Team")
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
    
    
elif add_selectbox == 'Natural Language Processing':   
    
    st.subheader('LABEL GENERATOR')    
    area = st.text_input('Enter the Text here', '#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850')

#     text_input = st.text("text")
    if st.button('submit'):
        st.write(final_prep_prop(area))
    else:
        st.write("nothing")
    
    
    st.subheader('SENTIMENT ANALYSIS')    
#     area = st.text_input('Enter the Text here', '#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850')

# #     text_input = st.text("text")
#     if st.button('submit'):
#         st.write(final_prep_prop(area))
#     else:
#         st.write("nothing")
        

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
    st.markdown('• <a href="https://www.linkedin.com/in/BhushanChougule/">Bhushan Chougule</a>',
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
                
