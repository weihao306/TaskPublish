from django.conf.urls import url
from server.request_views import manage_request


urlpatterns = [
    url(r'^$requests', manage_request, name='manage task'),
]
