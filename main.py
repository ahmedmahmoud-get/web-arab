import tempfile
import streamlit as st
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from tools import ImageCaptionTool, ObjectDetectionTool

def ImageModel():
    ########################
    ### Initialize agent ###
    ########################
    tools = [ImageCaptionTool(), ObjectDetectionTool()]

    conversational_memory = ConversationBufferWindowMemory(
        memory_key='chat_history',
        k=5,
        return_messages=True
    )

    llm = ChatOpenAI(
        openai_api_key='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',
        temperature=0,
        tiktoken_model_name="facebook/m2m100_418M" # microsoft/DialoGPT-medium
    )

    agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        max_iteration=5,
        verbose=True,
        memory=conversational_memory,
        early_stoppy_method='generate',
    )

    # set title
    st.title("Ask a question to an image")

    # set header
    st.header("Please upload an image")

    # upload file
    file = st.file_uploader("", type=["jpeg", "jpg", "png"])

    if file:
        # Display image
        st.image(file, use_column_width=True)

        # Text input
        user_question = st.text_input("Ask a question about your image")

        ##############################
        ### Compute agent response ###
        ##############################
        with tempfile.NamedTemporaryFile(dir='./images', delete=False) as f:
            f.write(file.getbuffer())
            image_path = f.name

        # Write agent response
        if user_question and user_question != "":
            with st.spinner(text="In progress"):
                response = agent.run(
                    f'{user_question}, this is the image path: {image_path}')
                st.write(response)
