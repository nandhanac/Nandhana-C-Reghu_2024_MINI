# Generated by Django 3.0.5 on 2023-09-20 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0011_auto_20230920_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
