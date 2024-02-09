# integreate the code with OpenAI API
import os
from constants import openai_key
from langchain_community.llms.openai import OpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain # connecting 2 chains together
from langchain.memory import ConversationBufferMemory # Saving memory

# print("--------------------------------")
# print(dir(OpenAI))
# print("--------------------------------")


import streamlit as st


os.environ['OPENAI_API_KEY'] = openai_key

#initialize the streamlit framework

st.title('Celebrity Search Results')
input_text = st.text_input("Search the topic you want")

# First Prompt Template 
first_input_prompt = PromptTemplate(
    input_variables = ['name'],
    template="Tell me about celebrity {name}"
)

# Memory
person_memory = ConversationBufferMemory(input_key='name', memory_key="chat_history")
dob_memory = ConversationBufferMemory(input_key='person', memory_key="chat_history")
description_memory = ConversationBufferMemory(input_key='dob', memory_key="description_history")



# LLMChain/OpenAI LLMs template
llm = OpenAI(temperature=0.8)
chain = LLMChain(llm=llm, prompt=first_input_prompt, verbose=True, output_key='person', memory=person_memory)

# Second Prompt Template 
second_input_prompt = PromptTemplate(
    input_variables = ['person'],
    template="When was {person} born"
)

chain2 = LLMChain(llm=llm, prompt=second_input_prompt, verbose=True, output_key='dob', memory=dob_memory)
parentChain = SequentialChain(chains=[chain, chain2],
                              input_variables=['name'],
                               output_variables=["person","dob"],
                                 verbose=True,
                                 memory=dob_memory)


# Third Prompt Template 
third_input_prompt = PromptTemplate(
    input_variables = ['dob'],
    template="Mention 5 major events happened around {dob} in the world."
)

chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='description', memory=description_memory)
parentChain = SequentialChain(chains=[chain, chain2, chain3],
                              input_variables=['name'],
                               output_variables=["person","dob","description"],
                                 verbose=True
                                 )

if input_text:
    st.write(parentChain({'name' : input_text}))   

    with st.expander('Person Name'):
        st.info(person_memory.buffer)

    with st.expander('Major Events'):
        st.info(description_memory.buffer)   


