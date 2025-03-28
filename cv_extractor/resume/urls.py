from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', upload_cv, name='home'),
    path('upload-cv/', upload_cv, name='upload_cv'),
   path('update-cv/', cv_update, name='update_cv'),

    path('profile/<int:user_id>/', profile_view, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
path('success/<int:cv_id>/', success, name='success'),
     path('register/', register, name='register'),
    path('extracted-info/<int:extracted_info_id>/', extracted_info_view, name='extracted_info'),  # New URL

    # Built-in login view
    path('login/', login_view, name='login'),  # Replace auth_views.LoginView with your custom login view

    # Built-in logout view
    path('logout/', logout_view, name='logout'),  # New logout route
]
