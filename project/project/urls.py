"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from app.views import ShowLoginPage, doLogin, logout_user

from app import AdminViews
from app.AdminViews import (
    admin_home, 
    add_staff, add_staff_save, add_course, add_course_save, 
    add_student, add_student_save,
    add_subject, add_subject_save,
    manage_staff, manage_student, manage_course, manage_subject,
    edit_staff, edit_staff_save, edit_student, edit_student_save,
)


from app.StaffViews import staff_home
from app import StaffViews

from app.StudentViews import student_home
from app import StudentViews

from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('demo', showDemoPage),
    # path('get_user_details', GetUserDetails),

    path('admin/', admin.site.urls),
    path("accounts/", include('django.contrib.auth.urls')),  # Ensure this is included


    path('', ShowLoginPage, name='show_login'),
    path('show_login/', ShowLoginPage, name='show_login'),

    path('doLogin', doLogin,name="do_login"),
    path('logout_user', logout_user,name="logout"),

    path('admin_profile', AdminViews.admin_profile,name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save,name="admin_profile_save"),
    

    # path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('admin_home/', login_required(AdminViews.admin_home), name='admin_home'),

    path('add_staff',AdminViews.add_staff,name="add_staff"),
    path('add_staff_save',AdminViews.add_staff_save,name="add_staff_save"),
    path('add_course',AdminViews.add_course,name="add_course"),
    path('add_course_save', AdminViews.add_course_save,name="add_course_save"),
    path('add_student',AdminViews.add_student,name="add_student"),
    path('add_student_save', AdminViews.add_student_save,name="add_student_save"),
    path('add_subject',AdminViews.add_subject,name="add_subject"),
    path('add_subject_save', AdminViews.add_subject_save,name="add_subject_save"),

    path('manage_staff',AdminViews.manage_staff,name="manage_staff"),
    path('manage_student',AdminViews.manage_student,name="manage_student"),
    path('manage_course',AdminViews.manage_course,name="manage_course"),
    path('manage_subject',AdminViews.manage_subject,name="manage_subject"),

    path('edit_staff/<str:staff_id>/', AdminViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', AdminViews.edit_staff_save,name="edit_staff_save"),
    path('edit_student/<str:student_id>', AdminViews.edit_student,name="edit_student"),
    path('edit_student_save', AdminViews.edit_student_save,name="edit_student_save"),

    path('delete_staff/<int:staff_id>/', AdminViews.delete_staff, name="delete_staff"),
    path("delete_student/<int:student_id>/", AdminViews.delete_student, name="delete_student"),

    path('manage_session',AdminViews.manage_session,name="manage_session"),
    path('add_session_save',AdminViews.add_session_save,name="add_session_save"),

    # Staff URL Path
    # path('staff_home', StaffViews.staff_home, name="staff_home"),
    # path('student_home', StudentViews.student_home, name="student_home"),
    path('staff_home/', login_required(StaffViews.staff_home), name='staff_home'),
    path('student_home/', login_required(StudentViews.student_home), name='student_home'),


    path('staff_profile', StaffViews.staff_profile,name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save,name="staff_profile_save"),

    path('student_profile', StudentViews.student_profile,name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save,name="student_profile_save"),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

