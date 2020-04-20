# Generated by Django 3.0.5 on 2020-04-20 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thesis', '0003_auto_20200419_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='for_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='reservation_for_user', to=settings.AUTH_USER_MODEL, verbose_name='For user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thesis_reservation', to='thesis.Thesis', verbose_name='Thesis for borrow'),
        ),
    ]