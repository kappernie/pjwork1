# Generated by Django 4.2.4 on 2023-10-24 11:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0009_property_for_rent_property_rent_duration_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="property",
            name="rent_duration_required_if_for_rent",
        ),
        migrations.RemoveField(
            model_name="property",
            name="rent_duration",
        ),
        migrations.AddField(
            model_name="property",
            name="max_rent_duration",
            field=models.IntegerField(blank=True, default=36, null=True),
        ),
        migrations.AddField(
            model_name="property",
            name="min_rent_duration",
            field=models.IntegerField(blank=True, default=12, null=True),
        ),
    ]
