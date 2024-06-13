from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .forms import UserLoginForm, UserSignupForm, AddressForm
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.dispatch import receiver
from .models import Profile, Address
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from cart.models import CartItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.urls import reverse_lazy, reverse




def home(request):
    subcategory = Category.objects.filter(parent__isnull=True)
    return render(request, 'website.html',{'subcategories': subcategory})

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
    else:
        instance.profile.save()
        
        
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        selected_address_id = request.POST.get('address')
        if not selected_address_id:
            return HttpResponse("Please select an address.")
        selected_address = get_object_or_404(Address, id=selected_address_id, user=request.user)
        # Process the order with selected_address
        return redirect('checkout_success')

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'addresses': addresses,
    })

def checkout_success(request):
    return render(request, 'cart/checkout_success.html')

class UserAddressCreateView(CreateView):
    """
    This class will create user address.
    """
    form_class = AddressForm
    template_name = 'cart/add_address.html'
    success_url = reverse_lazy('address_list')

    def post(self, request, *args, **kwargs):
        """
        This method will assign user to user address.
        """
        form = self.get_form(form_class=self.get_form_class())
        instance = form.save(commit=False)

        if form.is_valid():
            instance.user = request.user
        instance.save()
        return redirect(self.success_url)


class UserAddressListView(LoginRequiredMixin, ListView):
    """
    This class will return a list of addresses of specific user if user is authenticated.
    """
    model = Address
    template_name = 'cart/user_address_list.html'
    context_object_name = 'addresses'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        This method will pass extra context to template.
        """
        context = super(UserAddressListView, self).get_context_data(**kwargs)
        context['form'] = AddressForm
        return context

    def get_queryset(self):
        """
        Returns a queryset of user address of specific user.
        """
        return Address.objects.filter(user=self.request.user)


class UserAddressUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    """
    This class will update user address if user is authenticated.
    """
    model = Address
    form_class = AddressForm
    template_name = 'cart/user_address_update.html'
    success_url = reverse_lazy('address_list')

    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.user.id == self.request.user.id:
            return True


class UserAddressDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    """
    This class will delete user address if user is authenticated.
    """
    model = Address
    success_url = reverse_lazy('address_list')
    template_name = 'cart/address_confirm_delete.html'
    
    def test_func(self):
        """
        This method will check whether user has permission or not.
        """
        instance = self.get_object()
        if instance.user.id == self.request.user.id:
            return True
