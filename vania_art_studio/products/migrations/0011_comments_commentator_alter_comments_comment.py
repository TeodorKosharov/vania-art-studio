# Generated by Django 4.1.3 on 2022-12-07 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='commentator',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
