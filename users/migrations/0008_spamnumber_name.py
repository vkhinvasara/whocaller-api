# Generated by Django 5.0.6 on 2024-05-30 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_spamnumber'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamnumber',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]