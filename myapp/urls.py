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
]