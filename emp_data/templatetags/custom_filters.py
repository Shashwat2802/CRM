from django import template

register = template.Library()

@register.filter
def extract_from_hashtag(value):
    if value:
        start_idx = value.find('#')
        end_idx = value.find('\n', start_idx) if start_idx != -1 else -1
        updated= value[start_idx+1:end_idx] if end_idx != -1 else value
        print("COncat,",start_idx,end_idx,updated)
        return updated
    return 'NA'
