# Generated by Django 5.0.7 on 2024-07-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0003_rename_emailrecieptsenaabled_webbform_emailrecieptsenabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='webbform',
            name='headerEnabled',
            field=models.BooleanField(default=True),
        ),
    ]
