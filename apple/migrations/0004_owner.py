# Generated by Django 3.2.8 on 2021-12-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apple', '0003_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=1000)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]