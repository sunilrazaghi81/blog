from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'

urlpatterns = [
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='rest_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='passwor_reset_complate'),
    
]
