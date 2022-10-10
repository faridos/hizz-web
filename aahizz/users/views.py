from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {"form": form}
    return render(request, "users/register.html", context)

# Create your views here.
def login_view(request):
    # future -> ?next=/articles/create/
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/users')
    else:
        form = AuthenticationForm(request)
    context = {
        "form": form
    }
    return render(request, "users/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "users/logout.html", {})


def index(request):
    return render(request, 'users/users_view.html', {'hh': '222222'})
    # return HttpResponse("Hello, world. You're at the polls index.")



