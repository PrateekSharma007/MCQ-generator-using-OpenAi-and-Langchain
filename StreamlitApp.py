import os 
import json 
import traceback 
import pandas as pd 

from src.mcqgenerator.logger import logging 
from src.mcqgenerator.utils import read_file,get_table_data 
import streamlit as st

from src.mcqgenerator.MCQGENERATOR import generate_evaluate_chain
from langchain.callbacks import get_openai_callback

with open(r"C:\Users\sharm\OneDrive\Desktop\Opencv\MCQ-generator-using-OpenAi-and-Langchain\response.json") as file : 
    RESPONSE_JSON = json.load(file) 

st.title("MCQ Creator Application with Langchain") 

with st.form("user_inputs") : 
    uploaded_file = st.file_uploader("Upload a Pdf or Txt file") 

    mcq_count = st.number_input("No of MCQs" , min_value= 3 , max_value=50) 

    subject = st.text_input("Insert Subject" , max_chars = 20) 

    tone = st.text_input("Complexity Level of questions" , max_chars = 20 , placeholder="Simple") 

    button = st.form_submit_button("Create MCQ")


    if button and uploaded_file is not None and mcq_count and subject and tone : 
        with st.spinner("loading...") : 
            try : 
                text = read_file(uploaded_file)  
                with get_openai_callback() as cb : 
                    response  = generate_evaluate_chain({
                        "text" : text , 
                        "number" : mcq_count, 
                        "subject" : subject , 
                        "tone" :  tone , 
                        "response_json"  : json.dumps(RESPONSE_JSON)
                    })

            except Exception as e  : 
                traceback.print_exception(type(e),e,e.__traceback__) 
                st.error("Error")
 




