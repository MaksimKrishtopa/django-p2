# Generated by Django 4.2.7 on 2023-11-17 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_designcategory_designrequest_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designrequest',
            name='status',
            field=models.CharField(choices=[('Новая', 'Новая'), ('Принято в работу', 'Принято в работу'), ('Выполнено', 'Выполнено')], default='Новая', max_length=20),
        ),
    ]
