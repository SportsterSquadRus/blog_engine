from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def likeOrNotTag(context, obj, user):
    if len(obj.likes.filter(user=user)) == 0:
        return True
    else:
        return False