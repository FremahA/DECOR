# Generated by Django 3.2.15 on 2022-09-08 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posts', '0001_initial'),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercategory',
            name='category_following',
            field=models.ManyToManyField(related_name='usercategory', to='posts.Category'),
        ),
    ]