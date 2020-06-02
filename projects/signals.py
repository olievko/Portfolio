from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Project


@receiver(m2m_changed, sender=Project.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()

