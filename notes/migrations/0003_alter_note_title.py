# Generated by Django 4.0.2 on 2022-02-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_label_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]