from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.posts.models import Category

User = get_user_model()


class UserCategory(TimeStampedUUIDModel):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="mycategories")
    category_following = models.ManyToManyField(Category, related_name="usercategory")

    class Meta:
        verbose_name = _("User Category")
        verbose_name_plural = _("User Categories")


