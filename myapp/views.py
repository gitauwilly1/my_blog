from django.shortcuts import render
from .models import Blog

def index(request):
    context = { 'name': 'John Doe',}
    return render(request, 'index.html', context)

def about(request):
    context = { 'name': 'John Doe',}
    return render(request, 'about.html', context)

def contact(request):
    return render(request, 'contact.html')

def bloglist(request):
    blogs = Blog.objects.all()
    context = { 'blogs': blogs,}
    return render(request, 'blog_list.html', context)