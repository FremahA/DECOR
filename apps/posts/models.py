from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField
from apps.common.models import TimeStampedUUIDModel


User = get_user_model()


class PostPublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super(PostPublishedManager, self)
            .get_queryset()
            .filter(is_published=True)
        )


class Category(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50, unique=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Post(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='posts')
    photo = models.ImageField(verbose_name=_("Photo"), default="interior_sample.jpg", upload_to="media", null=True, blank=True)
    title = models.CharField(verbose_name=_("Post Title"), null=False, max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    description = models.TextField(verbose_name=_("Description"), default="say something about your post")
    website = models.URLField(verbose_name=_("Website"), null=True)
    is_published = models.BooleanField(verbose_name=_("Published Status"), default=False)
    saves = models.IntegerField(verbose_name=_("Post Saves"), default=0)
    category = models.ManyToManyField(Category)

    objects = models.Manager()
    published = PostPublishedManager()

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Post") 
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title


class PostSaves(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, editable=False)

    class Meta:
        unique_together = ("user", "post")
        verbose_name = _("Total Saves of Post")
        verbose_name_plural = _("Total Post Saves")

    def __str__(self):
        return (f"Total saves of - {self.post.title} is - {self.post.saves}")
