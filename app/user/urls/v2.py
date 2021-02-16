from django.urls import path

from user.views.v2.manage import ManageUserViewV2
from .v1 import urlpatterns as v1_urls

app_name = 'user'

urlpatterns = [
    path('me/', ManageUserViewV2.as_view(), name='me'),
]

urlpatterns.extend(v1_urls)
