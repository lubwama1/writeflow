from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ProfileForm, EmailChangeForm, CustomLoginForm
from .models import Profile
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification 
from notifications.signals import notify
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sessions.models import Session
from django.utils.timezone import now 
from allauth.account.views import ConfirmEmailView
from sphere.models import Post 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from notifications.models import Notification
# class UserLoginView(LoginView):
#     template_name = 'account/login.html'
#     success_url = reverse_lazy('sphere:home')
#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         password = form.cleaned_data['password']
#         user = authenticate(request=self.request, username=email, password=password)
#         if user is not None:
#             login(self.request, user)
#             return super().form_valid(form)
#         else:
#             form.add_error(None, "Invalid email or password")
#             return self.form_invalid(form)
    

def user_login(request):
    if request.method == 'POST':
        # form = AuthenticationForm(request, data=request.POST or None) 
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            # Authenticate via email (using Django's built-in User model)
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Optionally set the session expiration time if "Remember me" is checked
                if remember_me:
                    request.session.set_expiry(3600 * 24 * 7)  # 1 week session
                else:
                    request.session.set_expiry(0)  # Session expires when browser is closed

                return redirect('sphere:home')  # Redirect after successful login

            else:
                messages.error(request, 'Invalid email or password')
        else:
            messages.error(request, 'Please correct the errors below')
    
    return render(request, 'account/login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('account_login')
        else:
            messages.error(request, 'Registration failed')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'account/signup.html', context)

@login_required(login_url='account_login')
def user_account(request):
    return render(request, 'account/account.html')


class UserLogout(LogoutView): 
    template_name = 'account/logout.html'
    success_url = reverse_lazy('account_login')

def user_logout(request):
    logout(request)
    return redirect('account_login')

@login_required(login_url='account_login')
def user_profile(request, username=None):
    try:
        profile_instance = Profile.objects.get(user__username=username)
    except ObjectDoesNotExist:
        try:
            user_instance = User.objects.create(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('users:account')
        profile_instance = Profile.objects.create(user=user_instance)
        messages.info(request, 'A new profile has been created for you.')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=profile_instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile is updated successfully')
            notify.send(sender=request.user, recipient=request.user, verb='Profile picture updated successfully', description=f'Dear {request.user.username}, Profile picture updated successfully', target=profile)
            return redirect('users:profile', username=request.user.username)
        else:
            # messages.error(request, 'An Error Occurred in Account Creation')
            messages.error(request, f"Registration failed: {form.errors.as_text()}")

    else:
        form = ProfileForm(instance=profile_instance)

    context = {
        'form': form,
        'profile_instance': profile_instance,
        'profile': profile_instance  # Here profile is always available
    }

    return render(request, 'account/profile.html', context)


class UserConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirm.html'

def author_profile(request, pk):
    author = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(author=author) 
    paginated_by = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = paginated_by.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginated_by.page(1)
    except EmptyPage:
        page_obj = paginated_by.page(paginated_by.num_pages)     
    return render(request, 'users/author_profile.html', {'author': author, 'posts': page_obj})