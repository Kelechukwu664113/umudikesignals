from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from signals.models import SignalReport, LocationSuggestion
from .forms import AccountEditForm



def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend="accounts.backends.PhoneNumberBackend")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})



@login_required
def dashboard(request):
    reports = SignalReport.objects.filter(user=request.user).order_by("-updated_at")
    suggestions = LocationSuggestion.objects.filter(submitted_by=request.user).order_by("-created_at")

    if request.method == "POST":
        form = AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = AccountEditForm(instance=request.user)

    if request.user.full_name:
        parts = request.user.full_name.split()
        initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else parts[0][0].upper()
    else:
        initials = request.user.phone_number[-2:]

    return render(request, "dashboard.html", {
        "reports": reports,
        "suggestions": suggestions,
        "form": form,
        "initials": initials,
    })