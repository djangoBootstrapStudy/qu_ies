# Generated by Django 4.0.4 on 2022-06-18 09:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_quiz", "0005_alter_quiz_private"),
    ]

    operations = [
        migrations.AddField(
            model_name="quiz",
            name="create_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="quiz",
            name="update_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
