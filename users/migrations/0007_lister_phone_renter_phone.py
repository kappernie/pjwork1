# Generated by Django 4.2.4 on 2023-10-24 10:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_delete_agent"),
    ]

    operations = [
        migrations.AddField(
            model_name="lister",
            name="phone",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="renter",
            name="phone",
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]