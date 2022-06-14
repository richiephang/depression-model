import streamlit as st
from multiapp import MultiApp
from apps import model, home # import your app modules here

app = MultiApp()
st.set_page_config(page_title=" Depression Indicator App", page_icon=":pill:", layout="wide")
st.markdown("""
# Depression Indicator App :hospital:

This app is designed to detect depression through text mining and classify whether a person is having mild or severe depression based on their symptoms and behaviors.

""")

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Depression Indicator", model.app)
# The main app
app.run()
