# Generated by Django 4.2.4 on 2024-03-19 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_disease_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='first_name',
            new_name='firstName',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='last_name',
            new_name='lastName',
        ),
    ]