from dotenv import load_dotenv
import os
import streamlit as st
from langchain.llms.openai import OpenAI
from PyPDF2 import PdfReader
import warnings
warnings.simplefilter("always", PendingDeprecationWarning)



#loading environment variables
load_dotenv()



# OpenAI Response
def openai_response(input):
    llm = OpenAI(openai_api_key = "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",
             temperature=0.4,
             model = "gpt-4-0125-preview"),

    
