# Generated by Django 5.0.4 on 2024-05-05 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobSearch_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]