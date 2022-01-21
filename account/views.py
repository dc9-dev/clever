from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:   
                    login(request,user)
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
