# Generated by Django 2.0 on 2017-12-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20171231_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='phone',
            name='id',
            field=models.AutoField(auto_created=True, default=None, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='phone',
            name='number',
            field=models.IntegerField(),
        ),
    ]
