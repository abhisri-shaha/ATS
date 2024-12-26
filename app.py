# from dotenv import load_dotenv
# load_dotenv()

# import base64
# import streamlit as st
# import os
# import io
# from PIL import Image 
# import pdf2image
# import google.generativeai as genai

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(job_desc,pdf_content,prompt):
#     model=genai.GenerativeModel('gemini-1.5-flash')
#     response=model.generate_content([job_desc,pdf_content[0],prompt])
#     return response.text

# def input_pdf_setup(uploaded_file):
#     if uploaded_file is not None:
#         ## Convert the PDF to image
#         images=pdf2image.convert_from_bytes(uploaded_file.read())

#         first_page=images[0]

#         # Convert to bytes
#         img_byte_arr = io.BytesIO()
#         first_page.save(img_byte_arr, format='JPEG')
#         img_byte_arr = img_byte_arr.getvalue()

#         pdf_parts = [
#             {
#                 "mime_type": "image/jpeg",
#                 "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
#             }
#         ]
#         return pdf_parts
#     else:
#         raise FileNotFoundError("No file uploaded")

# ## Streamlit App

# st.set_page_config(page_title="ATS Resume Expert")
# st.header("ATS Tracking System")
# jd=st.text_area("Job Description: ",key="input")
# uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


# if uploaded_file is not None:
#     st.write("PDF Uploaded Successfully")


# submit1 = st.button("Tell Me About the Resume")

# submit2 = st.button("Percentage match")

# input_prompt1 = """
#  You are an experienced HR with tech experience in the field of any one job role from Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analysis, etc. 
#  Your task is to review the provided resume against the job description. 
#  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
#  Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
# """

# input_prompt2 = """
# You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role from Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analysis, etc. and deep ATS functionality, 
# your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
# the job description. First the output should come as percentage and then keywords missing and last final thoughts.
# """

# if submit1:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(jd,pdf_content,input_prompt1)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

# elif submit2:
#     if uploaded_file is not None:
#         pdf_content=input_pdf_setup(uploaded_file)
#         response=get_gemini_response(jd,pdf_content,input_prompt2)
#         st.subheader("The Repsonse is")
#         st.write(response)
#     else:
#         st.write("Please uplaod the resume")

import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt_template = """
Act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech fields like software engineering, data science, data analysis,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider that the job market is very competitive and provide
the best assistance for improving the resumes. Assign a percentage match 
based on the job description and the missing keywords with high accuracy.

Resume: {text}
Job Description: {jd}

I want the response in one single string with 3 pointers:
1. JD Match percentage
2. Missing keywords
3. Profile summary
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume")
jd = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Analyze CV")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        input_prompt = input_prompt_template.format(text=text, jd=jd)
        response = get_gemini_repsonse(input_prompt)
        st.subheader("ATS Analysis Result")
        st.write(response)
    else:
        st.write("Please upload a resume (PDF file).")
