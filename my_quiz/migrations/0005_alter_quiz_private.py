# Generated by Django 4.0.4 on 2022-06-18 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_quiz', '0004_remove_quiz_public_quiz_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='private',
            field=models.BooleanField(null=True),
        ),
    ]
