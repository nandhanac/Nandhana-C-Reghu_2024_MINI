# Generated by Django 3.0.5 on 2023-09-20 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0009_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='mechanic',
            name='job_title',
            field=models.CharField(choices=[('mechanic', 'Mechanic'), ('painter', 'Painter')], default='choice title', max_length=20),
        ),
    ]
