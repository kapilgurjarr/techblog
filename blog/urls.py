from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='index'),
    path('dashbord/',views.DashboardView.as_view(),name='user-dashbord'),
    path('create_post/',views.PostCreateView.as_view(),name='create-post'),
    path('post/comment/',views.PostCommentView.as_view(),name='post-comment'),
    path('<slug:slug>/',views.PostDetailView.as_view(),name='post-detail'),
    
    
]