# AI-For-Road-Safety


Challenge hosted by **Omdena Hyderabad Chapter**

**Original Repo Link** : https://github.com/OmdenaAI/omdena-india-roadsafety

**Final Presentation Link** : https://docs.google.com/presentation/d/1Gk53mIN270ovEqfSlX6FUAC4_ynEWU3hHXVGxUJZtRg/edit?usp=sharing

**Google Drive** : https://drive.google.com/drive/folders/1cGs5Inm8AaTxmG9Ad6-lX6X_5CWBq7Zx

**Data Wrangling & Pre-Processing Dashboard** : https://public.tableau.com/app/profile/nikhil2069/viz/road_safety_EDA/EDAofTweets

**Computer Vision Demo Link** : https://drive.google.com/file/d/153NX6Sm9Re-gc8ZLYQ7GuJrxWhM7YRhp/view?usp=sharing

# Streamlit Application :

Streamlit Link : https://share.streamlit.io/prathimacode-hub/ai-for-road-safety/main/main.py

# Docker Application : 

Docker Link : https://hub.docker.com/repository/docker/snikhil17/omdena_road_safety

# Docker Steps:

## Note: 
- **snikhil17** : login ID of Dockerhub (use own when deploying)
- **omdena_road_safety**: name of the image created (you may use something else)

## To Push the image and run in your PC
## Create the image
- **docker build -t snikhil17/omdena_road_safety .**
## Run the image in  local PC
- **docker run -it -p 8501:8501 snikhil17/omdena_road_safety**
- **To run streamlit: once docker image is run. Open a new browser and run http://localhost:8501/**

## To Push image in docker-hub
- **docker login**
- **docker push snikhil17/omdena_road_safety** 

## To  pull the image and run in your PC
- **docker pull snikhil17/customer_intention_1:latest**
- **docker run -it -p 8501:8501  snikhil17/omdena_road_safety**
- To run streamlit: once docker image is run. Open a new browser and run **http://localhost:8501/**


# Tasks Involved:

## Natural Language Processing

Label & Sentiment Generator - Check out this application through Streamlit Demo App Link provided.

## Computer Vision

Eye Gaze Estimation + Drowsiness Detection + Yawn Detection

This application doesn't support Streamlit, hence it can compiled directly on Local Drive using generated [Driver Attention Estimation .exe file](https://drive.google.com/drive/folders/1cGs5Inm8AaTxmG9Ad6-lX6X_5CWBq7Zx) files uploaded in the drive.

Demo Link : https://drive.google.com/file/d/153NX6Sm9Re-gc8ZLYQ7GuJrxWhM7YRhp/view?usp=sharing


