# ===============================
# Standard Library
# ===============================
from datetime import datetime, timedelta, date
from collections import defaultdict


# ===============================
# Django Core
# ===============================
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, QueryDict
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.cache import cache


# ===============================
# Django Authentication & Messages
# ===============================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages


# ===============================
# Third-Party Libraries
# ===============================
from rest_framework import generics


# ===============================
# Local
# ===============================
from .decorators import student_login_required, admin_login_required
from .models import Student, StudentIssueLog, ComponentCategory, Component, Branches,AvailableProjects,ProjectEnrolledStudents,Faculty


# ===============================
# Api
# ===============================
from .serializers import StudentIssueLogSerializer
from rest_framework import generics, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.pagination import PageNumberPagination


#=======================================================================
# GLOBAL CACHE:: RARELY CHANGES
#======================================================================
def get_all_available_projects():
    cache_key = "cached_all_available_projects"
    all_projects = cache.get(cache_key)

    if all_projects is None:
        all_projects = list(
            AvailableProjects.objects.select_related(
                'avail_proj_faculty_associated'
            )
        )
        # Cache indefinitely
        cache.set(cache_key, all_projects, timeout=None)
        # print("All available projects cached -> 1 DB hit")
    else:
        # print("Retrieved all available projects from cache -> no DB hit")
        pass

    return all_projects



def get_all_branches():
    cache_key = "cached_all_branches"
    branches = cache.get(cache_key)

    if branches is None:
        branches = list(Branches.objects.all())
        cache.set(cache_key, branches, None)

    return branches



def get_all_categories():
    cache_key = "cached_all_categories"
    categories = cache.get(cache_key)

    if categories is None:
        categories = list(ComponentCategory.objects.all())
        cache.set(cache_key,categories,None)

    return categories



def get_all_faculty():
    cache_key = "cached_all_faculty"
    faculty = cache.get(cache_key)

    if faculty is None:
        faculty = list(Faculty.objects.select_related("faculty_dept"))
        cache.set(cache_key, faculty, None)

    return faculty




#=======================================================================
# Cache all enrolled projects for a student ::: Until new enrollment  `
#======================================================================
def cached_student_projects(student):
    cache_key = f"cached_student_{student.std_first_name}_projects"
    projects = cache.get(cache_key)

    # use this to check....... PYTHON SHELL NOT WORKS AS LOCALMEMCACHE IS NOT SHARED ON DJANGO .... it is ONLY FOR BROWSER
    # print("retrieved from cache ==>> no db hit")

    if projects is None:

        projects = list(ProjectEnrolledStudents.objects.filter(
                        proj_enroll_student_id=student.std_id
                    ).select_related(
                        'proj_enroll_project',
                        'proj_enroll_project__avail_proj_faculty_associated'
                    ))
        # None for long-term
        # 15 days currently
        cache.set(cache_key, projects, timeout=1296000)
        # print(f"set cache for {student.std_id}==>> 1 db hit ")
    return projects




#=======================================================================
# Order of functions :::  Same as name tags `urls.py`
#======================================================================
def home(request):
    return render(request,'final/home.html')



def user_login(request):
    # ====== LOGIN  ======
    if request.method == 'POST'and request.POST.get("form_type") == "user_login":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if username.endswith("admin"):
                admin_user = authenticate(request,username=username,password=password)

                if admin_user and admin_user.is_staff:
                    login(request, admin_user)
                    return redirect('final:admin_dashboard')
            try:
                student = Student.objects.get(std_roll_number=username.upper())

            except Student.DoesNotExist:
                # put the page name in extra_tags to show message only in that page
                messages.error(request, "Invalid email or password",extra_tags='login_error')
                return render(request, 'final/login.html')

            if check_password(password, student.std_password):
                request.session['student_id'] = student.std_id          # custom session
                request.session["student_name"] = student.std_full_name
                return redirect('final:student_dashboard')

            messages.error(request, "Invalid email or password.",extra_tags='login_error')

    # ====== Signup  ======
    if request.method == 'POST' and request.POST.get("form_type") == "user_signup":
        first_name = request.POST.get("first_name").strip().lower()
        last_name = request.POST.get("last_name").strip().lower()
        roll_number = request.POST.get("roll_number").upper()
        email = request.POST.get("college_email")[:7].lower()
        password = request.POST.get("password")
        phone_number=request.POST.get("phone_number")

        branch = roll_number[5:7]
        std_year = request.POST.get("std_year")

        # ==== basic validation ====
        if Student.objects.filter(std_roll_number=roll_number).exists():
            messages.error(request, "Roll number already exists",extra_tags='login_error')
            return render(request, "final/login.html")

        if Student.objects.filter(std_college_email=email).exists():
            messages.error(request, "Email already registered",extra_tags='login_error')
            return render(request, "final/login.html")

        std_branch = get_object_or_404(Branches,branches_rollno_code=branch)

        try:
            Student.objects.create(
                std_first_name=first_name,
                std_last_name=last_name,
                std_roll_number=roll_number,
                std_college_email=email,
                std_password=make_password(password),
                std_phone_number=phone_number,
                std_branch=std_branch,
                std_year = std_year
            )

        except ValidationError as e:
            messages.error(request, "Cannot create user. Enter a valid roll number.", extra_tags='signup_error')
            return render(request, "final/login.html")

        except IntegrityError:
            messages.error(request, "data violates constraints.",extra_tags='signup_error')
            return render(request, "final/login.html")


        messages.success(request, "Registration successful. Please login.",extra_tags='login_success')
        return redirect("final:login")

    # ==== load initial login page ====
    return render(request, 'final/login.html')



