# Generated by Django 4.1.2 on 2023-09-11 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_customers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customers',
            name='user',
        ),
        migrations.DeleteModel(
            name='Feedback',
        ),
        migrations.DeleteModel(
            name='Customers',
        ),
    ]