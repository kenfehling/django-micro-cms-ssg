# Generated by Django 4.0.5 on 2022-06-25 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='static/venus/uploads/cats')),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('subtitle', models.CharField(max_length=64)),
                ('header_image', models.ImageField(upload_to='static/venus/uploads')),
                ('about_text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