@student_login_required
def student_dashboard(request):
    student = request.student

    # cached enrolled projects until student enrolls in a new one ...... SAVES A LOT OF DB HITS
    enrolled_projects = cached_student_projects(student)

    return render(request,"final/student/student_dashboard.html",
                  {"student": student,
                   "enrolled_projects":enrolled_projects})



# === NOT used decorators here broken session unlogged user can also access this  button ===
@require_POST
def student_logout(request):
    request.session.flush()
    return redirect('final:login')



# ==== THIS is Django based logout ========
@require_POST
def admin_logout(request):
    logout(request)
    return redirect("final:login")



@student_login_required
def enroll_in_projects(request):
    projects = get_all_available_projects()

    if request.method == 'POST':
        project_id = request.POST.get("project_id")

        if not project_id:
            messages.error(request, "Invalid project selection.",extra_tags="enroll_error")
            return redirect('final:student_dashboard')

        student = request.student
        project_obj = get_object_or_404(AvailableProjects, id=project_id)

        # prevent duplicate enrollment
        already_enrolled = ProjectEnrolledStudents.objects.filter(
            proj_enroll_project=project_obj,
            proj_enroll_student=student
        ).exists()

        if already_enrolled:
            messages.warning(request,"You are already enrolled in this project.",
                extra_tags="enroll_error"
            )
            return redirect('final:enroll_in_projects')

        ProjectEnrolledStudents.objects.create(
            proj_enroll_project=project_obj,
            proj_enroll_student=student
        )

        # ------ Invalidate cache for this student ---------
        cache.delete(f"cached_student_{student.std_first_name}_projects")


        messages.success(request,"Enrollment successful!",extra_tags="enroll_success")
        return redirect('final:student_dashboard')

    return render(request,"final/student/enroll_in_projects.html",
        {"projects": projects}
    )



@student_login_required
def issued_items(request):
    if not request.GET:
        # print("no  db hit direct load ")
        return render(request,"final/student/issued_items.html")

    # print("db hit happens")
    student_id = request.session.get('student_id')
    issue_status = request.GET.get("issue_status")  # current / returned / None
    date_range = request.GET.get("date_range")  # 7d / 1m / 3m / all
    selected_categories = request.GET.getlist("category")
    project_id = request.GET.get("project_id")    #from student dashboard


    qs = (
        StudentIssueLog.objects
        .filter(student_id=student_id)
        .select_related("component", "project")
    )

    if project_id:
        qs = qs.filter(project=project_id)

    if issue_status == "current":
        qs = qs.filter(std_issue_return_date__isnull=True)

    elif issue_status == "returned":
        qs = qs.filter(std_issue_return_date__isnull=False)


    if selected_categories:
        qs = qs.filter(
            component__comp_category__comp_cate_category_name__in=selected_categories
        )


    today = now().date()

    if date_range == "7":
        qs = qs.filter(std_issue_issue_date__gte=today - timedelta(days=7))

    elif date_range == "15":
        qs = qs.filter(std_issue_issue_date__gte=today - timedelta(days=15))

    elif date_range == "30":
        qs = qs.filter(std_issue_issue_date__gte=today - timedelta(days=30))


    elif date_range == "90":
        qs = qs.filter(std_issue_issue_date__gte=today - timedelta(days=90))

    # "all" → no filter applied (intentionally)

    return render(
        request,
        "final/student/issued_items.html",
        {
            "issued_items": qs,
            "issue_status": issue_status,
            "date_range": date_range,
            "selected_categories": selected_categories,
        }
    )



