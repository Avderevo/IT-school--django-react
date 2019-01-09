
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.ListUsers.as_view()),
    path('<int:pk>/', views.DetailUser.as_view()),
    path('current/', views.CurrentUserView.as_view()),
    path('create_user/',views.UserCreate.as_view(), name='create_user'),
    path('confirm/<code>/', views.ConfirmEmailView.as_view(), name='confirm'),
    path('all_students/<int:courseId>/', views.ListCourseStudents.as_view(), name='course_all_students'),

]
