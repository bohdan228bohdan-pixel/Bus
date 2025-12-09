from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Главная страница
def home(request):
    return render(request, 'index.html')

# Пример дополнительной страницы
def about(request):
    return HttpResponse('<h1>About Page</h1>')

def bova(request):
    return render(request, 'bova.html')

def eos(request):
    return render(request, 'eos.html')

def kvitokindex(request):
    return render(request, 'kvitokindex.html')

def mercedes2(request):
    return render(request, 'mercedes2.html')

def nashbusindex(request):
    return render(request, 'nashbusindex.html')

def neolplanwhite(request):
    return render(request, 'neolplanwhite.html')

def neoplanred(request):
    return render(request, 'Neoplanred.html')

def oplata(request):
    return render(request, 'oplata.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

def registerindex(request):
    context = {}
    if request.method == 'POST':
        # Визначаємо, яка форма відправлена (реєстрація чи логін)
        if 'repeatpass' in request.POST:
            # Реєстрація
            username = request.POST.get('login')
            email = request.POST.get('emeil')
            password = request.POST.get('password')
            repeatpass = request.POST.get('repeatpass')
            if password != repeatpass:
                context['register_error'] = 'Паролі не співпадають.'
            elif User.objects.filter(username=username).exists():
                context['register_error'] = 'Користувач з таким логіном вже існує.'
            elif User.objects.filter(email=email).exists():
                context['register_error'] = 'Користувач з такою поштою вже існує.'
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Profile буде створено автоматично через сигнал
                context['register_success'] = 'Реєстрація успішна! Тепер увійдіть.'
        else:
            # Логін
            username = request.POST.get('login')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                context['login_error'] = 'Невірний логін або пароль.'
    return render(request, 'registerindex.html', context)

def redirect_to_home(request):
    return HttpResponseRedirect('/home/')
def eos(request):
    return render(request, 'nashbusindex/eos.html')