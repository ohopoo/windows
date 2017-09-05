from django import template

import hashlib

register = template.Library()

@register.filter(name='gavatar')
def gavatar(email, size):
    return 'https://www.gravatar.com/avatar/{0}?d=identicon&s={1}'.format(hashlib.md5(email.encode('utf-8')).hexdigest(), size)