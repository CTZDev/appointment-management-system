# Generated by Django 5.1.3 on 2024-12-02 23:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_person_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='is_active',
        ),
    ]
