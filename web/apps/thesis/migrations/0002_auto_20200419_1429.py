# Generated by Django 3.0.5 on 2020-04-19 14:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thesis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thesis',
            name='pdf_file',
        ),
        migrations.AddField(
            model_name='thesis',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='thesis_author', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thesis',
            name='opponent',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='thesis_opponent', to=settings.AUTH_USER_MODEL,
                                    verbose_name='Opponent'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thesis',
            name='supervisor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='thesis_supervisor', to=settings.AUTH_USER_MODEL,
                                    verbose_name='Supervisor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='thesis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thesis_reservation',
                                    to='thesis.Thesis', verbose_name='Thesis for borrow'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thesis_category',
                                    to='thesis.Category'),
        ),
        migrations.AlterField(
            model_name='thesis',
            name='title',
            field=models.CharField(default='', max_length=128, verbose_name='Title'),
        ),
    ]