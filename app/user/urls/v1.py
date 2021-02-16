from django.urls import path

from user.views.v1.create_user import CreateUserView
from user.views.v1.manage import ManageUserView
from user.views.v1.get_token import GetToken

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', GetToken.as_view(), name='token'),
    path('refresh_token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
