# Generated by Django 4.1.1 on 2023-02-11 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="newsletter",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]