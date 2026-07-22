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



class RegisterService:
    def __init__(self):
        self.base_url = os.getenv('RENDER_APP_URL')
        # self.base_url = "http://127.0.0.1:8000"
        self.signup_url = f"{self.base_url}/login/"
        self.session = requests.Session()

    def get_csrf_token(self):
        response = self.session.get(self.signup_url)

        if response.status_code != 200:
            raise Exception("Unable to open signup page.")

        # Django stores csrftoken in cookies
        token = self.session.cookies.get("csrftoken")


        if not token:
            raise Exception("CSRF token not found.")

        return token


    def register(self,number_toenglish,roll_number,email):
        csrf = self.get_csrf_token()

        payload = {
            "csrfmiddlewaretoken": csrf,
            "form_type": "user_signup",
            "first_name": "bot",
            "last_name": f"{number_toenglish}",
            "roll_number": f"{roll_number}",
            "college_email": f"{email}",
            "password": f"Botone@123",
            "phone_number": f"98{random.randint(70000000,99999999)}",
            # "std_year": random.choice(["1", "2", "3", "4"]),
            "std_year":"4",
        }

        headers = {
            "Referer": self.signup_url
        }


        response = self.session.post(
            self.signup_url,
            data=payload,
            headers=headers,
        )
        if response.status_code == 200:
            print(f"Registered Succesfull for bot{number_toenglish}")
        else:
            print('Registration unsuccessful')

