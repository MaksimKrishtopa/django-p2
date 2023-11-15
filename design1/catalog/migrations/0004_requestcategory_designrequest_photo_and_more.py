# Generated by Django 4.2.7 on 2023-11-15 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_designrequest_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='designrequest',
            name='photo',
            field=models.ImageField(default='design_photos/default.jpg', upload_to='design_photos/'),
        ),
        migrations.AddField(
            model_name='designrequest',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='designrequest',
            name='title',
            field=models.CharField(default='Title', max_length=255),
        ),
        migrations.AlterField(
            model_name='designrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=50),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
