from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from app.models import CustomUser, Students, Subjects
from django.contrib import messages



def student_home(request):
    student_object = Students.objects.get(admin=request.user.id)
    
    total_students = Students.objects.count()
    total_subjects = Subjects.objects.count()

    return render(request,"student_template/student_home_template.html", 
                {"stud_obj": student_object, "total_students": total_students, "total_subjects":total_subjects})



@login_required  # Ensure only logged-in users can access this view
def student_profile(request):
    try:
        # Check if the logged-in user exists in CustomUser
        user = CustomUser.objects.get(id=request.user.id)
        student = Students.objects.get(admin=user)
        return render(request, "student_template/student_profile.html", {"user": user, "student":student})
    except CustomUser.DoesNotExist:
        # Handle the case where the user doesn't exist
        messages.error(request, "User does not exist.")
        return redirect("student_profile")  # Redirect to an appropriate page
    
@login_required
def student_profile_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(redirect("student_profile"))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if password:
                customuser.set_password(password)  # Update the password if provided

            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully!")
            return redirect("student_profile")
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile: User does not exist.")
            return redirect("student_profile")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
            return redirect("student_profile")