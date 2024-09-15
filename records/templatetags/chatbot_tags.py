from django import template

register = template.Library()

@register.inclusion_tag('templates/chatbot.html')
def render_chatbot_component(template_name='chatbot.html'):
    return {}
