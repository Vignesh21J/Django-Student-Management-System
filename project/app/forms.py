from django import forms
from app.models import Courses
from app.models import SessionYearModel


from django.forms import DateInput

class DateInput(forms.DateInput):
    input_type = "date"

class AddStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50, widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))

    course_list=[]
    try:
        courses=Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]


    session_list=[]
    # try:
    sessions = SessionYearModel.objects.all()

    for ses in sessions:
        small_ses = (ses.id, str(ses.session_start_year)+"   TO   "+str(ses.session_end_year))
        session_list.append(small_ses)
    # except:
    # session_list=[]


    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    course=forms.ChoiceField(label="Course",choices=course_list, widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year", widget=forms.Select(attrs={"class":"form-control"}), choices=session_list)
    profile_pic=forms.FileField(label="Profile Pic",max_length=50, widget=forms.FileInput(attrs={"class":"form-control"}))


class EditStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    course_list=[]
    try:
        courses=Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]

    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )



    # session_list=[]
    # try:
    #     sessions = SessionYearModel.objects.all()

    #     for ses in sessions:
    #         small_ses = (ses.id,ses.session_start_year+"-"+ses.session_end_year)
    #         session_list.append(small_ses)
    # except:
    #     #session_list=[]

    session_list=[]
    # try:
    sessions = SessionYearModel.objects.all()

    for ses in sessions:
        small_ses = (ses.id, str(ses.session_start_year)+"   TO   "+str(ses.session_end_year))
        session_list.append(small_ses)
    # except:
    # session_list=[]

    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Sex",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Year",widget=forms.Select(attrs={"class":"form-control"}), choices=session_list)
    
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)