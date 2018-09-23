import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qsite.settings')

import django
django.setup()

from quotry.models import Tag, Quote

def depopulate():
    Quote.objects.all().delete()
    Tag.objects.all().delete()

    # Print out what we have deleted
    print "Content is empty.\nAll Quotes and Tags have been erased."



# Start execution here!
if __name__ == '__main__':
    print "Starting quotrY depopulation script..."
    depopulate()