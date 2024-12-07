import streamlit as st
from datetime import datetime
import refresh as rfr

def display_last_refresh_date():
    st.text(F"Last Refresh: {rfr.last_refresh}")