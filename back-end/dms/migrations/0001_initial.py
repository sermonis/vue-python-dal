# Generated by Django 3.1.3 on 2020-11-13 17:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dms.models
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.FileField(blank=True, upload_to=dms.models.upload_to)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Publisher',
                'verbose_name_plural': 'Publishers',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Section',
                'verbose_name_plural': 'Sections',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('title', models.CharField(max_length=255)),
                ('annotation', models.TextField(blank=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.section')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('annotation', models.TextField(blank=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.AddField(
            model_name='section',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.subject'),
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('annotation', models.TextField(blank=True)),
                ('publication_date', models.DateField(default=datetime.date.today)),
                ('authors', models.ManyToManyField(blank=True, to='dms.Author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='dms.category')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.file')),
                ('publishers', models.ManyToManyField(blank=True, to='dms.Publisher')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Paper',
                'verbose_name_plural': 'Papers',
            },
        ),
        migrations.CreateModel(
            name='ClassMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('annotation', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('LE', 'lectures'), ('SE', 'seminars'), ('GR', 'groups'), ('PR', 'practices')], max_length=2)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.file')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.topic')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Class Material',
                'verbose_name_plural': 'Class Materials',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('annotation', models.TextField(blank=True)),
                ('publication_year', models.PositiveSmallIntegerField(default=dms.models.current_year)),
                ('authors', models.ManyToManyField(blank=True, to='dms.Author')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dms.file')),
                ('publishers', models.ManyToManyField(blank=True, to='dms.Publisher')),
                ('subjects', models.ManyToManyField(blank=True, to='dms.Subject')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
