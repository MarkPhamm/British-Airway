from openai import OpenAI
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
# see also python-decouple

load_dotenv()


current_date = datetime.now()

df = pd.read_csv('dataset\clean_data_expand.csv')
df['date_review'] = pd.to_datetime(df['date_review'])
# Filter the DataFrame for records within the current month and year
this_month_df = df.loc[(df['date_review'].dt.month == current_date.month) & (df['date_review'].dt.year == current_date.year)]
this_month_negative_input = this_month_df.loc[this_month_df['recommended'] == False]['review'].to_string(index = False)
this_month_positive_input = this_month_df.loc[this_month_df['recommended'] == True]['review'].to_string(index = False)

# openai.api_key = os.environ.get("OPEN_AI")
openai_api_key = os.getenv("OPENAI_KEY")
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

print(return_chatgpt_review_negative(input = this_month_negative_input))
# print(return_chatgpt_review_positive(this_month_positive_input))