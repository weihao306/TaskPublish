from django.conf.urls import url
from server.task_views import manage_task

urlpatterns = [
    url(r'^$', manage_task, name='manage task'),
]