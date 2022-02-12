import streamlit as st
import base64
from predict_label import final_prep_prop
import nltk
import time
import io
import tempfile, sqlite3
import os 
#import cv2
import subprocess, sys
from imageai.Detection import ObjectDetection

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('words')
from predict_label import regex_cleaning, word_2_vec_transform, final_prep_prop, model_gensim
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentimentAnalyser = SentimentIntensityAnalyzer()

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
    
    st.markdown('Each year, more than 1.2 million people die across the globe due to road crashes; there is a pressing need to understand the underlying cause of the problem. The important factors to consider are human errors, driver fatigue, poor traffic sense, mechanical fault of vehicle, speeding and overtaking violation of traffic rules, poor road conditions, traffic congestion and road encroachment. Lack of road safety measures and implementation of road safety laws are major concerns in our country.', unsafe_allow_html=True)
    st.markdown('To improve road safety measures, collecting and analyzing road accidents data can help in addressing this problem and take necessary precautions. Design an AI solution to detect driver’s condition & distractions like drowsiness, yawn and head pose that raise an alert when its detected. The main aim of this project is to help regulatory bodies, policymakers, and people while educating aspiring data scientists in solving real-world problems.', unsafe_allow_html=True)

    
elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• Analyze Road Accidents Data using Web Scraping various sources.', unsafe_allow_html=True) 
    st.markdown('• Build an NLP model to generate Label and Sentiment Analysis for the user-driven input thats submitted for prediction.', unsafe_allow_html=True) 
    st.markdown('• Build an AI-based method on Deep Learning & Intelligent Interior Vehicle Algorithms which can draw conclusions about a person’s alertness, attention and focus with high degrees of precision using drivers facial landmarks with webcam input.', unsafe_allow_html=True) 
    st.markdown('• Create a WebApp using Streamlit & Docker for the Road Safety.', unsafe_allow_html=True) 
    
    st.markdown('<h4>Developments Made</h4>', unsafe_allow_html=True)
    st.markdown('• Analyzed Road accidents data using Web Scraping from public databases, newspapers, web pages like Google News, Regional and National Newspapers and get a chart of accident prone areas in Hyderabad according to previous stats.',unsafe_allow_html=True)
    st.markdown('• Created a NLP model for that generates the Sentiment of a user text and adds a Label that predicts the kind of statement it is using keywords mentioned in the input.',unsafe_allow_html=True)
    st.markdown('• Created a Deep Learning model for driver monitoring system that studies the body movements that drives distraction while driving and signals back with a voice message to provide an alert.',unsafe_allow_html=True)
    st.markdown('• Initialized the Streamlit App and integrated the backend models to the application for users to visualize the analysis and check on with the results of the NLP models.',unsafe_allow_html=True)
    st.markdown('• Generated a .exe (executable) file for model that depicts Eye Gaze Estimation, Drowsiness Detection and Yawn Detection for it to be compiled on a local system directly. ',unsafe_allow_html=True)
    st.markdown('• Deployed the Streamlit App into Cloud (Docker) by activating and pushing the code sucessfully.',unsafe_allow_html=True)


