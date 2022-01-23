from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    print("The password is valid, but the account has been disabled!")
                # if user.is_active:
                #     login(request, user)
                #     return redirect('home')
                # else:
                #     print('jebac')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def logoutUser(request):

    logout(request)
    return redirect('login')

def register(request):

    user_form = UserRegistrationForm()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('home')
        else:
            user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': user_form})
