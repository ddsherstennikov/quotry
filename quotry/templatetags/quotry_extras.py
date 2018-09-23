from django import template
from quotry.models import Tag

register = template.Library()

@register.inclusion_tag('quotry/tags.html')
def get_tag_list(tag=None):
    return {'tags': Tag.objects.all(), 'act_tag': tag}