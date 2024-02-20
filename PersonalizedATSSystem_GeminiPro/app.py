import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
import warnings
warnings.simplefilter("always", PendingDeprecationWarning)

# Loading Environment Variables
load_dotenv()

# configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response

def gemini_pro_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

    

# streamlit setup
st.set_page_config(layout="wide")
# st.title("Welcome to Personalization of ATS System")
st.markdown("<h1 style='text-align: center;'>Welcome to Personalized of ATS System</h1>", unsafe_allow_html=True)


Col1,Col2 = st.columns(2)

with Col1:
    st.markdown("<h4 style='text-align: center;'>Paste the Job Description</h1>", unsafe_allow_html=True)
    jd = st.text_area("",height=500)
    uploaded_file = st.file_uploader("Upload the Resume", type=["pdf", "docx"], help="Please upload only Pdf or Word")

with Col2:
    # text_area = st.text_area(" ", height=500)
    
    if uploaded_file is not None:
        try:
            extracted_text = " "
            file_type = uploaded_file.name.split(".")[-1].lower()

            if file_type == 'pdf':
                pdf_reader = PdfReader(uploaded_file)
                for page in range(len(pdf_reader.pages)):
                    extracted_text += pdf_reader.pages[page].extract_text() + "\n"
            
            elif file_type == 'docx':
                doc = docx.Document(uploaded_file)
                for paragraph in doc.paragraphs:
                    extracted_text += paragraph.text + "\n"
            else:
                st.warning("Unsupported file type.")                
            
            # Clear and update the text area
            text_container = st.empty()
            # text_container.text(extracted_text)
            st.markdown("<h4 style='text-align: center;'>Paste the CV</h1>", unsafe_allow_html=True)
            abc = st.text_area(" ", value=extracted_text, height=500)
            # text_container.text(extracted_text)
            # st.markdown(extracted_text, unsafe_allow_html=True)
            
            
            
        except Exception as e:
            st.error(f'Error reading file: {e}')


input_desc_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field, such as Data Science, Machine Learning Engineer, Aritificial Intelligence Engineer, 
Natural Language Processing, Computer Vision and Generative AI Engineer.
Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resumes. mention how can i improve my resume with 
respect to the job description

I want the response in a bullet points as a Profile Summary as a Header
"""

input_per_prompt = """
Display the total percentage Matching based my resume and 
job description memtioned Machine Learning Engineer
as a title percentage matching
"""

input_keyWords_prompt = """
display the missing keywords with high accuracy from Machine Learning Engineer and Generative AI Engineer
as a title Missing Keywords
"""
        

if uploaded_file is not None:
    # Enable buttons after file upload
    submit = st.button("Submit", key="submit_button")
    percent = st.button("Percentage", key="percent_button")
    matching = st.button("Matching", key="matching_button")

    # Individual button click checks with your appropriate logic
    if submit:
        response = gemini_pro_response(input_desc_prompt)
        st.subheader(response)

    if percent:
        response = gemini_pro_response(input_per_prompt)
        st.subheader(response)

    if matching:
        response = gemini_pro_response(input_keyWords_prompt)
        st.subheader(response)






               












