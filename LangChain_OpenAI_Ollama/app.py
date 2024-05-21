# In this project I'll be using OpenAI and LangChain for a ChatBots
# importing libraries
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #where intial templates are given
from langchain_core.output_parsers import StrOutputParser # which help in creating parser
import requests
import logging

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

# Verify environment variables
openai_key = os.getenv('OPENAI_API_KEY')
langchain_key = os.getenv('LANGCHAIN_API_KEY')
langchain_project = os.getenv('LANGCHAIN_PROJECT')

if openai_key is None:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")
if langchain_key is None:
    raise ValueError("LANGCHAIN_API_KEY is not set in the .env file.")
if langchain_project is None:
    raise ValueError("LANGCHAIN_PROJECT is not set in the .env file.")

# request the API keys from .env
os.environ['OPENAI_API_KEY'] = openai_key
os.environ['LANGCHAIN_API_KEY'] = langchain_key
os.environ['LANGCHAIN_PROJECT'] = langchain_project
# langsmith trackinga
os.environ['LANGCHAIN_TRACKING_V2'] = "true"

print(f"OPENAI_API_KEY: {openai_key}")
print(f"LANGCHAIN_API_KEY: {langchain_key}")
print(f"LANGCHAIN_PROJECT: {langchain_project}")
print(f"LANGCHAIN_TRACKING_V2: {os.getenv('LANGCHAIN_TRACKING_V2')}")

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def send_tracking_data(data):
    url = ""  
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logging.debug(f"Tracking data sent successfully: {response.json()}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send tracking data: {e}")

# Your existing LangChain and OpenAI setup code here...

# Example function to track a request
def track_request(question, response):
    tracking_data = {
        "question": question,
        "response": response,
        "project": os.getenv('LANGCHAIN_PROJECT')
    }
    send_tracking_data(tracking_data)




# define the prompt template
prompt_template = ChatPromptTemplate.from_messages([

        # if you give any system prompt, then you should give user prompt also
        ("system","You are a helpful assistant. Please response to the user queries."),
        ("user","Question:{question}")
        ]                                          
                                                   )

# steamlit framework

st.title("LangChain Demo with OpenAI API")
input_text = st.text_input("Search the topic you want")

# OpenAI LLM
llm = ChatOpenAI(model='gpt-3.5-turbo')
output_parser = StrOutputParser()
chain=prompt_template|llm|output_parser # combining all 3 chains

if input_text:
    st.write(chain.invoke({'question': input_text}))

