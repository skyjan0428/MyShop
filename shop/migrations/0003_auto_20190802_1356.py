# Generated by Django 2.2.3 on 2019-08-02 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]