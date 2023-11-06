from django.shortcuts import render
from . forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False  # this means the user is not registered yet

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # it is coming from setting.py where we are hashing the password
            user.save()

            profile = profile_form.save(commit=False)  # we are setting it as false because we may get error of getting override with the above user
            profile.user = user     # this line of code is actually coming from models.py which is OneToOneField which we created and also linking to forms.py
            # profile.user - is OneToOneField user; and user - is user_form user

            if 'profile_pic' in request.FILES:  # here you can store any kind of file like image, csv, pdf, etc.
                profile.profile_pic = request.FILES['profile_pic']   # it will act as dictionary

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)    # if anyone or both became invalid

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")
    else:
        return render(request, 'basic_app/login.html', {})  # if you want to pass empty context you can otherwise not


@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")
# This method is used if any special page is created for only login time or something than for that purpose we can do like this.


@login_required     # this we have used over here because if user is logged in already.
def user_logout(request):    # so after this user will logout
    logout(request)
    return HttpResponseRedirect(reverse('index'))
