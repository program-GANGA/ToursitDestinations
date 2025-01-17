# Generated by Django 4.2.16 on 2024-10-27 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tourist_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TouristImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('tourist_des', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_images', to='tourist_app.touristdes')),
            ],
        ),
    ]
