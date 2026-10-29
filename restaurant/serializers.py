from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Booking, Menu

User = get_user_model()


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "title", "price", "inventory"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "first_name", "reservation_date", "reservation_slot"]
        read_only_fields = ["id"]

    def validate_reservation_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Reservations cannot be made for a past date.")
        return value


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
