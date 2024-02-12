from langchain_community.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv() # load environment variables from .env
print(os.getenv("OPENAI_API_KEY"))

import streamlit as st

# Function to load OpenAI model and get response
def get_openai_response(question):
    llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                 temperature=0.9)
    response = llm(question)
    return response


# initialize our Streamlit App
    
st.set_page_config(layout="wide", page_title="Q&A Demo")
st.header("LangChain Application")

input = st.text_input("Input: ", key="input")
response = get_openai_response(input)

submit = st.button("Ask the Question")

# if submit is clicked
if submit:
    st.subheader("The Response is")
    st.write(response)

