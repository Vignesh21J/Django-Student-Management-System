from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(choices=user_type_data, max_length=20, default=1)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False, default=None)  # Default added
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # This is the default manager, allows to perform DB queries and access objects in our database using Django's ORM


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, default=None)  # Default added
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # To Return Current Object Data


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # To Return Current Object Data


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)

    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()  # To Return Current Object Data


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



@receiver(post_save,sender=CustomUser)  #This method will run only when data added in CustomUser
# Now Creating a Function which will automatically insert data in HOD, Staff or Student

def create_user_profile(sender,instance,created,**kwargs):   # Creating Func which add Data into Admin, Staff, Student Table..
# Here Parameters like "Sender" is Class which Calls this method,. "Instance" is Current Inserted Data Model., "Created" is True/False, true when data inserted.,

    if created: 
        if instance.user_type==1:
            Admin.objects.create(admin=instance)   # Here instance is CustomUser..
        if instance.user_type==2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type==3:
            Students.objects.create(
                admin=instance,
                course_id=Courses.objects.get(id=1),

                # session_start_year="2020-01-01",
                # session_end_year="2029-01-01",
                session_year_id = SessionYearModel.objects.get(id=1) ,
                address="",
                profile_pic="",gender=""
            )


#Below Method will Call after "create_user_profile" Execution..,
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.admin.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()
