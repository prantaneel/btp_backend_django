# Generated by Django 4.2.5 on 2024-05-06 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream', '0002_process_error_prob'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='algo',
            field=models.CharField(default='LMS', max_length=20),
        ),
    ]