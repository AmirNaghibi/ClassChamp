# Generated by Django 2.0.7 on 2018-07-23 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20180723_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grades',
            name='course',
            field=models.ForeignKey(help_text='choose the course for the grade', on_delete=django.db.models.deletion.CASCADE, to='dashboard.Course'),
        ),
    ]