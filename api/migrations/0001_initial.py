# Generated by Django 2.1.1 on 2018-09-26 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KakaoUser',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_key', models.CharField(max_length=190, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackageQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('HBL', 'HBL / 운송장번호'), ('MBL', 'MBL'), ('CRG', '화물관리번호')], db_index=True, max_length=3)),
                ('tracking_number', models.CharField(max_length=190)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.KakaoUser')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
