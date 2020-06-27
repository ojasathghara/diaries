from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST);  #generates a form(with error messages, if any)
        
        if form.is_valid():
            form.save() #saves user to database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for user {username}! You are now able to Login!')
            return redirect('user-login')            
    
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context=context)

@login_required
def settings(request):

    # the user form expects a user instance and a profile form expects a profile instance.

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES ,instance=request.user.profile)

        # these forms already know what to save because we have passed request arg
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your Account info has been updated!')
            return redirect('user-settings')
            # https://stackoverflow.com/questions/3209906/django-return-redirect-with-parameters

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    u_posts = request.user.post_set.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'u_posts': u_posts,
        'title': 'Settings'
    }

    return render(request, 'users/settings.html', context=context)


