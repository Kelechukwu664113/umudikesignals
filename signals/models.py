from django.conf import settings
from django.db import models


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=150, unique=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
           
    def __str__(self):
        return self.name


class LocationSuggestion(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        REVIEWED = "reviewed", "Reviewed"

    suggested_name = models.CharField(max_length=150)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="location_suggestions"
    )
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.suggested_name} ({self.status})"


class SignalReport(models.Model):
    class Rating(models.IntegerChoices):
        NO_SIGNAL = 0, "No signal"
        WEAK = 1, "Weak"
        OK = 2, "OK"
        STRONG = 3, "Strong"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="signal_reports"
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="reports")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="reports")
    rating = models.IntegerField(choices=Rating.choices)
    used_router = models.BooleanField(default=False)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "location", "provider")

    def __str__(self):
        return f"{self.user} - {self.location} - {self.provider}: {self.get_rating_display()}"