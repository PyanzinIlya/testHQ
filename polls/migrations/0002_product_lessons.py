# Generated by Django 4.2.5 on 2023-09-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='lessons',
            field=models.ManyToManyField(to='polls.lesson'),
        ),
    ]
