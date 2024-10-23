import streamlit as st
from datetime import datetime
import config as cfg

def display_last_refresh_date():
    st.text(F"Last Refresh: {cfg.last_refresh}")