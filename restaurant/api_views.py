from django.db import IntegrityError, transaction
from rest_framework import generics, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking, Menu
from .serializers import BookingSerializer, MenuSerializer, RegistrationSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Guests may list and create reservations; editing/deleting requires login.
        if request.method in ("GET", "HEAD", "OPTIONS", "POST"):
            return True
        return bool(request.user and request.user.is_authenticated)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [BookingPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        date_value = self.request.query_params.get("date")
        if date_value:
            queryset = queryset.filter(reservation_date=date_value)
        return queryset

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)
        except IntegrityError:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"reservation_slot": "This date and time slot is already booked."})


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ObtainTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"detail": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
