# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin

# class LoginCheckMiddleWare(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Get the logged-in user
#         user = request.user

#         # Define URLs that are publicly accessible (even without login)
#         allowed_urls = [
#             reverse("show_login"),  # Login page
#             reverse("do_login"),   # Login action
#             reverse("logout"),     # Logout action
#             "/admin",              # Default Django admin page
#         ]

#         # Avoid redirect loops by checking if the requested path is already in `allowed_urls`
#         if request.path in allowed_urls or request.path.startswith("/admin"):
#             return None

#         # If the user is NOT authenticated
#         if not user.is_authenticated:
#             # Redirect to login page if accessing a restricted page
#             return HttpResponseRedirect(reverse("show_login"))

#         # If the user IS authenticated, enforce user_type-specific access
#         elif user.is_authenticated:
#             if user.user_type == "1":  # Admin
#                 if view_func.__module__ in ["app.AdminViews", "app.views"]:
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse("admin_home"))
#             elif user.user_type == "2":  # Staff
#                 if view_func.__module__ in ["app.StaffViews", "app.views"]:
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse("staff_home"))
#             elif user.user_type == "3":  # Student
#                 if view_func.__module__ in ["app.StudentViews", "app.views"]:
#                     return None
#                 else:
#                     return HttpResponseRedirect(reverse("student_home"))

#         # If none of the above conditions are met, redirect to the login page
#         return HttpResponseRedirect(reverse("show_login"))


from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# Child of MiddlewareMixin
class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)

        user = request.user  # Get the logged-in user

        # Define publicly accessible URLs
        allowed_urls = [
            reverse("show_login"),  # Login page
            reverse("do_login"),    # Login action
            reverse("logout"),      # Logout action
            "/admin",               # Default Django admin page
        ]

        # Allow access to allowed URLs and admin URLs
        if request.path in allowed_urls or request.path.startswith("/admin"):
            return None

        # Allow access to static files (e.g., images)
        if modulename == "django.views.static":
            return None
        
        # Allow access to reset password views
        if modulename == "django.contrib.auth.views":
            return None

        # Redirect unauthenticated users to login page
        if not user.is_authenticated:
            return HttpResponseRedirect(reverse("show_login"))

        # Handle access based on user type
        if user.is_authenticated:
            if user.user_type == "1":  # Admin
                 # Allow access only to admin views, static files, or reset password views
                if modulename in ["app.AdminViews", "app.views", "django.views.static", "django.contrib.auth.views"]:
                    return None
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":  # Staff
                # Allow access only to staff views or static files
                if modulename in ["app.StaffViews", "app.views", "django.views.static"]:
                    return None
                else:
                    return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type == "3":  # Student
                # Allow access only to student views or static files
                if modulename in ["app.StudentViews", "app.views", "django.views.static"]:
                    return None
                else:
                    return HttpResponseRedirect(reverse("student_home"))

        # Default fallback to login page
        return HttpResponseRedirect(reverse("show_login"))
