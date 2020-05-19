# Generated by Django 3.0.5 on 2020-04-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thesis', '0007_auto_20200425_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='state',
            field=models.CharField(choices=[('created', 'Created'), ('ready', 'Ready for pickup'), ('running', 'Running'), ('finished', 'Finished')], default='created', max_length=32, verbose_name='State'),
        ),
    ]