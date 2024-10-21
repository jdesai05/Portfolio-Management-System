import streamlit as st
from firebase_config import auth  # Assuming you have Firebase setup in firebase_config.py

def signup():
    st.title("Signup Page")

    # Input fields for username, password, and confirm password
    new_email = st.text_input("Enter new email")
    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    # Signup button
    if st.button("Signup"):
        # Check if the passwords match
        if new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            try:
                # Create a new user using Firebase Authentication
                user = auth.create_user_with_email_and_password(new_email, new_password)

                # Update session state upon successful signup
                st.success("Signup successful")
                st.session_state['username'] = new_email
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.session_state['page'] = 'portfolio'
                st.experimental_rerun()

            except Exception as e:
                st.error(f"Signup failed: {e}")

    # Button to redirect to the login page
    if st.button("Go to Login"):
        st.session_state['page'] = 'login'
        st.experimental_rerun()

# This part would ideally be in the main app script
if __name__ == "__main__":
    signup()
