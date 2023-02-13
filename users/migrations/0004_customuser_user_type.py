# Generated by Django 4.1.5 on 2023-02-13 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Customer', 'Customer'), ('Seller', 'Seller')], max_length=8, null=True),
        ),
    ]
