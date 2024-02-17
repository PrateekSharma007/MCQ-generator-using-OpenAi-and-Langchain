import os
import json
import PyPDF2
import pandas as pd
import traceback
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from src.mcqgenerator.MCQGENERATOR import generate_evaluate_chain


with open(r"Response.json", 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("Real-Time MCQ Creator with LangChain & Google Gemini Pro")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject", max_chars=20)

    tone=st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone: 
        with st.spinner("loading..."):
            try:
                text=read_file(uploaded_file)
                response=generate_evaluate_chain({
                    "text":text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(RESPONSE_JSON)
                })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")

            else:
                if isinstance(response, dict):
                    quiz_json_start = response['quiz'].find('{')
                    quiz_json_end = response['quiz'].rfind('}') + 1
                    quiz = response['quiz'][quiz_json_start:quiz_json_end]
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in table data")
                    else:
                        st.write(response)