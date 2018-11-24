"""ezhiGo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view
from rest_framework.authtoken import views

schema_view = get_swagger_view(title='Pastebin API')
from . import settings


import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls(title='API Documentation')),
    path('api-docs/', schema_view),
    path('api/v1/', include('base.urls_api')),


    path('users/', include('base.urls')),
    path('emall/', include('emall.urls')),
    path('scheme/', include('scheme.urls')),
    path('life/', include('life.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

