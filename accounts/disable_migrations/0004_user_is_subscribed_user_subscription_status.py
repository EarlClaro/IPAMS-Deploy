# Generated by Django 5.0.3 on 2024-05-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_student_student_id_alter_student_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_status',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
