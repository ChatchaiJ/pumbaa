'''
Created on Oct 20, 2013

@author: boatkrap
'''
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

from pumbaa import models, forms

@view_config(route_name='manager.pages.index', 
             renderer='/manager/pages/index.mako')
def index(request):
    topics = models.Topic.objects(status__ne='delete', page=True).all()
    return dict(
                topics=topics
                )

@view_config(route_name='manager.pages.compose', 
             permission='page',
             renderer='/manager/pages/compose.mako')
@view_config(route_name='manager.pages.edit', 
             permission='page',
             renderer='/manager/pages/compose.mako')
def compose(request):
    form = forms.topics.Page(request.POST)
    
    topic_id = request.matchdict.get('topic_id', None)
    if len(request.POST) > 0 and form.validate():
        title = form.data.get('title')
        description = form.data.get('description')
        tags = [tag.strip() for tag in form.data.get('tags').split(',')]
        comments_disable = form.data.get('comments_disable', None)
    else:
        form.data['comments_disable'] = 'disable'
        
        if topic_id is not None:
            topic = models.Topic.objects(id=topic_id).first()
            form.title.data = topic.title
            form.description.data = topic.description
            form.tags.data = ", ".join(topic.tags)
            form.comments_disable.data = 'disable' if topic.comments_disabled else 'enable'
        return dict(
                    form = form
                    )
    
    if topic_id:
        topic = models.Topic.objects(id=topic_id).first()
    else:
        topic = models.Topic()
        topic.author = request.user
        topic.published_date = topic.updated_date
        topic.status = 'publish'
        
    topic.title=title
    topic.description=description
    topic.tags=tags
    
    topic.ip_address = request.environ.get('REMOTE_ADDR', '0.0.0.0')
    topic.page = True
    if comments_disable:
        if comments_disable == 'enable':
            topic.comments_disabled = True
        else:
            topic.comments_disabled = False
    
    topic.save()
    
    return HTTPFound(location=request.route_path('pages.view', title=title))