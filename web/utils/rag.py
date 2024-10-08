

import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from tempfile import NamedTemporaryFile



def set_rag_sidebar():
    with st.sidebar:
        
        uploaded_files = st.file_uploader("上传文件", type=["pdf", "txt", "docx"], accept_multiple_files=True)
        if not uploaded_files: 
            st.error("请上传文件")
            return

        if uploaded_files:

            st.write("文件上传成功")
            if "processed_data" not in st.session_state:

                docs = get_docs(uploaded_files)
                document_chunks = get_text_chunks(docs)
                vectorstore = get_vectorstore(document_chunks)
                st.session_state.processed_data = {
                    "document_chunks": document_chunks,
                    "vectorstore": vectorstore,
                }
            else:
                document_chunks = st.session_state.processed_data["document_chunks"]
                vectorstore = st.session_state.processed_data["vectorstore"]




import os
from tempfile import NamedTemporaryFile

# 1. 保存文件
def save_file(file):
    folder = 'tmp'
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    file_path = f'./{folder}/{file.name}'
    with open(file_path, 'wb') as f:
        f.write(file.getvalue())
    return file_path

# 2. 零时文件        
def tmp_file_path(file):
    # 使用 NamedTemporaryFile 创建临时文件
    with NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(file.read())
        tmp_file_path = tmp_file.name
    return tmp_file_path    


def get_docs(uploaded_files):

    docs = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            #  使用本地存储或者临时文件存储
            # file_path = save_file(uploaded_file)
            file_path = tmp_file_path(uploaded_file)

            docs = get_pdf_page(file_path) 
        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
            docs.append(text)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # 读取 Word 文档
            # 注意：这里需要额外的库来处理 Word 文档
            # 可以使用 `docx` 库或其他方法
            pass
        else:
            st.write("不支持的文件类型")
    
    return docs



    

# 1. pdf 文件读取
def get_pdf_page(file_path):
    loader = PyPDFLoader(file_path)
    pages = []
    for page in loader.lazy_load():
        pages.append(page)
    return pages

# 2. 将pdf文件分割为文本块
def get_text_chunks(docs):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, 
        chunk_overlap=20,
        # length_function=len, # 这里可以改为已token 计算块长度
        # is_separator_regex=False,
    )
    docs_chunks = text_splitter.split_documents(docs)
    return docs_chunks

# 3. 将文本块转化为向量
def get_vectorstore(docs_chunks):
    from utils.embedding import get_qwen_embedding
    from langchain_community.vectorstores import Chroma
    
    embeddings = get_qwen_embedding()
    vectorstore = Chroma.from_documents(docs_chunks, embeddings)
    return vectorstore



# rag 问答
def chat_stream_rag_response(query):

    # 系统消息，定义的角色
    system_message = st.session_state.system_message 
    if system_message:
        st.session_state.messageHistory.append({"role": "system", "content": system_message})

    st.session_state.messageHistory.append({"role": "user", "content": query})
    msg = st.session_state.messageHistory

   
    if "processed_data" in st.session_state :
        vectorstore = st.session_state.processed_data["vectorstore"]

        rag_chain = get_conversation_chain(vectorstore)
        response = rag_chain.stream("用人单位在什么节日期间应当依法安排劳动者休假")
    else:
        from utils.llm import get_qwen_llm
        llm = get_qwen_llm()
        response = llm.stream(msg)

    
    return response      
  



def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)



def get_template_prompt():
    from langchain_core.prompts import PromptTemplate


    template = """
    你是用于回答问题的任务助手。请使用以下检索到的上下文来回答问题。如果你不知道答案，就说你不知道。请在三句话内给出简洁的回答。
    Question: {question} 
    Context: {context} 
    Answer:
    """

    prompt = PromptTemplate.from_template(template)
    return prompt


# 4. 创建对话问答链
def get_conversation_chain(vectorstore):

    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from utils.llm import get_qwen_llm


    llm = get_qwen_llm()
  
    retriever = vectorstore.as_retriever()
    prompt = get_template_prompt()

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    
    return rag_chain







