

# streamlit 封装session_state
import streamlit as st
from utils.sidebar import get_llm


def init_session_state():

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "你好，我是 Chatbot~, 您的智能助手, 有任何问题都可以问我哦~"
            }
        ]
    if "messageHistory" not in st.session_state:    
        st.session_state.messageHistory = []

    if "llm" not in st.session_state:     
        st.session_state.llm = ""
    if "system_message" not in st.session_state:    
        st.session_state.system_message = "你是一个智能聊天助手"
    if "temperature" not in st.session_state:    
        st.session_state.temperature = 0.7

def show_chat_history() -> None:
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            # 系统消息
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
        else:
            # 用户消息
            with st.chat_message("user", avatar="👨"):
                st.write(message["content"])



def chat_stream_chat_response(query):


    # 系统消息，定义的角色
    system_message = st.session_state.system_message 
    if system_message:
        st.session_state.messageHistory.append({"role": "system", "content": system_message})
    st.session_state.messageHistory.append({"role": "user", "content": query})

    msg = st.session_state.messageHistory
    llm = get_llm()
    response = llm.stream(msg)
    return response      