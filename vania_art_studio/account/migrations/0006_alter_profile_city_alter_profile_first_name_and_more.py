# Generated by Django 4.1.3 on 2022-12-02 19:43

from django.db import migrations, models
import vania_art_studio.account.validators


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[vania_art_studio.account.validators.city_validator]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[vania_art_studio.account.validators.first_name_validator]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[vania_art_studio.account.validators.last_name_validator]),
        ),
    ]