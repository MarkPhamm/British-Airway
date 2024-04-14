from openai import OpenAI
import pandas as pd
import os
from datetime import datetime
# from dotenv import load_dotenv
import streamlit as st
# see also python-decouple

# openai.api_key = os.environ.get("OPEN_AI")
# openai_api_key = os.getenv("OPENAI_KEY")
openai_api_key = st.secrets['OPENAI_KEY']
model = "gpt-3.5-turbo-0125"

client = OpenAI(
    api_key = openai_api_key
#   api_key=os.environ.get("OPENAI_API_KEY")    
)

def return_chatgpt_review_negative(input):
    instruction = """ Here's the list of review for British Airway, extract negative aspect of BA in the review (use 5-10 bullet points) 
    Eg: BA has crammed as many seats in business, cabin felt cramped, The bedding was atrocious, an old scraggly blanket and I’ll fitting seat cover,... """

    chat_completion = client.chat.completions.create(
        model=model,
        max_tokens=100,
        temperature=0,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": input},
        ],
    )
    return chat_completion.choices[0].message.content

def return_chatgpt_review_positive(input):
    instruction = """ Here's the list of review for British Airway, extract positive aspect of British Airway in the review (use 5-10 bullet points)
      """

    chat_completion = client.chat.completions.create(
        model=model,
        max_tokens=100,
        temperature=0,
        messages=[
            {"role": "system", "content": instruction},
            {"role": "user", "content": input},
        ],
    )
    return chat_completion.choices[0].message.content
