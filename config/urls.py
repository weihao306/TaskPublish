"""TaskPublish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from server.task_views import manage_task
from server.request_views import manage_request
from config import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'user/', include('server.user_urls')),
    # url(r'tasks', include('server.task_urls')),
    url(r'^tasks', manage_task, name='manage task'),
    # url(r'requests', include('server.request_urls'))
    url(r'^requests', manage_request, name='manage task')
]

admin.site.site_header = "[召集令 管理系统]"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
