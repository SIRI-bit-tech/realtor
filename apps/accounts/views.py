from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm

User = get_user_model()

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            
            # Redirect to next page or dashboard
            next_page = request.GET.get('next', reverse('users:dashboard'))
            
            if request.htmx:
                return render(request, 'partials/login_success.html', {
                    'redirect_url': next_page
                })
            
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
            if request.htmx:
                return render(request, 'partials/auth_errors.html', {'form': form})
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    
    return render(request, 'accounts/login.html', context)

def signup_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Auto login after registration
            login(request, user)
            
            if request.htmx:
                return render(request, 'partials/signup_success.html', {
                    'user': user
                })
            
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
            if request.htmx:
                return render(request, 'partials/auth_errors.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'accounts/signup.html', context)

@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

@login_required
def change_password_view(request):
    """Change password view"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

def password_reset_view(request):
    """Password reset view"""
    return render(request, 'accounts/password_reset.html')

def password_reset_done_view(request):
    """Password reset done view"""
    return render(request, 'accounts/password_reset_done.html')

def password_reset_confirm_view(request, uidb64, token):
    """Password reset confirm view"""
    return render(request, 'accounts/password_reset_confirm.html')

def password_reset_complete_view(request):
    """Password reset complete view"""
    return render(request, 'accounts/password_reset_complete.html')
