from django.template import loader, Context, Library

register = Library()


@register.simple_tag(takes_context=True)
def vote_area(context, obj):
    """ Create voting buttons and statistics. We provide common class names and
        Data parameters so that scripts can be easily added. Here, we determine
        the initial state of buttons.
    """
    template = loader.get_template('ideas/vote_area.html')
    if obj is None:
        return ''
    user = context['user']
    ctx = Context({'user': user, 'idea': obj, })
    if user.is_anonymous():
        pass
    elif len(obj.vote_set.filter(user=user, vote=True)):
        ctx.update({'voted_up': True, })
    elif len(obj.vote_set.filter(user=user, vote=False)):
        ctx.update({'voted_no': True, })
    return template.render(ctx)
