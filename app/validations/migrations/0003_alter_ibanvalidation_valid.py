# Generated by Django 3.2.19 on 2023-05-19 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('validations', '0002_alter_ibanvalidation_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ibanvalidation',
            name='valid',
            field=models.BooleanField(default=None, null=True),
        ),
    ]