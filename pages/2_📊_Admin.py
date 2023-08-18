import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import os
from admin_templates import *
from database import *

# Set Streamlit page configuration
st.set_page_config(
    page_title="Admin Panel",
    page_icon=":bar_chart:",
    layout="wide"
)

# Initialize Streamlit Authenticator
yaml_path = os.path.join(os.getcwd(), "config.yaml")
with open(yaml_path) as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# User authentication
name, authentication_status, username = authenticator.login('Login', 'main')

# Apply custom styles
st.markdown(styles, unsafe_allow_html=True)

# Display data in a table


def display_table(table_name):
    db_table = globals()[table_name]()
    entries = db_table.DisplayEntries()
    table_headers = db_table.columns[:]

    st.write(f"**{table_name} :**")
    data = [entry[:] for entry in entries]
    df = pd.DataFrame(data, columns=table_headers)
    df.index += 1

    st.dataframe(df)

# Add a record to a table


def add_record(table_name, values):
    table = globals()[table_name]()
    table.AddEntry(values)
    st.success("The object has been added successfully.")

# Edit a record in a table


def edit_record(table_name, values):
    table = globals()[table_name]()
    table.EditEntry(*values)
    st.success("The object has been edited successfully.")

# Delete a record from a table


def delete_record(table_name, values):
    table = globals()[table_name]()
    table.DeleteEntry(values)
    st.success("The object has been deleted successfully.")

# Extract text from PDFs


def extract_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.write(f"Error extracting text from {pdf}: {e}")
    return text

# Main section of the app


def main_section(choices):
    if choices == "Study Phases":
        study_phase_settings = st.radio("Settings", ['Add', 'Edit', 'Delete'])
        if study_phase_settings == "Add":
            study_phase_name_input = st.text_input("Study Phase name:")
            study_phase_add_button = st.button("Add Study Phase")
            if study_phase_add_button:
                add_record("StudyPhase", (None, study_phase_name_input))
        if study_phase_settings == "Edit":
            study_phase_edit_id_input = st.text_input("Study Phase ID:")
            study_phase_new_name_input = st.text_input("New Study Phase Name:")
            study_phase_edit_button = st.button("Edit Study Phase")
            if study_phase_edit_button:
                edit_record("StudyPhase", (study_phase_edit_id_input,
                                           study_phase_new_name_input))
        if study_phase_settings == "Delete":
            study_phase_delete_id_input = st.text_input("Study Phase ID:")
            study_phase_delete_button = st.button("Delete Study Phase")
            if study_phase_delete_button:
                delete_record("StudyPhase", study_phase_delete_id_input)
        display_table('StudyPhase')
    if choices == "Academic Years":
        academic_year_settings = st.radio(
            "Settings", ['Add', 'Edit', 'Delete'])

        if academic_year_settings == "Add":
            academic_year_name_input = st.text_input("Academic Year name:")
            academic_year_study_phase_add_id_input = st.text_input(
                "Academic Year Study Phase ID:")
            academic_year_add_button = st.button("Add Academic Year")
            if academic_year_add_button:
                add_record("AcademicYear", (None, academic_year_name_input,
                                            academic_year_study_phase_add_id_input,))
        if academic_year_settings == "Edit":
            academic_year_edit_id_input = st.text_input("Academic Year ID:")
            academic_year_new_name_input = st.text_input(
                "New Academic Year Name:")
            academic_year_new_study_phase_id_input = st.text_input(
                "New Academic Year Study Phase ID:")
            academic_year_edit_button = st.button("Edit Academic Year")
            if academic_year_edit_button:
                edit_record("AcademicYear", (academic_year_edit_id_input,
                                              academic_year_new_name_input, academic_year_new_study_phase_id_input))
        if academic_year_settings == "Delete":
            academic_year_delete_id_input = st.text_input("Academic Year ID:")
            academic_year_delete_button = st.button("Delete Academic Year")
            if academic_year_delete_button:
                delete_record("AcademicYear", academic_year_delete_id_input)
        display_table('AcademicYear')

    if choices == "Subjects":
        subjects_settings = st.radio("Settings", ['Add', 'Edit', 'Delete'])

        if subjects_settings == "Add":
            subjects_name_input = st.text_input("Subject name:")
            subjects_study_phase_add_id_input = st.text_input(
                "Subject Study Phase ID:")
            subjects_academic_year_add_id_input = st.text_input(
                "Subject Academic Year ID:")
            subjects_add_button = st.button("Add Subject")
            if subjects_add_button:
                add_record("Subjects", (None, subjects_name_input,
                                        subjects_study_phase_add_id_input, subjects_academic_year_add_id_input,))
        if subjects_settings == "Edit":
            subjects_edit_id_input = st.text_input("Subject ID:")
            subjects_new_name_input = st.text_input("New Subject Name:")
            subjects_new_study_phase_id_input = st.text_input(
                "New Subject Study Phase ID:")
            subjects_new_academic_year_id_input = st.text_input(
                "New Subject Academic Year ID:")
            subjects_edit_button = st.button("Edit Subject")
            if subjects_edit_button:
                edit_record("Subjects", (subjects_edit_id_input, subjects_new_name_input,
                                          subjects_new_study_phase_id_input, subjects_new_academic_year_id_input))
        if subjects_settings == "Delete":
            subjects_delete_id_input = st.text_input("Subject ID:")
            subjects_delete_button = st.button("Delete Subject")
            if subjects_delete_button:
                delete_record("Subjects", subjects_delete_id_input)
        display_table('Subjects')

    if choices == "PDF Files":
        pdf_name = st.text_input("PDF name:")
        subject_id = st.text_input("Subject ID:")
        pdf_file = st.file_uploader(
            "Upload your PDFs here", accept_multiple_files=True)

        if st.button("Add PDF"):
            with st.spinner(text="Progress..."):
                current_dir = os.getcwd()
                output_path = os.path.join(
                    current_dir, f"pdfs\\{subject_id}_{pdf_name.replace(' ', '_').lower()}.txt")
                content = extract_pdf_text(pdf_file)
                with open(output_path, "a", encoding="utf-8") as file:
                    file.write(content)
            st.success("File has been added successfully")

        folder_path = os.path.join(os.getcwd(), "pdfs")
        file_list = os.listdir(folder_path)
        files_subjects_id = []
        files_name = []

        for file_name in file_list:
            file_display_subject_id = int(file_name[:1])
            file_display_name = file_name[1:-4].replace("_", " ").upper()
            files_subjects_id.append(file_display_subject_id)
            files_name.append(file_display_name)

        data = {"File name": files_name, "Subject ID": files_subjects_id}
        df = pd.DataFrame(data)
        st.dataframe(df)



def main():
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    with st.sidebar:
        st.title(f'Welcome *{name}*')
        choices = st.radio("Data Base Tables", [
                           'Study Phases', 'Academic Years', 'Subjects', 'PDF Files'])
        logout_button = authenticator.logout(
            'Logout', 'main', key='unique_key')

    if authentication_status:
        main_section(choices)
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')


if __name__ == "__main__":
    main()
