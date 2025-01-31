from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, Staffs, Courses, Subjects, Students

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Admin)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)