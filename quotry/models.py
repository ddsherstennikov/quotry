from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Tag(models.Model):

    class Meta:
        verbose_name_plural = "Tags"

    # payload
    name    = models.CharField(blank=False, max_length=128, unique=True)

    # for ranging
    visits  = models.IntegerField(default=0)
    favs    = models.IntegerField(default=0)

    # tech
    slug    = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Quote(models.Model):

    # org
    tag     = models.ForeignKey(Tag)

    # payload required
    author  = models.CharField(blank=False, max_length=128)
    text    = models.TextField(blank=False)

    # payload addon
    title   = models.CharField(blank=True, max_length=128)
    url     = models.URLField(blank=True)

    # ranging
    likes   = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # if title is '' or None
        if not self.title:
            self.title = self.author + ": " + self.text[:100]
            if len(self.text) > 100:
                self.title += "..."
        super(Quote, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):

    # tech and payload
    user    = models.OneToOneField(User)

    # org
    favs    = models.ManyToManyField(Tag, blank=True)
    likes   = models.ManyToManyField(Quote, blank=True)

    # addon payload
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
