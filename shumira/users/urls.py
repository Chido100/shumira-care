from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path("register_user/", views.register_user, name="register-user"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("all_residents/", views.all_users, name="all-users"),
    path('resident_detail/<int:pk>/', views.user_details, name='user-details'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/', views.profile_view, name='profile'),
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]