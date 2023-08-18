import os
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from chat_templates import css, bot_template, user_template
from database import Subjects
from main import ImageModel
import speech_recognition as sr
from PyPDF2 import PdfReader

st.set_page_config(page_title="Chat with multiple PDFs",
                   page_icon=":books:", layout="wide")

# Cache data functions


@st.cache_data
def get_text_from_txt_files(txt_files):
    text = ""
    for txt_file_path in txt_files:
        try:
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                txt_content = txt_file.read()
                text += txt_content
        except Exception as e:
            st.write(f"Error reading text from {txt_file_path}: {e}")
    return text


@st.cache_data
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks


@st.cache_data
def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorestore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorestore


@st.cache_data
def get_conversation_chain(_vector_store):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=_vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain


# Handle user input function


def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{MSG}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{MSG}", message.content), unsafe_allow_html=True)

# Record audio function


def record_audio():
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = rec.listen(source)
            text = rec.recognize_google(audio, language="ar-AR")
        except sr.UnknownValueError:
            st.text("Could not understand audio")
        except sr.RequestError:
            st.text("Could not request results; check your network connection")
    return text

# Sidebar function


def sidebar():
    subject = Subjects()
    subjects = subject.DisplayEntries()

    subjects_name = [
        f'{subject_name[0]}- {subject_name[2]} - {subject_name[3]} - {subject_name[1]}' for subject_name in subjects]

    selected_subject_path = os.path.join(os.getcwd(), "selected_subject.txt")
    with open(selected_subject_path, "r", encoding="utf-8") as file:
        selected_subject_id = file.read().strip()

    selected_subject = st.radio(
        "Choose Subject:", subjects_name, index=subjects_name.index(selected_subject_id))

    st.session_state.selected_subject_id = selected_subject

    if selected_subject:
        selected_subject_id = selected_subject.split('-')[0].strip()

        folder_path = os.path.join(os.getcwd(), "pdfs")
        file_list = os.listdir(folder_path)
        files_path = []
        for file_name in file_list:
            if selected_subject_id == file_name[0] and file_name[0]:
                file_path = os.path.join(folder_path, file_name)
                files_path.append(file_path)
            else:
                file_path = os.path.join(
                    folder_path, "1000_subjects_error_handling.txt")
                files_path.append(file_path)
        with st.spinner(text="Process"):
            raw_text = get_text_from_txt_files(files_path)
            text_chunks = get_text_chunks(raw_text)
            vector_store = get_vector_store(text_chunks)
            st.session_state.conversation = get_conversation_chain(
                vector_store)

# Main function


def main():
    load_dotenv()

    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    chat_type = st.radio("Choose chat model", ["Text model", "Image model"])

    if chat_type == "Text model":
        record_button = st.button("Record Voice :microphone:")
        if record_button:
            record = record_audio()
            user_question = st.text_input(
                "Write your question here:", value=record)
            if user_question and user_question != "":
                handle_user_input(user_question)
        else:
            user_question = st.text_input(
                "Write your question here:", value="")
            if user_question and user_question != "":
                handle_user_input(user_question)
    if chat_type == "Image model":
        ImageModel()

    with st.sidebar:
        st.success(
            "Choose subject: \n\nSubject id- Phase id - Year id - Subject name")
        sidebar()


if __name__ == '__main__':
    main()
