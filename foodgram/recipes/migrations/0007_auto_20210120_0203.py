# Generated by Django 3.0.5 on 2021-01-19 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20210120_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
