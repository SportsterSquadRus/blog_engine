from django import template

register = template.Library()

@register.simple_tag
def likeOrNot(obj, user):
    if len(obj.likes.filter(user=user)) == 0:
        return True
    else:
        return False