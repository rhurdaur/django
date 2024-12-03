""" 
einen eigenen Filter anlegen, der im Template so genutzt werden kann:

{% if user|is_member:"Moderatoren" %}

(Prüfen, ob User Mitglieder einer bestimmten Gruppe)
"""

from django import template

register = template.Library()


@register.filter(name="is_member")
def is_member(user, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()