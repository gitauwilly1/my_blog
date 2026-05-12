from django.shortcuts import render, redirect
from .models import Blog, Subscriber
from django.contrib import messages

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

def subscribe(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Subscriber.objects.filter(email=email).exists():
            messages.error(request, 'This email is already subscribed.')
        else:
            subscriber = Subscriber(email=email)
            subscriber.save()
            messages.success(request, 'You have been subscribed successfully.')

            return redirect('subscribe')
        
    return render(request, 'subscribe.html')