# Generated by Django 5.1.2 on 2024-10-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycontact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='content',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='contact',
            name='surname',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
