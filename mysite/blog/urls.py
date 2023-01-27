from . import views
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('home/', views.PostList.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('tutorials/', views.TutorialView.as_view(), name='tutorials'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('login/', views.LoginRequest.as_view(), name='login'),
    path('logout', views.logout_request, name = 'logout'),
    path('profile/', views.profile, name='profile'),
    path('delete_comment', views.delete_comment, name='delete_comment'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)