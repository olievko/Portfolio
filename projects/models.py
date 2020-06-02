from django.db import models
from django.utils import timezone
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class PersonalInfo(models.Model):

    class Meta:
        verbose_name_plural = "Personal Info"

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    career = models.CharField(
        max_length=255,
        help_text="Illustrator and Web designer")
    overview = models.TextField()
    photo = models.ImageField(
        upload_to='users/%Y/%m/%d/',
        blank=True,
        null=True)
    years_experience = models.IntegerField(default=False)
    partners = models.IntegerField(default=False)
    completed_projects = models.IntegerField(default=False)
    clients = models.IntegerField(
        default=False,
        help_text="e.g., amount of clients")
    locality = models.CharField(
        max_length=255,
        help_text="e.g., city such as Kyiv")
    country = models.CharField(
        max_length=64,
        help_text="e.g., Ukraine")
    email = models.EmailField()
    phone = models.IntegerField(default=False)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    skype = models.CharField(
        max_length=255,
        help_text="skype: user_name", blank=True)
    linkedin = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)
    resume_file = models.FileField(
        upload_to='resume/%Y/%m/%d/',
        blank=True)
    meta_keywords = models.CharField(
        "Meta Keywords",
        max_length=255,
        null=True,
        blank=True,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.TextField(
        "Meta Description",
        max_length=255,
        null=True,
        blank=True,
        help_text='Content for description meta tag, maximum are 200 characters')

    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    def __str__(self):
        return self.full_name()


class Skill(models.Model):

    class Meta:
        ordering = ('name',)

    name = models.CharField(
        max_length=250,
        help_text="e.g., C++, Python, Java, JavaScript")
    slug = models.SlugField(
        max_length=250,
        blank=True)
    level = models.IntegerField(
        default=False,
        help_text="e.g., Indicate your level skills in percentage")

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Project(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        unique=True)
    image = models.ImageField(
        upload_to=image_folder,
        blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1000, 1280)],
        format='JPEG',
        options={'quality': 90})
    thumb = ImageSpecField(
        source='image',
        processors=[ResizeToFill(400, 400)],
        format='JPEG',
        options={'quality': 90})
    description = models.TextField(blank=True)
    technology = models.CharField(max_length=20)
    meta_keywords = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.TextField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Content for description meta tag, maximum are 200 characters')
    publish = models.DateTimeField(default=timezone.now)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    object = models.Manager()
    published = PublishedManager()
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='project_likes',
        blank=True)
    total_likes = models.PositiveIntegerField(
        db_index=True,
        default=0)

    class Meta:
        ordering = ('-added',)
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('project_detail',
                       args=[self.pk, self.slug])


def another_image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return "{0}/{1}".format(instance.slug, filename)


class Images(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.ImageField(
        upload_to=another_image_folder,
        blank=True)
    caption = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=70,
        null=True)
    added = models.DateTimeField(
        auto_now_add=True,
        db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.caption

    def get_absolute_url(self):
        return reverse('images_detail', args=[self.id, self.slug])


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comment_created',
        on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='comments')
    name = models.CharField(
        _('name'),
        max_length=80)
    email = models.EmailField(_('email'))
    body = models.TextField(_('body'))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.project)


class Testimonial(models.Model):
    first_name_client = models.CharField(
        max_length=255,
        default="Jane")
    last_name_client = models.CharField(
        max_length=255,
        default="Doe")
    photo_clients = models.ImageField(
        upload_to='clients/%Y/%m/%d/',
        blank=True)
    position_client = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g., CEO at Mighty Schools")
    body = models.TextField(
        blank=True,
        help_text="e.g., Natalia Dozor is just awesome. I am so happy to have met her!")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def full_name(self):
        return " ".join([self.first_name_client, self.last_name_client])

    def __str__(self):
        return self.full_name()


class Price(models.Model):
    TYPE_CHOICES = (
        ('Basic', 'Basic'),
        ('Pro', 'Pro'))
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='Basic')
    instrument = models.CharField(
        max_length=255,
        default="Adobe Illustrator")
    description = models.TextField(
        blank=True,
        help_text="Logo, newsletter, business cards...")
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2)
    active = models.BooleanField(default=True)

