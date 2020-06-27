from django.urls import path
from . import views

# app specific urls

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'), # use variables in urls
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/posts/', views.UserPostList.as_view(), name='user-posts'),
    path('about/', views.about, name='blog-about')
]

# class based views looks for template as: <appname>/<model>_<viewtype>.html ex: blog/post_list.html