# Generated by Django 4.2.17 on 2025-02-16 08:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='详情介绍'),
        ),
        migrations.AlterField(
            model_name='coursecategory',
            name='remark',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True, verbose_name='分类描述'),
        ),
        migrations.AlterField(
            model_name='coursechapter',
            name='summary',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='章节介绍'),
        ),
        migrations.AlterField(
            model_name='coursedirection',
            name='remark',
            field=ckeditor.fields.RichTextField(blank=True, default='', null=True, verbose_name='方向描述'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='brief',
            field=ckeditor.fields.RichTextField(max_length=1024, verbose_name='讲师描述'),
        ),
    ]
