# Generated by Django 4.1.7 on 2023-03-05 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_address_email_address_is_default_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('Out For Shipping', 'Out For Shipping'), ('Pending', 'Pending')], default='Pending', max_length=150),
        ),
    ]