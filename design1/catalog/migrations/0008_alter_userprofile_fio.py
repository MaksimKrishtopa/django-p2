# Generated by Django 4.2.7 on 2023-11-16 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_userprofile_delete_designrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fio',
            field=models.CharField(max_length=255),
        ),
    ]