elif add_selectbox == 'Features':

    st.subheader('FEATURES INVOLVED')

    st.markdown('• Label & Sentiment Generator', unsafe_allow_html=True)
    st.markdown('• Eye Gaze Estimation, Drowsiness Detection & Yawn Detection', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Natural Language Processing':   
    
    st.subheader('LABEL & SENTIMENT GENERATOR')    
    area = st.text_input('Enter the Text here (more than 3 words)', '#India has the largest number of ppl dying in road accidents. That + 99 more things to debate before we vote http://t.co/zkxbONv850')

    if st.button('submit'):
        sentiment = "positive" if sentimentAnalyser.polarity_scores(area)['compound'] > 0.5 else "negative" 
        label = final_prep_prop(area, model_gensim)
        if label == 'complaints' and sentiment == 'positive':
            st.write(f"Sentiment of Sentence: {sentiment} and Label of Sentence: General Information")
        elif label == 'appreciation' and sentiment == 'negative':
            st.write(f"Sentiment of Sentence: {sentiment} and Label of Sentence: disagreement")
        else:
            st.write(f"Sentiment of Sentence: {sentiment} and Label of Sentence: {label}")
    else:
        st.write("nothing")
        
        
# elif add_selectbox == 'Computer Vision':
    
#     st.subheader('OBJECT DETECTION')    
    
#     def detect_object(file, output_name):
#         detector = ObjectDetection()
#         detector.setModelTypeAsYOLOv3()
#         detector.setModelPath("yolo.h5")
#         detector.loadModel()
        
#         video_path = detector.detectObjectsFromImage(input_file_path= file,
#                                     output_file_path= output_name, 
#                                     frames_per_second=29, log_progress=True)
#         return video_path

#     def select_file(folder_path=os.getcwd()):
#         filenames = os.listdir(folder_path)
#         file_format = []
#         for file in filenames:
#             if file[-3:] == 'jpg':
#                 file_format.append(file)
#         selected_filename = st.selectbox('Select a image', file_format)
#         return os.path.join(folder_path, selected_filename)
    
#     home = os.getcwd()
#     opener ="open" if sys.platform == "darwin" else "xdg-open"

#     filename = select_file()
#     st.write('You selected `%s`' % filename)
#     if st.button('View Image'):
#         subprocess.call([opener, filename])
    
#     if st.button('Detect Objects and See Output'):
#         with st.spinner('Processing'):
#             output = detect_object(filename, 'final-output')
#         st.success('Done! Waiting for the output file to open')
#         time.sleep(1)
#         subprocess.call([opener, output])

    
elif add_selectbox == 'Visualizations':
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4>Analysis of Road Accidents Vs Areas</h4>', unsafe_allow_html=True)
    st.image("analysis_of_road_accidents_vs_areas.png", width=700)
    st.markdown('<h4>Road Accidents Word Cloud Image1</h4>', unsafe_allow_html=True)
    st.image("road_accidents_word_cloud_1.png", width=400)
    st.markdown('<h4>Road Accidents Word Cloud Image2</h4>', unsafe_allow_html=True)
    st.image("road_accidents_word_cloud_2.png", width=400)
    st.markdown('<h4>Word Cloud Using 100 Words</h4>', unsafe_allow_html=True)
    st.image("word_cloud_using_100words.png", width=400)
    st.markdown('<h4>Average of Positive & Negative Sentiments Score</h4>', unsafe_allow_html=True)
    st.image("average_of_positive_negative_sentiment_score.png", width=400)
    st.markdown('<h4>Average of Labels Score</h4>', unsafe_allow_html=True)
    st.image("average_of_labels_score.png", width=400)
    st.markdown('<h4>Median Number Of Sentences As Per Labels</h4>', unsafe_allow_html=True)
    st.image("median_sentences_per_labels.png", width=400)
    st.markdown('<h4>Median Number Of Words As Per Labels</h4>', unsafe_allow_html=True)
    st.image("median_words_per_labels.png", width=400)
    st.markdown('<h4>Facial Landmarks Points</h4>', unsafe_allow_html=True)
    st.image("facial_landmarks_model_visualization.png", width=400)

   
elif add_selectbox == 'Conclusion':

    st.subheader('TECH STACK')

    st.markdown('• Web Scraping - Twitter, Youtube, Reddit, Google News & News Channels & Road Accident Areas', unsafe_allow_html=True)
    st.markdown('• Data Wrangling & Pre-Processing - Word Cloud, Exploratory Data Analysis on Road Accidents & Images Data Annotation', unsafe_allow_html=True)
    st.markdown('• NLP Modelling - Label & Sentiment Generator', unsafe_allow_html=True) 
    st.markdown('• Image Classification & Computer Vision Modelling - Eye Gaze Estimation, Drowsiness Detection & Yawn Detection', unsafe_allow_html=True) 
    st.markdown('• Dashboard - Streamlit & Docker', unsafe_allow_html=True) 
    
    st.subheader('CONCLUSION')
    
    st.markdown('We have created a Centralized WebApp to Ensure Road Safety by checking on with the activities of the driver and activating label generator using NLP with Streamlit & Docker.', unsafe_allow_html=True)
    
    
elif add_selectbox == 'Team':
    
    st.subheader('COLLABORATORS')
   
    st.markdown('• <a href="https://www.linkedin.com/in/nikhilshreshta/">Nikhil Shrestha</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/hardik-tejani/">Hardik Tejani</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/harshaljhirpara/">Harshal Hirpara</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/shreyachawla1998/">Shreya Chawla</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/BhushanChougule/">Bhushan Chougule</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/tanisha-banik-04b511173/">Tanisha Banik</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/vamsi-chittoor-331b80189/">Chittoor Vamsi</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/viveklalex/">Vivek L. Alex</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/pawani-morum-42788521/">Pawani Kumari Morum</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/pawan-roy123/">Pawan Roy Choudhury</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/goli-tarun/">Tarun Goli</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/jayra-gaile-ortiz/">Jayra Gaile Ortiz</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/abdulbaaqi/">Abdul Baaqi Jempeji</a>',
                unsafe_allow_html=True)

    st.subheader('PROJECT MANAGER')

    st.markdown('• <a href="https://www.linkedin.com/in/shaik-muhammad-yahiya/">Muhammad Yahiya</a>', unsafe_allow_html=True)
