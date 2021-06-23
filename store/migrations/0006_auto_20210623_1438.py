# Generated by Django 3.2.2 on 2021-06-23 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_rename_available_items_availablity'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='category',
            field=models.CharField(choices=[('B', 'Bedsheet'), ('D', 'Dohar')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='items',
            name='size',
            field=models.CharField(choices=[('K', 'King - 108 x 120'), ('Q', 'Queen - 90 x 108'), ('S', 'Single'), ('D', 'Double')], default='K', max_length=1),
        ),
    ]
