# Generated by Django 4.1.7 on 2023-03-24 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30, unique=True)),
                ('base_address', models.URLField(default='', max_length=100)),
                ('format', models.CharField(blank=True, max_length=10)),
                ('params', models.JSONField(blank=True, default=dict, max_length=100)),
                ('token', models.JSONField(blank=True, default=dict, max_length=100)),
                ('switch_display_zones', models.BooleanField(default=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApiData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict, max_length=500)),
                ('tags', models.JSONField(default=dict, max_length=200)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='displayconf.api')),
            ],
        ),
    ]
