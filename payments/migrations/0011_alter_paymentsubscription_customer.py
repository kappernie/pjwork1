# Generated by Django 4.2.4 on 2023-11-04 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_lister_business_document"),
        ("payments", "0010_alter_plan_interval"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentsubscription",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.renter"
            ),
        ),
    ]