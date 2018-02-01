# Generated by Django 2.0 on 2018-01-05 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_post_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Photo')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Chat')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Photo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.Profile')),
            ],
        ),
    ]