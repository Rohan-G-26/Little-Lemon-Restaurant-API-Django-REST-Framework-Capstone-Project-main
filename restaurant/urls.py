from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import BookingViewSet, MenuViewSet, ObtainTokenView, RegisterView, LogoutView

router = DefaultRouter()
router.register("menu", MenuViewSet, basename="menu")
router.register("booking/tables", BookingViewSet, basename="booking-tables")

urlpatterns = [
    path("", views.home, name="home"),
    path("book/", views.book, name="book"),
    path("bookings", views.bookings_api, name="bookings_api"),
    path("reservations/", views.reservations_page, name="reservations"),
    path("api/", include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="api-register"),
    path("api/auth/token/", ObtainTokenView.as_view(), name="api-token"),
    path("api/auth/logout/", LogoutView.as_view(), name="api-logout"),
]
