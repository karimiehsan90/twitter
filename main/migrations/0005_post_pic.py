# Generated by Django 2.0 on 2018-01-02 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180102_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main.Photo'),
        ),
    ]
