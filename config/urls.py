"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.urls import path
from signals import views as signal_views
from accounts import views as account_views
from django.contrib.auth import views as auth_views
from accounts.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signal_views.home , name='home'),
    path('location/<int:location_id>/', signal_views.location_detail, name='location_detail'),
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('location/<int:location_id>/report/', signal_views.submit_report, name='submit_report'),
    path('suggest-location/', signal_views.suggest_location, name='suggest_location'),
    path('dashboard/', account_views.dashboard, name='dashboard'),
]
