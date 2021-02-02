# Generated by Django 3.0.6 on 2021-01-14 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_friendinvitation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendinvitation',
            name='profile_from',
        ),
        migrations.AddField(
            model_name='friendinvitation',
            name='profile_from',
            field=models.ManyToManyField(null=True, related_name='_friendinvitation_profile_from_+', to='blog.Profile'),
        ),
        migrations.RemoveField(
            model_name='friendinvitation',
            name='profile_to',
        ),
        migrations.AddField(
            model_name='friendinvitation',
            name='profile_to',
            field=models.ManyToManyField(null=True, related_name='_friendinvitation_profile_to_+', to='blog.Profile'),
        ),
    ]
