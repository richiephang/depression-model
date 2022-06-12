import streamlit as st
import requests
from streamlit_lottie import st_lottie
from PIL import Image

# ---- LOAD ASSETS ----
url = "https://assets10.lottiefiles.com/packages/lf20_ilwhiuo7.json"

def load_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def app():
    left_column, right_column = st.columns(2)
    with left_column:
        st.title('Home')
        st.write('This is the `Home Page` of the app')
        st.markdown("""
        ## What is Major depressive disorder?
        
        Major depressive disorder is among the most common and harmful mental health problems. 
        Depression is a prevalent mental disorder that can have a significant impact on people's mental health as well as their day-to-day lives. 
        Depression and mental illness are a key problem in society nowadays. It can cause a loss of interest in general activities that can lead to suicidal thoughts. 
        Hence, the need of an automated system that can help in detecting depression in people of various age groups is being realized.
        """)
        st.write("[Learn More >](https://www.healthyplace.com/depression/depression-information/what-is-depression-depression-definition-and-checklist)")
        st.write("---")
    with right_column:
        st_lottie(load_url(url), height=500, key="codings")
