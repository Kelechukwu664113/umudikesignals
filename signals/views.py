from django.shortcuts import render, get_object_or_404, redirect
from collections import Counter
from .models import Location, Provider, SignalReport
from .forms import SignalReportForm
from django.contrib.auth.decorators import login_required
from .models import LocationSuggestion
from .forms import LocationSuggestionForm


def home(request):
    locations = Location.objects.filter(is_published=True)
    return render(request, "home.html", {"locations": locations})


def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id, is_published=True)
    providers = Provider.objects.all()

    summaries = []
    for provider in providers:
        reports = SignalReport.objects.filter(location=location, provider=provider)
        if reports.exists():
            ratings = [r.rating for r in reports]
            most_common_rating = Counter(ratings).most_common(1)[0][0]
            summaries.append({
                "provider": provider,
                "rating_label": dict(SignalReport.Rating.choices)[most_common_rating],
                "count": reports.count(),
            })

    return render(request, "location_detail.html", {
        "location": location,
        "summaries": summaries,
    })


@login_required
def submit_report(request, location_id):
    location = get_object_or_404(Location, id=location_id, is_published=True)

    if request.method == "POST":
        form = SignalReportForm(request.POST)
        if form.is_valid():
            report, created = SignalReport.objects.update_or_create(
                user=request.user,
                location=location,
                provider=form.cleaned_data["provider"],
                defaults={
                    "rating": form.cleaned_data["rating"],
                    "used_router": form.cleaned_data["used_router"],
                    "note": form.cleaned_data["note"],
                },
            )
            return redirect("location_detail", location_id=location.id)
    else:
        form = SignalReportForm()

    return render(request, "submit_report.html", {"form": form, "location": location})


@login_required
def suggest_location(request):
    if request.method == "POST":
        form = LocationSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.submitted_by = request.user
            suggestion.save()
            return redirect("home")
    else:
        form = LocationSuggestionForm()

    return render(request, "suggest_location.html", {"form": form})