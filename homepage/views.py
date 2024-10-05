from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect
import random
import string

from django.utils import translation

from homepage.models import EmailVerification, TemporaryUser
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
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


# Global dictionary to store email and code for demonstration purposes
# You should store this more securely in your database
verification_codes = {}


def forget_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = request.POST.get('verification_code', None)

        # Step 1: Send email
        if email and not verification_code:
            if User.objects.filter(email=email).exists():
                code = generate_verification_code()

                # Store the email and verification code in the session
                request.session['reset_email'] = email
                request.session['verification_code'] = code

                # Send the email with the verification code
                send_mail(
                    'Password Reset Code',
                    f'Your password reset code is {code}',
                    'your-email@example.com',
                    [email],
                    fail_silently=False,
                )

                return JsonResponse({
                    'status': 'success',
                    'message': f"A reset code has been sent to {email}. Please enter the code.",
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': "No account is registered with this email."
                })

        # Step 2: Verify the code
        elif verification_code:
            stored_email = request.session.get('reset_email')
            stored_code = request.session.get('verification_code')

            if stored_email and stored_code and stored_code == verification_code:
                # Code is correct, redirect to reset password page or next step
                return JsonResponse({
                    'status': 'success',
                    'message': 'Verification successful! Redirecting to reset password page...',
                    'redirect_url': '/new_password/'  # Replace with the actual URL
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid verification code. Please try again.'
                })

    return render(request, 'homepage/forget_password.html')


def new_password_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        retype_password = request.POST.get('retype_password')

        email = request.session.get('reset_email')

        if password == retype_password:
            try:
                user = User.objects.get(email=email)

                user.password = make_password(password)
                user.save()

                messages.success(request, 'Password updated successfully.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email.')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('login')

    return render(request, 'homepage/new_password.html')


@login_required(login_url='/login')
def profile_view(request):
    if request.method == "POST":
        user = request.user

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if old_password and new_password and confirm_password:
            if not user.check_password(old_password):
                return JsonResponse({'error': "Old password is incorrect."}, status=400)

            if new_password != confirm_password:
                return JsonResponse({'error': "New passwords do not match."}, status=400)

            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()

        return JsonResponse({'success': "Profile updated successfully."}, status=200)

    return render(request, 'expendable/profile.html')
