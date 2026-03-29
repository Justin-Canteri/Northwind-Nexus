"""
URL configuration for configuracion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

#from. import views
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from base.views import views
from base.views import register
urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', include('base.urls')),
    path('', views.inicio),

    path('api/register/', register.registrar_usuario),
    # Esta ruta es para hacer LOGIN (obtener el token)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Esta ruta es para renovar el token cuando expire
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
