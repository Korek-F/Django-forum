# Generated by Django 3.0.6 on 2021-01-14 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_chatbox_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='chat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.ChatBox'),
        ),
        migrations.AlterField(
            model_name='chatbox',
            name='messages',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.ChatMessage'),
        ),
    ]