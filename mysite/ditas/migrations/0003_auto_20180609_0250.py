# Generated by Django 2.0.5 on 2018-06-08 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ditas', '0002_auto_20180607_0004'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meal',
            old_name='f_id',
            new_name='food',
        ),
        migrations.AlterUniqueTogether(
            name='meal',
            unique_together={('user', 'food', 'f_time')},
        ),
    ]
