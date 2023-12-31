# Generated by Django 4.2.4 on 2023-10-24 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "property",
            "0010_remove_property_rent_duration_required_if_for_rent_and_more",
        ),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="property",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("for_rent", True),
                        ("min_rent_duration__isnull", False),
                        ("max_rent_duration__isnull", False),
                    ),
                    models.Q(
                        ("for_rent", False),
                        ("min_rent_duration__isnull", True),
                        ("max_rent_duration__isnull", True),
                    ),
                    _connector="OR",
                ),
                name="rent_duration_required_if_for_rent",
            ),
        ),
    ]
