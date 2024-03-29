# Generated by Django 3.1.7 on 2021-03-25 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socialaccounts', to='network.network')),
            ],
            options={
                'ordering': ('-updated_date',),
            },
        ),
    ]
