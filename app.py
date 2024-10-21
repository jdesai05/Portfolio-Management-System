import streamlit as st
import login
import signup
import portfolio

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if st.session_state['page'] == 'login':
    login.login()
elif st.session_state['page'] == 'signup':
    signup.signup()
elif st.session_state['page'] == 'portfolio':
    if st.session_state.get('logged_in'):
        portfolio.portfolio()
    else:
        st.session_state['page'] = 'login'
        st.experimental_rerun()
