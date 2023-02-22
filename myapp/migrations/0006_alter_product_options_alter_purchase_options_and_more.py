# Generated by Django 4.1.6 on 2023-02-20 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_return_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='purchase',
            options={'ordering': ['-purchase_date'], 'verbose_name': 'purchase', 'verbose_name_plural': 'purchases'},
        ),
        migrations.AlterModelOptions(
            name='return',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='return',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
