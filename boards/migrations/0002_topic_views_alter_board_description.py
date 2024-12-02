# Generated by Django 5.1.2 on 2024-11-01 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='board',
            name='description',
            field=models.CharField(max_length=150),
        ),
    ]
