#  📑 Table of Contents
- [Readme Shortcuts/Notations](#-readme-shortcuts)
- [Features](#-features)
- [Installation](#-installation)
- [Directory Structre](#-directory-structure)
- [Future Improvements](#-future-improvementsfor-future-developers)
- [Problems](#-implementation-problems-)
- [Testing Doubts for me](#testing-doubts-for-me-)

---------------------------------------------------------------------------
## 🔑 ***Readme Shortcuts***
- `##` → section heading
- `***text***` → bold + italic emphasis
- `-` → bullet points
- `` `code` `` → inline code
- ``` ``` → code block
- `>` → note / important message
- enter for two lines to give space between each list point 
---------------------------------------------------------------------------

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

## ⏳ Future Improvements(For future developers)

> no PROJECT is perfect....

- Fix css in the teacher/activity page for buttons.
- paginate or order by most popular the Inventory_items  list or something else.. in order to fetch less from db
- Understand the working of apply filters or remove filters
- Wherever the Filters are applied you should keep their data unless new are applied even when you are reloading, pageshifting
- Student Profile table of componenet issue histroy must be paginated and filter based on date,category,not returned etc can be applied too.
Note: we have applied indexes on one tyoe of date so filter data on basis of that indexed date.
- DO we have to make the functionality of disappear sidebar on outside click. on student panel??????

1. Improve Home Page according to the business requirements.

2.  Change the  Project's views.py to a `Class-Based design` using OOPS principles

    Also implement try-catch wherver possible and give adequate messages.

3. Make the Code Modular remove Snippets/logic of code that are reused and define them single time.

4. Make the year of Student Editable. (If in case the website is used by student for more than one year.)

5. Make a feature to see the individual Component's issue records by repective students.

   ==>> Currently we have Components issued per Project. 
    
   ==>> Components issued by individual Student. 


6. Logic for` Deletion `needs to be configured:::
   - like when any entry like component,student,branch,project will get deleted what will happen 
   to related data.
   
 > 📌 **Remember:** think Twice before making this logic otherwise Database will be at risk.

7. Also transfer this into .csv file before then delete issue logs without sending important details.


8. Add a feature of `Forgot Password via the mail.`

 

9. TO make the process of issuing components Fastest as light ⚡
   - ***QR SCANNING*** :: for components directly to a specific project. This will include adding
   tokens and uuids instead of integer ids to table values to uniquely identify components.

   - I was not a web developer so future devs must apply their web development knowledge to 
     optimise the Backend and Frontend.

   > Topics like : HTMX, async () , API optimisation, advance JS(if there's such term) etc.  


10. Filtering and searching of data can be made better. 


11. `📊 Analytics` page showing growth, amount issued, usage, MAUs etc via appropriate graphs.


12. `Request Based System` like wishlist or add to cart and notifications when component available.


13. Email and phone number secure storage in database and  verification  but it will have to incur some cost.
  (I don't know how it is stored in actual Production when we have resources available.)


14. Currently we are doing Refresh every time a new request or approve comes.
    
    We can make it `Realtime` .


15. Transfer data of issue log per month or so to a csv file to keep backup. (Refer point 2 of implementation problems below.)


16. ### 🤖 AI integrations : 

    - Demand Prediction for every new project.
    - Issuing prediction as per student. 
    - low stock alerts and hackathons components classification etc.


17. Displaying 15 Most popular Components in the start in overall categories to directly issue which will
reduce query load on databse.  


---------------------------------------

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

> 💀💀 if by any means the email id on which the project is uploaded gets deleted i don;t know what will happen to data 

------------------------------------------

## Testing doubts for me :

- see that the activity page in the teacher section query the databse again and again if we 
    change the page but not change the filters.