if __name__ == "__main__":
    """ Keeping only one session To speed up registration only."""

    bot = RegisterService()

    students = [
        # -------------------- SECTION CX --------------------
        {"number_toenglish": "one", "email": "b230001", "roll_number": "23ESKCX001"},
        {"number_toenglish": "two", "email": "b230002", "roll_number": "23ESKCX002"},
        {"number_toenglish": "three", "email": "b230003", "roll_number": "23ESKCX003"},
        {"number_toenglish": "four", "email": "b230004", "roll_number": "23ESKCX004"},
        {"number_toenglish": "five", "email": "b230005", "roll_number": "23ESKCX005"},
        {"number_toenglish": "six", "email": "b230006", "roll_number": "23ESKCX006"},
        {"number_toenglish": "seven", "email": "b230007", "roll_number": "23ESKCX007"},
        {"number_toenglish": "eight", "email": "b230008", "roll_number": "23ESKCX008"},
        {"number_toenglish": "nine", "email": "b230009", "roll_number": "23ESKCX009"},
        {"number_toenglish": "ten", "email": "b230010", "roll_number": "23ESKCX010"},
        {"number_toenglish": "eleven", "email": "b230011", "roll_number": "23ESKCX011"},
        {"number_toenglish": "twelve", "email": "b230012", "roll_number": "23ESKCX012"},
        {"number_toenglish": "thirteen", "email": "b230013", "roll_number": "23ESKCX013"},
        {"number_toenglish": "fourteen", "email": "b230014", "roll_number": "23ESKCX014"},
        {"number_toenglish": "fifteen", "email": "b230015", "roll_number": "23ESKCX015"},
        {"number_toenglish": "sixteen", "email": "b230016", "roll_number": "23ESKCX016"},
        {"number_toenglish": "seventeen", "email": "b230017", "roll_number": "23ESKCX017"},
        {"number_toenglish": "eighteen", "email": "b230018", "roll_number": "23ESKCX018"},
        {"number_toenglish": "nineteen", "email": "b230019", "roll_number": "23ESKCX019"},
        {"number_toenglish": "twenty", "email": "b230020", "roll_number": "23ESKCX020"},

        # -------------------- SECTION CY --------------------
        {"number_toenglish": "twentyone", "email": "b230021", "roll_number": "23ESKCY021"},
        {"number_toenglish": "twentytwo", "email": "b230022", "roll_number": "23ESKCY022"},
        {"number_toenglish": "twentythree", "email": "b230023", "roll_number": "23ESKCY023"},
        {"number_toenglish": "twentyfour", "email": "b230024", "roll_number": "23ESKCY024"},
        {"number_toenglish": "twentyfive", "email": "b230025", "roll_number": "23ESKCY025"},
        {"number_toenglish": "twentysix", "email": "b230026", "roll_number": "23ESKCY026"},
        {"number_toenglish": "twentyseven", "email": "b230027", "roll_number": "23ESKCY027"},
        {"number_toenglish": "twentyeight", "email": "b230028", "roll_number": "23ESKCY028"},
        {"number_toenglish": "twentynine", "email": "b230029", "roll_number": "23ESKCY029"},
        {"number_toenglish": "thirty", "email": "b230030", "roll_number": "23ESKCY030"},
        {"number_toenglish": "thirtyone", "email": "b230031", "roll_number": "23ESKCY031"},
        {"number_toenglish": "thirtytwo", "email": "b230032", "roll_number": "23ESKCY032"},
        {"number_toenglish": "thirtythree", "email": "b230033", "roll_number": "23ESKCY033"},
        {"number_toenglish": "thirtyfour", "email": "b230034", "roll_number": "23ESKCY034"},
        {"number_toenglish": "thirtyfive", "email": "b230035", "roll_number": "23ESKCY035"},
        {"number_toenglish": "thirtysix", "email": "b230036", "roll_number": "23ESKCY036"},
        {"number_toenglish": "thirtyseven", "email": "b230037", "roll_number": "23ESKCY037"},
        {"number_toenglish": "thirtyeight", "email": "b230038", "roll_number": "23ESKCY038"},
        {"number_toenglish": "thirtynine", "email": "b230039", "roll_number": "23ESKCY039"},
        {"number_toenglish": "forty", "email": "b230040", "roll_number": "23ESKCY040"},

        # -------------------- SECTION CS --------------------
        {"number_toenglish": "fortyone", "email": "b230041", "roll_number": "23ESKCS041"},
        {"number_toenglish": "fortytwo", "email": "b230042", "roll_number": "23ESKCS042"},
        {"number_toenglish": "fortythree", "email": "b230043", "roll_number": "23ESKCS043"},
        {"number_toenglish": "fortyfour", "email": "b230044", "roll_number": "23ESKCS044"},
        {"number_toenglish": "fortyfive", "email": "b230045", "roll_number": "23ESKCS045"},
        {"number_toenglish": "fortysix", "email": "b230046", "roll_number": "23ESKCS046"},
        {"number_toenglish": "fortyseven", "email": "b230047", "roll_number": "23ESKCS047"},
        {"number_toenglish": "fortyeight", "email": "b230048", "roll_number": "23ESKCS048"},
        {"number_toenglish": "fortynine", "email": "b230049", "roll_number": "23ESKCS049"},
        {"number_toenglish": "fifty", "email": "b230050", "roll_number": "23ESKCS050"},
        {"number_toenglish": "fiftyone", "email": "b230051", "roll_number": "23ESKCS051"},
        {"number_toenglish": "fiftytwo", "email": "b230052", "roll_number": "23ESKCS052"},
        {"number_toenglish": "fiftythree", "email": "b230053", "roll_number": "23ESKCS053"},
        {"number_toenglish": "fiftyfour", "email": "b230054", "roll_number": "23ESKCS054"},
        {"number_toenglish": "fiftyfive", "email": "b230055", "roll_number": "23ESKCS055"},
        {"number_toenglish": "fiftysix", "email": "b230056", "roll_number": "23ESKCS056"},
        {"number_toenglish": "fiftyseven", "email": "b230057", "roll_number": "23ESKCS057"},
        {"number_toenglish": "fiftyeight", "email": "b230058", "roll_number": "23ESKCS058"},
        {"number_toenglish": "fiftynine", "email": "b230059", "roll_number": "23ESKCS059"},
        {"number_toenglish": "sixty", "email": "b230060", "roll_number": "23ESKCS060"},
    ]

    for i in students:
        bot.register(
            number_toenglish=i['number_toenglish'],
            email=i['email'],
            roll_number=i['roll_number']
        )
        time.sleep(0.3)
