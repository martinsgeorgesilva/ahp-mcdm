
from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'user'


urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
    path('add', views.UserCreate.as_view(), name='add'),
    path('detail/<str:pk>/', views.UserDetail.as_view(), name='detail'),
    path('update/<str:pk>/', views.UserUpdate.as_view(), name='update'),
    path('delete/<str:pk>', views.UserDelete.as_view(), name='delete'),
]

