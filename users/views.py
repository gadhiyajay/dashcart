from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import UserLoginForm, UserSignupForm
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import post_save
from django.contrib.auth.models import User



def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been successfully logged in.')  # Add success message
                return redirect('home')  # Redirect to home page after successful login
            else:
                # Display error message if authentication fails
                form.add_error(None, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):  
    if request.method == 'POST':  
        form = UserSignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  # Deactivate account till it is confirmed
            
            # Save the user to database
            user.save()
            
            # If the user is a seller, save the GST number
            user_profile = user.profile  # Assuming you have a profile model linked to user
            user_profile.gst_number = form.cleaned_data.get('gst_number')
            user_profile.save()
            
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                'token': account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(mail_subject, message, to=[to_email])  
            email.send()  
            return render(request, 'confirm-mail.html')  
    else:  
        form = UserSignupForm()  
    return render(request, 'signup.html', {'form': form})  

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  # Use force_str instead of force_text
        user = User.objects.get(pk=uid)  
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request, 'Thank you for your email confirmation. Now you can log in to your account.')  
        return redirect('home')  # Redirect to the home page after successful activation
    else:  
        messages.error(request, 'Activation link is invalid!')  
        return redirect('home')  # Redirect to the home page or any other appropriate page

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()