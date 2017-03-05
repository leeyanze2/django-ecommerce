from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY

from django.shortcuts import render


def login(request):
    context = {}

    if request.method == 'GET' and 'lang' in request.GET:
        translation.activate(request.GET['lang'])
        request.session[LANGUAGE_SESSION_KEY] = request.GET['lang']

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
    if LANGUAGE_SESSION_KEY in request.session:
        context['lang'] = request.session[LANGUAGE_SESSION_KEY]

    return render(request, 'login.html', context)
