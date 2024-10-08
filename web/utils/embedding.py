


# 导入所需模块
import streamlit as st
from langchain_community.embeddings import QianfanEmbeddingsEndpoint, DashScopeEmbeddings

# # 获取千帆模型嵌入对象
# def get_qianfan_embedding() -> QianfanEmbeddingsEndpoint:
#     return QianfanEmbeddingsEndpoint(
#         api_key=st.secrets["QIANFAN_API_KEY"],
#         secret_key=st.secrets["QIANFAN_SECRET_KEY"],
#     )

# 获取通义灵码模型嵌入对象
def get_qwen_embedding() -> DashScopeEmbeddings:
    return DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=st.secrets["DASHSCOPE_API_KEY"],
    )