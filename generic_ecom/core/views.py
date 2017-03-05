from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render


def login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            context['message_error_login'] = _("Login Failed")

    from .forms import FormLogin
    context['form'] = FormLogin

    context['layout_hide_nav'] = True

    return render(request, 'login.html', context)
