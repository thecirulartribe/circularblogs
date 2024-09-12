# Generated by Django 4.2.15 on 2024-08-10 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0009_alter_blog_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="author",
            field=models.CharField(
                choices=[
                    ("Shreyash", "Shreyash"),
                    ("Tanmay", "Tanmay"),
                    ("Prathmesh", "Prathmesh"),
                ],
                default=("Shreyash", "Shreyash"),
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="show_blog_at",
            field=models.CharField(
                choices=[("None", "None"), ("Main", "Main"), ("Side", "Side")],
                default=("None", "None"),
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="blog",
            name="sponsered",
            field=models.BooleanField(default=False),
        ),
    ]