# Generated by Django 4.2.4 on 2024-03-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_disease_datasetname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='datasetName',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
