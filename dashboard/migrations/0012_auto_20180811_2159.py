# Generated by Django 2.0.7 on 2018-08-12 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20180811_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='grade',
            field=models.IntegerField(help_text='Enter grade (ex. 83)'),
        ),
    ]