# Generated by Django 4.2.4 on 2023-10-24 09:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_lister_delete_realtor"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Agent",
        ),
    ]
