# Generated by Django 4.0.1 on 2022-01-28 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.user'),
        ),
    ]
