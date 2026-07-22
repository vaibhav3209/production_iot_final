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


# ================================
# Import Cache Methods
# ================================
"""This is just PYcharm Error"""
from final.views import (
    get_all_categories,
    component_in_category_x,
    get_all_available_projects
)





# ================================
# Import Login
# ================================
from bot_login_service import LoginService


class GenerateRequest:
    def __init__(self):
        self.projects = get_all_available_projects()
        self.categories = get_all_categories()
        self.base_url = os.getenv('RENDER_APP_URL')
        # self.base_url = "http://127.0.0.1:8000"
        self.login_url = f"{self.base_url}/login/"


    def generate_and_submit(self,session:requests.Session):

        """ One Random Project"""
        random_project = random.choice(self.projects)


        """ Select random category"""
        random_category = random.choice(self.categories)


        """Find Components in that category"""
        random_components = component_in_category_x(random_category)
        # print(random_components)


        """ Pick five compoenent ------ baad mein jayda bhi kar sakte """
        select_random_component = random.sample(random_components,min(5,len(random_components)))
        # print(select_random_component)



        """ Make transactions """
        project_id = [str(random_project.id)]
        component_ids = [str(i) for i in select_random_component]
        quantities = [str(1) for _ in range(len(select_random_component))]



        """Submit this request"""
        submit_url = f"{self.base_url}/student/submit_request/"

        # resp = session.get(self.login_url)
        resp = session.get(submit_url)
        csrftoken = session.cookies.get('csrftoken')



        data = {
            'csrfmiddlewaretoken': csrftoken,
            'project_id': project_id,
            'component_ids[]': component_ids,
            'quantities[]': quantities
        }

        response = session.post(
            url=submit_url,
            data=data,
            headers={"Referer": submit_url,
                     "X-CSRFToken": csrftoken
                     },
        )

        if response.status_code ==200:
            print("Request submitted succesfully")
            return True


        print("Unsuccessful request submission")
        print(response.text)
        return False



