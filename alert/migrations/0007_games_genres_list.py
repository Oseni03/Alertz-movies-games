# Generated by Django 4.1.1 on 2023-02-12 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0006_games_platform_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="games",
            name="genres_list",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]