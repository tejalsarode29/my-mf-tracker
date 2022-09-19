import streamlit as st
from multipage import MultiPage
from pages import mfTracker, stockTracker 

st.sidebar.success("This Is V1.0.0")

# Create an instance of the app 
app = MultiPage()

app.add_page("MF Tracker", mfTracker.app)
app.add_page("Stock Tracker", stockTracker.app)

# The main app
app.run()