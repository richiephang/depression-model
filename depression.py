
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import contractions
import nltk
nltk.download(['punkt', 'stopwords'])
from nltk.tokenize import word_tokenize

from gibberish_detector import detector
import re
from gensim.parsing.preprocessing import remove_stopwords,    \
                                         strip_non_alphanum,  \
                                         strip_numeric,       \
                                         strip_punctuation,   \
                                         strip_multiple_whitespaces, \
                                         STOPWORDS

path = r"probability.pkl"

f = open(path, "rb")
saved_model = pickle.load(f)
f.close()

path2 = r"classifier.pkl"
f = open(path2, "rb")
classifier = pickle.load(f)
f.close()

def clean_text(text):
    text = contractions.fix(text)
    text = pd.Series(text).str.replace("@[A-Za-z0-9_]+","", regex=True)
    text = text.str.replace(r"http\S+", "", regex=True)
    text = text.str.replace('[^\w\s#@/:%.,_-]', '', flags=re.UNICODE, regex=True)
    text = text.values.tolist()[0]
    text = strip_punctuation(text)
    text = strip_non_alphanum(text)
    text = strip_numeric(text)
    text = strip_multiple_whitespaces(text)
    text = text.lower()
    text = remove_stopwords(text)
    text = remove_gibberish(text)
    return text

path = 'big.model'
Detector = detector.create_from_model(path)

def remove_gibberish(text):
    words = word_tokenize(text)
    not_gibberish = [w for w in words if not Detector.is_gibberish(w)]
    return " ".join(not_gibberish)

class DepressionIndicator():
    """
    Depression Indicator implemented using Multinomial Naive Bayes model
    """

    def __init__(self, model, model2):
        self.model = model
        self.model2 = model2


    def chat(self):
        st.title("Welcome to Depression Chatbot")
        st.write("Hi! I am Bingo. Nice to meet you!")

        if 'count' not in st.session_state:
            st.session_state.count = 0
        if 'total_prob' not in st.session_state:
            st.session_state['total_prob'] = 0

        user_text = st.text_input('Enter Here or Q to quit: ').lower()
        if user_text == "q":
            st.write("Bingo has left the chat...")
            st.session_state.count = 0
            st.session_state['total_prob'] = 0

        elif user_text:
            st.session_state.count += 1       
            prob = self.predict(user_text)
            st.write("Probability:", prob)
            st.session_state['total_prob'] += prob
            st.write('Overall Probability:', st.session_state['total_prob'] / st.session_state.count)
            if prob>0.5:
                self.classify_depression()
 
    def classify_depression(self):
        mild_suggestion="**Suggestion 1: Exercise**  \n- There is strong evidence that any kind of regular exercise is one of the best antidepressants.  \n- Exercise helps to lower symptoms of anxiety, improve sleep quality, and boost energy levels.  \n  \n**Suggestion 2: Gratitude**  \n - Expressing gratitude has been shown to have a positive emotional effect on people with depression  \n- What you appreciate in your life can increase activity in the medial prefrontal cortex, the brain region often associated with depression.  \n  \n**Suggestion 3: Social connection**  \n- Join a group devoted to something for which you have a strong passion.  \n- For instance, volunteering for a favorite cause can keep you connected with others on a regular basis, plus you have the extra motivation to engage because of your personal interest."
        severe_suggestion="**Suggestion 1: Music Therapy Music has powerful effects on the mind**  \n- Different styles of music can have a significant effect on a person’s mood very quickly.  \n- It can help them experience and process a wide range of emotions, from happiness to excitement, as well as sadness, calmness, and thoughtfulness.  \n  \n**Suggestion 2: Seek help from mental health helplines**  \n  \n**First Organisation: MALAYSIAN MENTAL HEALTH ASSOCIATION (MMHA)**  \nContact Number: 03-2780 6803  \nE-Mail: admin@mmha.org.my  \nWebsite: https://mmha.org.my/  \n  \n**Second Organisation: SOLS HEALTH**  \nContact Number: 6018-900-7247  \nE-Mail: center@thethrive.center / info@thethrive.center  \nWebsite: https://www.thethrive.center/"
        st.markdown("***")
        st.header("\nWe detected that you might have depression.")
        st.write("We strongly suggest you to take the depression test below.")
        st.write("Over the last 2 weeks, how often have you been bothered by any of the following problems?")
        st.text("")
        st.subheader("\nRate from 0 - 3")
        st.text("0 represents NOT AT ALL")
        st.text("1 represents SEVERAL DAYS")
        st.text("2 represents MORE THAN HALF THE DAYS")
        st.text("3 represents NEARLY EVERY DAY\n")
        st.text("")
        st.text("")
        st.text("")
        q1 = st.slider("Little interest or pleasure in doing things: ",0,3,0)
        q2 = st.slider("Feeling down, depressed, or hopeless: ",0,3,0)
        q3 = st.slider("Feeling bad about yourself: ",0,3,0)
        q4 = st.slider("Feeling tired or having little energy: ",0,3,0)
        q5 = st.slider("Thoughts that you would be better off dead, or of hurting yourself: ",0,3,0)

        if st.button('Check result'):
            st.subheader("Result:")
            y_pred2 = self.model2.predict([[q1,q2,q3,q4,q5]])

            if y_pred2==1:
                st.subheader("You have a Severe Depression")
                st.write(severe_suggestion)
            else:
                st.subheader("You have a Mild Depression")
                st.write(mild_suggestion)

    def predict(self, text):
        clean = clean_text(text)
        pred = self.model.predict([clean])
        proba = np.max(self.model.predict_proba([clean]))
        if pred[0] == 1:
            st.write('Depressed')
            return proba
        else:
            st.write('Not Depressed')
            return 1 - proba

if __name__ == "__main__":
    depression_indicator = DepressionIndicator(saved_model,classifier)
    depression_indicator.chat()