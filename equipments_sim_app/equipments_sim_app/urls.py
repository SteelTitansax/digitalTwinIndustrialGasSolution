# -----------------------------------------------------------------------------------------------
# Author : Manuel Portero Leiva 
# -----------------------------------------------------------------------------------------------
# Purpose : URL configuration for IndSim app.
# --------------------------------------------------------------
# The `urlpatterns` list routes URLs to views. For more information please see:
# https://docs.djangoproject.com/en/5.2/topics/http/urls/
# --------------------------------------------------------------
# Examples:
# Function views
#    1. Add an import:  from my_app import views
#    2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#    1. Add an import:  from other_app.views import Home
#    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#    1. Import the include() function: from django.urls import include, path
#    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# -------------------------------------------------------------

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from equipments_sim import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('signup/', views.signup,name='signup'),
    path('signin/', views.signin,name='signin'),
    path('logout/', views.signout, name='logout'),
    path('landing/', views.landing,name='landing'),
    path('absortion_column/', views.absortion_column,name='absortion_column'),
    path('compressor/', views.compressor,name='compressor'),
    path('distillator_column/', views.distillator_column,name='distillator_column'),
    path('heat_exchanger/', views.heat_exchanger,name='heat_exchanger'),
    path('valve_joule_thompson/', views.valve_joule_thompson,name='valve_joule_thompson')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)