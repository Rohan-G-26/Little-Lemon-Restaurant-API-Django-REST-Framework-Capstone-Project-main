# Generated for the Little Lemon capstone starter project.
import django.core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Menu",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ("inventory", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["title"]},
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("first_name", models.CharField(max_length=100)),
                ("reservation_date", models.DateField()),
                ("reservation_slot", models.PositiveSmallIntegerField(choices=[(hour, f"{hour:02d}:00") for hour in range(10, 22)], validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(21)])),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="bookings", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["reservation_date", "reservation_slot"]},
        ),
        migrations.AddConstraint(model_name="booking", constraint=models.UniqueConstraint(fields=("reservation_date", "reservation_slot"), name="unique_booking_date_slot")),
    ]
