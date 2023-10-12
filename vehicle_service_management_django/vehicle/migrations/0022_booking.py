# Generated by Django 4.2.5 on 2023-10-08 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0021_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('customer_name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=20)),
                ('selected_service_image', models.ImageField(upload_to='service_images/')),
                ('selected_service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('selected_subsubcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.subsubcategory')),
            ],
        ),
    ]