# Generated by Django 5.1.5 on 2025-02-04 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sphere', '0002_alter_comment_options_alter_contact_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reactions',
            field=models.JSONField(default=dict),
        ),
    ]
