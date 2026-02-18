from django import template

register = template.Library()

#to fix whitespaces when filtering with pagination
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    request = context['request']
    query = request.GET.copy()

    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()