# Generated by Django 3.1.5 on 2021-02-15 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20210215_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(related_name='_post_comments_+', to='blog.Post_comment'),
        ),
    ]