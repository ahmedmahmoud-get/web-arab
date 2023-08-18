import streamlit_authenticator as stauth

passwords = ['abc123', 'def123', 'abc123']  # List of plain-text passwords
hashed_passwords = stauth.Hasher(passwords).generate()

print(hashed_passwords)  # Print the generated hashed passwords

