from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY

from django.views import View

from django.shortcuts import render, redirect


# @login_required(login_url='login/')
class LandingView(View):
    def get(self, request):
        if request.user.is_superuser:
            user_group_str = _("Super Admin")
        else:
            user_group_str = []
            for x in request.user.groups.all():
                user_group_str.append(x.name)
                pass

        context = {
            'user': request.user,
            'user_groups': user_group_str
        }

        context = {
            'user': request.user,
            'user_groups': user_group_str
        }

        return render(request, 'index.html', context)


class LoginView(View):
    def get(self, request):
        context = self._common_context({})

        if 'lang' in request.GET:
            translation.activate(request.GET['lang'])
            request.session[LANGUAGE_SESSION_KEY] = request.GET['lang']

        if LANGUAGE_SESSION_KEY in request.session:
            context['lang'] = request.session[LANGUAGE_SESSION_KEY]

        return self._default_render(request, context)

    def post(self, request):
        context = self._common_context({})

        if LANGUAGE_SESSION_KEY in request.session:
            context['lang'] = request.session[LANGUAGE_SESSION_KEY]

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            context['message_error_login'] = _("Login Failed")

        return self._default_render(request, context)

    def _common_context(self, context):
        from .forms import FormLogin
        context['form'] = FormLogin
        context['layout_hide_nav'] = True

        return context

    def _default_render(self, request, context={}):
        return render(request, 'login.html', context)


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return render(request, 'logout.html')
