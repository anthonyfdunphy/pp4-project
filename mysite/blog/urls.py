from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('home/', views.PostList.as_view(), name='index'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name= 'about'),
    path('tutorials', views.tutorials, name='tutorials'),
    path('contact', views.contact, name='contact'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name = 'logout'),
    path('<slug:slug>/', views.post_detail, name='post_detail')
]

# urlpatterns = [
#     path('', views.PostList.as_view(), name='home'),
#     path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
# ]