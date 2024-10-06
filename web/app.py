
import streamlit as st



# 配置页面布局为宽模式，设置页面图标和标题
st.set_page_config(layout="wide", page_icon="🤖", page_title="聊天机器人")


# Contact
with st.sidebar.expander("✉️  联系我"):
    st.write("**GitHub:**",  "[聊天机器人](https://github.com/solate/chatbot)")
    st.write("**知乎：**", "https://www.zhihu.com/people/zhang-jin-65-28")

   
#Title
st.markdown(
    """
    <h4 style='text-align: center;'>聊天机器人 🤖</h4>
    """,
    unsafe_allow_html=True,)

st.markdown("---")



