# Generated by Django 3.1.5 on 2021-02-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210129_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=4000)),
                ('owner', models.ManyToManyField(blank=True, related_name='_post_owner_+', to='blog.Profile')),
            ],
        ),
    ]
