from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('post-list/', views.post_list, name='post_list'), 
    path('post-create/', views.post_create, name='post_create'),
    path('post-edit/<int:post_id>/', views.post_edit, name='post_edit'), 
    path('post-delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('post-detail/<int:post_id>/', views.post_detail, name='post_detail'),    
    path('register/', views.register, name='register'), 
    # path('login/', views.login, name='login'), 
]
