# Generated by Django 5.0 on 2024-01-06 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_customuser_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pic',
            field=models.ImageField(blank=True, default='profile_pictures/default-profile.jpg', null=True, upload_to='profile_pictures/'),
        ),
    ]
