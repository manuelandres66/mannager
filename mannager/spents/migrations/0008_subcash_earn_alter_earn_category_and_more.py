# Generated by Django 4.2.7 on 2023-11-29 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spents', '0007_alter_account_total_pesos_alter_spent_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcash',
            name='earn',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='spents.earn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='earn',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='spents.earncategory'),
        ),
        migrations.AlterField(
            model_name='spent',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='spents.spentcategory'),
        ),
    ]