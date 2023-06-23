"""irrigation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignIn, name='signin'),
    path('forget-password/', views.ForgetPassword, name='forget_password'),
    path('change-password/<str:token>/', views.ChangePassword, name='change_password'),
    path('signup/', views.SignUp, name='signup'),
    path('logout/', views.Logout, name='logout'),
    path('home/', views.HomePage, name='home'),
    path('mesespaces/',views.mesespaces,name='mesespaces'),
    path('ajouter_ferme/', views.ajouter_ferme, name='ajouter_ferme'),
    path('supprimer_ferme/<str:farm_id>/', views.supprimer_ferme, name='supprimer_ferme'),
    path('guide/', views.guide, name='guide'),
    path('farm/<str:farm_id>/zone/<str:zone_id>/', views.dash, name='dash'),
    path('dash/<str:zone_id>/', views.dash, name='dash'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('ajouter-plante/', views.ajouter_plante, name='ajouter_plante'),
    path('zones/<str:farm_id>/', views.zones_view, name='zones'),
    path('zones/<str:farm_id>/ajouter_zone/', views.ajouter_zone, name='ajouter_zone'),
    path('zones/<int:zone_id>/temperature-humidite/', views.afficher_temperature_humidite, name='afficher_temperature_humidite'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

