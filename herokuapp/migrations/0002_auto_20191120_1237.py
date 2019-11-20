# Generated by Django 2.1.7 on 2019-11-20 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herokuapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='userprofileinfo',
            name='name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='documents',
            name='authors',
            field=models.ManyToManyField(to='herokuapp.UserProfileInfo'),
        ),
    ]
