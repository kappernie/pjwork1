# Generated by Django 4.2.4 on 2023-08-03 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("property", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("settled", models.BooleanField(default=False)),
                ("settlement_date", models.DateTimeField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="property.property",
                    ),
                ),
                (
                    "renter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.renter"
                    ),
                ),
            ],
        ),
    ]
