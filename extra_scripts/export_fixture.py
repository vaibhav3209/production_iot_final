# This is a safety script to Dump data into a json file to shift databse from online to offline
# or vice versa

from django.core.management import call_command
import os
import django

# Setup Django (only needed if running outside manage.py context)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teststudy.settings")
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", indent=2, stdout=f)