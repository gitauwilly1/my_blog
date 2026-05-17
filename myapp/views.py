import pyotp
import qrcode
from io import BytesIO
import base64
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Subscriber
from django.contrib import messages
from .forms import BlogForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialApp
from django.views.decorators.http import require_http_methods



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
            user = form.get_user()
            
            if user.two_factor_enabled:
                # Store user ID in session for 2FA verification
                request.session['user_id'] = user.id
                return redirect('verify_2fa')
            else:
                # Complete login without 2FA
                login(request, user)
                return redirect('index')

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

@login_required
def setup_2fa(request):
    """Generate QR code for 2FA setup."""
    user = request.user
    
    if request.method == 'POST':
        secret = request.POST.get('secret')
        code = request.POST.get('code')
        
        # Verify the code
        totp = pyotp.TOTP(secret)
        if totp.verify(code):
            # Save secret to user
            user.otp_secret = secret
            user.two_factor_enabled = True
            user.save()
            messages.success(request, "Two-Factor Authentication enabled successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid code. Please try again.")
    
    # Generate new secret
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    
    # Generate QR code
    uri = totp.provisioning_uri(
        name=user.email,
        issuer_name='My App'
    )
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    qr_code = base64.b64encode(buf.getvalue()).decode()
    
    context = {
        'qr_code': qr_code,
        'secret': secret,
    }
    return render(request, 'users/setup_2fa.html', context)

@login_required
@require_http_methods(["POST"])
def disable_2fa(request):
    """Disable 2FA for the user."""
    user = request.user
    user.two_factor_enabled = False
    user.save()
    messages.success(request, "Two-Factor Authentication disabled.")
    return redirect('profile')

def verify_2fa(request):
    """Verify 2FA code during login."""
    if request.method == 'POST':
        code = request.POST.get('code')
        user = request.session.get('user_id')
        
        if not user:
            return redirect('login')
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user_obj = User.objects.get(id=user)
        totp = pyotp.TOTP(user_obj.otp_secret)
        
        if totp.verify(code):
            # Complete login
            login(request, user_obj)
            messages.success(request, f"Logged in successfully!")
            return redirect('index')
        else:
            messages.error(request, "Invalid 2FA code.")
    
    return render(request, 'users/verify_2fa.html')