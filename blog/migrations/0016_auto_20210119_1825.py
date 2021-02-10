# Generated by Django 3.0.6 on 2021-01-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_profile_chats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatbox',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='chatbox',
            name='user2',
        ),
        migrations.AddField(
            model_name='chatbox',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='_chatbox_users_+', to='blog.Profile'),
        ),
    ]