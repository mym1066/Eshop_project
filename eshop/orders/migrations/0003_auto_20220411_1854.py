# Generated by Django 3.2.12 on 2022-04-11 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20220403_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'تخفیف ', 'verbose_name_plural': 'تخفیفات'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('paid', '-updated'), 'verbose_name': 'سفارش ', 'verbose_name_plural': 'سفارشات'},
        ),
    ]
