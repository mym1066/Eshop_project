# Generated by Django 4.0.3 on 2022-03-21 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otpcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='otpcode',
            options={'verbose_name': 'کد ارسالی ', 'verbose_name_plural': 'کدهای ارسالی'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
    ]
