# Generated by Django 4.2.4 on 2023-10-25 07:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0006_alter_plan_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentsubscription",
            name="status",
            field=models.SmallIntegerField(
                choices=[
                    (1, "Active"),
                    (2, "Non renewing"),
                    (3, "Attention"),
                    (4, "Completed"),
                    (5, "Cancelled"),
                ],
                default=1,
            ),
        ),
    ]