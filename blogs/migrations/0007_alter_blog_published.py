# Generated by Django 4.2.16 on 2025-03-14 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0006_blog_revert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]
