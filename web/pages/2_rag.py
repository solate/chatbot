import streamlit as st

st.set_page_config(page_title="chatbot RAG", page_icon="")
st.header('2. RAG')
st.write('实现文档搜索检索，实现知识库问答')



from utils.rag import *
from utils.state import *


class BasicRAGChatbot:

    def __init__(self):
        init_session_state()
        show_chat_history()
        set_rag_sidebar()

    def run(self):
        # 用户输入
        user_query = st.chat_input("说点什么...")
        if user_query:
            # 显示用户输入的内容到聊天窗口
            with st.chat_message("user", avatar="👨"):
                st.write(user_query)
                # 在聊天窗口输出用户输入的问题
                st.session_state.messages.append({"role": "user", "content": user_query})

                response = chat_stream_rag_response(user_query)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("AI 正在思考..."): 
                    message_placeholder = st.empty()
                    ai_response = ""
                    
                    for chunk in response:
                        if chunk is not None:
                            ai_response += chunk.content
                            message_placeholder.markdown(ai_response + "|")
                    message_placeholder.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})      



if __name__ == "__main__":
    obj = BasicRAGChatbot()
    obj.run()