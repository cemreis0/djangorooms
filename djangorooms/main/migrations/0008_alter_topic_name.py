# Generated by Django 4.0.4 on 2022-07-11 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_message_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.TextField(max_length=200),
        ),
    ]
