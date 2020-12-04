from django.conf.urls import url
from server.user_views import register, login, info

urlpatterns = [
    url(r'^register$', register, name='user register'),
    url(r'^login$', login, name='user login'),
    url(r'^info$', info, name='user info'),
]
