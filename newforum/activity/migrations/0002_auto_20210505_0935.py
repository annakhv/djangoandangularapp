# Generated by Django 3.1.7 on 2021-05-05 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='deleteFromGetter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='deleteFromSender',
            field=models.BooleanField(default=False),
        ),
    ]