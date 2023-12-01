# Generated by Django 4.2.7 on 2023-12-01 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spents', '0008_subcash_earn_alter_earn_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='earn',
            old_name='money',
            new_name='dollars',
        ),
        migrations.AddField(
            model_name='earn',
            name='in_dollar',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spent',
            name='in_dollar',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]