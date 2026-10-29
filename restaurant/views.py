import json
from datetime import date

from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from .models import Booking

VALID_SLOTS = set(range(10, 22))


def home(request):
    return render(request, "restaurant/home.html")


@require_http_methods(["GET", "POST"])
def book(request):
    if request.method == "GET":
        return render(request, "restaurant/book.html", {"today": date.today().isoformat()})

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON request."}, status=400)

    first_name = str(payload.get("first_name", "")).strip()
    reservation_date = payload.get("reservation_date", "")
    raw_slot = payload.get("reservation_slot", "")

    if not first_name or not reservation_date or raw_slot == "":
        return JsonResponse({"error": "Please complete all three fields."}, status=400)

    try:
        parsed_date = date.fromisoformat(reservation_date)
        slot = int(raw_slot)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Please provide a valid date and reservation slot."}, status=400)

    if parsed_date < date.today():
        return JsonResponse({"error": "Reservations cannot be made for a past date."}, status=400)
    if slot not in VALID_SLOTS:
        return JsonResponse({"error": "That reservation slot is not valid."}, status=400)

    try:
        with transaction.atomic():
            booking = Booking.objects.create(
                first_name=first_name,
                reservation_date=parsed_date,
                reservation_slot=slot,
            )
    except IntegrityError:
        return JsonResponse(
            {"error": "This reservation slot is already booked. Please choose another time."},
            status=409,
        )

    return JsonResponse(
        {
            "message": "Booking successful.",
            "booking": {
                "id": booking.pk,
                "first_name": booking.first_name,
                "reservation_date": booking.reservation_date.isoformat(),
                "reservation_slot": booking.reservation_slot,
            },
        },
        status=201,
    )


@require_GET
def bookings_api(request):
    selected_date = request.GET.get("date")
    queryset = Booking.objects.all()

    if selected_date:
        try:
            date.fromisoformat(selected_date)
        except ValueError:
            return JsonResponse({"error": "Use date format YYYY-MM-DD."}, status=400)
        queryset = queryset.filter(reservation_date=selected_date)

    data = [
        {
            "id": booking.pk,
            "first_name": booking.first_name,
            "reservation_date": booking.reservation_date.isoformat(),
            "reservation_slot": booking.reservation_slot,
        }
        for booking in queryset.order_by("reservation_date", "reservation_slot")
    ]
    return JsonResponse(data, safe=False)


@require_GET
def reservations_page(request):
    return render(request, "restaurant/reservations.html")
