import streamlit as st
import os
import webbrowser
from app_templates import styles
from database import StudyPhase, AcademicYear, Subjects

# Configure the Streamlit page
st.set_page_config(
    page_title="Chat with multiple PDFs",
    page_icon=":books:",
    layout="wide"
)


def hide_streamlit_elements():
    # Hide Streamlit's default elements
    hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    [data-testid="collapsedControl"] {right: 0;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)


def display_subject_buttons(subjects_list):
    num_columns = 4
    name_groups = [
        subjects_list[i:i + num_columns]
        for i in range(0, len(subjects_list), num_columns)
    ]

    columns = st.columns(num_columns)
    for group in name_groups:
        for i, subject_name in enumerate(group):
            button = columns[i].button(subject_name)
            if button:
                selected_subject_id = subject_name
                selected_subject_path = os.path.join(
                    os.getcwd(), "selected_subject.txt")
                with open(selected_subject_path, "wb") as file:
                    file.write(selected_subject_id.encode("utf-8"))
                link_url = "https://web-arab.streamlit.app/Chat"  # Replace with the desired URL
                st.write("<a href="https://web-arab.streamlit.app/Chat">", usafe_allow_html=True)


def main():
    # Display custom styles and headers
    st.markdown(styles, unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">المراحل الدراسية</h1>',
                unsafe_allow_html=True)

    # Connect to the database tables
    study_phase = StudyPhase()
    academic_year = AcademicYear()
    subject = Subjects()

    # Retrieve data from database tables
    study_phases = study_phase.DisplayEntries()
    academic_years = academic_year.DisplayEntries()
    subjects = subject.DisplayEntries()

    for study_phase_data in study_phases:
        study_phase_name = study_phase_data[1]
        st.header(f"{study_phase_name} :")

        for academic_year_data in academic_years:
            if academic_year_data[2] == study_phase_data[0]:
                academic_year_name = academic_year_data[1]
                st.subheader(f"{academic_year_data[0]} - {academic_year_name}")
                study_phase_id = study_phase_data[0]
                academic_year_id = academic_year_data[0]

                # Filter subjects based on academic year and study phase
                subjects_for_academic_year = [
                    f"{subject_data[0]}- {study_phase_id} - {academic_year_id} - {subject_data[1]}"
                    for subject_data in subjects
                    if subject_data[2] == study_phase_id and subject_data[3] == academic_year_id
                ]

                display_subject_buttons(subjects_for_academic_year)


if __name__ == "__main__":
    hide_streamlit_elements()
    main()
