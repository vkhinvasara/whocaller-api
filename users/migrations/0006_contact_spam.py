# Generated by Django 5.0.6 on 2024-05-30 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_contact_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='spam',
            field=models.BooleanField(default=False),
        ),
    ]
