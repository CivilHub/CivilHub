from django import template

from rest_framework.renderers import JSONRenderer

from ..serializers import LocationMapDataSerializer

register = template.Library()


@register.simple_tag(takes_context=True)
def current_location_data(context):
    """ Get data to use in map inputs - set initial center location and zoom.
        This values depends on location's kind and size.
    """
    location = context.get('location')
    if location is None:
        return JSONRenderer().render({})
    s = LocationMapDataSerializer(location)
    return JSONRenderer().render(s.data)
