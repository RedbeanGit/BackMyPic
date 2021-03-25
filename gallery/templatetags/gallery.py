from django import template
register = template.Library()


@register.filter
def index(indexable, i):
	return indexable[i]

	
@register.filter
def frontpage(num, page_size):
	return num % (page_size*2) < page_size