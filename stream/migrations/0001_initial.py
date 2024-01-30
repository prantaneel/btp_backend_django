# Generated by Django 4.2.5 on 2024-01-16 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device_id', models.CharField(max_length=100)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_id', models.CharField(max_length=20, unique=True)),
                ('strategy', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iteration', models.FloatField()),
                ('high_cost_data', models.FloatField(null=True)),
                ('low_cost_data', models.JSONField()),
                ('w_iter', models.JSONField()),
                ('mse', models.FloatField(default=0)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.device')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.process')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.process'),
        ),
        migrations.CreateModel(
            name='ConsolidatedMSE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iteration', models.FloatField()),
                ('mse_array', models.JSONField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.device')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.process')),
            ],
        ),
    ]