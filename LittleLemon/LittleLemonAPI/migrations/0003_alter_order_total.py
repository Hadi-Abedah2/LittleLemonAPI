# Generated by Django 4.2.4 on 2023-08-09 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0002_userproxy_alter_category_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total",
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
