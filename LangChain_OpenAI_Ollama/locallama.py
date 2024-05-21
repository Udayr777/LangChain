from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate #where intial templates are given
from langchain_core.output_parsers import StrOutputParser # which help in creating parser
from langchain_community.llms import Ollama # for 3rd party LLM we use langchain_community

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv() # load the API key from the environment file

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

## Prompt Template

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please response to the user queries"),
        ("user","Question:{question}")
    ]
)
## streamlit framework

st.title('Langchain Demo With LLAMA2 API')
input_text=st.text_input("Search the topic u want")

# ollama LLAma2 LLm 
llm=Ollama(model="llama2")
output_parser=StrOutputParser()
chain=prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question":input_text}))

# for Ollama after installing it, you need to open the cmd prompt and type "ollama run gemma/llama2/gpt", so it will start pullingg the code

