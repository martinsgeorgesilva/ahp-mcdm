
from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'criterion'


urlpatterns = [
    path('', views.CriterionList.as_view(), name='list'),
    path('add', views.CriterionCreate.as_view(), name='add'),
    path('detail/<str:pk>/', views.CriterionDetail.as_view(), name='detail'),
    path('update/<str:pk>/', views.CriterionUpdate.as_view(), name='update'),
    path('delete/<str:pk>', views.CriterionDelete.as_view(), name='delete'),
]

