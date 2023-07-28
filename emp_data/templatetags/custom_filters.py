from django import template

register = template.Library()

@register.filter
def extract_from_hashtag(value):
    if value:
        start_idx = value.find('#')
        end_idx = value.find('\n', start_idx) if start_idx != -1 else -1
        updated= value[start_idx+1:end_idx] if end_idx != -1 else value
        return updated
    return 'NA'

@register.filter
def combined_list(list1,list2):
    return zip(list1,list2)
