# Generated by Django 2.2 on 2021-05-18 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('ideas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='user',
            field=models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, related_name='ideas', to='users.User'),
            preserve_default=False,
        ),
    ]
