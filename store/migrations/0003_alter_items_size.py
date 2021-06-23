# Generated by Django 3.2.2 on 2021-06-22 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_banner_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='size',
            field=models.CharField(choices=[('K', 'King - 108 x 120'), ('Q', 'Queen - 90 x 108')], default='K', max_length=1),
        ),
    ]
