# Generated by Django 4.1 on 2022-08-17 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userfeatures', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projecttags',
            name='style',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
