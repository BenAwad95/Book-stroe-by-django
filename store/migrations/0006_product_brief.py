# Generated by Django 3.0.7 on 2020-07-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brief',
            field=models.TextField(null=True),
        ),
    ]
