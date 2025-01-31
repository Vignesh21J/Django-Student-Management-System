from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from app.models import CustomUser, Staffs, Subjects, Courses, Students
from django.contrib import messages

def staff_home(request):
    total_subjects = Subjects.objects.count()

    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_id_list = []
    for sub in subjects:
        course = Courses.objects.get(id=sub.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    #TO Remove Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()

    return render(request,"staff_template/staff_home_template.html", 
                {"total_subjects":total_subjects, "students_count": students_count})

@login_required  # Ensure only logged-in users can access this view
def staff_profile(request):
    try:
        # Check if the logged-in user exists in CustomUser
        user = CustomUser.objects.get(id=request.user.id)
        staff = Staffs.objects.get(admin=user)
        return render(request, "staff_template/staff_profile.html", {"user": user, "staff":staff})
    except CustomUser.DoesNotExist:
        # Handle the case where the user doesn't exist
        messages.error(request, "User does not exist.")
        return redirect("staff_profile")  # Redirect to an appropriate page
    
@login_required
def staff_profile_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(redirect("staff_profile"))
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

            staff = Staffs.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully!")
            return redirect("staff_profile")
        except CustomUser.DoesNotExist:
            messages.error(request, "Failed to Update Profile: User does not exist.")
            return redirect("staff_profile")
        except Exception as e:
            messages.error(request, f"Failed to Update Profile: {str(e)}")
            return redirect("staff_profile")