from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"




from django.contrib.auth import authenticate, login


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("profile"))
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class LogoutView(TemplateView):
    template_name = "registration/logout.html"
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")

from .forms import ProfileForm
from .models import Profile



class ProfilePage(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.exclude(user=request.user).exists():
            return redirect(reverse("edit_profile"))

        context = {
            "selected_user": request.user,
        }
        return render(request, self.template_name, context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
                messages.success(request, u"Профиль успешно обновлен!")
                return redirect(reverse("profile"))
        return render(request, self.template_name, {'form': form})

    def get_profile(self, user):
        try:
            return user.profile
        except:
            return None


from .models import Profile

class ProfileList(TemplateView):
    template_name = "registration/profilelist.html"

    def dispatch(self, request, *args, **kwargs):
        profiles = Profile.objects.exclude(user=request.user)

        context = {
            "profiles": profiles,
        }
        return render(request, self.template_name, context)

from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User

class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect(reverse("login"))

        return render(request, self.template_name)