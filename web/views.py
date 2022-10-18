from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from web.models import Advertisement, User
from web.forms import AdvertForm, AuthForm


def main_view(request):
    return redirect('advert_list')


def main_board_view(request):
    search = request.GET.get('search', None)
    adverts = Advertisement.objects.all().order_by('-updated_at')
    if search:
        adverts = adverts.filter(
            Q(title__icontains=search) |
            Q(text__icontains=search)
        )
    return render(request, 'web/main.html', {
        'adverts': adverts,
        'search': search

    })


def one_advert_view(request, id):
    advert = get_object_or_404(Advertisement, id=id)
    user_email = get_object_or_404(User, id=advert.user_id).email
    is_owner = False
    if request.user.id == advert.user_id:
        is_owner = True
    return render(request, 'web/one_adv.html', {
        'advert': advert,
        'is_owner': is_owner,
        'user_email': user_email
    })


def edit_advert(request, id=None):
    form = AdvertForm()
    advert = None
    if id is not None:
        advert = get_object_or_404(Advertisement, user=request.user, id=id)
        form = AdvertForm(instance=advert)

    if request.method == 'POST':
        form = AdvertForm(request.POST, instance=advert, initial={'user': request.user})
        if form.is_valid():
            advert = form.save()
            return redirect('one_advert', advert.id)

    return render(request, 'web/add_advert.html', {
        'id': id,
        'form': form
    })


def registration_view(request):
    form = AuthForm()
    is_success = False
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        try:
            if form.is_valid():
                User.objects.create_user(**form.cleaned_data)
                is_success = True
        except:
            message = 'Пожалуйста, исправьте ошибки'


    return render(request, 'web/registration.html', {
        'form': form,
        'is_success': is_success,
        'message': message
    })


def auth_view(request):
    form = AuthForm()
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = 'Электронная почта или пароль неверны'
            else:
                login(request, user)
                return redirect('main')
    return render(request, 'web/login.html', {
        'form': form,
        'message': message
    })


def logout_view(request):
    logout(request)
    return redirect('main')


class RegistrationView(View):
    def _render(self, request, form=None, is_success=False):
        return render(request, "web/registration.html", {
            "form": form or AuthForm(),
            'is_success': is_success
        })

    def get(self, request, *args, **kwargs):
        return self._render(request)

    def post(self, request, *args, **kwargs):
        is_success = False
        form = AuthForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            is_success = True
        return self._render(request, form, is_success)
