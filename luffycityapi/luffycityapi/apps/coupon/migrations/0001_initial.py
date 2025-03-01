# Generated by Django 4.2.17 on 2025-03-01 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_activity_discounttype_discount_courseactivityprice'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, verbose_name='名称/标题')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('orders', models.IntegerField(default=0, verbose_name='序号')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('discount', models.SmallIntegerField(choices=[(1, '减免'), (2, '折扣')], default=1, verbose_name='优惠方式')),
                ('coupon_type', models.SmallIntegerField(choices=[(0, '通用类型'), (1, '指定方向'), (2, '指定分类'), (3, '指定课程')], default=0, verbose_name='优惠券类型')),
                ('total', models.IntegerField(blank=True, default=100, verbose_name='发放数量')),
                ('has_total', models.IntegerField(blank=True, default=100, verbose_name='剩余数量')),
                ('start_time', models.DateTimeField(verbose_name='启用时间')),
                ('end_time', models.DateTimeField(verbose_name='过期时间')),
                ('get_type', models.SmallIntegerField(choices=[(0, '系统赠送'), (1, '自行领取')], default=0, verbose_name='领取方式')),
                ('condition', models.IntegerField(blank=True, default=0, verbose_name='满足使用优惠券的价格条件')),
                ('per_limit', models.SmallIntegerField(default=1, verbose_name='每人限制领取数量')),
                ('sale', models.TextField(help_text='\n            *号开头表示折扣价，例如*0.82表示八二折；<br>\n            -号开头表示减免价,例如-10表示在总价基础上减免10元<br>   \n            ', verbose_name='优惠公式')),
            ],
            options={
                'verbose_name': '优惠券',
                'verbose_name_plural': '优惠券',
                'db_table': 'ly_coupon',
            },
        ),
        migrations.CreateModel(
            name='CouponLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('orders', models.IntegerField(default=0, verbose_name='序号')),
                ('is_show', models.BooleanField(default=True, verbose_name='是否显示')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='名称/标题')),
                ('use_time', models.DateTimeField(blank=True, null=True, verbose_name='使用时间')),
                ('use_status', models.SmallIntegerField(blank=True, choices=[(0, '未使用'), (1, '已使用'), (2, '已过期')], default=0, null=True, verbose_name='使用状态')),
                ('coupon', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='coupon.coupon', verbose_name='优惠券')),
                ('order', models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_coupon', to='orders.order', verbose_name='订单')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_coupon', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '优惠券发放和使用日志',
                'verbose_name_plural': '优惠券发放和使用日志',
                'db_table': 'ly_coupon_log',
            },
        ),
        migrations.CreateModel(
            name='CouponDirection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('coupon', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_direction', to='coupon.coupon', verbose_name='优惠券')),
                ('direction', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_coupon', to='courses.coursedirection', verbose_name='学习方向')),
            ],
            options={
                'verbose_name': '优惠券与学习方向',
                'verbose_name_plural': '优惠券与学习方向',
                'db_table': 'ly_coupon_course_direction',
            },
        ),
        migrations.CreateModel(
            name='CouponCourseCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('category', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_coupon', to='courses.coursecategory', verbose_name='课程分类')),
                ('coupon', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_category', to='coupon.coupon', verbose_name='优惠券')),
            ],
            options={
                'verbose_name': '优惠券与课程分类',
                'verbose_name_plural': '优惠券与课程分类',
                'db_table': 'ly_coupon_course_category',
            },
        ),
        migrations.CreateModel(
            name='CouponCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('coupon', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_course', to='coupon.coupon', verbose_name='优惠券')),
                ('course', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='to_coupon', to='courses.course', verbose_name='课程')),
            ],
            options={
                'verbose_name': '优惠券与课程信息',
                'verbose_name_plural': '优惠券与课程信息',
                'db_table': 'ly_coupon_course',
            },
        ),
    ]
