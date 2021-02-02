# Generated by Django 3.0.6 on 2021-01-15 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20210114_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatbox',
            name='messages',
        ),
        migrations.AddField(
            model_name='chatbox',
            name='messages',
            field=models.ManyToManyField(related_name='_chatbox_messages_+', to='blog.ChatMessage'),
        ),
    ]
