# Generated by Django 3.2.2 on 2021-06-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_items_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='featured',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
