# Generated by Django 3.0.6 on 2021-01-11 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20210106_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('displayed', models.BooleanField(default=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('profile_from', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Profile')),
                ('profile_to', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Profile')),
            ],
        ),
    ]
