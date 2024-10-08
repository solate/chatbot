

# llm 选择器方法

import streamlit as st
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_openai import ChatOpenAI


def get_qianfan_llm(model="ERNIE-3.5-8K", temperature = 0.7):
    llm = QianfanChatEndpoint(
        api_key=st.secrets["QIANFAN_API_KEY"],
        secret_key=st.secrets["QIANFAN_SECRET_KEY"],
        temperature=temperature,
        stream=True,
    )
    return llm

def get_openai_llm(model="gpt-3.5-turbo", temperature = 0.7):
    llm = ChatOpenAI(
            model=model, 
            api_key=st.secrets["OPENAI_API_KEY"], 
            base_url=st.secrets["OPENAI_BASE_URL"],
            temperature=temperature,
            stream=True,
        )
    return llm

def get_self_openai_llm(openai_api_key, model="gpt-3.5-turbo", temperature = 0.7):
    llm = ChatOpenAI(
            model=model, 
            api_key=openai_api_key, 
            temperature=temperature,
            stream=True,
        )
    return llm


def get_qwen_llm(model="qwen-plus", temperature = 0.7):
    from langchain_community.chat_models.tongyi import ChatTongyi
    llm = ChatTongyi(
        model=model,
        api_key=st.secrets["DASHSCOPE_API_KEY"],
        temperature=temperature,
        stream=True,
    )
    return llm  

