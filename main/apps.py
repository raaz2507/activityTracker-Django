from django.apps import AppConfig

from django.db.models.signals import post_migrate

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals   # 👈 signals register हो जाएँगे

        # 👇 this code for insert dult activiye
        ''' 
        इसका फायदा ये होगा कि हर बार जब आप migrate करेंगे, तो आपका ACTIVITY_SCHEMA dictionary अपने-आप database में load हो जाएगा (duplicate create नहीं होगा, सिर्फ नए add होंगे)।
        '''
        from .models import activity_schema
        from .activityRecord_schema import ACTIVITY_SCHEMA
        from django.db.utils import IntegrityError
        from django.utils.text import slugify

        def insert_default_activities(sender, **kwargs):
            for key, value in ACTIVITY_SCHEMA.items():
                try:
                    activity_schema.objects.get_or_create(
                        activity_name=key,
                        defaults = {
                            'usr_id' : None,
                            "slug" : slugify(key),
                            "source": value['source'],
                            "trigger" : value['trigger'],
                            "extra": value.get('extra', {}),
                            "color_field": value.get('color', "#fff") or '#FFFFFF',
                            'icon': value.get('icon', 'Activity_icons/default_icon.svg') or 'Activity_icons/default_icon.svg',
                        }
                    )
                except IntegrityError:
                    pass # अगर पहले से है तो error ignore
        
        post_migrate.connect(insert_default_activities, sender=self)