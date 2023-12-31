# Generated by Django 4.2.4 on 2023-10-27 15:30

from django.db import migrations, models
import property.models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0011_property_rent_duration_required_if_for_rent"),
    ]

    operations = [
        migrations.AlterField(
            model_name="propertyimage",
            name="upload",
            field=models.ImageField(
                upload_to=property.models.get_property_images_upload_path
            ),
        ),
    ]
