# Generated by Django 4.2.4 on 2023-10-31 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0015_alter_propertyimage_property_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="currency",
            field=models.CharField(choices=[("GHS", "GHS")], max_length=200, null=True),
        ),
    ]
