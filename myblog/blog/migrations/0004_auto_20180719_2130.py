# Generated by Django 2.0.7 on 2018-07-19 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_blo_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='blo_comment',
            new_name='blog_comment',
        ),
    ]
