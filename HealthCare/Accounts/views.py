from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

# need to create a login with html necessary imports
from Accounts.models import CustomUser
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
import json


def Index(request):
    return HttpResponse(
        "<h1> Hello World Welcome to my <i>HealthCare</i> Project </h1>"
    )


def IndexView(request):
    return render(request, "index.html")


# function that connects html and receives the input and validate
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # redirecting to appoitments page
            return redirect("apptlist")

        else:
            return HttpResponse("<h1>Invalid email or password</h1>")
    return render(request, "login.html")


# sample appointments page displaying html function
def apptlist(request):
    return render(request, "apptlist.html")


# register function that takes input and register and return welcome page for the doctor
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        location = request.POST.get("location")
        phone = request.POST.get("phone")

        # Create a new user
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            location=location,
            phone=phone,
        )

        # Redirect to a welcome page or login page
        return redirect("welcome")

    return render(request, "register.html")


def welcomehtml(request):
    return render(request, "welcomepage.html")


# login api with token
@csrf_exempt
def token_generator(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate or retrieve the token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"token": token.key})
        else:
            return JsonResponse({"error": "Invalid email or password."}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=400)
