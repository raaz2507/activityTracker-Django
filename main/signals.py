import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import activity_schema

# 🟢 Update होने पर पुराना icon delete
@receiver(pre_save, sender=activity_schema)
def delete_old_icon(sender, instance, **kwargs):
    if not instance.pk:   # नया object है, कोई पुराना icon नहीं
        return
    
    try:
        old_instance = activity_schema.objects.get(pk=instance.pk)
    except activity_schema.DoesNotExist:
        return
    
    old_icon = old_instance.icon
    new_icon = instance.icon

    # default icon को delete मत करना
    if old_icon and old_icon != new_icon:
        if old_icon.name != "Activity_icons/preDefined/default_icon.svg":
            if os.path.isfile(old_icon.path):
                os.remove(old_icon.path)

# 🟢 Model delete होने पर icon delete
@receiver(post_delete, sender=activity_schema)
def delete_icon_on_delete(sender, instance, **kwargs):
    icon = instance.icon
    if icon:
        if icon.name != "Activity_icons/preDefined/default_icon.svg":   # default वाली फाइल को मत हटाना
            if os.path.isfile(icon.path):
                os.remove(icon.path)
