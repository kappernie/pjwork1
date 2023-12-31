# Generated by Django 4.2.4 on 2023-11-03 23:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0017_alter_propertytype_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="property_document",
            field=models.FileField(
                blank=True, null=True, upload_to="uploads/documents/property"
            ),
        ),
        migrations.AddField(
            model_name="property",
            name="property_types_text",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
