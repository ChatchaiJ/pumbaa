'''
Created on Oct 18, 2013

@author: boatkrap
'''
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response

from pumbaa import models, forms

@view_config(route_name='forums.topics.index', 
             renderer='/forums/topics/index.mako')
def index(request):
    topics = models.Topic.objects(status__ne='delete').all()
    return dict(
                topics=topics
                )

@view_config(route_name='forums.topics.compose', 
             permission='member',
             renderer='/forums/topics/compose.mako')
def compose(request):
    form = forms.topics.Topic(request.POST)
    
    if len(request.POST) > 0 and form.validate():
        title = form.data.get('title')
        description = form.data.get('description')
        tags = [tag.strip() for tag in form.data.get('tags').split(',')]
    else:
        return dict(
                    form = form
                    )
    
    topic = models.Topic(title=title, description=description, tags=tags)
    topic.author = request.user
    topic.published_date = topic.updated_date
    topic.status = 'publish'
    topic.ip_address = request.environ.get('REMOTE_ADDR', '0.0.0.0')
    
    topic.save()
    
    
    return HTTPFound(location=request.route_path('forums.topics.index'))

@view_config(route_name='forums.topics.view', 
             renderer='/forums/topics/view.mako')
def view(request):
    topic_id = request.matchdict.get('topic_id')
    title = request.matchdict.get('title')
    try:
        topic = models.Topic.objects.with_id(topic_id)
    except:
        return Response('Not Found, topic title:%s'%title, status='404 Not Found')
        
    return dict(
                topic=topic
                )