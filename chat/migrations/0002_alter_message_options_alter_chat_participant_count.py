# Generated by Django 4.0.1 on 2022-01-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('time_created',)},
        ),
        migrations.AlterField(
            model_name='chat',
            name='participant_count',
            field=models.IntegerField(default=1),
        ),
    ]
