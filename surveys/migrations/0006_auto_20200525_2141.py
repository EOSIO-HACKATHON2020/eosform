# Generated by Django 3.0.6 on 2020-05-25 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20200525_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'DRAFT'), (2, 'PUBLISHED'), (3, 'DELETED')], default=1, verbose_name='Status'),
        ),
    ]
