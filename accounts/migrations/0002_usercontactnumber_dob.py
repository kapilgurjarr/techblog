# Generated by Django 4.2 on 2023-04-17 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontactnumber',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
