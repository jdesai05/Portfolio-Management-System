import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('API_KEY')
storage_bucket = os.getenv('STORAGE_BUCKET')
auth_domain = os.getenv('AUTH_DOMAIN')
database_url = os.getenv('DATABASE_URL')

config = {
    "apiKey": api_key,
    "authDomain": auth_domain,
    "databaseURL": database_url,
    "storageBucket": storage_bucket,
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
