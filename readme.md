# Index :


- [Checkpoints](#checkpoints-before-starting)
- [Tips](#tips)
- [Project Guide Know hows](#project-guidelines)
- [MY Mistakes](#mistakes-that-i-have-done)
- [Testing](#how-to-test)
- [Django important Functionalities](django-functionalities)
- [My Learnings](#-things-i-learnt-new-besides-django)
- [Security Notes](#security-notes)

---------------------------------------------------------------------------


---------------------------------------------------------------------------
## ⚙️ ***Installation***

- **Clone the repository**


- Make a virtual environment inside the cloned directory and install all dependencies

- > Activate the virtual env

- Go to the `settings.py` file inside `teststudy/` and check the hidden configuration 
  tags  
  - `config()`  
  - `os.getenv()`


- These values must be defined in your own `.env` file inside the `CONFIG/` directory
> 📌 **Remember:** ⚠️ keep the ``.env`` file there only. (NOT UPLOAD)
  

- If you want to use a ***local database***:
  - Uncomment `db.sqlite3` lines
  - Do this  in the `DATABASES` section of `settings.py`


```
- Run this command :: python manage.py migrate
📝 This will create the database file the first time it is run
```

- Create a Django superuser
(This will help in the teacher login panel)
    
    `python manage.py createsuperuser`   


-  then use username and password to login to teacher panel.

> 📌 **Remember:**  username should be 10digit only as set by me in> 


`login.html` and `model Student` constraints


- Check whether the project is running

  `python manage.py runserver`
---------------------------------------------------------------------------



----
## Checkpoints before Starting
- ⚠️ The application will not start if `DATABASE_URL` is missing. Ensure this environment variable is set before deployment. Admin interface will not be available otherwise.



---
## Tips

- `__str__() in Django Models`
  
  - In Django models, the __str__() method defines how an object is displayed when it is printed or shown in the Django admin.  
What this does

- Controls how the object appears when you run: `print(category)`


- Improves readability in:

    Django Admin
    
    Django Shell
    
    Debug logs
    
    Queryset outputs

 - Without __str__()
<Category: Category object (1)>

- With __str__()
Electrical Components
---------------------------------------------------------------------------
## PROJECT GUIDELINES

1.  Kept small Letters of all column names.


2.  Every column will start from a prefix of its table name. 


    comp_cate_                   ==>>  for Component_categories
    comp_attribute_              ==>>  for Component model
    std_attribute_               ==>>  for Student model
    std_issue_                  ==>>  for StudentIssueLog model
  

3. see table definitions from the `models.py` file.


4. >📌 **Remember:**  keep DEBUG == TRUE in development and
         DEBUG == False in production as u don't want users to see errors.


5. Put business logic in `models.py` file and HTML, session based(HTTPRequest) in ``views.py``.


6. Student signup/login form can values in any Case but searching/Storing of values in databse 
   is done in upper case for roll.no and Lower case for firstname and lastname 

7.  ### `INDEXING RULES`:

      - Use Indexing for those fileds that are not Write heavy.  
---------------------------------------------------------------------------


---------------------------------------------------------------------------
# MISTAKES THAT I HAVE DONE  (***IMPORTANT***)


1.  We didn't used `Django--User model` as it was slow.......
      
(it may be due to our wrong code but it was.) and we don't accept our product to be SLOW....
I TRIED `shifting to USer model` AFTER MAKING PROTOTYPE OF OUR PROJECT (which was a very bad 
decision costing me 2 days
       and i have to SHIFT BACK TO ORIGINAL PROTOTYPE)


2.   You should not write `html`,`css`,`js` all in one file. why? 
- a. If you wan the same css in some files. You have to write it everywhere!!! 
- b. let's say you used all code in one file but if you have to change anything in the repeated 
  code you have to change in `EVERY FILE`

  
>📌 **Remember:**  Never delete or change  schema from database online if online databse you 
     are using  
     (Except you can delete 
     data from table from anywhere)

> ***IMPACT***:: otherwise your local `migrations` and `migrations` table in database  will 
     conflict then it will be a problem.

> ***Solution***: command `python manage.py makemigrations --fake`   but it is not worth it.


3. `<str:category>` in `urls.py` not allow `micro / boards` urls with spaced, underscores. 

Thats why companies uses `SLUG FIELDS` To better fit the urls. (BUT i don't used them here 😄)

> ***SOLUTION*** :: slash lagane k liye `<path:category_key>` kardo


4.  ***NOTE***:   `url == admin/`  will point to django admin. So if i wented to write teacher 
    dashboard add the keyword Teacher not admin

### team work: Make sure this!!
 
- don't make additional migrations  as other team members database will differ as they don't 
  have the migrations that you have made. 
- 
---------------------------------------------------------------------------
## HOW to Test for all possible bugs:

1. 

---------------------------------------------------------------------------

---------------------------------------------------------------------------
## Django Functionalities

### 1. how Related_name works in a foreign key:: It allows easy reverse queries. 

        student = Student.objects.get(id=1)
            student.issue_logs.all()

     means:::: Give me all issue log records that belong to this student.


Category table

| id | category_name        |
|----|----------------------|
| 1  | Sensors              |
| 2  | Microcontrollers     |


Component

| id | component_name | category_id |
|----|----------------|-------------|
| 1  | DHT11          | 1           |
| 2  | Ultrasonic     | 1           |
| 3  | Arduino Uno    | 2           |
| 4  | ESP32          | 2           |


| Query | Without related_name           | With related_name           |
|------|--------------------------------|-----------------------------|
| Get category of component | `component.comp_category`      | `component.comp_category`   |
| Get components of category | `category.component_set.all()` | `category.componentcategory_fkey.all()` |


### 2.  `__` means “go inside model”  if we are referncing two models you will see this in html code.


### 3. 🧠 Django ORM → SQL Mental Mapping

| Django ORM          | SQL Think        |
|---------------------|------------------|
| `.filter()`         | `WHERE`          |
| `.select_related()` | `JOIN`           |
| `.only()`           | `SELECT columns` |
| `.all()`            | `SELECT *`       |


| Django ORM | SQL Equivalent | Notes                                                          |
|------------|----------------|----------------------------------------------------------------|
| `Component.objects.filter(comp_category_id=1)` | `SELECT * FROM component WHERE comp_category_id = 1;` | Filters rows by condition                                      |
| `Component.objects.select_related("comp_category")` | `SELECT component.*, category.* FROM component INNER JOIN category ON component.comp_category_id = category.id;` | Joins related FK table to avoid extra queries                  |
| `Component.objects.only("comp_name", "comp_quantity_available")` | `SELECT id, comp_name, comp_quantity_available FROM component;` | Fetch only selected columns; others deferred                   |
| `comp = Component.objects.only("comp_name").first()`<br>`comp.comp_price` | `SELECT comp_price FROM component WHERE id = 1;` | gets first row . Accessing deferred field triggers extra query |
|  `logs = request.user.student.issue_logs.all()` | `SELECT * FROM studentissuelog WHERE student_id = <current_student_id>;` | Fetch all issue logs for a student |
| `student.issue_logs.filter(status_from_teacher="Approved").count()` | `SELECT COUNT(*) FROM studentissuelog WHERE student_id = <student_id> AND status_from_teacher = 'Approved';` | Count only approved items |
|  `student.issue_logs.filter(component=component, status_from_teacher="Pending").exists()` | `SELECT 1 FROM studentissuelog WHERE student_id = <student_id> AND component_id = <component_id> AND status_from_teacher = 'Pending' LIMIT 1;` | Returns True if a pending request exists |


| Query style            | What you get  | How to access   |
| ---------------------- | ------------- | --------------- |
| `.all()` / `.filter()` | Model objects | `obj.field`     |
| `.values()`            | Dictionaries  | `dict["field"]` |
| `.values_list()`       | Tuples        | `tuple[index]`  |



---------------------------------------------------------------------------


### 4.✅ `Advantages of Django ORM:`  
- Pros
    - ✔ Safe (SQL injection protected)
    - ✔ Readable & maintainable
    - ✔ Easy to refactor
    - ✔ DB-agnostic (Postgres / SQLite / MySQL)
    - ✔ Django handles joins efficiently
    - ✔ Easier for teammates (or future you)

- Cons
  - ❌ Very complex queries can get ugly
  - ❌ Rare edge-case optimizations harder


### `Why not Raw SQL!!!`

- Pros
    - ✔ Absolute control
    - ✔ Best for very complex aggregations
    - ✔ Can squeeze last 5–10% performance

- Cons
  - ❌ Easy to introduce bugs
  - ❌ Hard to maintain
  - ❌ DB-specific
  - ❌ No automatic security unless careful
  - ❌ Harder to refactor models
---------------------------------------------------------------------------
## THINGS I LEARNT NEW BESIDES "DJANGO"

### 1. 🔐 Row Level Security (RLS) – Access Matrix

| Who                   | SELECT | INSERT | UPDATE | DELETE |
| --------------------- | ------ | ------ | ------ | ------ |
| Django backend        | ✅     | ✅     | ✅     | ✅     |
| Students (via Django) | ✅     | ❌     | ❌     | ❌     |
| Supabase anon         | ✅     | ❌     | ❌     | ❌     |
| Supabase REST         | ✅     | ❌     | ❌     | ❌     |


### 🧠 RLS Basics (How security works in this project)

Row Level Security (RLS) is a database-level protection layer provided by PostgreSQL (used by Supabase).
It controls who can read or write rows, independent of application code.

### How we use RLS in this project

🔐 Django is the only trusted backend

🚫 Direct database access from clients is blocked

🧱 RLS acts as a safety net in case someone bypasses the backend

### Important concepts
1️⃣ Django backend bypasses RLS

- Django connects using a privileged database role

- Table owners and service roles ignore RLS

- This is why Django continues to work even when RLS is enabled

2️⃣ Students do NOT talk to Supabase directly

- Students authenticate via Django(which is in service-role or the creater of databse mode so 
  django can see all tables)

- Supabase does not know Django users

- From Supabase’s perspective, students are treated as anonymous(and there's no access for 
  anonymous users as created in our RLS policy....)


### What RLS protects against

- ❌ Direct Supabase REST access

- ❌ Anonymous API abuse

- ❌ Frontend mistakes

- ❌ Future misconfiguration


---------------------------------------------------------------------------


---------------------------------------------------------------------------
 


*********************************
FUTURE Improvements
*********************************

1. createrd by dalna haui kya 
3. admin.site.urls ko env mein daalna

6. add compnent ka button hta diya from inventory.html

7. cateogy k cards jo aate hai usko dynamic karna

8. Agar har lab mein implement karna to kaise setup karenge iska dekho

- [ ] TOdo : add er diagram if possible

- [ ] introduction 


### Tokenising(Prevent URL Exposure)
- use `uuids` to store student id's and component id's etc.
- Instead of giving `<path:>` give a` random token ` value for each category which expires after 
  short time to avoid Guessing by users.



-----
## 🔐 Security Notes

### In settings.py file --- 
- `DEBUG` 
  - intentionally not given a default value.
    It **must** be set explicitly via environment variables.
    This prevents accidental exposure of sensitive debug information in production.

  - What users / attackers actually see when DEBUG = False?

      - A generic 404 or 500 page
    
      - No stack traces
    
      - No settings, paths, SQL, or secrets

  - What (Attackers can see)happens when DEBUG = True (the dangerous part)?

      - Full stack traces
    
      - File paths on your server
    
      - Installed apps
    
      - Environment hints
    
      - Sometimes secret keys via misconfig

- `ADMIN_PATH`
  - The Django admin URL is configurable via 
    and should be set in the environment in production deployments.

  - used a different admin path as admin/ can be gueseed by even a bot

  - `with safety: ` ADMIN_PATH = os.getenv("ADMIN_PATH", "admin/")

- Extra safety cookie settings , Allowed hosts ,  csrf tokens safety also written in `settings.py` 
  file  

🚨**Warning:** Exclude `localhost` from `ALLOWED_HOSTS` in production deployments to maintain 
security.

- ⚡ Session Cookies

  - `SESSION_COOKIE_HTTPONLY = True`  
    - Ensures JavaScript cannot access session cookies, reducing XSS risk.

  - `SESSION_COOKIE_SECURE = config('DEBUG', cast=bool)`  
    - Cookies are sent **only over HTTPS**. Must be enabled in production.

  - `SESSION_COOKIE_SAMESITE = 'Lax'`  
    - Protects against CSRF attacks. `'Strict'` is stricter but may break cross-site functionality.

  - `SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE')`  
     - Defines idle timeout for sessions (default: 30 minutes).

  - `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`  
     - Session expires automatically when the browser closes.



- 🛡️ CSRF Cookies
  - `CSRF_COOKIE_SECURE = config('DEBUG', cast=bool)`  
    - Ensures CSRF cookies are sent only over HTTPS.

  - `CSRF_COOKIE_HTTPONLY = True`  
    - Allows JS to read cookie for AJAX POST requests safely.

  - `CSRF_COOKIE_SAMESITE = 'Lax'`  
    - Helps prevent CSRF attacks via cross-site requests.


- 🌐 HTTPS & Proxy Settings
  - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`  
    - Required when running behind proxies (like Render) to correctly detect HTTPS.

  - `SECURE_SSL_REDIRECT = not DEBUG`  
    - Forces all HTTP requests to redirect to HTTPS in production.


- 🛡️ Security Headers
  - `SECURE_BROWSER_XSS_FILTER = True`  
     - Enables browser XSS filtering.

  - `SECURE_CONTENT_TYPE_NOSNIFF = True`  
    - Prevents MIME type sniffing attacks.

  - `X_FRAME_OPTIONS = 'DENY'`  
    - Prevents clickjacking by disallowing embedding in iframes.

🚨 **Warning:**  
1. SESSION_COOKIE_HTTPONLY should remain True even with AJAX to protect session cookies from XSS.

2. Setting CSRF_COOKIE_HTTPONLY = True prevents JS from accessing the CSRF token, which can break 
AJAX POST requests.

---

- **`whitenoise.middleware.WhiteNoiseMiddleware`**  
  Serves static files efficiently in production without relying on a separate web server.  
  ⚡ Automatically handles caching and compression for CSS, JS, and images.  
  Recommended for deployments on platforms like Heroku or Render where a dedicated static file server is not used.

**Note:** Order of writing the middleware is IMPORTANT(in installed_apps in `settings.py`) .    

---

### 🚀 Features

### 🧱 Dependencies
- ***os***  

  Used to read environment variables and manage environment-specific
  configuration such as secrets and deployment settings.

- ***dj-database-url***  

  Used to parse a database connection string and automatically extract
  credentials such as host, port, username, password, and database name.
  This simplifies database configuration via environment variables,
  especially in production deployments.

- ***pathlib.Path***

  Used for cross-platform filesystem paths, making path handling
  safer and more readable than raw strings.

- ***python-dotenv (`load_dotenv`)***  

  Loads environment variables from a `.env` file at runtime, allowing
  configuration without hardcoding secrets.

- ***python-decouple (`config`)***  

  Reads environment variables or `.env` values in a `type-safe way`.
  `Differenece from dotenv: ` Allows defaults for local development while keeping production secure.
