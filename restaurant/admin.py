from django.contrib import admin
from .models import Booking, Menu

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("first_name", "reservation_date", "reservation_slot", "created_by")
    list_filter = ("reservation_date", "reservation_slot")
    search_fields = ("first_name",)
    ordering = ("reservation_date", "reservation_slot")

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "inventory")
    search_fields = ("title",)
