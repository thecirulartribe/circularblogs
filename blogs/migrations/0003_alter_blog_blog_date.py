# Generated by Django 4.2.14 on 2024-07-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_blog_blog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]