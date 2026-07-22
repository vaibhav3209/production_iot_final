from collections import defaultdict

# cache handling instead of requesting everytime
from iot_inventory_mgmt.final.views import students_per_project

from supabase import create_client
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "config" / ".env")


SUPABASE_URL= os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY= os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY)

# students = (
#     supabase
#     .table("final_projectenrolledstudents")
#     .select("proj_enroll_project_id","proj_enroll_student_id")
#     .limit(5)
#     .execute()
# )
#
# print(students.data)
#
# mydict = defaultdict(list)
# for i in students.data:
#     mydict[i['proj_enroll_project_id']].append(i['proj_enroll_student_id'])
#
