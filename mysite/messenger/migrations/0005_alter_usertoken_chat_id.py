# Generated by Django 4.2.1 on 2023-09-24 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_alter_usertoken_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='chat_id',
            field=models.IntegerField(null=True),
        ),
    ]
