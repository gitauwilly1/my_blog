from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Subscriber
from django.contrib import messages
from .forms import BlogForm

def index(request):
    context = {'name': 'John Doe'}
    return render(request, 'index.html', context)

def about(request):
    
    return render(request, 'about.html')

def contact(request):
    
    return render(request, 'contact.html')

def bloglist(request):    
    blogs = Blog.objects.all()
    context = {'blogs': blogs}
    return render(request, 'blog_list.html', context)

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, 'You are already subscribed')
        else:   
            subscriber = Subscriber(email=email)
            subscriber.save()
            messages.success(request, 'Thank you for subscribing to our monthly newsletters!')
        
        return redirect('subscribe')
    return render(request, 'subscribe.html')

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blogs')
    else:
        form = BlogForm()
    
    return render(request, 'add_blog.html', {'form': form})

def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog-detail', id=blog.id)
    else:
        form = BlogForm(instance=blog)
    
    context = {'form': form, 'blog': blog, 'is_edit': True}
    return render(request, 'add_blog.html', context)

def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog post deleted successfully!')
        return redirect('blogs')
    
    context = {'blog': blog}
    return render(request, 'delete_blog.html', context)