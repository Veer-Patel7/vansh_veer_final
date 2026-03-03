from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import SuperAdminLoginForm, UserLoginForm, UserRegistrationForm, ForgotPasswordForm, OTPVerificationForm, SetNewPasswordForm
from .utils import generate_otp
from hotels.models import Hotel

User = get_user_model()


# ========================== DASHBOARD REDIRECT ==========================
@login_required
def dashboard_redirect(request):
    if request.user.role == "super_admin":
        return redirect("superadmin:super_dashboard")

    elif request.user.role == "hotel_admin":
        hotel = Hotel.objects.filter(owner=request.user).first()
        if hotel:
            return redirect("hotels:hotel_dashboard", hotel_id=hotel.id)
        return redirect("hotels:hotelregister")

    elif request.user.role == "customer":
        return redirect("customer:customer_dashboard")

    return redirect("/")


# ========================== CUSTOMER LOGIN ==========================
def customer_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user_obj = User.objects.filter(email=email, role="customer").first()

            if not user_obj:
                form.add_error(None, "Invalid email or password")
            else:
                user = authenticate(request, username=user_obj.username, password=password)

                if user is None:
                    form.add_error(None, "Invalid email or password")
                elif not user.is_verified:
                    form.add_error(None, "Please verify OTP first")
                else:
                    login(request, user)
                    return redirect("customer:customer_dashboard")
    else:
        form = UserLoginForm()

    return render(request, "accounts/customer_login.html", {"form": form})


# ========================== SUPER ADMIN LOGIN ==========================
def super_login(request):
    if request.method == "POST":
        form = SuperAdminLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if not user:
                form.add_error(None, "Invalid username or password")

            elif user.role != "super_admin":
                form.add_error(None, "Not a super admin account")

            elif not user.is_active:
                form.add_error(None, "Account is disabled")

            else:
                login(request, user)
                return redirect("superadmin:super_dashboard")
    else:
        form = SuperAdminLoginForm()

    return render(request, "accounts/super_login.html", {"form": form})

# ========================== HOTEL LOGIN ==========================
def hotel_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user_obj = User.objects.filter(email=email, role="hotel_admin").first()

            if not user_obj:
                form.add_error(None, "Invalid email or password")
            else:
                user = authenticate(request, username=user_obj.username, password=password)

                if user is None:
                    form.add_error(None, "Invalid email or password")
                elif not user.is_verified:
                    form.add_error(None, "Please verify OTP first")
                else:
                    login(request, user)

                    hotel = Hotel.objects.filter(owner=user).first()

                    if hotel:
                        return redirect("hotels:hotel_dashboard", hotel_id=hotel.id)
                    else:
                        return redirect("hotels:hotelregister")
    else:
        form = UserLoginForm()

    return render(request, "accounts/hotel_login.html", {"form": form})
# ========================== CUSTOMER SIGNUP ==========================
def customer_signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                form.add_error("username", "Username already taken")

            elif User.objects.filter(email=email).exists():
                form.add_error("email", "Email already registered")

            else:
                otp = generate_otp()

                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role="customer",
                    otp=otp,
                    is_active=False,
                    is_verified=False,
                )

                send_mail(
                    "OTP Verification",
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                return redirect(f"/accounts/verify/?email={email}")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/customer_signup.html", {"form": form})


# ========================== HOTEL SIGNUP ==========================
def hotel_signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            first = form.cleaned_data["first_name"]
            last = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                form.add_error("username", "Username already taken")

            elif User.objects.filter(email=email).exists():
                form.add_error("email", "Email already registered")

            else:
                otp = generate_otp()

                User.objects.create_user(
                    username=username,
                    first_name=first,
                    last_name=last,
                    email=email,
                    password=password,
                    role="hotel_admin",
                    otp=otp,
                    is_active=False,
                    is_verified=False,
                )

                send_mail(
                    "OTP Verification",
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                return redirect(f"/accounts/verify/?email={email}")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/hotel_signup.html", {"form": form})


# ========================== VERIFY ACCOUNT OTP ==========================
def verify(request):
    email = request.GET.get("email")

    if request.method == "POST":
        otp = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("/")

        if user.otp == otp:
            user.is_verified = True
            user.is_active = True
            user.otp = ""
            user.save()
            return redirect("accounts:dashboard_redirect")

        messages.error(request, "Invalid OTP")

    return render(request, "accounts/verify.html", {"email": email})


# ========================== FORGOT PASSWORD ==========================
def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)

                otp = generate_otp()
                user.otp = otp
                user.save()

                # ✅ VERY IMPORTANT
                request.session["reset_email"] = email

                send_mail(
                    "Password Reset OTP",
                    f"Your OTP is {otp}",
                    settings.EMAIL_HOST_USER,
                    [email],
                )

                return redirect("accounts:verify_reset_otp")

            except User.DoesNotExist:
                form.add_error("email", "Email not registered")
    else:
        form = ForgotPasswordForm()

    return render(request, "accounts/forgotpassword.html", {"form": form})

# ========================== VERIFY RESET OTP ==========================
def verify_reset_otp(request):
    email = request.session.get("reset_email")

    if not email:
        return redirect("accounts:forgot_password")

    if request.method == "POST":
        form = OTPVerificationForm(request.POST)

        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]

            user = User.objects.get(email=email)

            if user.otp == entered_otp:
                return redirect("accounts:set_new_password")
            else:
                form.add_error("otp", "Invalid OTP")
    else:
        form = OTPVerificationForm()

    return render(request, "accounts/verify_reset_otp.html", {"form": form})

# ========================== SET NEW PASSWORD ==========================
def set_new_password(request):
    email = request.session.get("reset_email")

    if not email:
        return redirect("accounts:forgot_password")

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]

            user = User.objects.get(email=email)

            user.set_password(password)
            user.otp = ""
            user.save()

            # clear session
            del request.session["reset_email"]

            if user.role == "customer":
                return redirect("accounts:customer_login")
            elif user.role == "hotel_admin":
                return redirect("accounts:hotel_login")
            elif user.role == "super_admin":
                return redirect("accounts:super_login")
    else:
        form = SetNewPasswordForm()

    return render(request, "accounts/set_new_password.html", {"form": form})

# ========================== LOGOUT ==========================
def user_logout(request):
    logout(request)
    return redirect("/")

def auth_view(request):
    return render(request, "customer/auth.html")
