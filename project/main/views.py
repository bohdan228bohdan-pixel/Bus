import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import EmailVerification


# ========================
# СТАТИЧНІ СТОРІНКИ
# ========================

def home(request):
    return render(request, 'index.html')


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


def redirect_to_home(request):
    return HttpResponseRedirect('/home/')


# ========================
# РЕЄСТРАЦІЯ + ЛОГІН
# ========================

def registerindex(request):
    context = {}

    if request.method == "POST":

        # ========================
        # РЕЄСТРАЦІЯ
        # ========================
        if "repeatpass" in request.POST:
            username = request.POST.get("login")
            email = request.POST.get("emeil")
            password = request.POST.get("password")
            repeat = request.POST.get("repeatpass")

            if password != repeat:
                context["register_error"] = "Паролі не співпадають"
                return render(request, "registerindex.html", context)

            if User.objects.filter(username=username).exists():
                context["register_error"] = "Такий логін вже існує"
                return render(request, "registerindex.html", context)

            if User.objects.filter(email=email).exists():
                context["register_error"] = "Така пошта вже використовується"
                return render(request, "registerindex.html", context)

            # ❗ Створюємо НЕАКТИВНОГО користувача
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_active=False
            )

            # 6-значний код
            code = str(random.randint(100000, 999999))

            EmailVerification.objects.create(
                user=user,
                code=code
            )

            send_mail(
                "Підтвердження email — Dieller Bus",
                f"Ваш код підтвердження: {code}",
                None,
                [email],
                fail_silently=False,
            )

            request.session["verify_user_id"] = user.id
            return redirect("verify_email")

        # ========================
        # ЛОГІН
        # ========================
        else:
            username = request.POST.get("login")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is None:
                context["login_error"] = "Невірний логін або пароль"
                return render(request, "registerindex.html", context)

            if not user.is_active:
                context["login_error"] = "Підтвердіть email перед входом"
                return render(request, "registerindex.html", context)

            auth_login(request, user)
            return redirect("home")

    return render(request, "registerindex.html", context)


# ========================
# ПІДТВЕРДЖЕННЯ EMAIL
# ========================

def verify_email(request):
    user_id = request.session.get("verify_user_id")

    if not user_id:
        return redirect("registerindex")

    user = User.objects.get(id=user_id)
    verification = EmailVerification.objects.get(user=user)

    if request.method == "POST":
        code = request.POST.get("code")

        if verification.code == code:
            user.is_active = True
            user.save()
            verification.delete()

            auth_login(request, user)
            return redirect("profile")

        return render(request, "verify_email.html", {
            "error": "Невірний код"
        })

    return render(request, "verify_email.html")

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_ticket(request):
    if request.method == "POST":
        from_city = request.POST["from"]
        to_city = request.POST["to"]
        passengers = int(request.POST["passengers"])
        travel_date = request.POST["date"]
        price = int(request.POST["price"])  # грн

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "uah",
                    "product_data": {
                        "name": f"Квиток {from_city} → {to_city}",
                    },
                    "unit_amount": price * 100,
                },
                "quantity": passengers,
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/payment-success/"),
            cancel_url=request.build_absolute_uri("/payment-cancel/"),
        )

        Ticket.objects.create(
            user=request.user,
            from_city=from_city,
            to_city=to_city,
            travel_date=travel_date,
            passengers=passengers,
            price=price * passengers,
            stripe_session_id=session.id
        )

        return redirect(session.url)

    return redirect("home")


@login_required
def payment_success(request):
    return render(request, "payment_success.html")


@login_required
def payment_cancel(request):
    return render(request, "payment_cancel.html")

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY


def kvitokindex(request):
    return render(request, "kvitokindex.html")


@login_required
def create_ticket(request):
    if request.method == "POST":
        from_city = request.POST["from_city"]
        to_city = request.POST["to_city"]
        passengers = int(request.POST["passengers"])
        travel_date = request.POST["travel_date"]
        price = int(request.POST["price"])  # за 1 квиток

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "uah",
                    "product_data": {
                        "name": f"Квиток {from_city} → {to_city}",
                    },
                    "unit_amount": price * 100,
                },
                "quantity": passengers,
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/payment-success/"),
            cancel_url=request.build_absolute_uri("/payment-cancel/"),
        )

        Ticket.objects.create(
            user=request.user,
            from_city=from_city,
            to_city=to_city,
            travel_date=travel_date,
            passengers=passengers,
            total_price=price * passengers,
            stripe_session_id=session.id
        )

        return redirect(session.url)

    return redirect("kvitokindex")


@login_required
def payment_success(request):
    return render(request, "payment_success.html")


@login_required
def payment_cancel(request):
    return render(request, "payment_cancel.html")


@login_required
def profile(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, "profile.html", {"tickets": tickets})

def oplata(request):
    return render(request, "oplata.html")