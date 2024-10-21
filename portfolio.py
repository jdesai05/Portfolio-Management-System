import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, storage
import os

storage_bucket = os.getenv('STORAGE_BUCKET')

# Initialize Firebase app if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\jaini\OneDrive\Desktop\Portfolio Management\firebase_credentials.json")
    firebase_admin.initialize_app(cred, storage_bucket)

bucket = storage.bucket()

if 'sname' not in st.session_state:
    st.session_state.sname = ()
    st.session_state.sprice = ()
    st.session_state.squant = ()

def add_stock(name, price, quant):
    st.session_state.sname += (name,)
    st.session_state.sprice += (price,)
    st.session_state.squant += (quant,)

def remove_stock(name):
    if name in st.session_state.sname:
        i = st.session_state.sname.index(name)
        st.session_state.sname = st.session_state.sname[:i] + st.session_state.sname[i+1:]
        st.session_state.sprice = st.session_state.sprice[:i] + st.session_state.sprice[i+1:]
        st.session_state.squant = st.session_state.squant[:i] + st.session_state.squant[i+1:]

def clear_portfolio():
    st.session_state.sname = ()
    st.session_state.sprice = ()
    st.session_state.squant = ()

def display_stock():
    df = pd.DataFrame({
        'Stock Name': st.session_state.sname,
        'Stock Price': st.session_state.sprice,
        'Quantity': st.session_state.squant
    })
    return df

def add_stocks_from_csv(file):
    df = pd.read_csv(file)
    for index, row in df.iterrows():
        if row['Stock Name'] not in st.session_state.sname:
            add_stock(row['Stock Name'], row['Stock Price'], row['Quantity'])

def get_csv_data():
    df = display_stock()
    return df.to_csv(index=False).encode('utf-8')

def upload_csv_to_firebase():
    csv_data = get_csv_data()
    filename = f"portfolio_{st.session_state['username']}.csv"
    
    # Save the CSV locally first
    with open(filename, 'wb') as f:
        f.write(csv_data)

    try:
        # Upload the CSV to Firebase Storage
        blob = bucket.blob(f"portfolios/{st.session_state['username']}/{filename}")
        print(f"Uploading {filename} to {blob.name}...")
        blob.upload_from_filename(filename)

        # Get the URL for the uploaded CSV file
        csv_url = blob.public_url
        return csv_url
    
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {e}")
    
    finally:
        # Delete the local CSV file after upload
        if os.path.exists(filename):
            os.remove(filename)

def portfolio():
    st.title('Portfolio Management System')
    st.write(f"Welcome, {st.session_state.get('username', 'Guest')}!")

    st.subheader('Add New Stock')
    new_stock_name = st.text_input('Stock Name')
    new_stock_price = st.number_input('Stock Price', min_value=1.00, step=1.00)
    new_stock_quant = st.number_input('Stock Quantity', min_value=1, step=1)

    if st.button('Add Stock'):
        if not new_stock_name:
            st.error('Please enter a stock name')
        elif new_stock_price <= 0:
            st.error('Stock price needs to be more than zero')
        elif new_stock_quant < 1:
            st.error('Minimum quantity is 1')
        else:
            add_stock(new_stock_name, new_stock_price, new_stock_quant)
            st.success(f'Stock {new_stock_name} added')

    st.subheader('Upload CSV to Add Multiple Stocks')
    upload_file = st.file_uploader("Choose a file", type="csv")

    if upload_file is not None:
        add_stocks_from_csv(upload_file)
        st.success('Stocks added from CSV')

    st.subheader('Current Portfolio')
    df = display_stock()
    st.write(df)

    st.subheader('Remove a Stock')
    remove_stock_name = st.text_input('Enter Stock Name to Remove')
    if st.button('Remove Stock'):
        if remove_stock_name in st.session_state.sname:
            remove_stock(remove_stock_name)
            st.success(f'Stock {remove_stock_name} removed')
        else:
            st.error(f'Stock {remove_stock_name} not found')

    st.subheader('Remove entire Portfolio')
    if st.button('Remove Portfolio'):
        clear_portfolio()
        st.success('Portfolio Cleared')

    st.subheader('Portfolio Statistics')
    total_stocks = len(st.session_state.sname)
    total_attributes = 3 
    st.write(f'Total number of entities (stocks): {total_stocks}')
    st.write(f'Number of attributes per entity: {total_attributes}')

    st.subheader('Save Current Portfolio to Cloud')
    if st.button('Save to Cloud'):
        csv_url = upload_csv_to_firebase()
        if csv_url:
            st.success('Portfolio saved to the cloud.')
            st.write(f'Download your portfolio from [here]({csv_url})')

    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['page'] = 'login'
        st.experimental_rerun()

# Call the portfolio function to run the app
if __name__ == '__main__':
    portfolio()
