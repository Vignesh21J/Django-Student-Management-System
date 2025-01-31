from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import AddStudentForm, EditStudentForm
from app.models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required


# from app.forms import AddStudentForm, EditStudentForm
# from app.models import CustomUser, Staffs, Courses, Subjects, Students


def admin_home(request):

    student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    context = {
        "student_count":student_count,
        "staff_count":staff_count,
        "subject_count":subject_count,
        "course_count":course_count,
    }

    return render(request,"admin_template/home_content.html", context)

def add_staff(request):
    return render(request,"admin_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                last_name=last_name,
                first_name=first_name,
                user_type=2
            )
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return redirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return redirect(reverse("add_staff"))

def add_course(request):
    return render(request,"admin_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return redirect(reverse("add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return redirect(reverse("add_course"))

def add_student(request):
    courses = Courses.objects.all()
    form = AddStudentForm()
    return render(request, "admin_template/add_student_template.html", {"courses":courses,"form": form})

def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
        
            session_year_id=form.cleaned_data["session_year_id"]

            course_id=form.cleaned_data["course"]
            sex=form.cleaned_data["sex"]

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name,profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    last_name=last_name,
                    first_name=first_name,
                    user_type=3
                )
                user.students.address = address

                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj

                session_year=SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year

                user.students.profile_pic = profile_pic_url
                user.students.gender = sex
                user.save()

                messages.success(request, "Successfully Added Student")
                return redirect(reverse("add_student"))
            except Exception as e:
                messages.error(request, f"Failed to Add Student: {e}")
                return redirect(reverse("add_student"))
        else:
            form=AddStudentForm(request.POST)
            return render(request, "admin_template/add_student_template.html", {"form": form})


def add_subject(request):
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"admin_template/add_subject_template.html",{"staffs":staffs,"courses":courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff) #DB la irukura same name here also in lefthandside
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return redirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return redirect(reverse("add_subject"))


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"admin_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"admin_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses=Courses.objects.all()
    return render(request,"admin_template/manage_course_template.html",{"courses":courses})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"admin_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    # return HttpResponse(f"Staff ID: {staff_id}")

    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"admin_template/edit_staff_template.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return redirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    # courses = Courses.objects.all()

    request.session['student_id']=student_id
    student = Students.objects.get(admin = student_id)
    form = EditStudentForm()
    
    form.fields['email'].initial=student.admin.email
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['address'].initial=student.address
    form.fields['course'].initial=student.course_id.id
    form.fields['sex'].initial=student.gender
    form.fields['session_year_id'].initial=student.session_year_id.id

    return render(request, "admin_template/edit_student_template.html", {"form":form, "id" : student_id, "username":student.admin.username})


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id = request.session.get("student_id")
        if student_id==None:
            return redirect(reverse("manage_student"))

        form=EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            course_id = form.cleaned_data["course"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                student=Students.objects.get(admin=student_id)
                student.address=address
    
                session_year=SessionYearModel.objects.get(id=session_year_id)
                student.session_year_id = session_year

                student.gender=sex
                course=Courses.objects.get(id=course_id)
                student.course_id=course
                if profile_pic_url!=None:
                    student.profile_pic=profile_pic_url
                student.save()

                del request.session['student_id']

                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except:
                messages.error(request,"Failed to Edit Student")
                return redirect(reverse("edit_student",kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"admin_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})
        

def delete_staff(request, staff_id):
    try:
        user = CustomUser.objects.get(id=staff_id)
        
        if user.user_type != "2":
            messages.error(request, "The selected user is not a staff member.")
            return redirect(reverse("manage_staff"))

        # Delete the user (this will also delete the related Staffs record)
        user.delete()
        return redirect(reverse("manage_staff"))
    except CustomUser.DoesNotExist:
        return redirect(reverse("manage_staff"))
    except Exception as e:
        return redirect(reverse("manage_staff"))
    

def delete_student(request, student_id):
    try:
        student = get_object_or_404(Students, admin=student_id)
        user = student.admin 
        
        student.delete()
        user.delete()

        return redirect("manage_student")
    except Exception as e:
        return redirect("manage_student")


def manage_session(request):
    return render(request, "admin_template/manage_session_template.html")

def add_session_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_course')
    else:
        session_start_year = request.POST.get('session_start')
        session_end_year = request.POST.get('session_end')

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Year added Successfully!")
            return redirect("manage_session")
        except:
            messages.error(request, "Failed to Add Session Year")
            return redirect("manage_session")
        

# def admin_profile(request):
#     user = CustomUser.objects.get(id=request.user.id)
#     return render(request, "admin_template/admin_profile.html", {"user":user})

@login_required  # Ensure only logged-in users can access this view
def admin_profile(request):
    try:
        # Check if the logged-in user exists in CustomUser
        user = CustomUser.objects.get(id=request.user.id)
        return render(request, "admin_template/admin_profile.html", {"user": user})
    except CustomUser.DoesNotExist:
        # Handle the case where the user doesn't exist
        messages.error(request, "User does not exist.")
        return redirect("admin_profile")  # Redirect to an appropriate page

# def admin_profile_save(request):
#     if request.method != 'POST':
#        return HttpResponseRedirect(redirect("admin_profile"))
#     else:
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         password = request.POST.get('password')
#         try:
#             customuser = CustomUser.objects.get(id=request.user.id)
#             customuser.first_name = first_name
#             customuser.last_name = last_name

#             if password != None and password != '':
#                 customuser.set_password(password)

#             customuser.save()
#             messages.success(request, "Profile Updated Successfully!")
#             return redirect("admin_profile")
#         except:
#             messages.error(request, "Failed to Update Profile")
#             return redirect("admin_profile")

@login_required
def admin_profile_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(redirect("admin_profile"))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if password:
                customuser.set_password(password)  # Update the password if provided

            customuser.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect("admin_profile")
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile: User does not exist.")
            return redirect("admin_profile")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
            return redirect("admin_profile")