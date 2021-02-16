from django.urls import path, include, re_path
from django.contrib import admin
from .v1 import v1_urls

app_name = 'my_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^v1/user/', include('user.urls.v1', namespace='v1')),
    re_path(r'^v2/user/', include('user.urls.v2', namespace='v2')),
]
# urlpatterns += v1_urls
