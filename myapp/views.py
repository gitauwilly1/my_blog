from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Subscriber
from django.contrib import messages
from .forms import BlogForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialApp


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

def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Authenticate the newly created user using the raw password so
            # Django sets the `backend` attribute when multiple backends
            # are configured. This avoids the "must provide the backend"
            # error when calling `login()` directly with a User instance.
            raw_password = form.cleaned_data.get('password1')
            auth_user = authenticate(request, username=form.cleaned_data.get('email'), password=raw_password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, f"Account created for {auth_user.email}. Welcome!")
                return redirect('index')
            else:
                # Fallback: if authentication failed for some reason, still
                # redirect and show an info message.
                messages.info(request, "Account created. Please log in.")
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in as {user.email}.")
                next_url = request.POST.get('next') or 'index'
                return redirect(next_url)
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()

    google_login_url = None
    try:
        if SocialApp.objects.filter(provider='google').exists():
            google_login_url = '/accounts/google/login/'
    except Exception:
        pass

    return render(request, 'users/login.html', {'form': form, 'google_login_url': google_login_url})

def logout_view(request):
    """Handle user logout."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out successfully.")
    return redirect('index')

@login_required
def profile_view(request):
    """Display user profile."""
    return render(request, 'users/profile.html')