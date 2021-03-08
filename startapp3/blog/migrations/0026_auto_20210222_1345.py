# Generated by Django 3.1.5 on 2021-02-22 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_post_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post_comment',
            options={'ordering': ['-date', '-date_time']},
        ),
        migrations.CreateModel(
            name='Report_Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('report_type', models.CharField(choices=[('N', 'Nagość'), ('T', 'Obraźliwa treść'), ('S', 'Spam'), ('I', 'Inne')], default='T', max_length=2)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]
