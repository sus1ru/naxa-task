# Generated by Django 3.2.17 on 2023-02-05 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('P', 'present'), ('p', 'present'), ('A', 'absent'), ('a', 'absent')], default='A', max_length=1),
        ),
    ]