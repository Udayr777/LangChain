# Conversational Q&A Chatbot
# Where it helps to remember the message from the previous message
from langchain_community.llms.openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import ChatOpenAI
import os

load_dotenv() # load the API key from the environment file

# streamlit
st.set_page_config(layout="wide", page_title="Conversational Q&A Chatbot")
st.header("Hey, lets Chat")


chat = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),
                  temperature = 0.9)

print("API Key:", os.getenv("OPENAI_API_KEY"))


if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        SystemMessage(content= "You are a comedian AI assistant")]

def get_chatmodel_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = chat(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content

input = st.text_input("Input", key="input" )
response = get_chatmodel_response(input)

submit = st.button("Ask your Question")

# If button is clicked
if submit:
    st.subheader("Your answer is")
    st.write(response)












