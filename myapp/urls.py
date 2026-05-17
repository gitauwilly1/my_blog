from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.bloglist, name='blogs'),
    path('blogs/<int:id>/', views.blog_detail, name='blog-detail'),
    path('blogs/<int:id>/edit/', views.edit_blog, name='edit-blog'),
    path('blogs/<int:id>/delete/', views.delete_blog, name='delete-blog'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('add-blog/', views.add_blog, name='add-blog'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('setup-2fa/', views.setup_2fa, name='setup_2fa'),
    path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
    path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
]