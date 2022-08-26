from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from apps.common.models import TimeStampedUUIDModel
from apps.users.models import Profile


User = get_user_model()

class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PostPublishedManager, self)
            .get_queryset()
            .filter(is_published=True)
        )


class Category(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Post(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    photo = models.ImageField(verbose_name=_("Photo"), null=False, blank=False)
    title = models.CharField(verbose_name=_("Post Title"), null=False, max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    description = models.TextField(verbose_name=_("Description"), default="say something about your post")
    website = models.URLField(verbose_name=_("Website"), null=True)
    category = models.ManyToManyField(Category, blank=False)
    is_published = models.BooleanField(verbose_name=_("Published Status"), default=False)
    saves = models.IntegerField(verbose_name=_("Total Saves"), default=0)

    objects = models.Manager()
    published = PostPublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Post") 
        verbose_name_plural = _("Posts")


class PostSaves(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_saves')
    post = models.ForeignKey(Post, related_name="post_saves", on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"Total saves of - {self.post.title} is - {self.post.saves} save(s)"
        )

    class Meta:
        verbose_name = _("Total Saves of Post")
        verbose_name_plural = _("Total Post Saves")