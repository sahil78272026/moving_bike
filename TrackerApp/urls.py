"""
URL configuration for TrackerApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from django.views.static import serve

from TrackerApp.error_handler import CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/customer/',include('customer.api.urls')),
    path('api/v1/driver/',include('driverapp.api.urls')),
    path('api/v1/admin/',include('adminapp.api.urls')),
    path('api/v1/superadmin/',include('superadmin.api.urls')),
    path('api/v1/login/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/login/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler403='utils.views.error_403'
handler404='utils.views.error_404'
handler500='utils.views.error_500'