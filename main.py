import streamlit as st
import base64
from predict_label import final_prep_prop
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('words')
from predict_label import regex_cleaning, word_2_vec_transform,  final_prep_prop, model_gensim
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
    
    st.markdown('', 
         unsafe_allow_html=True)

    
elif add_selectbox == 'About':
    
    st.subheader('ABOUT THE PROJECT')

    st.markdown('<h4>Project Goals</h4>', unsafe_allow_html=True)
    st.markdown('• Analyzing Road accidents data using Web Scraping from public databases, newspapers, web pages like Google News, Regional and National Newspapers and get a chart of accident prone areas in Hyderabad according to previous stats. etc. 2. Build an AI-Based method based on Machine Learning algorithms & Deep Learning to detect traffic accidents in real-time with the use of traffic cameras with high degrees of precision.', unsafe_allow_html=True) 
    st.markdown('• Build an NLP model for Label Generator which detects the kind of statement that it is using keywords mentioned in a data and Sentiment Analysis to  ', unsafe_allow_html=True) 
    st.markdown('• Build a Deep Learning-based solution for the driver monitoring system by studying a person’s posture and body movements, intelligent interior vehicle algorithms which can draw conclusions about a person’s alertness, attention and focus.', unsafe_allow_html=True) 
    st.markdown('• A Web Application to predict the probability of an accident from input video and actions of the driver.', unsafe_allow_html=True) 
    
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
    
    st.subheader('LABEL & SENTIMENT GENERATOR ')    
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
 
    
elif add_selectbox == 'Visualizations':
    
    st.subheader('PROJECT VISUALIZATIONS')
    st.markdown('<h4>Analysis of Road Accidents Vs Areas</h4>', unsafe_allow_html=True)
    st.image("analysis_of_road_accidents_vs_areas.png", width=800)
    st.markdown('<h4>Road Accidents Word Cloud Image1</h4>', unsafe_allow_html=True)
    st.image("road_accidents_word_cloud_1.png", width=400)
    st.markdown('<h4>Road Accidents Word Cloud Image2</h4>', unsafe_allow_html=True)
    st.image("road_accidents_word_cloud_2.png", width=800)

   
elif add_selectbox == 'Conclusion':

    st.subheader('TECH STACK')

    st.markdown('• Web Scraping - Twitter, Youtube, Reddit, Google News & News Channels', unsafe_allow_html=True)
    st.markdown('• Data Wrangling & Pre-Processing - Word Cloud, Exploratory Data Analysis on Road Accidents, Images Data Annotation', unsafe_allow_html=True)
    st.markdown('• NLP Modelling - Label Generator & Sentiment Analysis', unsafe_allow_html=True) 
    st.markdown('• Image Classification & Computer Vision Modelling - Eye Gaze Estimation, Drowsiness Detection, Yawn Detection, and Object Detection', unsafe_allow_html=True) 
    st.markdown('• Dashboard - Streamlit & Docker', unsafe_allow_html=True) 

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
    st.markdown('• <a href="https://www.linkedin.com/in/hardik-tejani/">Hardik Tejani</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/harshaljhirpara/">Harshal Hirpara</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/prathima-kadari/">Prathima Kadari</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/BhushanChougule/">Bhushan Chougule</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/tanisha-banik-04b511173/">Tanisha Banik</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/shreyachawla1998/">Shreya Chawla</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/pawani-morum-42788521/">Pawani Kumari Morum</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/vamsi-chittoor-331b80189/">Chittoor Vamsi</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/viveklalex/">Vivek L. Alex</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/goli-tarun/">Tarun Goli</a>',
                unsafe_allow_html=True)
    st.markdown('• <a href="https://www.linkedin.com/in/jayra-gaile-ortiz/">Jayra Gaile Ortiz</a>',
                unsafe_allow_html=True)
    

    st.subheader('PROJECT MANAGER')

    st.markdown('• <a href="https://www.linkedin.com/in/shaik-muhammad-yahiya/">Muhammad Yahiya</a>', unsafe_allow_html=True)
            
   
