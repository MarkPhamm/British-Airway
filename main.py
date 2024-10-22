import os
import sys
import warnings

import streamlit as st
from dotenv import load_dotenv

import config as cfg
import app.pages.chatbot as chatbot
import app.pages.dashboard as dashboard

# Load environment variables
load_dotenv('.env')
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')

# Handle deployment configurations
if cfg.deploy:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    aws_access_key_id = st.secrets['aws_access_key_id']
    aws_secret_access_key = st.secrets['aws_secret_access_key']

import warnings

def configure_page():
    """Set the Streamlit page configuration."""
    st.set_page_config(layout="wide", page_title="British Airways Dashboard", page_icon="🛫")

def select_topic():
    """Create a sidebar for topic selection."""
    return st.sidebar.radio("Choose a topic", ["Review Dashboard", "Review Chatbot"])

def display_selected_topic(topic):
    """Display the selected topic's content."""
    if topic == "Review Chatbot":
        chatbot.display_chatbot()
    else:
        dashboard.display_dashboard(aws_access_key_id, aws_secret_access_key)

def main():
    # Suppress warnings
    warnings.filterwarnings("ignore")
    
    configure_page()
    topic = select_topic()
    display_selected_topic(topic)

if __name__ == "__main__":
    main()