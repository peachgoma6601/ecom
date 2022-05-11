# Generated by Django 4.0.4 on 2022-05-09 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('catagory_name', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=50)),
                ('catagory_image', models.ImageField(blank=True, upload_to='images/catagory')),
            ],
            options={
                'verbose_name': 'Catagory',
                'verbose_name_plural': 'Catagories',
            },
        ),
    ]