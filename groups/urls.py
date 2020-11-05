
from django.contrib import admin
from django.urls import path, include
from . import views


app_name = 'groups'


urlpatterns = [
    path('', views.GroupsList.as_view(), name='list'),
    path('add', views.GroupsCreate.as_view(), name='add'),
    path('detail/<str:pk>/', views.GroupsDetail.as_view(), name='detail'),
    path('update/<str:pk>/', views.GroupsUpdate.as_view(), name='update'),
    path('delete/<str:pk>', views.GroupsDelete.as_view(), name='delete'),
    path('relationship/<str:pk>', views.RelationshipCreate.as_view(), name='relationship'),
    # path('execution/<str:pk>', views.ExecutionView.as_view(), name='execution'),
    path('preview/<str:pk>', views.PublishView.as_view(), name='preview'),
    path('publish/<str:pk>', views.PublishView.as_view(), name='publish'),
]

