from rest_framework_jwt.views import refresh_jwt_token
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token-auth/', obtain_jwt_token, name='token-auth'),
    path('token-refresh/', refresh_jwt_token, name='token-refresh'),
    path('api-token-verify/', verify_jwt_token, name='token-verify'),
    path('users/', include('users.urls')),
    path('study/', include('study.urls')),

    re_path('', views.ReactAppView.as_view()),

]

