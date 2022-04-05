from re import template
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy, reverse
from .forms import LoginForm, UserRegistrationForm, CustomerCreateForm
from .models import Customer, UserBase

def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('warehouses')
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


def password_change(request, id):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            #keep current user logged in
            update_session_auth_hash(request, user)
            messages.success(request, 'password updated!')
            return redirect('detail-user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'account/password.html', {'form': form})
   

class UserDetailView(DetailView):
    model = UserBase
    template_name = 'account/detail_user.html'
    context_object_name = 'user'


class CustomerCreateView(CreateView):
    
    model = Customer
    template_name = 'account/create_customer.html'
    form_class = CustomerCreateForm
    success_url = reverse_lazy('create-order')

    def get(self, request, *args, **kwargs):
        context = {'form': CustomerCreateForm()}
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
            

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'account/detail_customer.html'


