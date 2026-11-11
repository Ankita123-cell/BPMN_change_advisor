from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import os
import pandas as pd
import streamlit as st

load_dotenv()
# hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
do_sample=True
# Task_temperature_map = {
#    "Summarization":0.3,
#    "Email Drafting":0.5,
#    "Brainstorming":0.8,
#    "Requirement Writing":0.6,
#    "SQL Help":0.2
#}
#temp_compare = [0.2,0.6,1.2]
st.title("BPMN rules suggestion for Process Models")
# model_input = st.selectbox("Select Model Name",["Llama","ChatGpt"])
# temperature_input = st.number_input("Enter temperature parameter")
#Mode = st.radio(
#    "Select Temperature Mode",
#    ["Select temperature","Select task type for auto suggestion"]
#)
#if Mode == "Select temperature":
#   st.markdown("Adjust the model response style using temperature")
#   temperature_input = st.selectbox("Select temperature range",["Low Temperature (0.0-0.3)","Moderate Temperature (0.4-0.8)","High Temperature (0.9-1+)"])
#   if temperature_input == "Low Temperature (0.0-0.3)":
#      temperature_input1 = 0.2
#   elif temperature_input == "Moderate Temperature (0.4-0.8)":
#      temperature_input1 = 0.6
#   elif temperature_input == "High Temperature (0.9-1+)":
#      temperature_input1 = 1.2
#if Mode == "Upload the pdf file of process map":
st.markdown("Upload PDF file")
uploaded_pdf = st.file_uploader("Upload Process Document (PDF)", type=["pdf"])
# 4. Trigger LLM Analysis
if st.button("Analyze & Suggest BPMN Changes", type="primary"):
    if not uploaded_pdf:
        st.warning("Please upload a PDF file first.")
    else:
        #with st.spinner("Extracting text from PDF and analyzing BPMN impact..."):
        #    pdf_text = extract_text_from_pdf(uploaded_pdf)
            
            # Construct a domain-specific BPMN prompt
        system_prompt = """
        You are an expert Business Process Architect specializing in BPMN 2.0.
        Analyze the provided document (and optional existing BPMN workflow) and recommend specific BPMN changes.
            
        Structure your response clearly using BPMN 2.0 terminology:
        1. **Pools & Swimlanes**: Identify new roles, departments, or external participants.
        2. **Tasks & Sub-processes**: Specify User Tasks, Service Tasks (automation opportunities), or Manual Tasks to add, modify, or remove.
        3. **Gateways**: Identify Exclusive (XOR), Parallel (AND), or Inclusive (OR) gateways needed for new decision rules or parallel approvals.
        4. **Events & Exception Handling**: Highlight Start/End events, Timer events (SLAs/deadlines), Message events, or Error boundary events.
        5. **Summary of Business Impact**: Briefly explain why these changes reduce bottlenecks or ensure compliance.
        """

        #user_content = f"### Uploaded Document Content:\n{pdf_text[:30000]}" # Truncated safeguard for token limits
        #if current_bpmn.strip():
        #    user_content += f"\n\n### Current BPMN / As-Is Process:\n{current_bpmn}"

        #try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            temperature=0.2
        )
                
        st.subheader("Suggested BPMN 2.0 Modifications")
        st.markdown(response.choices[0].message.content)
#model = ChatOpenAI(model="gpt-4o-mini", temperature=temperature_input1)
#elif model_input == "Llama":
#    llm = HuggingFaceEndpoint(
#    repo_id='Tinyllama/TinyLlama-1.1B-Chat-v1.0',
#    huggingfacehub_api_token=hf_token,
#    task='text-generation',
#    temperature=float(temperature_input) if temperature_input > 0 else 0.1,
#        max_new_tokens=100,
#        do_sample=True
#    )
#    model = ChatHuggingFace(llm=llm)
#for i in range(0,3):
#    temperature_input1 = temp_compare[i]
#    st.write(f"Temperature is {temperature_input1}")
#    result = model.invoke(formatted_input)
#    st.write(result.content)