from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
import random
import string
from homepage.models import EmailVerification, TemporaryUser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug info
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response_data = {
                'status': 'success',
                'message': 'Logged in successfully'
            }
            return JsonResponse(response_data)
        else:
            response_data = {
                'status': 'failed',
                'message': 'Username and password are not correct'
            }
            return JsonResponse(response_data)
    return render(request, 'homepage/login.html')


def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def home(request):
    return render(request, 'homepage/index.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if check_email(email) == "not valid":
            return JsonResponse({'status': 'failed', 'message': 'enter a valid UIU\'s email'})
        elif User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'failed', 'message': 'the email is already registered'})
        elif User.objects.filter(username=email).exists():
            return JsonResponse({'status': 'failed', 'message': 'the username is already used'})
        else:
            TemporaryUser.objects.filter(email=email).delete()
            temp_user = TemporaryUser.objects.create(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )

            request.session['email'] = email

            code = generate_verification_code()

            EmailVerification.objects.create(email=email, verification_code=code)

            send_mail(
                'Your Verification Code',
                f'Your verification code is {code}',
                'smartuiu@uiu.ac.bd',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success', 'message': 'A verification code has sent to your email'})
    return render(request, 'homepage/signup.html')


def check_email(email):
    patterns_student = [
        r"^[A-Za-z0-9._%+-]+@bscse\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bseds\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bsmsj\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bsce\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bseee\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bsbba\.uiu\.ac\.bd$"
    ]

    patterns_faculty = [
        r"^[A-Za-z0-9._%+-]+@cse\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@eds\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@msj\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@ce\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@eee\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@bba\.uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@uiu\.ac\.bd$",
        r"^[A-Za-z0-9._%+-]+@admin\.bscse\.uiu\.ac\.bd$"
    ]

    for pattern in patterns_student:
        if re.match(pattern, email):
            return "student"

    for pattern in patterns_faculty:
        if re.match(pattern, email):
            return "faculty"

    return "not valid"


def verification_view(request):
    if request.method == 'POST':
        code = request.POST['code']

        email = request.session.get('email')

        if email:
            try:
                verification = EmailVerification.objects.get(email=email, verification_code=code)

                temp_user = TemporaryUser.objects.get(email=email)

                user = User.objects.create_user(
                    username=temp_user.username,
                    password=temp_user.password,
                    email=temp_user.email,
                    first_name=temp_user.first_name,
                    last_name=temp_user.last_name
                )

                user.save()

                temp_user.delete()
                del request.session['email']

                return JsonResponse({'status': 'success', 'message': 'Verification successful. User registered!'})
            except EmailVerification.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Invalid verification code'})
            except TemporaryUser.DoesNotExist:
                return JsonResponse({'status': 'failed', 'message': 'Temporary user data not found'})
        else:
            return JsonResponse({'status': 'failed', 'message': 'No email found in session'})
    return render(request, 'homepage/verification.html')


@login_required(login_url='/login')
def contacts_view(request):
    return render(request, 'homepage/contact.html')


@login_required(login_url='/login')
def homepage_view(request):
    return render(request, 'homepage/homepage.html')


@login_required(login_url='/login')
def developers_view(request):
    return render(request, 'homepage/about.html')


def logout_view(request):
    logout(request)
    return redirect('index')
