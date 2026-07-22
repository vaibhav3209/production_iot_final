# ================================
# Libraries
# ================================

import random
import time
import requests
import os,sys
import django
from pathlib import Path
from dotenv import load_dotenv



# ================================
# Make Configurations (required)
# ================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

'''Debug Path before loading'''
# print(BASE_DIR)

sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teststudy.settings")

django.setup()







# ================================
# Load env.simulated file
# ================================
load_dotenv(BASE_DIR / "config" / ".env.simulated")



class LoginService:
    def __init__(self):
        self.base_url = os.getenv('RENDER_APP_URL')
        # self.base_url = "http://127.0.0.1:8000"
        self.login_url = f"{self.base_url}/login/"

    def login(self,session:requests.Session, username, password):

        # Step 1: get CSRF token from login page (one time)
        login_page = session.get(self.login_url)
        csrftoken = session.cookies.get('csrftoken')


        # Step 2: post credentials
        resp = session.post(
            self.login_url,
            data={
                "form_type":'user_login',
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrftoken,
            },
            headers={"Referer": self.login_url},
        )

        if resp.url.endswith('/student/'):
            print(f"{username} Login Succesfull",resp.status_code)
            return True

        return False



"""
Usage: 
import requests

from services.login_service import LoginService

session = requests.Session()

login_service = LoginService()

success = login_service.login(
    session=session,
    username="23ESK001",
    password="mypassword"
)

if success:
    print("Ready for next module.")
else:
    print("Login failed.")"""







