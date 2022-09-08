# Generated by Django 3.2.15 on 2022-09-08 03:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0002_usercategory_category_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercategory',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='mycategories', to=settings.AUTH_USER_MODEL),
        ),
    ]
