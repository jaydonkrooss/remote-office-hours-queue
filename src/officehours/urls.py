"""officehours URL Configuration

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
from django.urls import re_path, path, include
from django.views.generic import TemplateView
from django.conf import settings
import watchman.views

urlpatterns = [
    path('', include('officehours_ui.urls')),
    path('api/', include('officehours_api.urls')),
    re_path(r'^oidc/', include('mozilla_django_oidc.urls')),
    re_path(r'^watchman/', include('watchman.urls')),
    re_path(r'^status/?$', watchman.views.bare_status),
    path('admin/', admin.site.urls),
    path('403/', TemplateView.as_view(template_name='403.html')),
    path('500/', TemplateView.as_view(template_name='500.html')),
]

if 'mozilla_django_oidc' not in settings.INSTALLED_APPS:
    urlpatterns += [path('accounts/', include('django.contrib.auth.urls'))]
