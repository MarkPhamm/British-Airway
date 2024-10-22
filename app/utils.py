import streamlit as st
from datetime import datetime


def display_last_refresh_date():
    current_date = datetime.now()
    st.text(F"Last Refresh: {current_date}")