# Generated by Django 4.1.2 on 2022-10-26 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
