# Generated by Django 2.0.7 on 2018-07-19 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180719_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='blo_comment',
            field=models.IntegerField(default=0),
        ),
    ]
