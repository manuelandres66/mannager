# Generated by Django 4.2.7 on 2023-11-25 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spents', '0004_alter_earn_date_alter_spent_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('total', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='earn',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='earn',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='spent',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='spent',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='earn',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spents.account'),
        ),
        migrations.AddField(
            model_name='spent',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spents.account'),
        ),
    ]
