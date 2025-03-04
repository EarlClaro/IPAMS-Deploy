# Generated by Django 5.0.4 on 2024-05-20 16:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('plan_id', models.IntegerField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(blank=True, max_length=50, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('duration_months', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('sub_id', models.IntegerField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('user_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('plan_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='records.subscriptionplan')),
            ],
        ),
    ]
