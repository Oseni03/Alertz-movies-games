# Generated by Django 4.1.1 on 2023-01-31 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("djstripe", "0011_2_7"),
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="subscription",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user",
                to="djstripe.subscription",
            ),
        ),
        migrations.AddField(
            model_name="customer",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="user",
                to="djstripe.customer",
            ),
        ),
    ]
