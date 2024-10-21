import streamlit as st
from firebase_config import auth  # Assuming you have the Firebase setup in firebase_config.py

def login():
    st.title("Login Page")

    # Check if the user is already logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Input fields for email and password
    email = st.text_input("Enter email")
    password = st.text_input("Enter password", type="password")

    # Login button
    if st.button("Login"):
        try:
            # Attempt to authenticate the user with Firebase
            user = auth.sign_in_with_email_and_password(email, password)
            
            # Update session state upon successful login
            st.session_state['username'] = email
            st.session_state['logged_in'] = True
            st.session_state['user'] = user
            st.session_state['page'] = 'portfolio'  # Redirect to the portfolio page
            st.success(f"Logged in as {email}")
            st.experimental_rerun()
        
        except Exception as e:
            st.error("Invalid email or password. Please try again.")

    # Button to redirect to signup page
    if st.button("Go to Signup"):
        st.session_state['page'] = 'signup'
        st.experimental_rerun()

# This part would ideally be in the main app script
if __name__ == "__main__":
    login()
