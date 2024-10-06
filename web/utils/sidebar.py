
import streamlit as st

from utils.llm import *


def set_sidebar():
    with st.sidebar: 
        llm_form()
    

def llm_form() :
    with st.form("llm_form"):

        system_message = st.text_area("角色定义", st.session_state.system_message)
        
        temperature = st.slider("多样性概率", min_value=0.0, max_value=2.0,value=0.7, step=0.1, help='值越大生成越随机', format= "%.1f")

        llm_list = [
            "ERNIE-3.5-8K",
            "gpt-3.5-turbo",
        ]

        llm_opt = st.radio(label= "选择LLM", options=llm_list, key="llm_opt")
        llm = get_llm()
        print(llm_opt,"====" ,llm)    
    
        submitted = st.form_submit_button("确定")
        if submitted:
            st.write("LLM已切换")
            st.session_state.clear()
            st.session_state.llm = llm
            st.session_state.llm_opt = llm_opt
            st.session_state.system_message = system_message
            st.session_state.temperature = temperature



def get_llm():
    llm_opt = st.session_state.llm_opt
    temperature = st.session_state.temperature
    
    if llm_opt == "gpt-3.5-turbo":
        llm = get_openai_llm(llm_opt, temperature)

    elif llm_opt == "ERNIE-3.5-8K":
        llm = get_qianfan_llm(llm_opt, temperature)
    return llm 


