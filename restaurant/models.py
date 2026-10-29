from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

RESERVATION_SLOTS = [(hour, f"{hour:02d}:00") for hour in range(10, 22)]


class Menu(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    reservation_slot = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(21)], choices=RESERVATION_SLOTS
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings"
    )

    class Meta:
        ordering = ["reservation_date", "reservation_slot"]
        constraints = [models.UniqueConstraint(fields=["reservation_date", "reservation_slot"], name="unique_booking_date_slot")]

    def __str__(self):
        return f"{self.first_name} — {self.reservation_date} {self.get_reservation_slot_display()}"
