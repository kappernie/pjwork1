# Generated by Django 4.2.4 on 2023-11-04 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0018_property_property_document_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="Location",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="property.location",
            ),
        ),
    ]
