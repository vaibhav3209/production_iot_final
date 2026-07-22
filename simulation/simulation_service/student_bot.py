import requests

from iot_inventory_mgmt.simulation.simulation_service.bot_login_service import LoginService
from iot_inventory_mgmt.simulation.simulation_service.request_generation_service import GenerateRequest


class StudentBot:

    def __init__(self):
        self.session = requests.Session()

        self.login_service = LoginService()
        self.request_service = GenerateRequest()

    def run(self, username, password):

        logged_in = self.login_service.login(
            self.session,
            username,
            password
        )

        if not logged_in:
            print("Login failed")
            return

        submission = self.request_service.generate_and_submit(self.session)



bot1 = StudentBot()
bot1.run(username="23ESKCX120",password="vaibhav123")