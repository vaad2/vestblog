import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vestblog.settings")
django.setup()

from django.conf import settings
from django.core.management import call_command
call_command('makemessages', verbosity=2, locale=[lng[0] for lng in settings.LANGUAGES], extensions=['j2', 'html'])

call_command('compilemessages', verbosity=2, locale=[lng[0] for lng in settings.LANGUAGES])
