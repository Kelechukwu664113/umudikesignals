from django.contrib import admin
from .models import Provider, Location, LocationSuggestion, SignalReport


@admin.action(description="Promote selected suggestions to published locations")
def promote_to_location(modeladmin, request, queryset):
    for suggestion in queryset:
        Location.objects.get_or_create(name=suggestion.suggested_name)
        suggestion.status = LocationSuggestion.Status.REVIEWED
        suggestion.save()


class LocationSuggestionAdmin(admin.ModelAdmin):
    list_display = ["suggested_name", "submitted_by", "status", "created_at"]
    actions = [promote_to_location]


admin.site.register(Provider)
admin.site.register(Location)
admin.site.register(LocationSuggestion, LocationSuggestionAdmin)
admin.site.register(SignalReport)