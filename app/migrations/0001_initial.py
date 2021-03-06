# Generated by Django 2.0.3 on 2018-03-22 22:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Mileage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('value', models.IntegerField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.AddField(
            model_name='mileage',
            name='series',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.Series'),
        ),
    ]
