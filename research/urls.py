
from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'research'


urlpatterns = [
    path('', views.ResearchList.as_view(), name='list'),
    path('add', views.ResearchCreate.as_view(), name='add'),
    path('detail/<str:pk>/', views.ResearchDetail.as_view(), name='detail'),
    path('update/<str:pk>/', views.ResearchUpdate.as_view(), name='update'),
    path('delete/<str:pk>', views.ResearchDelete.as_view(), name='delete'),
    path('execution/<str:pk>', views.ExecutionView.as_view(), name='execution'),
    path('success', views.Success.as_view(), name='success'),

]

