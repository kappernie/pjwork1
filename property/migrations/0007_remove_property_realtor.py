# Generated by Django 4.2.4 on 2023-10-18 09:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0006_alter_property_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="property",
            name="realtor",
        ),
    ]
