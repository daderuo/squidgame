# Generated by Django 4.0 on 2021-12-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_match_turn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='turn',
            field=models.IntegerField(default=0.42928140821997196),
        ),
    ]