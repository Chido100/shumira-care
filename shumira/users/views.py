from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Profile
from  .forms import RegisterUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token




# Activation email
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you for confirming your email. You can now login to your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
    return redirect('login')

def activate_email(request, user, to_email):
    mail_subject = "Activate your account."
    message = render_to_string("users/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear {user}, please check your email {to_email} and click on the activation link to verify account.') 
    else:
        messages.error(request, f"There's been a problem sending email to {to_email}, please check that email address is correct.")



# Register User
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            activate_email(request, new_user, form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register_user.html', {'form': form})


# User Details
@login_required
def user_details(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_details.html', {'user': user})


# View all Users
@login_required
def all_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/all_users.html', {'users': users})




# User Profile
@login_required
def profile_view(request):
    template_name = 'users/profile.html'
    user_form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm

    u_form = user_form_class(instance=request.user)

    if hasattr(request.user, 'profile'):
        p_form = profile_form_class(instance=request.user.profile)
    else:
        p_form = profile_form_class()
    
    if request.method == 'POST':
        u_form = user_form_class(request.POST, instance=request.user)

        if hasattr(request.user, 'profile'):
            p_form = profile_form_class(request.POST, request.FILES, instance=request.user.profile)
        else:
            p_form = profile_form_class(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            if not hasattr(request.user, 'profile'):
                profile = p_form.save(commit=False)
                profile.user = request.user
                profile.save()
            else:
                p_form.save()

            messages.info(request, 'Your account has been updated!')
            return redirect('profile')
    return render(request, template_name, {'u_form': u_form, 'p_form': p_form})

