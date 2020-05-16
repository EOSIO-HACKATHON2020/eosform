# Generated by Django 3.0.6 on 2020-05-16 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_auto_20200516_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'DRAFT'), (2, 'PUBLISHED'), (3, 'DEACTIVATED')], default=1, verbose_name='Status'),
        ),
    ]
