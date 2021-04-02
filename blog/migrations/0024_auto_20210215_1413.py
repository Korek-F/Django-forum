# Generated by Django 3.1.5 on 2021-02-15 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20210213_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date', '-date_time']},
        ),
        migrations.CreateModel(
            name='Post_comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=2000)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]