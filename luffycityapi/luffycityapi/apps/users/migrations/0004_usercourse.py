# Generated by Django 4.2.17 on 2025-03-11 19:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_credit'),
        ('users', '0003_credit'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_time', models.IntegerField(default=0, verbose_name='学习时长')),
                ('chapter', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_chapter', to='courses.coursechapter', verbose_name='章节')),
                ('course', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='course_users', to='courses.course', verbose_name='课程名称')),
                ('lesson', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_lesson', to='courses.courselesson', verbose_name='课时')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_courses', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户购买课程记录',
                'verbose_name_plural': '用户购买课程记录',
                'db_table': 'lf_user_courses',
            },
        ),
    ]
