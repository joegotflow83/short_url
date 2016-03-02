from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.datetime_safe import datetime

from .models import URL, Click
from .forms import URLForm, UserForm


class IndexView(View):


    def post(self, request):
        """Allow a user to login"""
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('converter'))
        else:
            return render(request, 'main/invalid.html')

    def get(self, request):
        """Display form to log in"""
        return render(request, 'main/login.html')

class RegisterView(FormView):


    template_name = 'main/register.html'
    form_class = UserForm
    fields = ['username', 'email', 'password1', 'password2']

    def get_success_url(self):
        """Override the success url to redirect to login view"""
        return reverse('login')

    def form_valid(self, form):
        """Validate the form"""
        user = User.objects.create_user(form.cleaned_data['username'],
                                        form.cleaned_data['email'],
                                        form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)


class AuthLogout(View):


    def get(self, request):
        """Log a user out"""
        logout(request)
        return redirect(reverse('login'))


class ConverterView(View):


    def post(self, request):
        """Allow a user to fill out the form"""
        form = URLForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            Click.objects.create(bookmark=URL(data.pk), accessed=datetime.now())
            return redirect(reverse('converter'))

    def get(self, request):
        """Display the url form"""
        form = URLForm()
        user_data = URL.objects.all()
        print(user_data)
        return render(request, 'main/converter_form.html', {'form': form, 'users': user_data})


class URLView(View):


    def get(self, request, url):
        """Redirect user to their url"""
        new_url = get_object_or_404(URL, short=url)
        update_click = Click.objects.update(bookmark=new_url, accessed=datetime.now())
        update_click.save()
        return redirect(new_url.url)


class BookmarkList(ListView):


    model = Click
