#  📑 Table of Contents
- [Readme Shortcuts/Notations](#-readme-shortcuts)
- [Account Required](#account-required-)
- [Dependencies](#-dependencies)
- [Features](#-features)
- [Installation](#-installation)
- [Directory Structre](#-directory-structure)
- [ER diagram](#er-diagram-paste-in-future)
- [Future Improvements](#-future-improvementsfor-future-developers)
- [Problems](#-implementation-problems-)
- [Testing Doubts for me](#testing-doubts-for-me-)

---------------------------------------------------------------------------

## 🌐 Account Required
- upstash(for cache)
- render
- supabse


-------------------------------------------------------------------
## 🧩 Dependencies

This project uses the following core technologies in production(***rest are inclusive in these only***):

🐍 Backend Framework

`Django 5` – High-level Python web framework used to build the core application logic.

`Django REST Framework` – Used for building RESTful APIs.

🗄️ Database

`PostgreSQL` – Production-grade relational database.

`psycopg2-binary` – PostgreSQL adapter for Python (enables Django to connect to Postgres).

`dj-database-url` – Parses database URLs for easy production configuration (Render/Supabase compatible).

⚡ Caching

`Redis` – In-memory data store used for caching.

`django-redis` – Django integration for Redis caching backend.

🚀 Production Server & Static Files

`Gunicorn` – Production WSGI server used to serve the Django application.

`Whitenoise` – Serves static files efficiently in production.

🔐 Environment Configuration

`python-decouple` – Secure management of environment variables (SECRET_KEY, DATABASE_URL, etc.).

📊 Additional Integrations

`OpenPyXL` – Excel file generation and processing.

`Requests` – HTTP client for external API calls.



-------------------------------------------------------------------

## ✨ Features


- **Student Registration**
  - Register students using roll number and basic details
  - Remaining details can be completed later from the dashboard


- **Student Profile View**
  - issue components
  - view currently issued and returned 
  - project specific issuance


- **Admin / Teacher Dashboard**
  - Centralized dashboard for teachers/admins
  - View all students and issued components
  - Approve or reject component issue requests
  - Adding new projects  
  - Clickable roll number to view full student details
  - Displays all components issued to one particular student


- **Component Issuance System**
  - Track issued components with issue date and quantity
  - Maintain complete issuance history per student
  - Prevent issuing components beyond available quantity

    
- **Role-Based Access**
  - Separate access for students and teachers/admins
  - Django superuser support for admin panel
---------------------------------------------------------------------------

## 🛠️ Installation

> commands will differ for MAC users


1. Clone the repository. 
`https://github.com/vaibhav3209/production_iot_final`


2. Virtual ENV: see this page and create and activate your virtual env.
`https://www.w3schools.com/python/python_virtualenv.asp`

> 📌 **Remember:** keep the name of environment anything other than venv,env as it will cause reading issued from .env file that 
> we have in our project.


3. Now do  ` pip install -r config/requirements.txt` since the requirement.txt file is in config folder.


4. Populate the .env file. (Take it from the team leader.)
    Fields for env file are:: 

    - DATABASE_URL  ⚠️ The application will not start if `DATABASE_URL` is missing. Admin interface will not be available otherwise.
    - SECRET_KEY : (make new key every time from django)
    - DEBUG=True/False
    - ALLOWED_HOSTS
    - ADMIN_PATH
    - SESSION_COOKIE_SECURE=True/False
    - CSRF_COOKIE_SECURE=True/False
    - SESSION_COOKIE_AGE=True/False
    - CSRF_TRUSTED_ORIGINS
    - MAIL_API_KEY
    - REDIS_URL




> 📌 **Remember:** IF NOT present,, make gitignore file and  ⚠️!EXCLUDE .env from uploading to github.


6.  if you want Local database, you can select `db.sqlite3` from `settings.py` and uncomment it.


7.  (ONLY if) using local database run ::  `python manage.py migrate`  to translate models into the database tables. 
   
 
8.  using RENDER:   
    - make a build command like... 
     
            `pip install -r config/requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`

    - and start command like ...
    
        `gunicorn teststudy.wsgi:application`


9. Generate new Secret Key everytime: 
    
        python manage.py shell
        >>from django.core.management.utils import get_random_secret_key
        >>print(get_random_secret_key())

10. Create a Django superuser
(the username and password will help in the teacher login panel)
    
    `python manage.py createsuperuser`  

> 📌 **Remember:**  username should be 10digit only as set by me in `login.html` and `model Student` constraints


11. Check whether the project is running 
            
    `python manage.py runserver`

  
>⚠️️ 💀**Remember:**  Never delete or change  schema from database from online portals.

> ***IMPACT***:: otherwise your local `migrations` and `migrations` table in database  will 
     conflict then it will be a problem.

> ✅✅***Practice*** : Always make changes from Django only which is our only Backend For now.

---------------------------------------------------------------------------

## 🗂️ Directory Structure

project_root/

    ├── manage.py

    ├── README.md

    ├── .gitignore  (not on github)

    ├── db.sqlite3  (not on github)

    │──extra_Scripts/
            ├── test_db.py
            ├── export_fixture.py
    


    ├── staticfilesforproduction/           (not on github) # collectstatic output (production)

    ├── config/                             # Non-code configuration
        ├── .env
        └── requirements.txt


    ├── teststudy(package)/                  # Project name
        ├── __init__.py
        ├── settings.py                      # settings & config
        ├── urls.py
        ├── asgi.py
        └── wsgi.py


    ├── final(package)/                      # Main Django app
        ├── __init__.py
        ├── admin.py                         # registers model here for Django admin panel
        ├── apps.py                          # register you app if we make new
        ├── decorators.py                    # checks login for admin and student
        ├── models.py                        # database tables 
        ├── views.py                         # Logic for project 
        ├── urls.py                          # Routing 
        ├── migrations(package)/
            └── __init__.py
        
        ├── templates/
            └── final/
                └── *.html
        
        ├── static/
           └── final/
               ├── css/
               ├── js/
               └── images/
       
           ├── management(package)/
                ├── __init__.py
                └── commands(package)/
                    ├── __init__.py
                    └── import_components.py
---------------------------------------------------------------------------

## 📖 ER Diagram( Paste in Future)



---------------------------------------------------------------------------

## 📚 PROJECT GUIDELINES

- We didn't used `Django--User model` as it was slow....... MAY BE due to our bad code but it was slow...
---------------------------------------------------------------------------
## ⏳ Improvements(For future developers)

> Please don't change the code structure without proper planning. Everything is ***mostly*** organised. 

> use AI but with proper knowledge.


### UI/UX changes:

- General changes:
    - First and Foremost, ask the teachers to keep the login page directly or making the home page useful.

    - Then Fix overall CSS of homepage. then on moving to login page see what can we ***MATCH*** in the CSS of internal as well as both external pages. 
    (***keep in mind***  not to remove the message box in the login page below title student login.)

    - Adding a ***forgot password*** option in the login page.

    - Getting Photos of components if added in the Database.

    - Add proper messages in the website only whenever there's chances of Server Error.

    -  All the tables follow the same CSS but the issue is when we select a table row and click add 
        the ***selection hover disappears***.  We have to fix this.

    > IF you can make the Tables horizontally scroll instead of current CSS ==>> that will be some good work.
    
    - Quick ***Search bar*** feature for fetching component by name both in teacher and student panels.
    
      `This can work as the Components will be less in number.` 


- Student Interface changes:(***Primarily used on mobile***)
    - On the Dashboard, the ***View All*** and ***View Issued Components*** can be made some different Style.
    
    - Keeping the Filters intact even if the user Switch pages and their respective results too.
    (Unless new filter applied or site closed)

    - When we click Request Components>>Request component sidebar ===== That needs some UI changes.
        - Select project popup comes out of Screen that is not required.
        - Selected components should come in good Orientation not just normal text as it is currently.
        - Decorate buttons too (***But with same color scheme as the entire Project***)
    
    - ""Add"" button in table row expands more when clicked. We want inplace.


- Admin Interface :
  
    - IF required we can make this work on ***Mobile version***.
    - Add a column for Student name also in admin dashboard panel.
    - You are Free to change the Student Proile CSS, new ideas are Welcomed...


### Backend Changes 

- Adding a ***forgot password*** feature (ONLY FOR STUDENTS). Note that the passwords are encrypted in the database. 


- We can keep the student always logged in unless he logs out(like erp as there's not much personal data).


- Change the  Project's views.py to a ***Class-Based design*** using OOPS principles

    Also implement try-catch wherever possible and give adequate messages.

    Example: 
        
    - whenever the currently available==0 and requested is there ==>> if teacher clicks accept then ***SERVER ERROR*** happens.
    Give a message instead of this. 


- See all possibilities of Going into a ***Server error*** situation throughout the website.


- The ***Add component*** Button in the Admin dashboard->>Inventory page is not adding the components in the specific category.


- Amin dahsboard-->>Inventory-->>any category ,then we see a table which has `mark as deleted` but doesn't have 
    ***mark as working*** option again to  change deleted component if we want to.


- Admin Dashboard-->>All students-->> When we Search by Name it gives a server Error. We have made it Compulsory to give
    year and branch but the name feature should also work.


- Add new Faculty has some issue with IOT and Electrical Mismatch.


- Add Filter based on ***OUT OF STOCK*** in the existing filters. 


-  Optimixations like : HTMX, async () ,  advance JS(if there's such term) etc.  


### Database changes(By me)

> Note: we have applied indexes on one tyoe of date so filter data on basis of that indexed date.
 Don't change indexes Randomly.


- Storing of ***phone numbers*** in the database is direct. Is there any way we can encrypt phone numbers?
How are they stored in real world applications?


- Should we completely ***remove the year*** column as it will change after sometime 
and the year can be identified from the roll no. ?


- We can afford adding component pictures for better UI/UX(but to some extent).
  
    Then we have to see Overall affect on speed, performance and optimise in ***QUICK MODE*** if required.


-  ***API*** 
    - It can be made to filter results based on some conditions , as that would make the load of api query less. 
    - Currently API can be accesed by admins and staff only make it accesible to student but only their records.

    

### Testing and Security 

- We want to check and ensure specific number of logins a user can make from multiple devices.Right now it
is not configured.


- Tokenising(Prevent URL Exposure)
    - use `uuids` to store student id's and component id's etc.
    - Instead of giving `<path:>` give a` random token ` value for each category which expires after 
      short time to avoid Guessing by users.


-  Add Github Branch Protection to secure it from `git push -- force` and every push will be made only by pull request. 


- Keep data secured in transit in network.(like passwords, api calls etc)

- Controlling/ Manage read and writes on the same table like issue Records.


### Completely new features 

- ***QUICK MODE*** can be enabled once the student is logged in :
    
  - QR code can be applied for 6 main categories..***(Not for ALL COMPONENTS)*** 
    then on Scanning a quick list of most popular components come and the student just
    add quantity requested and add project then submit.

    (This might be done by adding tokens and special uuids for each category.)


- ***Save login credentials***: (like many social media sites like instagram) to increase
    the speed of process. (may be on google save passwords or like saved profiles feature on instagram)

    Then after 15 days or so reinput password for some security.


-  ***Records BACKUP***: All the records of current and previous students must be stored for a long time.
    Add a feature to transfer records to Csv or Excel after a year or semester.(This is important and Can't mess up.)


- ***Analytics page***: We can show Visualisations and analytics of components issued per unit time,
    user engagement , monthly active users, efficiency increase vs offline issuing of components etc


-   Currently, we are doing Refresh every time a new request or approve comes.
    
    We can make it ***Realtime*** .(But it comes with More load on database)


- Sending Email Functionality for forgot Password or One time Mobile Verification. 


- Allowing admins to see Data in any form:
    - Components Issued by a Student
    - Components Issued in specific Project.
    - Records for a Particular Component, etc
-----------------------



## ⚠️ Implementation Problems 

1. There can be a case of `Virtual Issuing`

    A student can make a request and the teacher can approve it but in actual scenario ...

    no component is taken from the lab.

2. At the initial stage of the project the lab teacher have to maintain a register to keep a physical record of issue requests.
    This can be solved by transferring data everyday to a csv file. 

3. Teacher panel will have multiple requests and he/she can click multiple approve buttons at the same time,
    
    However i have added `with.transaction()` that will submit only one transaction at a time. 

    >❗ BUT if not Optimise this bulk submission of requests' approvals  and rejection from the admin dashboard panels. 

4. Managing multiple API requests and Connection from user side since we are using the free version of Databse service is limited.


5.  We have not made the feature due to Said Business Requirement that teacher will manually issue components.

    - But if there might be a case: that student might issue all the quantity of a component and the teacher can't change
    
    so he/she will have to either reject the request or approve the whole qty which will be unfair to ither users.

    > ***✨ Solution: New feature of aproving dynamic range of quantities similar to add option in the student request components. Allow teacher to issue the quantity he want. 
depending upon the  availibilty and need per project.***
    
    - so student only sends the name on component and qunatity requested.
------------------------------------------