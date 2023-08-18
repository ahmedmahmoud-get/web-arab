import sqlite3
import streamlit_authenticator as stauth

# Connect to the SQLite database
connect = sqlite3.connect(
    r"C:\Users\HP\Desktop\streamlit_app\database_file.db")
cursor = connect.cursor()

# Create the StudyPhase table
cursor.execute('''
CREATE TABLE IF NOT EXISTS StudyPhase (
    id INTEGER PRIMARY KEY,
    study_phase_name TEXT
)
''')

# Create the AcademicYear table
cursor.execute('''
CREATE TABLE IF NOT EXISTS AcademicYear (
    id INTEGER PRIMARY KEY,
    year_name TEXT,
    year_study_phase_id INTEGER,
    FOREIGN KEY (year_study_phase_id) REFERENCES StudyPhase (id)
)
''')

# Create Subjects table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Subjects (
    id INTEGER PRIMARY KEY,
    subject_name TEXT,
    subject_study_phase_id INTEGER, -- Updated column name
    subject_academic_year_id INTEGER,
    FOREIGN KEY (subject_study_phase_id) REFERENCES StudyPhase (id), -- Updated foreign key
    FOREIGN KEY (subject_academic_year_id) REFERENCES AcademicYear (id)
)
''')

# Create the PDFs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS PDFFile (
    id INTEGER PRIMARY KEY,
    name TEXT,
    pdf_file BLOB,
    pdf_file_study_subject_id INTEGER,
    FOREIGN KEY (pdf_file_study_subject_id) REFERENCES Subjects (id)
)
''')

# Create the Users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    name TEXT,
    password TEXT
)
''')


class BaseDatabase:
    def __init__(self, table_name, columns) -> None:
        self.table_name = table_name
        self.columns = columns
        self.connect = sqlite3.connect(
            r"C:\Users\HP\Desktop\streamlit_app\database_file.db")
        self.cursor = self.connect.cursor()

    def CommitAndClose(self):
        self.connect.commit()
        # self.connect.close()

    def AddEntry(self, values):
        try:
            # Exclude the id column from placeholders and values
            placeholders = ', '.join(['?' for _ in self.columns[1:]])
            query = f"INSERT INTO {self.table_name} ({', '.join(self.columns[1:])}) VALUES ({placeholders})"
            # Exclude the first value (id)
            self.cursor.execute(query, values[1:])
        except sqlite3.Error as er:
            print(f"Error adding data {er}")
        finally:
            if self.connect:
                self.CommitAndClose()

    def EditEntry(self, id, *new_values):
        try:
            placeholders = ', '.join(
                [f"{column} = ?" for column in self.columns[1:]])
            query = f"UPDATE {self.table_name} SET {placeholders} WHERE id = ?"
            self.cursor.execute(query, new_values + (id,))
        except sqlite3.Error as er:
            print(f"Error editing data {er}")
        finally:
            if self.connect:
                self.CommitAndClose()

    def DeleteEntry(self, id):
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = ?"
            self.cursor.execute(query, (id,))
        except sqlite3.Error as er:
            print(f"Error deleting data {er}")
        finally:
            if self.connect:
                self.CommitAndClose()

    def DisplayEntries(self):
        try:
            query = f"SELECT * FROM {self.table_name}"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as er:
            print(f"Error reading data {er}")
        finally:
            if self.connect:
                self.CommitAndClose()


class StudyPhase(BaseDatabase):
    def __init__(self) -> None:
        super().__init__("StudyPhase", ["id", "study_phase_name"])


class AcademicYear(BaseDatabase):
    def __init__(self) -> None:
        super().__init__("AcademicYear", [
            "id", "year_name", "year_study_phase_id"])


class Subjects(BaseDatabase):
    def __init__(self) -> None:
        super().__init__("Subjects", [
            "id", "subject_name", "subject_study_phase_id", "subject_academic_year_id"])


class PDFFile(BaseDatabase):
    def __init__(self) -> None:
        super().__init__("PDFFile", ["id", "name",
                                     "pdf_file", "pdf_file_study_subject_id"])

    def AddEntry(self, values):
        try:
            placeholders = ', '.join(['?' for _ in self.columns[1:]])
            query = f"INSERT INTO {self.table_name} ({', '.join(self.columns[1:])}) VALUES ({placeholders})"
            self.cursor.execute(query, values[1:])
        except sqlite3.Error as er:
            print(f"Error adding data {er}")
        finally:
            if self.connect:
                self.CommitAndClose()


class Users(BaseDatabase):
    def __init__(self) -> None:
        super().__init__("Users", ["id", "username", "name", "password"])


if __name__ == '__main__':
    study_phase = StudyPhase()
