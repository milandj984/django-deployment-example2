from django.shortcuts import render
from .forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, 'signin/base.html')

def register(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(request.POST['password']) # Ova naredba hash-uje password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # Ovo je ono sto pravi vezu One To One - user kolona tj. user_id povezuje sa user objektom user_form-e
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()

            registered = True
        else: # Ovaj else je ovde cisto onako...
            print(user_form.errors, profile_form.errors)

    return render(request, 'signin/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password']) # Vraca user obekat ako postoji
        if user:
            if user.is_active:
                login(request, user)
                # print(dir(request))
                # print(dir(request.user))
                parameters = {'compname': request.META['COMPUTERNAME'], 'HTTP_USER_AGENT': request.META['HTTP_USER_AGENT'], 'REMOTE_ADDR': request.META['REMOTE_ADDR']}
                return render(request, 'signin/base.html', parameters)
                # return HttpResponseRedirect(reverse('signin:index'))
            return HttpResponse('User is not active!')
        else:
            return render(request, 'signin/signin.html', {'error': 'Invalid username or password'})
    return render(request, 'signin/signin.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('signin:index'))

@login_required
def special(request):
    return HttpResponse('You are logged in {0}'.format(request.user.username))