import streamlit as st
#from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from htmlTemplate import css, bot_template, user_template
OpenAI.api_key = st.secrets["OPENAI_API_KEY"]
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunk(text):
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size=100,
        chunk_overlap= 50,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
   
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
   
def main():
    #load_dotenv()
    OpenAI.api_key = st.secrets["OPENAI_API_KEY"]
    st.set_page_config(page_title = "chat with multiple PDFs", page_icon = ":books")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    st.header("chat with multiple pdfs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
    st.write(user_template.replace("{{MSG}}", "hello robot, help me today to refine resumes"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "hello human, yes sure!! I can help you with that. Kindly upload the resumes on left and press process button"), unsafe_allow_html=True)
    with st.sidebar:
        st.subheader("Welcome! 😄")
        pdf_docs = st.file_uploader("upload your pdfs here and click process", accept_multiple_files= True) #storing content of files into pdf_docs
        if st.button("process"):
            with st.spinner("processing"):
            #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunk(raw_text)
                vectorstore = get_vectorstore(text_chunks)

            #get the text chunks
            #create vector store
            st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == '__main__':
    main()