@student_login_required
def request_components(request):
    student = request.student
    enrolled_projects = cached_student_projects(student)

    return render(request,
                  'final/student/request_components.html',
                  {"enrolled_projects":enrolled_projects})



@student_login_required
def category_items(request ,slug):
    category = get_object_or_404(
        ComponentCategory,
        comp_cate_category_name=slug
    )

    components = (
                Component.objects
                  .select_related('comp_category')
                  .filter(comp_category=category)
                  .order_by("-comp_popularity")
                  )

    student = request.student
    enrolled_projects = cached_student_projects(student)

    paginator = Paginator(components, 15)  # 15 per page
    page_number = request.GET.get("page", 1)

    # now this statement hits db before it was a lazy query
    page_obj = paginator.get_page(page_number)

    return render(request, 'final/student/category_items.html', {
        # 'components': components,    #no need to send after pagination
        'category_name': category.comp_cate_category_name,
        "enrolled_projects": enrolled_projects,
        "page_obj":page_obj
    })


# 7.c.  submit request from right sidebar
@student_login_required
def submit_request(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    component_ids = request.POST.getlist('component_ids[]')
    quantities = request.POST.getlist('quantities[]')
    project_id= request.POST.get("project_id")
    # print(request.POST)

    #get the project object --  direct id is not inserted
    project = get_object_or_404(AvailableProjects,id=project_id)
    # print(component_ids,quantities)

    if not component_ids or not quantities:
        messages.error(request, "No components selected",extra_tags='error_requestcomp')
        return redirect('final:request_components')

    if len(component_ids) != len(quantities):
        return HttpResponseBadRequest("Mismatched data")


    student = request.student
    # print(type(student))
    # print(student.std_full_name,student.std_roll_number)

    # ---- FETCH ALL COMPONENTS IN ONE QUERY (FAST) ----
    # old one was giving multiple requset to database
    components_map = Component.objects.in_bulk(component_ids)

    issue_logs = []

    for comp_id, qty in zip(component_ids, quantities):
        component = components_map.get(int(comp_id))
        if not component:
            continue

        try:
            qty = int(qty)
            if qty <= 0:
                continue
        except ValueError:
            continue

        issue_logs.append(
            StudentIssueLog(
                student=student,
                component=component,
                project=project,
                std_issue_quantity_issued=qty,
                std_issue_form_date=datetime.now().date()
            )
        )

    if not issue_logs:
        messages.error(request, "Invalid component selection",extra_tags='error_requestcomp')
        return redirect('final:request_components')

    # ---- ATOMIC SAVE (SAFE) ----
    with transaction.atomic():
        StudentIssueLog.objects.bulk_create(issue_logs)

    messages.success(request, "Request submitted successfully",extra_tags='success_requestcomp')

    response = redirect('final:request_components')
    response.set_cookie('clearLocalStorage', 'true')  # frontend signal
    return response



#=== note: Default dict is not loaded in html so convert it in dictionary ONLY  ===
@admin_login_required
def admin_dashboard(request):
    # FOR new Entry ==>>  both issue_Date, return_date null
    requests_qs = (
        StudentIssueLog.objects
        .filter(std_issue_issue_date__isnull=True,
                std_issue_return_date__isnull=True)
        .values(
             'student__std_roll_number',
            'component__comp_name',
            'component__comp_category__comp_cate_category_name',
            'std_issue_form_date',
            'component__comp_quantity_available',
            'std_issue_quantity_issued'
        )
        .order_by('component__comp_category__comp_cate_category_name', '-std_issue_form_date')
    )

    grouped_requests = defaultdict(list)
    for r in requests_qs:
        grouped_requests[r['component__comp_category__comp_cate_category_name']].append(r)
    # print(grouped_requests)
    return render(
        request,
        'final/teacher/admin_dashboard.html',
        {'grouped_requests': dict(grouped_requests)}
    )



@admin_login_required
def add_new_project(request):

#note:::  _id in the second statement is used as field name otherwise it needs to be a faculty instance
#  and we don;t want any db hits
    if request.method == "POST":
        action = request.POST.get("action")
        #  EDIT EXISTING PROJECT
        if action == "edit":
            project_id = request.POST.get("project_id")

            project = get_object_or_404(AvailableProjects, id=project_id)
            project.avail_proj_project_name = request.POST.get("project_name")
            project.avail_proj_faculty_associated_id = request.POST.get("faculty")
            project.save()

        #  ADD NEW PROJECT
        else:
            AvailableProjects.objects.create(
                avail_proj_project_name=request.POST.get("project_name"),
                avail_proj_faculty_associated_id=request.POST.get("faculty"),
            )



        # only invalidate cache
        cache.delete("cached_all_available_projects")

        return redirect("final:add_new_project")

#from cache
    projects = get_all_available_projects()
    faculties = get_all_faculty()

    return render(
        request,
        "final/teacher/add_new_project.html",
        {"projects": projects,
         "faculties":faculties}
    )



@admin_login_required
def add_new_faculty(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "edit":
            faculty_id = request.POST.get("faculty_id")
            faculty_name = request.POST.get("faculty_name")
            branch_id = request.POST.get("branch")

            Faculty.objects.filter(id=faculty_id).update(
                faculty_name=faculty_name,
                faculty_dept_id=branch_id
            )

        else:
            faculty_name = request.POST.get("faculty_name")
            branch_id = request.POST.get("branch")

            Faculty.objects.create(
                faculty_name=faculty_name,
                faculty_dept_id=branch_id
            )

        # invalidate cache
        cache.delete("cached_all_faculty")

        return redirect("final:add_new_faculty")



    faculties = get_all_faculty()
    branches = get_all_branches()
    return  render(request,"final/teacher/add_new_faculty.html",
                   {"faculties":faculties,
                    "branches":branches})




@admin_login_required
def activity(request):
    now = datetime.now()

    # quick range
    quick_range = request.GET.get("quick_range", "today")

    # optional custom range
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")

    print(from_date,to_date,quick_range)
    issues = StudentIssueLog.objects.select_related(
        "component", "student", "project"
    ).order_by("-std_issue_issue_date")

    #jo __str__ mein likha vo print hoga
    # print(issues)

    # -------- DATE FILTER --------
    today = date.today()

    if from_date and to_date:
        start_dt = date.fromisoformat(from_date)
        end_dt = date.fromisoformat(to_date)

        issues = issues.filter(
            std_issue_form_date__range=(start_dt, end_dt)
        )

    else:
        if quick_range == "today":
            issues = issues.filter(
                std_issue_issue_date=today
            )

        elif quick_range == "3":
            issues = issues.filter(
                std_issue_issue_date__gte=today - timedelta(days=3)
            )

        elif quick_range == "7":
            issues = issues.filter(
                std_issue_issue_date__gte=today - timedelta(days=7)
            )
    #
    print(issues)
    # paginator = Paginator(issues,15)  # 15 students per page
    # page_number = request.GET.get("page",1)
    # page_obj = paginator.get_page(page_number)
    #
    # # ✅ BUILD FILTER-SAFE QUERY STRING (NO PAGE)
    # querydict = request.GET.copy()
    # querydict.pop("page", None)


    context = {
        # "page_obj": page_obj,
        "issues":issues,
        "days": quick_range,
        "from_date": from_date,
        "to_date": to_date,
        # "querystring": querydict.urlencode(),
    }
    # print(page_obj)
    return render(request,'final/teacher/activity.html',context)



@admin_login_required
def approved(request):
    # jo iisued entry hai uski return_date null hogi
    requests_approved = (StudentIssueLog.objects
                         .select_related("student", "component",
                                        "component__comp_category")
                         .filter(std_issue_issue_date__isnull=False,
                                 std_issue_return_date__isnull=True)
                         .values(
         'student__std_roll_number', 'std_issue_issue_date', 'component__comp_name',
        'component__comp_category__comp_cate_category_name', 'component__comp_quantity_available',
        'std_issue_quantity_issued').order_by('component__comp_category__comp_cate_category_name', '-std_issue_form_date'))

    # Step 2: Group by category
    grouped_requests = defaultdict(list)

    for req in requests_approved:
        grouped_requests[req['component__comp_category__comp_cate_category_name']].append(req)

    # print(grouped_requests.items())

    return render(request, 'final/teacher/approved.html', {
        'grouped_requests': dict(grouped_requests)})



@admin_login_required
def inventory(request):
    categories = get_all_categories()
    return render(request,"final/teacher/inventory.html",{"categories":categories})



@require_POST
@admin_login_required
def add_component(request):
    #default mein empty string diya nahi to strip() dikkat akrta if None
        new_component = request.POST.get("component_name","").strip()
        new_category = request.POST.get("component_category")

        try:
            new_quantity = int(request.POST.get("component_qty"))
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity")
            return redirect("final:inventory")

#we can add this in databse constraints also but ye abhi exact match wala hi dekhega also
    # ignoring lower or uppercase
        # 🔍 DUPLICATE CHECK
        if Component.objects.filter(
            comp_name__iexact=new_component,
            comp_category=new_category
        ).exists():
            messages.warning(
                request,
                f"Component '{new_component}' already exists ."
            )
            return redirect("final:inventory")

        try:
            category = ComponentCategory.objects.get(comp_cate_category_name=new_category)
        except ComponentCategory.DoesNotExist:
            messages.error(request, "Category not found")
            return redirect("final:inventory")


        try:
            Component.objects.create(
                comp_name=new_component,
                comp_qunatity_available=new_quantity,
                comp_category=category
            )
            messages.success(
                request,
                f"Component '{new_component}' added in category {category}."
            )
        except Exception:
            messages.error(request, f"Failed to add component {new_component}")

        return  redirect('final:inventory')



@admin_login_required
def inventory_items(request, slug):
    category = get_object_or_404(
        ComponentCategory,
        comp_cate_category_name=slug
    )
    categories = ComponentCategory.objects.all()
    components = Component.objects.select_related('comp_category').filter(
        comp_category=category
    )

# for editing components ::
    if request.method == 'POST':
        component_id = request.POST.get("component_id")
        action = request.POST.get("action")
        change_category = get_object_or_404(ComponentCategory,id=request.POST.get("category_id"))
        component = get_object_or_404(Component, id=component_id)

        if action == "save":
            component.comp_name = request.POST.get("comp_name")
            component.comp_quantity_available =  request.POST.get("comp_quantity")
            component.comp_category = change_category
            component.save()

        elif action=="delete":
            # Soft delete 0 == deleted  1== working
            component.comp_status = 0
            component.save(update_fields=['comp_status'])

            # ye sab messages login form par dikh rhe hai inhe sahi karo
            messages.success(request, f"{component.comp_name} marked as deleted.")


    return render(request, 'final/teacher/inventory_items.html', {
        'components': components,
        'categories':categories,
        'category_name': category.comp_cate_category_name,
    })



@require_POST
@admin_login_required
def update_status(request):
    roll_number = request.POST.get("roll_number")
    form_date = request.POST.get("form_date")
    issue_date = request.POST.get("issue_date")
    component_name = request.POST.get("component_name")
    status_to_update = request.POST.get("status_to_update")
    # print("data is:", form_date, action, component_name, roll_number)


    if status_to_update in ("approve","reject"):
        logs = StudentIssueLog.objects.select_related("component", "student").filter(
            student__std_roll_number=roll_number,
            component__comp_name=component_name,
            std_issue_form_date=form_date
        )


    elif status_to_update == "return":
        logs = StudentIssueLog.objects.select_related("component", "student").filter(
            student__std_roll_number=roll_number,
            component__comp_name=component_name,
            std_issue_issue_date = issue_date,
            std_issue_return_date__isnull=True
        )

    else: return HttpResponse("Invalid action", status=400)

    if not logs.exists():
        return HttpResponse("Log not found", status=404)

    with transaction.atomic():
        if status_to_update == "reject":
            # Delete all matching logs
            deleted_count, _ = logs.delete()

            if deleted_count > 0:
                messages.success(request, "Log deleted successfully.")
            else:
                messages.error(request, "No matching log found.")

        else:
            for log in logs:
                component = Component.objects.select_for_update().get(
                    id=log.component_id
                )

                if status_to_update == "approve":
                    if component.comp_quantity_available < log.std_issue_quantity_issued:
                        return HttpResponse(
                            f"Not enough quantity available for {component.name}",
                            status=400
                        )

                    # Update log
                    log.std_issue_issue_date = now().date()

                    # Deduct stock
                    component.comp_quantity_available -= log.std_issue_quantity_issued

                    # increaase populraity by one
                    component.comp_popularity+=1
                    component.save()
                    log.save()

                elif status_to_update == "return":
                    log.std_issue_return_date = now().date()

                    component.comp_quantity_available += log.std_issue_quantity_issued
                    component.save()

                    log.save()
                    return redirect('final:approved')

    return redirect('final:admin_dashboard')



@admin_login_required
def all_students(request):
    # NOTE: 1. ye get request se aara
    #       2. getlist use karre as multiple aare


    selected_branches = request.GET.getlist("branch")
    selected_years = request.GET.getlist("year")
    selected_active = request.GET.getlist("active")

    name_query = request.GET.get("name", "").strip().lower()
    name_mode = request.GET.get("name_mode", "startswith")

    # ***NOTE *** : Direct hit nahi karta db ko ye LAZYQUERY BANARHA HAI
    students = Student.objects.all()

    # REQUIRED filters
    students = students.filter(
        std_branch__branches_branch_code__in=selected_branches,
        std_year__in=selected_years
    )

    # Active / inactive
    if set(selected_active) == {"1"}:
        students = students.filter(std_deactivated_at__isnull=True)
    elif set(selected_active) == {"0"}:
        students = students.filter(std_deactivated_at__isnull=False)

    # Optional name filter
    if name_query:
        if name_mode == "startswith":
            students = students.filter(std_full_name__istartswith=name_query)
        else:
            students = students.filter(std_full_name__icontains=name_query)

    # 🔥 PAGINATION (DB hit happens here, with LIMIT/OFFSET)
    paginator = Paginator(students,15)  # 15 students per page
    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    # ✅ BUILD FILTER-SAFE QUERY STRING (NO PAGE)
    querydict = request.GET.copy()
    querydict.pop("page", None)


    return render(request, "final/teacher/all_students.html", {
        "page_obj": page_obj,
        "branches_list":Branches.objects.all(),
    # send these back to template to retain filters
    "selected_branches": selected_branches,
    "selected_years": selected_years,
    "selected_active": selected_active,
    "name_query": name_query,
    "name_mode": name_mode,
        "querystring": querydict.urlencode(),
    'remove_filter':remove_filter
    })



@admin_login_required
def student_details(request,id):
    student = get_object_or_404(
        Student,
        std_id=id
    )

    issued_components = (
        StudentIssueLog.objects
        .select_related("component",'student')
        .filter(student_id=student.std_id)
        .order_by("-std_issue_issue_date")
    )

    return render(request, "final/teacher/student_details.html", {
        "student": student,
        "issued_components": issued_components
    })





#=======================================================================
# Extra Logic
#======================================================================
@admin_login_required
def remove_filter(request, key, value=None):
    q = request.GET.copy()
    if value:
        values = q.getlist(key)
        values.remove(value)
        q.setlist(key, values)
    else:
        q.pop(key, None)
    q.pop("page", None)
    return q.urlencode()



# ================================================
# API FUNCTIONS
# ================================================
class AdminIssuePagination(PageNumberPagination):
    page_size = 100          # Items per page
    page_size_query_param = None  # Not allow client to set page size
    max_page_size = 100     # Maximum allowed for safety


class StudentIssueLogAPI(generics.ListAPIView):
    queryset = StudentIssueLog.objects.select_related("student", "project","component").all()

    serializer_class = StudentIssueLogSerializer
    permission_classes = [permissions.IsAdminUser]          # Only admins
    pagination_class = AdminIssuePagination
    renderer_classes = [JSONRenderer]                       # Force JSON only

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request

        # ------------------- Basic filters -------------------
        category = request.GET.get("category")
        if category:
            qs = qs.filter(component__comp_category__comp_cate_category_name__icontains=category)

        branch = request.GET.get("branch")
        if branch:
            qs = qs.filter(student__std_branch__branches_branch_code__icontains=branch)

        year = request.GET.get("year")
        if year:
            qs = qs.filter(student__std_year=year)


        # ------------------- Date filters -------------------
        form_date_from = request.GET.get("form_date_from")
        form_date_to = request.GET.get("form_date_to")
        if form_date_from:
            qs = qs.filter(std_issue_issue_date__gte=form_date_from)
        if form_date_to:
            qs = qs.filter(std_issue_issue_date__lte=form_date_to)

        # Issue date range
        issue_date_from = request.GET.get("issue_date_from")
        issue_date_to = request.GET.get("issue_date_to")
        if issue_date_from:
            qs = qs.filter(std_issue_issue_date__gte=issue_date_from)
        if issue_date_to:
            qs = qs.filter(std_issue_issue_date__lte=issue_date_to)

        # Return date range
        return_date_from = request.GET.get("return_date_from")
        return_date_to = request.GET.get("return_date_to")
        if return_date_from:
            qs = qs.filter(std_issue_return_date__gte=return_date_from)
        if return_date_to:
            qs = qs.filter(std_issue_return_date__lte=return_date_to)

        # ------------------- Ordering -------------------
        ordering = request.GET.get("ordering", "-std_issue_form_date")
        qs = qs.order_by(ordering)

        return qs